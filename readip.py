import re
import pandas as pd

f = open('./ja3_all/error_ja3_test.txt', 'r')
#print([i for i in f])
ip=[]
for r in f:
    ret = re.search(r'((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)', r)
    if (ret):
        ip.append(ret.group())
print(set(ip))
print(len(set(ip)))
error_ip=pd.DataFrame(set(ip))
error_ip['res']=['white']*len(error_ip)
print(error_ip)
error_ip.to_csv('error_ja3_test_result.txt',index=False,header=False)#columns=['source_ip','res'])
print(len(error_ip))