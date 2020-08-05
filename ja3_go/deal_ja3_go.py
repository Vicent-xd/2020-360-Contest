import pandas as pd
import numpy as np
import glob,os
path=r'./'
'''
blacklist=path+'malware_ja3_go.csv'
whitelist=path+'legal_ja3.csv'
figerprint_col='ja3_digest'
ip='source_ip'
target_file=path+'test_ja3_go.csv'
output_file=path+'ja3_result.csv'
'''
blacklist=path+'malware_ja3_go.csv'
whitelist=path+'legal_ja3.csv'
figerprint_col='ja3s_digest'
ip='destination_ip'
target_file=path+'test_ja3_go.csv'
output_file=path+'ja3_result.csv'

debug=False
#file=glob.glob(os.path.join(path, "*.csv"))
#print(file)
ip_ja3_white=pd.read_csv(whitelist,sep=',',index_col=None,usecols=[figerprint_col])#'destination_ip','ja3_digest'])
print("白名单digest个数：",len(ip_ja3_white.drop_duplicates()))
ip_ja3_black=pd.read_csv(blacklist,sep=',',index_col=None,usecols=[figerprint_col])#['destination_ip','ja3_digest'])
print("黑名单digest个数：",len(ip_ja3_black.drop_duplicates()))
#print(ip_ja3s_black.duplicated())
#print(ip_ja3s_black.drop_duplicates())
#print(ip_ja3s_white.drop_duplicates())
ja3_black_white_jiaoji=pd.merge(ip_ja3_black.drop_duplicates(),ip_ja3_white.drop_duplicates()) #既在black里又在white里
#print(ja3_black_white_jiaoji)
print("黑白名单digest交集个数：",len(ja3_black_white_jiaoji))
#print(pd.merge(ip_ja3s_white,ip_ja3s_black,on=['ja3_digest'],how='outer'))

##white里去掉交集
ja3_white_minus_jiaoji=ip_ja3_white.drop_duplicates().append(ja3_black_white_jiaoji).append(ja3_black_white_jiaoji)
ja3_white_minus_jiaoji=ja3_white_minus_jiaoji.drop_duplicates(keep=False)
print('白名单中去掉交集后还剩%d个digest' % (len(ja3_white_minus_jiaoji)))
if debug:
    ja3_white_minus_jiaoji.to_csv('debug_white_export.csv',index=False,header=True)
##black里去掉交集
ja3_black_minus_jiaoji=ip_ja3_black.drop_duplicates().append(ja3_black_white_jiaoji).append(ja3_black_white_jiaoji)
ja3_black_minus_jiaoji=ja3_black_minus_jiaoji.drop_duplicates(keep=False)
print('黑名单中去掉交集后还剩%d个digest' % (len(ja3_black_minus_jiaoji)))
if debug:
   ja3_black_minus_jiaoji.to_csv('debug_black_export.csv',index=False,header=True)
#print(ja3s_white_minus_jiaoji)
#添加ssbl黑样本库
sslbl=False
if sslbl:
    ssbl=pd.read_csv(path+'sslbl.csv',sep=',',index_col=None,usecols=[figerprint_col])
    ja3_black_minus_jiaoji=ja3_black_minus_jiaoji.append(ssbl)
    print('黑名单中添加sslbl后共有%d个digest' % (len(ja3_black_minus_jiaoji)))
    #去掉白名单中的sslbl ip
    ja3_white_minus_jiaoji=ja3_white_minus_jiaoji.append(ssbl).append(ssbl)
    ja3_white_minus_jiaoji=ja3_white_minus_jiaoji.drop_duplicates(keep=False)
    print('白名单中去掉sslbl后还剩%d个digest' % (len(ja3_white_minus_jiaoji)))


ip_ja3_test=pd.read_csv(target_file,sep=',',index_col=None,usecols=[ip,figerprint_col])
#提取白样本
ja3_white=pd.merge(ip_ja3_test,ja3_white_minus_jiaoji)
#print(ja3_white.drop_duplicates())
print("从test共提取出%d条白样本"%len(ja3_white.drop_duplicates(subset=[ip])))
#提取黑样本
ja3_black=pd.merge(ip_ja3_test,ja3_black_minus_jiaoji)
print("从test共提取出%d条黑样本"%len(ja3_black.drop_duplicates(subset=[ip])))

#是否合并结果并输出
output_result=True
if output_result:
    #添加结果
    ja3_white['res']=['white']*len(ja3_white)
    #ja3s_white.to_csv('result.csv',index=False,header=False,columns=['destination_ip','res'])
    ja3_black['res']=['black']*len(ja3_black)
    #合并结果并输出
    result=ja3_white.append(ja3_black)
    result=result.drop_duplicates(subset=[ip,'res'])
    result.to_csv(output_file,index=False,header=True,columns=[ip,'res'])
    print('%s共%d行'%(output_file,len(result)))

#是否提取出黑白名单中去掉交集后的清单

export=True
if export :
    full_ja3_white=pd.read_csv(whitelist,sep=',',index_col=None,usecols=[ip,figerprint_col])
    #print(full_ja3_white)
    ip_ja3_white_export=pd.merge(full_ja3_white,ja3_white[figerprint_col],how='inner').drop_duplicates(subset=[figerprint_col,ip])
    ip_ja3_white_export.to_csv('export_whitelist.csv',index=False,header=True,columns=[figerprint_col,ip])
    print('从白名单中匹配出%d条'% len(ip_ja3_white_export))
    #print(ip_ja3_white_export)
    #print(ja3_white['ja3_digest'])
    full_ja3_black=pd.read_csv(blacklist,sep=',',index_col=None)
    ip_ja3_black_export=pd.merge(full_ja3_black,ja3_black[figerprint_col],how='inner').drop_duplicates(subset=[figerprint_col,ip])
    ip_ja3_black_export.to_csv('export_blacklist.csv',index=False,header=True,columns=[figerprint_col,ip])
    print('从黑名单中匹配出%d条'% len(ip_ja3_black_export))

merge = True
if merge:
    ja3_result=pd.read_csv(output_file,sep=',',index_col=None,usecols=None)
    all_ip=pd.read_csv(path+'all_ip.csv',sep=',',index_col=None,usecols=['source_ip','res'])
    #result=ja3_result.append(all_ip).drop_duplicates(subset=['source_ip'],keep='first',inplace=False)
    all_ip.rename(columns={'source_ip':ip},inplace = True)
    #print(all_ip)
    result=ja3_result.append(all_ip).drop_duplicates(subset=[ip],keep='first',inplace=False)
    result.to_csv('result.csv',index=False,header=True)#,columns=['source_ip','res'])
    print('result.txt条数：%d'%len(result))
