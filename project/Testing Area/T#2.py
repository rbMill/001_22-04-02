from myLib.myLibrary import myList

yami = myList.gen2D(5,5,orientation='lr-tb')

def sort2D(arr2D,orientation):
    ore = orientation
    _col,_row = zip(*arr2D)
    res = []

    if orientation[:2] == 'tb' or orientation[:2] == 'bt':
        flip = True
    else:
        flip = False
    def change(val,dir):
        dik = {'lr': sorted(val), 'rl': sorted(val,reverse=True), 'bt': sorted(val), 'tb': sorted(val,reverse=True)}
        return dik.get(dir)
    d1 = orientation[:2]
    d2 = orientation[-2:]
    xcol = change(_col,d1)
    yrow = change(_row,d2)
    xs = change(list(set(xcol)),d1)
    ys = change(list(set(xcol)),d2)
    xdic = dict(zip(xs,[[] for _ in xs]))
    ydic = dict(zip(ys, [[] for _ in ys]))
    for x,y in arr2D:
        xdic[x].append(y)
        ydic[x].append(x)
    print(xdic,ydic)
    def sort(top,bot,flip):
        for t in top:
            for b in bot:
                if flip:
                    res.append([b,t])
                else:
                    res.append([t,b])
    # print(_col,xcol,xs,'',_row,yrow,ys,sep='\n')


    return res
print(yami,'\n')
morn = sort2D(yami,'lr-tb')
# print(yami)
print('\n',morn,sep='')
