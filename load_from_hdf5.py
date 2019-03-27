import pandas as pd
import time
import numpy as np


class Relay():
    def __init__(self, model_id):
        self.model_id = model_id

class Element(Relay):

    def __init__(self, model_id, parameters_to_filter):
        super().__init__(model_id)
        self.parameters_to_filter = parameters_to_filter

    def filter(self, pdframe, column, pdfunction):
        temp =  pdfunction(pdframe[column], self.parameters_to_filter)
        return temp

listXRIO = ['A8999C9F_A43A_466A_8790_A6715F5148D7', 'B206956F_DCA9_44AA_AE78_9227E00F84BA', 'DAE53492_94C8_4AE2_8CF6_45AADCC0A570', 'CE34671E_D55D_4EE0_82C9_35B3F3E607B1', 'A8999C9F_A43A_466A_8790_A6715F5148D7', 

'E0F117E4_D2A2_4643_9FA0_B96DD79C8863', 'DD1AA4A0_9D86_454C_ACF6_A2DDA29B4F90']

x =list(map(lambda x : 'XRioID =' + x , listXRIO))
where_clause =  ' | '.join(x) 


p546 = Element('p546',['A8999C9F_A43A_466A_8790_A6715F5148D7', 'B206956F_DCA9_44AA_AE78_9227E00F84BA', 'DAE53492_94C8_4AE2_8CF6_45AADCC0A570', 'CE34671E_D55D_4EE0_82C9_35B3F3E607B1', 'A8999C9F_A43A_466A_8790_A6715F5148D7', 

'E0F117E4_D2A2_4643_9FA0_B96DD79C8863', 'DD1AA4A0_9D86_454C_ACF6_A2DDA29B4F90'])


print()

ips = pd.read_hdf('D:/IPS_dumps/ips.h5', where= where_clause)
print(ips)



    





location_data = pd.read_csv('D:/IPS_dumps/location_data.csv', delimiter=';', skiprows=[1], encoding='mbcs')
print()

