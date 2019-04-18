import pandas as pd
import csv

x = pd.read_csv('C:\\Users\\Aziz\\Desktop\\data3.csv', delimiter='~',  quoting=csv.QUOTE_NONE, skiprows=[1], encoding='mbcs', chunksize=1000000, error_bad_lines=False)

for index, chunk in enumerate(x):
    print()
    chunk.to_csv('C:\\Users\\Aziz\\Desktop\\models{}.csv'.format(index))
    print()