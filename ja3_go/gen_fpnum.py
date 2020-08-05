#gen fp_num
import pandas as pd
import numpy as np
import glob,os
path=r'./'

target_file=path+'malware_ja3_go.csv'
figerprint_col='ja3_digest'
ip='source_ip'
'''
target_file=path+'legal_ja3.csv'
figerprint_col='ja3_digest'
ip='source_ip'
'''
new_file='./fp_num_'+target_file[2:]

target=pd.read_csv(target_file,sep=',',index_col=None,usecols=[ip,figerprint_col])
target.drop_duplicates(inplace=True)
target_no_na=target.dropna(inplace=False)
#取出na部分
tmp_na=target.append(target_no_na).append(target_no_na)
tmp_na=tmp_na.drop_duplicates(keep=False)
tmp_na['fp_num']=[0]*len(tmp_na)
#计算剩余部分每个ip的digest种类数，生成ip-num
ip_num=target_no_na[ip].value_counts().rename_axis(ip).reset_index(name='fp_num')
#追加到target_no_na表后
target_no_na=pd.merge(target_no_na,ip_num,how='outer')
#append na部分
result=target_no_na.append(tmp_na)
#result.to_csv(new_file,index=False,header=True)
#追加到完整原始文件最后一列
target=pd.read_csv(target_file,sep=',',index_col=None)
result=pd.merge(target,result,how='outer')
result.to_csv(new_file,index=False,header=True)
#print(result)
'''
all_ip=pd.read_csv('all_ip.csv',sep=',',index_col=None,usecols=['source_ip'])
all_ip['fp_num']=[0]*len(all_ip)
all_ip.rename(columns={'source_ip':ip},inplace=True)
result=pd.merge(result,all_ip,how='outer')
result.to_csv(new_file,index=False,header=True)
#print(result)
'''