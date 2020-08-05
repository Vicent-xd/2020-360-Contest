import pandas as pd
import numpy as np
import glob,os
path=r'./ja3_all/'
all_ip=[]
ip_ja3_test=pd.read_csv(path+'ip_ja3_test.csv',sep=',',index_col=None,usecols=['source_ip'])
ip_ja3s_test=pd.read_csv(path+'ip_ja3s_test.csv',sep=',',index_col=None,usecols=['source_ip'])
ii=pd.read_csv(path+'ip_ja3_test.csv',sep=',',index_col=None,usecols=['destination_ip'])
dd=pd.read_csv(path+'ip_ja3s_test.csv',sep=',',index_col=None,usecols=['destination_ip'])

ip_ja3_test=ip_ja3_test.drop_duplicates()
ip_ja3s_test=ip_ja3s_test.drop_duplicates()
m1=ip_ja3_test.append(ip_ja3s_test).drop_duplicates()
m2=ii.append(dd).drop_duplicates()

ip_ja3_test['res']=['white']*len(ip_ja3_test)
ip_ja3_test.to_csv('pour.txt',index=False,header=False)
print(ip_ja3_test)

#print(len(m1)+len(m2))
for a in m1['source_ip']:
    all_ip.append(a)
#for b in m2['destination_ip']:
#    all_ip.append(b)
#print(len(set(all_ip)))