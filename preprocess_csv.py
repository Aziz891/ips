
import pandas as pd 
import numpy as np 
import re



semicolon_finder = re.compile(r';')


with open('D:/IPS_dumps/data.csv', 'r', encoding='mbcs') as f, open('D:/IPS_dumps/data_corrected.csv', 'w', encoding='mbcs') as out :
    for index,line in enumerate(f):

        match = semicolon_finder.findall(line)
    
        if match.__len__() >6:
            split_string  = line.split(';')
            corrected_string = ','.join(split_string[6:])
            whole_string = ';'.join((*split_string[:6], corrected_string))
            out.write((whole_string + '\r\n'))
        else:
            out.write((line))


    
            

      
        
      
print()



    
    


