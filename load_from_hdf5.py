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
                                                                              'd3165fb1-91c3-49e0-b74f-89b96e3dabb1']))
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

    def parse(self, dataframe):
        if dataframe.empty:
            return False, np.nan, np.nan, np.nan

        if dataframe['RelParPatternID'].iloc[0] in self.p546_patterns:
            reach, line_impedance, flags = Pattern().p546_calculate_elements(dataframe)
            return True, 'P546' ,reach, line_impedance, flags
        elif dataframe['RelParPatternID'].iloc[0] in self.red670_patterns:
            reach, line_impedance, flags = Pattern().red670_calculate_elements(dataframe)
            return True, 'RED670' , reach, line_impedance, flags

        else:
            return False, np.nan, np.nan, np.nan

    def hdf5_string(self):

        temp = list(map(lambda x: 'RelParPatternID =' + '\'' + x + '\'', self.p546_patterns))
        return ' | '.join(temp)



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

        impedance_factor = (vt_primary / vt_secondary) / (ct_primary / ct_secondary)

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
            if mode == 0:
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

        zline = settings_frame['Actual'][settings_frame['ParamPathENU'] == '3003']
        z1 = float(z1.iloc[0]) if len(z1.index) > 0 else np.nan
        zline = float(zline.iloc[0]) if len(zline.index) > 0 else np.nan
        z1 = z1 if values == 0 else z1 * impedance_factor
        zline = zline if values == 0 else zline * impedance_factor
        if z1 is not np.nan and zline is not np.nan:
            if z1 > 0.9 * zline or z1 < 0.4 * zline:
                flags.append(' z1 out of bounds')

        return (z1, zline, ' , '.join(flags)) if mode == 1 else (zline * z1 / 100, zline, ' , '.join(flags))

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
        r1 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin([
                                                                              'CUSTOM.PARAM.APP_CONFIG.ID_201722_1.ID_116541_2.ID_ZMQPDIS1.ID_SETTING_GROUP1.ID_APP1_DISTANCE_SE95Z1_A_1_SET_28_VALUE_SETTING_ZMQPDIS__SG_1'])]
        if len(r1.index) == 0:
            flags.append('"missing distance zone 1 resistance" ')
            r1 = np.nan

        else:
            r1 = float(r1.iloc[0])
        z1 = math.sqrt((x1 ** 2 + r1 ** 2))
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

        if z1 is not np.nan and zline is not np.nan:
            if z1 > 0.9 * zline or z1 < 0.4 * zline:
                flags.append(' z1 out of bounds')

        return (z1, zline, ' , '.join(flags))


locations_type = ['58EA705D-BE4D-4520-89C3-312DF1ADF48D', '3CF34EF0-1BA7-4FA5-B62B-5EF77C787428',
                  'CD2E75F4-A0F3-433A-9B87-64BC516AB566']
regex = re.compile('380|230|115|132|110')
location_data = pd.read_csv("D:\IPS_dumps\locations_data_new.csv", delimiter=';', skiprows=[1], encoding='mbcs')
location_data = location_data[(location_data['LocationTypeID'].isin(locations_type)) & (
    location_data['NameENU'].apply(lambda x: True if regex.match(str(x)) else False))]
location_data.set_index(['Location', 'AssetID'], inplace=True)
location_data.sort_index(inplace=True)

reaches = []
line_impedances = []
flagses = []
parser = Parser(relay_patterns)



count = 0
results = []
result_pd = pd.DataFrame()
pd_iterator = location_data.iterrows()

for i in grouper(31, pd_iterator):
    t1 = time.perf_counter()

    search_string =  pd.Series( asset_concat(i))


    ips_group = pd.read_hdf("D:\IPS_dumps\ips_with_path.h5", where= ' AssetID = search_string')
    print(count,time.perf_counter() - t1)
    t1 = time.perf_counter()
    ips_group.loc[:, ['Actual']] = ips_group['Actual'].map(lambda x: enum_dict.get(x, x))
    for j in i:
        if j is None:
            continue
        ips = ips_group[ips_group['AssetID'] == j[0][1]]
        temp = [*parser.parse(ips)]

        #
        # if result[2] is not np.nan:
        #     result_pd = result_pd.append([result], ignore_index=True)
        if temp[0]:
            result = [j[0][0], j[0][1], *temp[1:4], temp[2]/ temp[3] *100, temp[4] ]
            result_pd = result_pd.append([result], ignore_index=True)


        count += 1

        # if count == 500:
        #     break

result_pd.columns = ['Location', 'AssetID', 'relay', 'Z1', 'line Impedance', 'reach' , 'Flags']
result_pd.set_index(['Location', 'AssetID'])
result_pd.sort_index(inplace=True)
result_pd.to_csv('output.csv', index=False)

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
