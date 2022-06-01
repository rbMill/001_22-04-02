x = [190,220,270,360,460,540]
y  = [9,8,13,17,23,27]

sum = [0,0,0,0,0]

for (k,v) in zip(x,y):
    # print(f"{k}, {v}, {k**2}, {v**2}, {k*v}")
    sum[0]+=k
    sum[1]+=v
    sum[2]+=k**2
    sum[3]+=v**2
    sum[4]+=k*v
    # print(v*k)
for i in sum:
    print(i)