import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import tensorflow as ts 
import re, csv, pickle

location_data = pd.read_csv('D:/IPS_dumps/location_data.csv', delimiter=';', skiprows=[1], encoding='mbcs')
filter_frame = pd.DataFrame()
for index in range(26):
    
    with open('D:/IPS_dumps/data_corrected{}.pkl'.format(index), 'rb') as file_in:
        ips = pickle.load(file_in)
    setting_filter = ips['XRioID'].isin(['A8999C9F_A43A_466A_8790_A6715F5148D7', 'B206956F_DCA9_44AA_AE78_9227E00F84BA', 'DAE53492_94C8_4AE2_8CF6_45AADCC0A570', 'CE34671E_D55D_4EE0_82C9_35B3F3E607B1', 'A8999C9F_A43A_466A_8790_A6715F5148D7', 

'E0F117E4_D2A2_4643_9FA0_B96DD79C8863', 'DD1AA4A0_9D86_454C_ACF6_A2DDA29B4F90'])
    filter_frame = filter_frame.append(ips[setting_filter])

filter_frame = filter_frame[['AssetID', 'Actual']].join(location_data.set_index('AssetID'), on='AssetID')
filter_frame= filter_frame[filter_frame['Actual'].astype(float) > 200]
print(filter_frame)




# print(filter_frame['Actual'].astype(float))
# filter_frame['Actual'].astype(float).plot.hist(bins=300)
# plt.show()



