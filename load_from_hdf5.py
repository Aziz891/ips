import pandas as pd
import time, pickle, csv, re, math
import numpy as np



t1 = time.perf_counter()
with open('relay_models.pkl', 'rb') as f:
    relay_models = pickle.load(f)

with open('enum_dict.pkl', 'rb') as f:
    enum_dict = pickle.load(f)




class Relay():
    def __init__(self, model):
        self.model_relay = model['id']
        self.elements = model['elements']

    def filter_all(self):
        temp = []
        for _ , value in self.elements.items():
            temp = temp + value
        temp = 'XRioID in [ {0}  ]   '.format( ' , '.join(temp[:31]))
        print()
        return temp
    def filter_all_2(self):
        temp = []
        for _ , value in self.elements.items():
            temp = temp + value
        temp = 'XRioID in [ {0}  ]   '.format( ' , '.join(temp[31:61]))
        print()
        return temp

    

class P546(Relay):

    def __init__(self, model):
        super().__init__(model)

    def calculate_reach(self, zone_settings):
        flags = []
       
        mode = zone_settings['Actual'][zone_settings['XRioID'].isin(self.elements['setting_mode'])]
        if len(mode.index) == 0 :
            flags.append('"missing distance mode setting. Assumed to be \"advanced\" " ')
            mode = 1
        else: 
            mode = mode.iloc[0] 

        z1_status = zone_settings['Actual'][zone_settings['XRioID'].isin(self.elements['z1_status'])]
        if len(z1_status.index) == 0 :
            flags.append('"missing distance zone 1 activation status" ')
     
        else: 
            z1_status = z1_status.iloc[0] 
            if mode == 0:
                flags.append('"zone 1 disabled" ')
        distance_status = zone_settings['Actual'][zone_settings['XRioID'].isin(self.elements['distance_status'])]
        if len(distance_status.index) == 0 :
            flags.append('"missing distance function activation status" ')
        else:
            distance_status =distance_status.iloc[0]
            if distance_status == 0:
                flags.append('"distance function disableld"')

        
        z1 = (zone_settings['Actual'][zone_settings['XRioID'].isin(self.elements['z1_ohm'])])
        zline = (zone_settings['Actual'][zone_settings['XRioID'].isin(self.elements['line_impedance'])])
        z1 = float(z1.iloc[0]) if len(z1.index) > 0 else np.nan
        zline = float(zline.iloc[0]) if len(zline.index) > 0 else np.nan
        if z1 is not np.nan and zline is not np.nan:
            if z1 > 0.85 * zline or z1 < 0.6 * zline:
                flags.append(' z1 out of bounds')
        
        return (z1, zline, ' , '.join(flags)) if mode == 1 else (zline * z1 / 100, zline,  ' , '.join(flags))

           


p546 = P546(relay_models['P546'])

reaches = []
line_impedances = []
flagses = []

ips = pd.read_hdf('D:/IPS_dumps/ips.h5', where=  p546.filter_all() )
ips2 = pd.read_hdf('D:/IPS_dumps/ips.h5', where=  p546.filter_all_2() )
ips = pd.concat([ips,  ips2])


ips.loc[:, ['Actual']] = ips['Actual'].map(lambda x: enum_dict.get(x,x))
assets = pd.DataFrame(ips['AssetID'].unique(), columns=['AssetID'])

for i in assets['AssetID']:

    
    filter_settings = ips[ips['AssetID'] == i]
    if  len(filter_settings.index) > 0:
     
        reach, line_impedance, flags = p546.calculate_reach(filter_settings)
        reaches += [reach]
        line_impedances += [line_impedance]
        flagses += [flags]

    else:
        print()

assets['z1'] =  pd.Series(reaches, index= assets.index)
assets['line_impedance'] =  pd.Series(line_impedances, index= assets.index)
assets['flags'] =  pd.Series(flagses, index= assets.index)

location_data = pd.read_csv('D:/IPS_dumps/location_data.csv', delimiter=';', skiprows=[1], encoding='mbcs')
location_data =  location_data.set_index('AssetID')
assets = assets.join(location_data, on='AssetID')
assets = assets[['Location', 'AssetID', 'z1', 'line_impedance', 'flags' ] ]
assets.set_index(['Location', 'AssetID'], inplace=True)




assets.to_csv('D:/IPS_dumps/output.csv')
assets.sort_index(inplace=True)
t2 = time.perf_counter() - t1


