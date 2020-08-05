import pandas as pd
import numpy as np
import glob,os
path=r'./ja3_all/'

#file=glob.glob(os.path.join(path, "*.csv"))
#print(file)
ip_ja3s_white=pd.read_csv(path+'ip_ja3s_white.csv',sep=',',index_col=None,usecols=['ja3_digest'])#'destination_ip','ja3_digest'])
ip_ja3s_black=pd.read_csv(path+'ip_ja3s_black.csv',sep=',',index_col=None,usecols=['ja3_digest'])#['destination_ip','ja3_digest'])
#print(ip_ja3s_black.duplicated())
#print(ip_ja3s_black.drop_duplicates())
#print(ip_ja3s_white.drop_duplicates())
ja3s_black_white_jiaoji=pd.merge(ip_ja3s_black.drop_duplicates(),ip_ja3s_white.drop_duplicates()) #既在black里又在white里
#print(pd.merge(ip_ja3s_white,ip_ja3s_black,on=['ja3_digest'],how='outer'))

##white里去掉交集
ja3s_white_minus_jiaoji=ip_ja3s_white.drop_duplicates().append(ja3s_black_white_jiaoji).drop_duplicates(keep=False)
##black里去掉交集
ja3s_black_minus_jiaoji=ip_ja3s_black.drop_duplicates().append(ja3s_black_white_jiaoji).drop_duplicates(keep=False)
#print(ja3s_white_minus_jiaoji)

ip_ja3s_test=pd.read_csv(path+'ip_ja3s_test.csv',sep=',',index_col=None,usecols=['destination_ip','ja3_digest'])
#提取白样本
ja3s_white=pd.merge(ip_ja3s_test,ja3s_white_minus_jiaoji)
#提取黑样本
ja3s_black=pd.merge(ip_ja3s_test,ja3s_black_minus_jiaoji)

#添加结果
ja3s_white['res']=['white']*len(ja3s_white)
#ja3s_white.to_csv('result.csv',index=False,header=False,columns=['destination_ip','res'])
ja3s_black['res']=['black']*len(ja3s_black)
#合并结果并输出
ja3s_white.append(ja3s_black).to_csv('ja3s_result.txt',index=False,header=False,columns=['destination_ip','res'],)





ip_ja3_white=pd.read_csv(path+'ip_ja3_white.csv',sep=',',index_col=None,usecols=['destination_ip','ja3_digest'])
ip_ja3_black=pd.read_csv(path+'ip_ja3_black.csv',sep=',',index_col=None,usecols=['destination_ip','ja3_digest'])


'''
print(ip_ja3s_white)
print(ip_ja3s_black)
'''