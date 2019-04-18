import pandas as pd
import time, pickle, csv, re, math
import numpy as np
from itertools import zip_longest


with open('enum_dict.pkl', 'rb') as f:
    enum_dict = pickle.load(f)

relay_patterns = {'p546': list(
    map(lambda x: x.upper(), ['9e6a7fb0-a9a8-4a02-9e0d-6ea64a2a7815', '6feb01fb-00f1-4b72-b680-5d786f7090bd',
                              '08702862-3cb4-49f3-90f9-aa1b06556186', '08702862-3cb4-49f3-90f9-aa1b06556186'
        , 'cf32d233-bd41-42bb-beba-2904d0d4d53a', '08410b49-abef-4480-8c1a-7b818c70413c'
                                                  'fc15a43f-dfa2-41d3-baf5-fd45cde9ad0c',
                              'dcfbb6ac-3dc5-4bdc-aa0a-06e5397819e5'])),
                  'red670': list(map(lambda x: x.upper(),
                                     ['6d8efa16-a0c3-44fc-b1c4-aecf3351eff2', '62f796dd-e4e9-4dd3-b9b1-e11e9b449759'
                                                                              'd3165fb1-91c3-49e0-b74f-89b96e3dabb1'])),
        '7sd522' : {'779C87B1-6469-40B8-A514-6D47CFDC550F', '9A12628E-31C8-486C-91C0-B8774F22A5EA',
                    '1700E526-EAA3-4C14-B992-632EE4CD104A'}
                  }

def grouper(n, iterable, fillvalue=None):

    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def asset_concat(args):
    temp = list(map(lambda x: 'AssetID =' + '\'' + x + '\'', [i[0][1] for i in args if i is not None ]))

    return [i[0][1] for i in args if i is not None ]
    return ' | '.join(temp)


class Parser():

    def __init__(self, dictionary):
        self.p546_patterns = dictionary['p546']
        self.red670_patterns = dictionary['red670']
        self.s7sd522_paterns = dictionary['7sd522']

    def parse(self, dataframe):
        if dataframe.empty:
            return False, np.nan, np.nan, np.nan, np.nan

        if dataframe['RelParPatternID'].iloc[0] in self.p546_patterns:
            return [True, 'P546', *Pattern().p546_calculate_elements(dataframe)]
        elif dataframe['RelParPatternID'].iloc[0] in self.red670_patterns:
            return [True, 'RED670' , *Pattern().red670_calculate_elements(dataframe)]
        elif dataframe['RelParPatternID'].iloc[0] in self.s7sd522_paterns:
            return [True, '7SD522', *Pattern().s7sd522_calculate_elements(dataframe)]


        else:
            return [False]

    def hdf5_string(self):

        temp = list(map(lambda x: 'RelParPatternID =' + '\'' + x + '\'', self.p546_patterns))
        return ' | '.join(temp)
    def parse_location(self, dataframe, location_type, parent_location_type):
        '''
        ['Location','Asset Name', 'Relay type', 'Technology', 'Location has no relays', 'Relay placed in incorrect location', 'Relay has missing PSD','Relay has no settings',
        'latest setting not Active',  'Setting has no parameters']
         '''
        flags = [None, None, None, None, None, None]
        if  dataframe.empty:
            if locations_type not in excluded_types:
                flags[0] = True
        else:

            if locations_type in excluded_types:
                flags[1] = True
            if parent_location_type == excluded_types[0]:
                flags[1] = True

            ctvt = psd[psd['AssetID'] == dataframe['AssetID'].iloc[0]]
            if len(ctvt.index) < 2:
                flags[2] = True



            if len(dataframe.index) == 1:
                if dataframe['RelaySettingID'].isnull().any().any():
                    flags[3] = True
                else:
                    if dataframe['Active'].iloc[0] != 1:
                        flags[4] = True

                    if dataframe['XRioID'].isnull().any().any() :
                        flags[5] = True

            else:

                if dataframe['Active'].iloc[0] != 1:
                    flags[4] = True




        return [True, *flags]


class Pattern():

    def p546_calculate_elements(self, settings_frame):
        flags = []

        vt_primary = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0A01']
        if len(vt_primary.index) == 0:
            flags.append('"missing primary VT" ')
            vt_primary = np.nan

        else:
            vt_primary = float(vt_primary.iloc[0])

        vt_secondary = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0A02']
        if len(vt_secondary.index) == 0:
            flags.append('"missing secondary VT" ')
            vt_secondary = np.nan

        else:
            vt_secondary = float(vt_secondary.iloc[0])

        ct_primary = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0A07']
        if len(ct_primary.index) == 0:
            flags.append('"missing primary ct" ')
            ct_primary = np.nan

        else:
            ct_primary = float(ct_primary.iloc[0])

        ct_secondary = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0A08']
        if len(ct_secondary.index) == 0:
            flags.append('"missing primary ct" ')
            ct_secondary = np.nan

        else:
            ct_secondary = float(ct_secondary.iloc[0])

        impedance_factor = (vt_primary *1000 / vt_secondary) / (ct_primary / ct_secondary)

        mode = settings_frame['Actual'][settings_frame['ParamPathENU'] == '310C']
        if len(mode.index) == 0:
            flags.append('"missing distance mode setting. Assumed to be \"advanced\" " ')
            mode = 1
        else:
            mode = mode.iloc[0]

        values = settings_frame['Actual'][settings_frame['ParamPathENU'] == '092E']
        if len(values.index) == 0:
            flags.append('"missing setting values. Assumed to be \"secondary\" " ')
            values = 1
        else:
            values = values.iloc[0]

        z1_status = settings_frame['Actual'][settings_frame['ParamPathENU'] == '3120']
        if len(z1_status.index) == 0:
            flags.append('"missing distance zone 1 activation status" ')

        else:
            z1_status = z1_status.iloc[0]
            if z1_status == 0:
                flags.append('"zone 1 disabled" ')

        distance_status = settings_frame['Actual'][settings_frame['ParamPathENU'] == '090B']
        if len(distance_status.index) == 0:
            flags.append('"missing distance function activation status" ')
        else:
            distance_status = distance_status.iloc[0]
            if distance_status == 0:
                flags.append('"distance function disableld"')

        z1 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['3202'])] if mode == 1 else \
            settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['3121'])]

        z2 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['3210'])] if mode == 1 else \
            settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['3131'])]

        z3 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['3220'])] if mode == 1 else \
            settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['3141'])]

        z1 = float(z1.iloc[0]) if len(z1.index) > 0 else np.nan
        z1 = z1 if values == 0 else z1 * impedance_factor

        z2 = float(z2.iloc[0]) if len(z2.index) > 0 else np.nan
        z2 = z2 if values == 0 else z2 * impedance_factor
        
        z3 = float(z3.iloc[0]) if len(z3.index) > 0 else np.nan
        z3 = z3 if values == 0 else z3 * impedance_factor

        zline = settings_frame['Actual'][settings_frame['ParamPathENU'] == '3003']
        zline = float(zline.iloc[0]) if len(zline.index) > 0 else np.nan

        zline = zline if values == 0 else zline * impedance_factor
        if z1 is not np.nan and zline is not np.nan:
            if z1 > 0.9 * zline or z1 < 0.4 * zline:
                flags.append(' z1 out of bounds')

        return (z1, z2, z3, zline, ' , '.join(flags)) if mode == 1 else ( zline * z1 / 100, zline * z2 / 100,zline * z3 / 100,zline, ' , '.join(flags))

    def red670_calculate_elements(self, settings_frame):
        flags = []

        z1_status = settings_frame['Actual'][settings_frame[
                                                 'ParamPathENU'] == 'CUSTOM.PARAM.APP_CONFIG.ID_201722_1.ID_116541_2.ID_ZMQPDIS1.ID_SETTING_GROUP1.ID_APP1_DISTANCE_SE95Z1_A_1_SET_2_VALUE_SETTING_ZMQPDIS__SG_1']
        if len(z1_status.index) == 0:
            flags.append('"missing distance zone 1 activation status" ')

        else:
            z1_status = z1_status.iloc[0]
            if z1_status == 0:
                flags.append('"zone 1 disabled" ')

        x1 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin([
                                                                              'CUSTOM.PARAM.APP_CONFIG.ID_201722_1.ID_116541_2.ID_ZMQPDIS1.ID_SETTING_GROUP1.ID_APP1_DISTANCE_SE95Z1_A_1_SET_27_VALUE_SETTING_ZMQPDIS__SG_1'])]
        if len(x1.index) == 0:
            flags.append('"missing distance zone 1 reactance" ')
            x1 = np.nan

        else:
            x1 = float(x1.iloc[0])
        x2 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin([
                                                                              'CUSTOM.PARAM.APP_CONFIG.ID_201722_1.ID_116541_2.ID_ZMQAPDIS2.ID_SETTING_GROUP1.ID_APP1_DISTANCE_SE95Z1_A_2_SET_27_VALUE_SETTING_ZMQAPDIS__SG_1'])]
        if len(x2.index) == 0:
            flags.append('"missing distance zone 2 reactance" ')
            x2 = np.nan

        else:
            x2 = float(x2.iloc[0])
        x3 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin([
                                                                              'CUSTOM.PARAM.APP_CONFIG.ID_201722_1.ID_116541_2.ID_ZMQAPDIS3.ID_SETTING_GROUP1.ID_APP1_DISTANCE_SE95Z1_A_3_SET_27_VALUE_SETTING_ZMQAPDIS__SG_1'])]
        if len(x3.index) == 0:
            flags.append('"missing distance zone 3 reactance" ')
            x3 = np.nan

        else:
            x3 = float(x3.iloc[0])
        r1 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin([
                                                                              'CUSTOM.PARAM.APP_CONFIG.ID_201722_1.ID_116541_2.ID_ZMQPDIS1.ID_SETTING_GROUP1.ID_APP1_DISTANCE_SE95Z1_A_1_SET_28_VALUE_SETTING_ZMQPDIS__SG_1'])]
        if len(r1.index) == 0:
            flags.append('"missing distance zone 1 resistance" ')
            r1 = np.nan

        else:
            r1 = float(r1.iloc[0])
        r2 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin([
                                                                              'CUSTOM.PARAM.APP_CONFIG.ID_201722_1.ID_116541_2.ID_ZMQAPDIS2.ID_SETTING_GROUP1.ID_APP1_DISTANCE_SE95Z1_A_2_SET_28_VALUE_SETTING_ZMQAPDIS__SG_1'])]
        if len(r2.index) == 0:
            flags.append('"missing distance zone 2 resistance" ')
            r2 = np.nan

        else:
            r2 = float(r2.iloc[0])
        r3 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin([
                                                                              'CUSTOM.PARAM.APP_CONFIG.ID_201722_1.ID_116541_2.ID_ZMQAPDIS3.ID_SETTING_GROUP1.ID_APP1_DISTANCE_SE95Z1_A_3_SET_28_VALUE_SETTING_ZMQAPDIS__SG_1'])]
        if len(r3.index) == 0:
            flags.append('"missing distance zone 3 resistance" ')
            r3 = np.nan

        else:
            r3 = float(r3.iloc[0])

        x1l = settings_frame['Actual'][settings_frame[
                                           'ParamPathENU'] == 'CUSTOM.PARAM.APP_CONFIG.ID_114436_1.ID_116685_2.ID_LMBRFLO1.ID_SETTING_GROUP1.ID_APP1_FAULTLOC_1_SET_5_VALUE_SETTING_LMBRFLO__SG_1']
        if len(x1l.index) == 0:
            flags.append('"missing line reactance" ')
            x1l = np.nan

        else:
            x1l = float(x1l.iloc[0])
        r1l = settings_frame['Actual'][settings_frame[
                                           'ParamPathENU'] == 'CUSTOM.PARAM.APP_CONFIG.ID_114436_1.ID_116685_2.ID_LMBRFLO1.ID_SETTING_GROUP1.ID_APP1_FAULTLOC_1_SET_6_VALUE_SETTING_LMBRFLO__SG_1']
        if len(r1l.index) == 0:
            flags.append('"missing line reactance" ')
            r1l = np.nan

        else:
            r1l = float(r1l.iloc[0])
        zline = math.sqrt((x1l ** 2 + r1l ** 2))
        z1 = math.sqrt((x1 ** 2 + ((x1 / x1l) *  r1l) ** 2))
        z2 = math.sqrt((x2 ** 2 + ((x2 / x1l) *  r1l) ** 2))
        z3 = math.sqrt((x3 ** 2 + ((x3 / x1l) *  r1l) ** 2))

        if z1 is not np.nan and zline is not np.nan:
            if z1 > 0.9 * zline or z1 < 0.4 * zline:
                flags.append(' z1 out of bounds')

        return (z1, z2, z3, zline, ' , '.join(flags))

    def s7sd522_calculate_elements(self, settings_frame):
        flags = []

        vt_primary = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0203']
        if len(vt_primary.index) == 0:
            flags.append('"missing primary VT" ')
            vt_primary = np.nan

        else:
            vt_primary = float(vt_primary.iloc[0])

        vt_secondary = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0204']
        if len(vt_secondary.index) == 0:
            flags.append('"missing secondary VT" ')
            vt_secondary = np.nan

        else:
            vt_secondary = float(vt_secondary.iloc[0])


        ct_primary = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0205']
        if len(ct_primary.index) == 0:
            flags.append('"missing primary ct" ')
            ct_primary = np.nan

        else:
            ct_primary = float(ct_primary.iloc[0])

        ct_secondary = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0206']
        if len(ct_secondary.index) == 0:
            flags.append('"missing primary ct" ')
            ct_secondary = np.nan

        else:
            ct_secondary = float(ct_secondary.iloc[0])
            if ct_secondary == 1:
                ct_secondary = 5
            else:
                ct_secondary = 1


        impedance_factor = (vt_primary *1000 / vt_secondary) / (ct_primary / ct_secondary)




        values = 1

        z1_status = settings_frame['Actual'][settings_frame['ParamPathENU'] == '1601']
        if len(z1_status.index) == 0:
            flags.append('"missing distance zone 1 activation status" ')

        else:
            z1_status = z1_status.iloc[0]
            if z1_status == 3:
                flags.append('"zone 1 disabled" ')


        distance_status = settings_frame['Actual'][settings_frame['ParamPathENU'] == '0115']
        if len(distance_status.index) == 0:
            flags.append('"missing distance function activation status" ')
        else:
            distance_status = distance_status.iloc[0]
            if distance_status == 2:
                flags.append('"distance function disableld"')

        x1 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['1603'])]
        x1 = float(x1.iloc[0]) if len(x1.index) > 0 else np.nan
        x2 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['1613'])]
        x2 = float(x2.iloc[0]) if len(x2.index) > 0 else np.nan
        x3 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['1623'])]
        x3 = float(x3.iloc[0]) if len(x3.index) > 0 else np.nan

        r1 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['1603'])]
        r1 = float(r1.iloc[0]) if len(r1.index) > 0 else np.nan


        length = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['1113'])]
        length = float(length.iloc[0]) if len(length.index) > 0 else np.nan

        x_per_km = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['1111'])]
        x_per_km = float(x_per_km.iloc[0]) if len(x_per_km.index) > 0 else np.nan

        line_angle = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['1105'])]
        line_angle = float(line_angle.iloc[0]) if len(line_angle.index) > 0 else np.nan

        zline = (length * x_per_km / math.sin( line_angle * (  math.pi /180 ))) * impedance_factor


        z1 = ( x1 /   math.sin( line_angle * (  math.pi /180 )) )* impedance_factor
        z2 = ( x2 /   math.sin( line_angle * (  math.pi /180 )) )* impedance_factor
        z3 = ( x3 /   math.sin( line_angle * (  math.pi /180 )) )* impedance_factor




        if z1 is not np.nan and zline is not np.nan:
            if z1 > 0.9 * zline or z1 < 0.4 * zline:
                flags.append(' z1 out of bounds')

        return (z1, z2, z3, zline, ' , '.join(flags))
locations_type = ['58EA705D-BE4D-4520-89C3-312DF1ADF48D', '3CF34EF0-1BA7-4FA5-B62B-5EF77C787428',
                  'CD2E75F4-A0F3-433A-9B87-64BC516AB566']
excluded_types = [ 'D3752375-D674-446D-ADD8-DFC81C0514B3', '3D79BABE-EB5B-4DF3-9025-F6A3FBB7DA84', '2FD122B5-C47E-415C-8D1E-789BB7CF2331',
                   'AF2580E1-3D27-4F2B-B9C8-EDFAFC4E8E7F', 'A8CE7184-1C9D-49E3-AFFB-17486F0E74F6', 'AD0A13AB-61DE-4FBF-8ECB-24058170A17A', 'CBAFC824-9235-445C-8A3C-EB9D2D2EFCEB', '7B2E75C3-F0E0-4AB2-A2D9-AC0D84DE3B1A']
regex = re.compile('NG|CENTRAL|EAST|SOUTH|WEST')
location_data = pd.read_csv("D:\\IPS_dumps\\locations_data_new.csv", delimiter='~',quoting=csv.QUOTE_NONE, skiprows=[], encoding='mbcs')
location_data = location_data[( location_data['Location'].apply(lambda x: True if regex.match(str(x)) else False))]
location_data.set_index(['Location', 'AssetID'], inplace=True)
location_data.sort_index(inplace=True)

psd = pd.read_csv("D:\\IPS_dumps\\psd.csv", delimiter=';', encoding='mbcs')
reaches = []
line_impedances = []
flagses = []
parser = Parser(relay_patterns)



count = 0
results = []
result_pd = pd.DataFrame()
result_pd_relays = pd.DataFrame()

for i in location_data.iterrows():
    t1 = time.perf_counter()

    if count % 5000 == 0:
        print(count)

    if count == 578:
        print()

    search_string = str(i[0][1])

    ips = pd.read_hdf("D:\\IPS_dumps\\ips_with_path.h5", where=' AssetID = \"{}\"'.format(search_string))
    print(count,time.perf_counter() - t1)
    t1 = time.perf_counter()
    ips.loc[:, ['Actual']] = ips['Actual'].map(lambda x: enum_dict.get(x, x))

    temp = [*parser.parse_location(ips, i[1]['LocationTypeID'], i[1]['ParentLocationTypeID'])]


    if temp[0]:
        # result = [j[0][0], j[0][1], *temp[1:4], temp[2]/ temp[3] *100, temp[4] ]
        if not all(v is None for v in temp[1:]):
            result = [i[0][0], i[1]['Name'], i[1]['NameENU'], i[1]['DisplayENU']  , *temp[1:]]
            result_pd = result_pd.append([result], ignore_index=True)


    if i[1]['LocationTypeID'] in locations_type:


        temp2 = [*parser.parse(ips)]


        if temp2[0]:
            # return True, 'P546' ,reach, line_impedance, flags
            result = [i[0][0], i[0][1], *temp2[1:-1], temp2[2]/ temp2[5] *100, temp2[3]/ temp2[5] *100, temp2[4]/ temp2[5] *100, temp2[-1] ]

            result_pd_relays = result_pd_relays.append([result], ignore_index=True)


    count += 1

    if count == 5000:
        break

result_pd.columns = ['Location','Asset Name', 'Relay type', 'Technology', 'Location has no relays', 'Relay placed in incorrect location',
                     'Relay has missing PSD','Relay has no settings',  'latest setting not Active',  'Latest etting has no parameters']
result_pd.set_index(['Location'])
result_pd.sort_index(inplace=True)
result_pd.to_csv('output_locations.csv', index=False)

result_pd_relays.columns = ['Location','AssetID', 'relay', 'z1', 'z2', 'z3', 'line Impedance','reach_z1', 'reach_z2', 'reach_z3','flags']
result_pd_relays.set_index(['Location'])
result_pd_relays.sort_index(inplace=True)
result_pd_relays.to_csv('output_relays.csv', index=False)
# assets['z1'] = pd.Series(reaches, index=assets.index)
# assets['line_impedance'] = pd.Series(line_impedances, index=assets.index)
# assets['flags'] = pd.Series(flagses, index=assets.index)
#
# location_data = pd.read_csv('D:/IPS_dumps/location_data.csv', delimiter=';', skiprows=[1], encoding='mbcs')
# location_data = location_data.set_index('AssetID')
# assets = assets.join(location_data, on='AssetID')
# assets = assets[['Location', 'AssetID', 'z1', 'line_impedance', 'flags']]
# assets.set_index(['Location', 'AssetID'], inplace=True)
#
# assets.to_csv('D:/IPS_dumps/output.csv')
# assets.sort_index(inplace=True)
# t2 = time.perf_counter() - t1
