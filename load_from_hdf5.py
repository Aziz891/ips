import pandas as pd
import time, pickle, csv, re, math
import numpy as np

t1 = time.perf_counter()
with open('relay_models.pkl', 'rb') as f:
    relay_models = pickle.load(f)

with open('enum_dict.pkl', 'rb') as f:
    enum_dict = pickle.load(f)

relay_patterns = {'p546' : list(map(lambda x: x.upper(),[ '9e6a7fb0-a9a8-4a02-9e0d-6ea64a2a7815', '6feb01fb-00f1-4b72-b680-5d786f7090bd',
                             '08702862-3cb4-49f3-90f9-aa1b06556186', '08702862-3cb4-49f3-90f9-aa1b06556186'
                             , 'cf32d233-bd41-42bb-beba-2904d0d4d53a', '08410b49-abef-4480-8c1a-7b818c70413c'
                             'fc15a43f-dfa2-41d3-baf5-fd45cde9ad0c', 'dcfbb6ac-3dc5-4bdc-aa0a-06e5397819e5'])),
                  'red670' : list(map(lambda x: x.upper(),[ '6d8efa16-a0c3-44fc-b1c4-aecf3351eff2', '62f796dd-e4e9-4dd3-b9b1-e11e9b449759'
                                                            'd3165fb1-91c3-49e0-b74f-89b96e3dabb1']))
                  }


class Parser():

    def __init__(self, dictionary):
        self.p546_patterns = dictionary['p546']
        self.red670_patterns = dictionary['red670']

    def parse(self, dataframe):
        if dataframe.empty:
            return np.nan, np.nan, np.nan

        if dataframe['RelParPatternID'].iloc[0] in self.p546_patterns:
            reach, line_impedance, flags = Pattern().p546_calculate_elements(dataframe)
            return reach, line_impedance, flags
        elif dataframe['RelParPatternID'].iloc[0] in self.red670_patterns:
            reach, line_impedance, flags = Pattern().red670_calculate_elements(dataframe)
            return reach, line_impedance, flags

        else:
            return np.nan,  np.nan,  np.nan



class Pattern():


    def p546_calculate_elements(self, settings_frame):
        flags = []

        mode = settings_frame['Actual'][settings_frame['ParamPathENU'] == '310C']
        if len(mode.index) == 0:
            flags.append('"missing distance mode setting. Assumed to be \"advanced\" " ')
            mode = 1
        else:
            mode = mode.iloc[0]

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

        z1 = settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['3202'])] if mode ==1 else settings_frame['Actual'][settings_frame['ParamPathENU'].isin(['3121'])]
        zline =  settings_frame['Actual'][settings_frame['ParamPathENU'] == '3003']
        z1 = float(z1.iloc[0]) if len(z1.index) > 0 else np.nan
        zline = float(zline.iloc[0]) if len(zline.index) > 0 else np.nan
        if z1 is not np.nan and zline is not np.nan:
            if z1 > 0.9 * zline or z1 < 0.4 * zline:
                flags.append(' z1 out of bounds')

        return (z1, zline, ' , '.join(flags)) if mode == 1 else (zline * z1 / 100, zline, ' , '.join(flags))


    def red670_calculate_elements(self, settings_frame):
        flags = []

        mode = settings_frame['Actual'][settings_frame['ParamPathENU'] == '310C']
        if len(mode.index) == 0:
            flags.append('"missing distance mode setting. Assumed to be \"advanced\" " ')
            mode = 1
        else:
            mode = mode.iloc[0]

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
        if z1 is not np.nan and zline is not np.nan:
            if z1 > 0.9 * zline or z1 < 0.4 * zline:
                flags.append(' z1 out of bounds')

        return (z1, zline, ' , '.join(flags)) if mode == 1 else (zline * z1 / 100, zline, ' , '.join(flags))


locations_type = ['58EA705D-BE4D-4520-89C3-312DF1ADF48D', '3CF34EF0-1BA7-4FA5-B62B-5EF77C787428',
                  'CD2E75F4-A0F3-433A-9B87-64BC516AB566']
regex = re.compile('380|230|115|132|110')
location_data = pd.read_csv('D:/IPS_dumps/locationS_data_new.csv', delimiter=';', skiprows=[1], encoding='mbcs')
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

for i in location_data.iterrows():
    t1 = time.perf_counter()
    ips = pd.read_hdf('D:/IPS_dumps/ips_with_path.h5', where='AssetID = "{}" '.format(i[0][1]))
    print(time.perf_counter() - t1)
    t1 = time.perf_counter()
    ips.loc[:, ['Actual']] = ips['Actual'].map(lambda x: enum_dict.get(x, x))
    result = [i[0][0], i[0][1],    *parser.parse(ips)]
    #
    # if result[2] is not np.nan:
    #     result_pd = result_pd.append([result], ignore_index=True)
    result_pd = result_pd.append([result], ignore_index=True)


    count += 1

    if count == 50:
        break
    if result[2] is not np.nan:
        print('found')


result_pd.columns = ['Location', 'AssetID', 'Z1', 'line Impedance', 'Flags']
result_pd.set_index(['Location', 'AssetID'])
result_pd.sort_index(inplace=True)
result_pd.to_csv('D:/IPS_dumps/output.csv', index=False)



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
