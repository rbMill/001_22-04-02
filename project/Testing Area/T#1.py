
def bitGenerator(start,stop):
    size = len(bin(stop)[2:])
    result = []
    for i in range(start,stop+1):
        txt = bin(i)[2:]
        bn = ('0' * (size - len(txt))) + txt
        result.append(bn)
    return result

y = bitGenerator(1,100)
print(sorted(y,reverse=True))