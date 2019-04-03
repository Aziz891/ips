
import pandas as pd 
import numpy as np 
import re



semicolon_finder = re.compile(r';')

count = 0
with open('D:/IPS_dumps/settings.csv', 'r', encoding='mbcs') as f, open('D:/IPS_dumps/settings_corrected.csv', 'w', encoding='mbcs') as out :
    for index,line in enumerate(f):

        match = semicolon_finder.findall(line)
    
        if match.__len__() >8:
            split_string  = line.split(';')
            corrected_string = ','.join(split_string[6:])
            whole_string = ';'.join((*split_string[:6], corrected_string))
            out.write((whole_string + '\r\n'))
            count += 1
            print(count)
        else:
            out.write((line))


    
            

      
        
      
print()



    
    


