import csv, re

line =';2;3;;;6;7;k'

split_string  = line.split(';')
corrected_string = ','.join(split_string[6:])
whole_string = ';'.join((*split_string[:6], corrected_string))
print(whole_string)




