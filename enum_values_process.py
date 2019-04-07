import csv,pickle
from collections import defaultdict
import numpy as np

enum_dict = defaultdict(lambda: None)




with open('D:\IPS_dumps\enum_values.csv', 'r') as f:
    reader = csv.reader(f, delimiter=';')

    for row in reader:
        key = '{' + row[0] + '}'
        if row[1] != 'NULL':
            value = int(row[1])
        else:
            continue
        enum_dict[key] = value


enum_dict = dict(enum_dict)

with open('enum_dict.pkl', 'wb') as f:
    pickle.dump(enum_dict, f)

