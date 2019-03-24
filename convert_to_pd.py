
import pandas as pd 
import numpy as np 
import tensorflow as ts 
import re
import csv












x = pd.read_csv('D:/IPS_dumps/data_corrected.csv', delimiter=';',  parse_dates=[4], skiprows=[1], encoding='mbcs', chunksize=5000000)
count =0
for index,chunck in enumerate(x):
    print('chunck # ' + str(index))
    count += 1
    print
    if count >2:
        break


print('count of chuncks is ' + str(count))
print(chunck)
