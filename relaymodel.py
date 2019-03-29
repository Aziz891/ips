from collections import defaultdict
import pickle

relay_models = defaultdict(lambda : None)

relay_models['P546'] = {
'id' : 'P546',

'ct_primary' : [

'D3D3DE6B_29AF_4028_B3C2_1B3CCB8E4D4D' , 'EDFDA8B6_446C_45F8_9F24_DCCE1A5FDE46' , 
'E4E93E5F_0C68_400E_8524_128571A743F9' , 'E307B2CF_6F55_4C56_A8AB_C2A2D06D7FB1' , 
'ACD1D7C5_16D8_4491_B5F5_D549101B862C' , 'C7F0B86F_A7D6_4807_9D1A_DA104F3110B1' , 
'A9D027C6_4C5C_4212_BF60_BC935E98BB61'

]
,
'ct_secondary' : [
'CF071D79_A5A5_4757_ACDC_122481FD154E' , 'B8023827_8F54_46DC_9ADA_70865ECE0286' ,
'E93DD451_7EB5_4F5C_BDFE_4BD938F917A8' , 'A03BBE1A_533F_48F6_92AA_756F4ABD54BB' ,
'FA0FA7E8_0BDE_4227_9528_7F41E2F0F92F' , 'AED6BF08_DAAC_44BF_8A41_7C952CC9232B' ,
'DC9E8F64_7D37_481E_B3E8_695A6BD72CD5'




],





'vt_primary' : [
'AED85DB7_F777_4EBE_9954_6E9449AE7093' , 'A93FE612_60B3_4BC4_8E0A_038D2A0F0635' ,
'BBD99317_763A_4EAD_99B9_7C3A3ACA5BCC' , 'B01EE323_F22B_44D2_A371_B030E86ECC10' ,
'B8A05E0C_C4FD_4C15_AB06_CB0983DBBEAE' , 'A4A184A0_5ACB_4525_AE56_FAA9C1A2E56A' ,
'FA89037E_1360_4BDC_819E_58F789E7BAD1' , 


],

'vt_secondary' : [
'A8CDC509_8816_423A_A5CE_ED8B46AABC63' , 'A5ECA8D2_08A5_491D_B344_301F33DC2669' ,
'F3893E90_F070_4355_8CF6_EA7BA749379C' , 'E439D2B6_DCB8_4123_B67B_4C78EEAE2806' ,
'F2D4AEC8_8494_4661_882B_B1527DB76BAC' , 'A317FFEF_3A6D_463C_A425_A334898C63AB' , 
'E69A0375_4CD8_4D09_8358_C6556EBBFE2D'


],

'distance_status' : [
'C62A6455_5CF3_4BE9_98A5_95C15AD5E8D1' , 'D2291661_EE5F_4351_B03B_26DCAAB1F258' ,
'E54BF400_3206_4C42_AC85_2F79A0DF06FF' , 'CFBBE313_138E_4A0A_9439_72D315F6DB9B' ,
'D1F94CD5_FBCF_44DF_BE9A_810270DECAA7' , 'A6B8D289_D6CD_4375_B634_501E7FED49DC'
],
'elements' : {
'line_impedance' : [
'A8999C9F_A43A_466A_8790_A6715F5148D7', 'B206956F_DCA9_44AA_AE78_9227E00F84BA',
'DAE53492_94C8_4AE2_8CF6_45AADCC0A570', 'CE34671E_D55D_4EE0_82C9_35B3F3E607B1', 
'E0F117E4_D2A2_4643_9FA0_B96DD79C8863', 'DD1AA4A0_9D86_454C_ACF6_A2DDA29B4F90', 
],

'setting_mode' : [
'D26DEEF4_27FB_4C2E_B1BE_6041769A3434' , 'C1BDFC7A_C7C6_4766_936D_BE1C4DC0E749',
'AC3FACDA_736F_4A71_B718_635715AB7D11' , 'EFEB6FA3_88AD_42D3_9EC7_69BE69DBAD19',
'A8D1F409_B915_4DC2_9619_4ABECDA7CFF1'
],


'z1_ohm' : [
'BA99DFE9_278E_4BEB_9611_57684872D003' , 'CE9ECBA6_F17D_4F2C_BC50_5B7CB9A10A9A',
'AFD9AF98_5947_479F_A3A4_9101447B9F13' , 'AFD9AF98_5947_479F_A3A4_9101447B9F13',
'DF8583DF_D5FC_4680_BFF2_D3EF939F29AA'


  
],

'z1_percentage' : [
'B2416FD6_E479_4203_84DA_0AC1C428B35A' , 'FEF3D991_BFEB_4B94_8004_D74CCFA1E7DD' ,
'DDFE1A50_66EB_47AF_B6B3_38C2BB96C5EB' , 'EDE86A42_030F_402A_8B18_0530BA2F218F' ,
'AD132401_BE6E_4663_9908_14082449EA6E'

],

'z1_status' : [
'DFFF8FC6_B61F_4886_BEA4_130CC33A4F66' , 'C7262DCD_4DFA_461C_98FE_A7FDEF7E15D9' ,
'DDFE1A50_66EB_47AF_B6B3_38C2BB96C5EB' , 'B1D73BCA_6DF3_4E6B_A76C_46B2C8E3135D' , 
'FD5B743C_B42E_4A9A_B173_DA143D03F0AA' , 'A2132E55_4CB9_429C_A42C_00173B1DD0C6'


],

'line_angle' : [
'EB34D292_423F_47CE_A0A2_89C5988D9C29', 'F0A57AD5_846F_4272_A67D_E40665625767', 
'F5914D31_348F_4303_86C9_F242A54BC59B', 'DA6F8892_A72A_490E_AD22_C1309CC503AD'] # incomplete


 }
 }
relay_models= dict(relay_models)

with open('relay_models.pkl', 'wb') as f:
    pickle.dump(relay_models, f)  