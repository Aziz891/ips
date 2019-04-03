
import pandas as pd 
import numpy as np 
import tensorflow as ts 
import re, csv, pickle









x = pd.read_csv('D:/IPS_dumps/settings_corrected.csv', delimiter=';',  quoting=csv.QUOTE_NONE, parse_dates=[4], skiprows=[1,2], encoding='mbcs', chunksize=3000000)
count =0
for chunck in x:
    # # if count == 2:
    # #     count +=1
    # #     break
    # if count in [3,2]:
    #     chunck.to_csv('test{}.csv'.format(count))
    

    print('entered loop')    
    # if count == 2:
    #     count += 1
    #     break
     
    chunck['Active'].fillna(value=2, inplace=True) 
    dtype0= {'AssetID': 'str',
 'RelaySettingID': 'str',
 'IpsUserName': 'str',
 'Active': 'int64',
 'DateSetting': 'datetime64',
 'XRioID':  'str',
 'Actual': 'str',
 'ParamPathENU' : 'str',
 'RelParPatternID' : 'str'}
    chunck= chunck.astype(dtype0)    
    print(chunck.head())

    chunck.to_hdf('D:/IPS_dumps/ips_with_path.h5', 'ips',  format='table',  data_columns=True, append=True, min_itemsize={'IpsUserName':20,'ParamPathENU' : 300, 'Actual' : 130, 'AssetID' : 45, 'XRioID': 45})
    print('done')
    count += 1




print('count of chuncks is ' + str(count))
