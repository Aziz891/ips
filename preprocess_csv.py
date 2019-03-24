
import pandas as pd 
import numpy as np 
import tensorflow as ts 
import re
import csv





# x = pd.read_csv('D:/IPS_dumps/data.csv', delimiter=';', sep=';', parse_dates=[4], skiprows=[1, 34923 , 34955-1], error_bad_lines=False, encoding='mbcs', chunksize=10000000)
# count =0
# for index,chunck in enumerate(x):
#     print('chunck # ' + str(index))
#     chunck.info()
#     count += 1


# print('count of chuncks is ' + str(count))



semicolon_finder = re.compile(r';')


with open('D:/IPS_dumps/data.csv', 'r', encoding='mbcs') as f, open('D:/IPS_dumps/data_corrected.csv', 'w', encoding='mbcs') as out :
    for index,line in enumerate(f):

        match = semicolon_finder.findall(line)
    
        if match.__len__() >6:
            split_string  = line.split(';')
            corrected_string = ','.join(split_string[6:])
            whole_string = ';'.join((*split_string[:6], corrected_string))
            out.write((whole_string + '\n'))
        else:
            out.write((line + '\n'))


    
            

      
        
      
print()



    
    


