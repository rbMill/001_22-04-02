from myLib.myLibrary import myList
import regex



dirc = 'lr-bt'
yami = myList.gen2D(5,2,orientation=dirc)
morn = myList.sort2D(yami,'tb-lr')
print(f'{len(yami)} ~ {len(morn)}')
for a,b in zip(yami,morn):
     print(f'{a} is {b}, {morn.index(a)}')
print(yami == morn)