#count
res=[]
f = open('result.txt','r')
for x in f:
    res.append(x)
print(len(res))
