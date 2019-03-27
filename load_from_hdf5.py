import pandas as pd


store = pd.HDFStore('ips_hdf5.h5')

for i in range(13):

 x = store['chunck_{}'.format(i)]
 print(x.head())
print()
