def CorCof(x_v,y_v):
    sum_x = 0
    sum_y = 0
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    n = len(x_v)
    for x,y in zip(x_v,y_v):
        print(x,y)
        sum_x+=x
        sum_y+=y
        sum_xy+=x*y
        sum_x2+=x*x
        sum_y2+=y*y
    top = n*sum_xy - (sum_x*sum_y)
    bottom = ((n*sum_x2-sum_x**2)*
    ((n*sum_y2-sum_y**2)))**0.5
    result = round(top/bottom,3)
    return result

def mean(l):
    return round(sum(l)/len(l),3)

def sde(l,m):
    result = 0
    for i in l:
        result += (i-m)**2
    return round((result/len(l))**0.5,3)

x = [9,12,6,15,3,18,10,13,7]
x1 = [9,17,9,20,2,21,15,22,26]
mewx = mean(x)
mewx1 = mean(x1)
print("mean",mewx,mewx1)
devx = sde(x,mewx)
devx1 = sde(x1,mewx1)
print("standard devs",devx,devx1)
#critical value == 1.860


