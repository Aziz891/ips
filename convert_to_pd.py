
import pandas as pd 
import numpy as np 
import tensorflow as ts 
import re, csv, pickle









store = pd.HDFStore('ips_hdf5.h5')
x = pd.read_csv('D:/IPS_dumps/data_corrected.csv', delimiter=';',  parse_dates=[4], skiprows=[1,2], encoding='mbcs', chunksize=10000000)
count =0
for index,chunck in enumerate(x):

    print('entered loop')    
#     if count == 18:
#         count += 1
#         continue
     
    chunck['Active'].fillna(value=2, inplace=True) 
    dtype0= {'AssetID': 'str',
 'RelaySettingID': 'str',
 'IpsUserName': 'str',
 'Active': 'int64',
 'DateSetting': 'datetime64',
 'XRioID':  'str',
 'Actual': 'str'}
    chunck= chunck.astype(dtype0)    
    print(chunck)

    store['chunck_{}'.format(index)] = chunck
    print('done')
    count += 1




print('count of chuncks is ' + str(count))
