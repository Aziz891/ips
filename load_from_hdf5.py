import pandas as pd
import time, pickle
import numpy as np




with open('relay_models.pkl', 'rb') as f:
    relay_models = pickle.load(f)


class Relay():
    def __init__(self, model):
        self.model_relay = model['id']
        self.elements = model['elements']

    def filter_all(self):
        temp = []
        for key, value in self.elements.items():
            temp = temp + value
        temp =list(map(lambda x : 'XRioID =' + x , temp))
        return ' | '.join(temp) 

    def calculate_reach(self, zone_settings):
        z1 = float(zone_settings['Actual'][zone_settings['XRioID'].isin(self.elements['z1'])].iloc[0])
        zline = float(zone_settings['Actual'][zone_settings['XRioID'].isin(self.elements['line_impedance'])].iloc[0])
        return zline * z1 / 100



p546 = Relay(relay_models['p546'])
where_clause = p546.filter_all()
reaches = []

ips = pd.read_hdf('D:/IPS_dumps/ips.h5', where= where_clause)
for i in ips['AssetID'].unique():
    filter_settings = ips[ips['AssetID'] == i]
    if  len(filter_settings.index) == 4:
        reach = p546.calculate_reach(filter_settings)
        reaches += [reach]

reaches = pd.Series(reaches)





    





location_data = pd.read_csv('D:/IPS_dumps/location_data.csv', delimiter=';', skiprows=[1], encoding='mbcs')
print()

