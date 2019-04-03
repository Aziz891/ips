import os, csv, pickle
import pandas as pd
from collections import defaultdict

relay_models = defaultdict(lambda : None)
relays = ['p546', 'sel-411', 'red670', '7sd52']


for relay in relays:
    
    root = 'IPS_MODELS\\' + relay

    relay_models[relay]= pd.DataFrame()


    for i in os.listdir(root):
        path = os.path.join(root,i)
        models = pd.read_csv(path, encoding='utf-16', delimiter='\t')
        relay_models[relay] =   pd.concat([relay_models[relay], models[['XRioID', 'Path English']]])


relay_models = dict(relay_models)


with open('relay_models.pkl', 'wb') as f:
        pickle.dump(relay_models, f)









