#merge_all_ip and ja3_result
import pandas as pd
import numpy as np
import glob,os
path=r'./'

ja3_result=pd.read_csv(path+'ja3_result.csv',sep=',',index_col=None,usecols=None)
all_ip=pd.read_csv(path+'all_ip.csv',sep=',',index_col=None,usecols=None)
#print(ja3_result)
#print(all_ip)
result=ja3_result.append(all_ip).drop_duplicates(subset=['source_ip'],keep='first',inplace=False)
result.to_csv('result.txt',index=False,header=False,columns=['source_ip','res'])
print(len(result))