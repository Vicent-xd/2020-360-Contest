#coding:utf-8
import pandas as pd
import numpy as np
import glob,os
path=r'./ja3_go/'
legal_ja3_go=pd.read_csv(path+'legal_ja3_go.csv',sep=',',index_col=None,usecols=['ja3_digest'])

#ja3_digest计数
res=legal_ja3_go['ja3_digest'].value_counts().rename_axis('ja3_digest').reset_index(name='fp_num')
#print(res)

#整理原始文件到ip-ja3_digest-计数项:source_ip的格式
legal_ja3_go_full=pd.read_csv(path+'legal_ja3_go.csv',sep=',',index_col=None,usecols=None)
legal_ja3_go_full.drop([len(legal_ja3_go_full)-1],inplace=True)
legal_ja3_go_full['source_ip'].fillna(method='ffill',inplace=True)
legal_ja3_go_full=legal_ja3_go_full.dropna().reset_index()

#拼接fp_num到整理后的文件
legal_ja3_go_full=pd.merge(legal_ja3_go_full,res,how='inner')
print(legal_ja3_go_full)

#输出到csv
legal_ja3_go_full.to_csv('legal_ja3_go_fp_num.csv',index=False,header=True,columns=None)
'''
col1=pd.DataFrame(legal_ja3_go_full['source_ip'].fillna(method='ffill'))
print(col1)
print(len(col1))
col2=pd.DataFrame(legal_ja3_go_full['ja3_digest'].dropna())
print(len(col2))
col1['ja3_digest']=list(col2)
print(col1)
#print(legal_ja3_go_full.dropna())
pd1=pd.merge(legal_ja3_go_full,res,how='outer')
pd1.to_csv('legal_ja3_go_fp_num.csv',index=False,header=True,columns=None)
#print(pd1)
'''