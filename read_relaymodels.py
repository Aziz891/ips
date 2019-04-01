import os, csv
import pandas as pd
from collections import defaultdict

relay_models = defaultdict(lambda : None)
relays = ['p546', 'sel-411', 'red670', '7sd52']

for relay in relays:
    
    root = '\\\\10.164.215.18\\ped-shared\\Aziz\\IPS_MODELS\\' + relay

    relay_models[relay]= pd.DataFrame()


    for i in os.listdir(root):
        path = os.path.join(root,i)
        models = pd.read_csv(path, encoding='utf-16', delimiter='\t')
        relay_models[relay] =   pd.concat([relay_models[relay], models])


print








