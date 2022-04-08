import time
import json
import ast
import tkinter
import types
import os
import regex
import ctypes
import math
from PIL import ImageTk as PILimageTk
from PIL import Image as PILimage
from configparser import ConfigParser

class myConstants():
    def __init__(self):
        self.monthDikLong = {'JANUARY' : '01','FEBRUARY' : '02','MARCH' : '03','APRIL' : '04','MAY' : '05','JUNE' : '06','JULY' : '07','AUGUST' : '08','SEPTEMBER' : '09','OCTOBER' : '10','NOVEMBER' : '11','DECEMBER' : '12',}
        self.monthDikShort = {'JAN' : '01','FEB' : '02','MAR' : '03','APR' : '04','MAY' : '05','JUN' : '06','JUL' : '07','AUG' : '08','SEP' : '09','OCT' : '10','NOV' : '11','DEC' : '12',}
        self.angele_direction = {-45:'dr',-135:'dl',45:'ur',135:'ul',0:'right',90:'up',-90:'down',180:'left'}

    def screensize(self=None):
        user = ctypes.windll.user32
        return [user.GetSystemMetrics(0),user.GetSystemMetrics(1)]
class myMath():
    def angleBetweenPoints(orig, targ):
        deltaX = targ['x'] - orig['x']
        deltaY = targ['y'] - orig['y']
        arctan = math.atan2(deltaY, deltaX)
        return math.degrees(arctan)

    def fixNumber(num):
        end = None
        if type(num) == str:
            try:
                end = ast.literal_eval(num)
            except SyntaxError:
                if num == '.':
                    end = 0
        elif type(num) == int or type(num) == float:
            end = num
        else:
            raise ValueError(f'Invalid value ({str(num)})')
        if end == None:
            raise ValueError(f'Invalid value ({str(num)})')
        if type(end) == float and end - int(end) == 0:
            end = int(end)
        return end


    def mathList(lists, operation='+', handlezeroas=False):
        result = []
        if len(lists) <= 1: raise ValueError('Insuffecient List No comparison')
        for i in lists:
            while len(result) < len(i):
                result.append(None)
            if type(i) == tuple:
                i = list(i)
            if type(i) != list: raise TypeError('Must be a list')
            for In, x in enumerate(i):
                if type(x) == str:
                    if x.count('.') == 0:
                        try:
                            x = int(x)
                        except TypeError:
                            raise ValueError(f'Invalid Number for ({x})')
                    else:
                        try:
                            x = float(x)
                        except TypeError:
                            raise ValueError(f'Invalid Number for ({x})')
                if result[In] == None:
                    result[In] = x
                elif result[In] != None:
                    try:
                        result[In] = myMath.doMath(result[In], x, op=operation)
                    except ZeroDivisionError:
                        if handlezeroas == False:
                            raise ZeroDivisionError(f'When ({result[In]} / {x})')
        return result

    def doMath(num1,num2,op="+",orderhandling=False):
        if bool(regex.search(r'[+x*/-]',op)) == False:
            raise ValueError(f'DoMath\n\tNonMatching Opperand\ngiven: ({op})')
        if orderhandling == True:
            if num2 > num1:
                n1 = num1
                num1 = num2
                num2 = n1
        if op == "+":
            return num1 + num2
        elif op == "-":
            return num1 - num2
        elif op == "/":
            if num2 != 0:
                return num1/num2
            else:
                raise ZeroDivisionError
        elif op == "*" or op == 'x':
            return num1 * num2
    def clamp(input, minlim, maxlim):
        if minlim > maxlim:
            return
        if (int(input) <= minlim):
            return int(minlim)
        elif (input >= maxlim):
            return int(maxlim)
        else:
            return input
    def inverseNums(start,end):
        for x in range(int(end)):
            if int(x/2)-float(x/2) == 0:
                print(x)
            elif int(x/2)-float(x/2) == 0:
                print(end-x)

    def strtoMath(statement,allowexponents=True):
        if type(statement) != str:
            TypeError("Error Must Be a string")
            return
        statement = statement.replace("x", "*")
        statement = statement.replace("^", "**")
        if allowexponents == False and statement.count('**') > 0: return 0
        if bool(regex.search("[0-9]", statement)) == False or bool(regex.search("[a-zA-Z]", statement)):
            ValueError("Wrong Expression")
            return
        try:
            return eval(statement)
        except ZeroDivisionError or ProcessLookupError:
            return
class myColor():
    def confirmHex(val):
        if val.count('#') == 1:
            if bool(regex.search('#[0123456789abcdefABCDEF]{6}')):
                return True
        elif val.count('#') == 0:
            if bool(regex.search('#[0123456789abcdefABCDEF]{6}')):
                return True
        else:
            return False
    def rgb(r=0, g=0, b=0):
        re = myMath.clamp(r, 0, 255)
        gr = myMath.clamp(g, 0, 255)
        bl = myMath.clamp(b, 0, 255)

        def rghex(num):
            scndval = int(float(num) / 16)
            fstval = int(float(num % 16))

            def hexcon(num):
                if num == 0:
                    return str(num)
                if 16 > num >= 10:
                    after9 = ["A", "B", "C", "D", "E", "F"]
                    return after9[int(num) - 10]
                elif 9 >= num > 0:
                    return str(num)
                elif num >= 16:
                    return "0"


            return str(hexcon(scndval)) + str(hexcon(fstval))

        return "#" + rghex(re) + rghex(gr) + rghex(bl)


    def hexRGB(hexrgb="None", returntype="None"):
        if hexrgb.startswith('#') and len(hexrgb) == 7:
            def HexInt(x):
                AlNum = ["A", "B", "C", "D", "E", "F"]
                if str(x).isdigit():
                    return int(x)
                elif str(x).isalpha() and str(x) in AlNum:
                    return int(AlNum.index(x.upper())) + 10
                else:
                    return "Value not allowed"

            Dualhex = lambda x, y: HexInt(hexrgb[x]) * 16 + HexInt(hexrgb[y])
            if str(returntype) == "ALL":
                return str(Dualhex(1, 2)) + ", " + str(Dualhex(3, 4)) + ", " + str(Dualhex(5, 6))
            if str(returntype) == "GET RED":
                return str(Dualhex(1, 2))
            if str(returntype) == "GET GREEN":
                return str(Dualhex(3, 4))
            if str(returntype) == "GET BLUE":
                return str(Dualhex(5, 6))
            else:
                return str("Return type incorrect.\n \n"
                           "    Return type available as follow:\n"
                           "ALL == show all number in vector3\n"
                           "GET RED == show value for red\n"
                           "GET GREEN == show value for green\n"
                           "GET BLUE == show value for blue")

        else:
            return "Incorrect Input"
class myList(list):
    def bitGenerator(start, stop):
        size = len(bin(stop)[2:])
        result = []
        for i in range(start, stop + 1):
            txt = bin(i)[2:]
            bn = ('0' * (size - len(txt))) + txt
            result.append(bn)
        return list(result)

    def list_subtract(l1, l2):
        len1 = myList.list_element_count(l1)
        len2 = myList.list_element_count(list(filter(lambda x: l1.count(x) >= 1, l2)))
        dif = myString.dicMath([len1, len2], operator='-', orderhandling=False)
        fixed = myList.dik_sort_byList(dif, l1)
        return myList.dikCounted_instance_tolist(fixed)

    def unique_list(lis):
        return list(dict.fromkeys(lis).keys())

    def dik_sort_byList(dik, lis):
        duk = {}
        for i in lis:
            if i in list(dik.keys()):
                duk[i] = dik[i]
        return duk

    def dikCounted_instance_tolist(dik):
        result = []
        for k, v in dik.items():
            if type(v) != int: raise TypeError('Must be int')
            for _ in range(v):
                result.append(k)
        return result

    def list_max(*args):
        _ = 0
        highest = None
        for i in args:
            if len(i) >= _:
                _ = len(i)
                highest = i
        return highest

    def list_min(*args):
        _ = len(args[0])
        lowest = None
        for i in args:
            if len(i) <= _:
                _ = len(i)
                lowest = i
        return lowest

    def list_element_count(lis):
        res = {}
        for i in set(lis):
            res[i] = lis.count(i)
        return res

    def list_remove(l1, l2):
        result = []
        left = []
        for i in l1:
            if l2.count(i) == 0:
                result.append(i)
            else:
                left.append(i)
        return [result,left]

    def list_get(list, element, so=None):
        result = {}
        for I, i in enumerate(list):
            result[i] = i
        return result.get(element, so)

    def listMath(var, operation='+'):
        result = 0
        for i in var:
            if type(i) == str:
                i = ast.literal_eval(i)
            result = myMath.doMath(result, i, op=operation)
        return result
    def lisAppend(__lis,__val):
        if type(__lis) != list:
            __lis = []
        if type(__val) == str:
            if __lis.count(__val) == 0:
                __lis.append(__val)
            return __lis
        elif type(__val) == list:
            for i in __val:
                if __lis.count(i) == 0:
                    __lis.append(i)
            return __lis
    def TimeSort(time, dependency=[], reverse=False):
        # This function sorts a list with matching list len in reference to an ordered time list reference
        ftime = {}
        sorting = []
        order = {}
        ordered = []
        final = []
        bdependency = []
        fine = True

        for xc,t in enumerate(dependency):
            bdependency.append([])
            if xc > 0:
                if len(t) != len(dependency[xc-1]):
                    fine = False

        if fine == False:
            raise ValueError("Unmatching Array Elements")
            return

        for It, ntime in enumerate(time):
            if str(ntime).count('PM') == 1:
                mp = 1
            elif str(ntime).count('AM') == 1:
                mp = 0
            else:
                mp = -1
            tme = str(ntime)[:-2].split(':')
            tme = f'{int(tme[0]) + (mp * 12)}{tme[1]}'
            imana = ' '.join(myString.strlist(list(ftime.keys()))).count(tme)
            if imana == 0:
                ftime[f'{tme}.0'] = ntime
                order[f'{tme}.0'] = It
                sorting.append(float(tme))

            elif imana > 0:
                ftime[f'{tme}.{imana}'] = ntime
                order[f'{tme}.{imana}'] = It
                sorting.append(float(f'{tme}.{imana}'))
        sorting.sort(reverse=reverse)
        for mt, x in enumerate(sorting):
            ordered.append(order[str(x)])
            final.append(ftime[str(x)])
        if len(bdependency) > 0:
            for Id, deps in enumerate(dependency):
                for IoE, deplems in enumerate(deps):
                    # print(f'{Id}{deps}. {IoE}"{deplems}"')
                    # print("old",bdependency[Id][IoE])
                    # print(ordered[IoE])
                    # print(dependency[Id][ordered[IoE]])
                    # print("new",deps[ordered[IoE]])
                    bdependency[Id].append(deps[ordered[IoE]])
        return (final, bdependency)

    def MathYawa(X):
        for x in X:
            sin = round(math.sin(x), 4)
            cos = round(math.cos(x), 4)
            tan = round(math.tan(x), 4)
            sec = round(1 / cos, 4)
            try:
                csc = round(1 / sin, 4)
            except ZeroDivisionError:
                csc = 'Undefined'
            try:
                cot = round(1 / tan, 4)
            except ZeroDivisionError:
                cot = 'Undefined'
            print(f'{sin}  {cos}  {tan}  {sec}  {csc}  {cot}\n')

    def mathLis(self):
        """
        :return: a dictionary with the total amount, the average of it
        """
        data = self
        sum = 0
        for i in data:
            if type(i) == float or type(i) == int:
                sum+=i
            elif type(i) == str:
                sum += len(i)
        return {'total':sum,'average':sum/len(data)}
    def lenNestLisCount(self,offset=1,start=1):
        data = self
        final = [start]
        vallen = [start]
        sum = 0
        for x,y in enumerate(data):
            cnt = final[x] + len(y) + offset
            final.append(cnt)
            sum+=cnt
            vallen.append(len(y) + offset + start)
        return [sum,final,vallen]

    def sortMDY(self, reversed=False,seperator=None):
        date = self
        if seperator is None:
            seperator = '-'
        if str(type(date)) != "<class 'myLibrary.myList'>" or ''.join(date).count(seperator) != len(date)*2:
            raise TypeError(f'Must be a list, elements are string with format of\n'
                            f' month seperator day seperator year\n'
                            f'e.g 11-21-21 or 12/21/22')
            return

        place = {}
        order = []
        result = []

        # combines element to a string
        for x, y in enumerate(date):
            ndate = y.split(seperator)
            place[f'{ndate[2]}{ndate[0]}{ndate[1]}'] = y
            order.append(int(f'{ndate[2]}{ndate[0]}{ndate[1]}'))
            order.sort(reverse=reversed)
        for x, y in enumerate(order):
            result.append(place.get(str(y)))
        return result
class myString(str):
    def val_to_posTuple(val):
        def convert(var):
            if var <= 9 and var >= 0:
                return (0, int(str(var)[-1]))
            elif var > 9:
                if len(str(var)) > 2:
                    # print('as',var,str(var)[:-1])
                    return (int(str(var)[:-1]), int(str(var)[-1]))
                elif len(str(var)) <= 2:
                    return (int(str(var)[-2]), int(str(var)[-1]))

        if type(val) == str:
            val = val.upper()
            if len(val) > 1:
                if bool(regex.search('[A-Z0][0-9]', val)):
                    return convert(myString.chess_to_int(val))
                else:
                    raise ValueError('did not match [A-Z][0-9]')
            elif len(val) == 1:
                if bool(regex.search('[A-Z]', val)):
                    return convert(myLibrary.myString.chess_to_int(val))
                elif bool(regex.search('[0-9]', val)):
                    return (0, int(val))
                else:
                    raise ValueError('did not match [0-9] or [A-Z]')

    def posTuple_to_chesspos(val):

        if val[0] < 0 or val[0] > 26:
            raise ValueError('exceeded limits 0->26 for first value')
        if val[1] < 0 or val[1] > 9:
            raise ValueError('exceeded limits 0->9 for first value')
        if val[0] > 0:
            return f'{chr(val[0] + ord("A") - 1)}{val[1]}'
        elif val[0] == 0:
            return f'0{val[1]}'

    def chess_to_int(val):
        if type(val) != str:
            raise TypeError('Must Be an String Value')
        val = val.upper()
        if len(val) == 1:
            if bool(regex.search(r'[0-9]',val)):
                return int(val)
            elif bool(regex.search(r'[A-Z]',val)):
                return int(ord(val)-ord('A')+1)*10
        elif len(val) == 2:
            if bool(regex.search(r'[A-Z][0-9]',val)):
                return (int(ord(val[0]) - ord('A') + 1) * 10) + int(val[1])
            elif  bool(regex.search(r'0[0-9]',val)):
                return int(val[-1])
            else:
                raise ValueError(f'Incorrect Value ({val})')
        else:
            raise ValueError(f'Incorrect Value ({val})')

    def int_to_chess(val):
        if type(val) == str:
            val = ast.literal_eval(val)
        if type(val) != int:
            raise TypeError('Must Be an Integer Value')
        if val >= 270 or val < 0:
            raise ValueError('Exceeded 270 limit\n or was less than 0')
        val = str(val / 10)
        pre = chr(int(val[:-2]) + ord('A') - 1)
        pre = pre.replace('@', '0')
        post = val[-1]
        return f'{pre}{post}'

    def indexInstance(self, val):
        result = []
        listedself = []
        if type(self) is str:
            for i,c in enumerate(self):
                try:
                    listedself.append(self[i:i+len(val)])
                except IndexError:
                    pass
        self = listedself
        for i in range(self.count(val)):
            offset = 0
            curpos = self.index(val)
            result.append(curpos)
            self[curpos] = chr(ord(val[0]) + 1)
        return result

    def myReplace(self, new, start=None, end=None):
        """
        :param orig: str(value) what you want to edit
        :param new: what you inted to replace on a specific index range
        :param start: start of index
        :param end: end of index
        :return: Returns the edited string
        """
        orig = self
        if start is None:
            start = 0
            end = len(new)
        elif end is None:
            end = len(new) + start

        start = int(start)
        end = int(end)
        def smlreplace(var, index, value):
            final = []
            for x, y in enumerate(var):
                if x == int(index):
                    final.append(str(value))
                if x != int(index):
                    final.append(y)
            return ''.join(final)

        u = orig
        for x in range(end - start):
            if start + x < len(orig) and x < len(new):
                u = smlreplace(u, start + x, new[x])
            elif start + x >= len(orig) and x >= len(new):
                return u
        return u
    def dicCombine(dics):
        allDics = {}
        for dic in dics:
            for key,value in dic.items():
                allDics[key] = value
        return allDics

    def _dicAddInt(dics,operator="+",orderhandling=True):
        allDics = {}
        for dic in dics:
            for item in dic:
                if bool(regex.search(r'[0-9]+',str(dic[item]))) == False:
                    raise ValueError(f'Must be a number or integer in {item} of {dic}')
                allDics[item] = 0
        for Id,dic in enumerate(dics):
            for item in allDics:
                if list(dic.keys()).count(item) == 1:
                    result = myMath.doMath(num1=myMath.fixNumber(allDics[item]),num2=myMath.fixNumber(dic.get(item,0)),op=operator,orderhandling=orderhandling)
                    allDics[item] = round(myMath.doMath(num1=myMath.fixNumber(allDics[item]),num2=myMath.fixNumber(dic.get(item,0.0)),op=operator,orderhandling=orderhandling),3)
        return allDics
    def dicMath(dics,operator="+",orderhandling=True):
        result = {}
        for Dc,dic in enumerate(dics):
            for key,val in dic.items():
                if key not in list(result.keys()):
                    result[key] = val
                if Dc > 0:
                    result[key] = myMath.fixNumber(myMath.doMath(result[key],val,op=operator,orderhandling=orderhandling))
        return result

    def dicTotalInternal(self,operation="+"):
        dik = self
        total = 0
        for item in dik.items():
            total = myMath.doMath(total,item[1],operation)
        return total
    def AlphatoNum():
        Alpha = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        name = input("Whats your name? \n")
        var = 0
        for x in name:
            try:
                vx = Alpha.index(x)
                nx = lambda x: x - 26 if x > 26 else x
                var = var + nx(vx)
            except:
                pass
        return "Sigma: " + str(var)

    def setDicValues(dic, val):
        for y in dic:
            dic[y] = val
        return dic
    def encrypt(password, key):
        def nospace(text):
            etext = text.strip()
            etext = etext.lower()
            etext = etext.split()
            new_text = ""
            i = 0
            while i < len(etext):
                new_text = new_text + etext[i]
                i += 1
            return new_text

        fKey = nospace(key)

        def convert(v0, v1):
            leest = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            v2 = v1
            while len(v2) < len(leest):
                v2 = v2 + v1
            i = 0
            encrypted = ""
            while i < len(v0):
                x = str(v0[i])
                y = leest.index(x)
                z = v2[y]
                encrypted = str(encrypted) + str(z)
                i += 1
            return encrypted

        final = convert(password, fKey)
        return final

    def strlist(list):
        try:
            x = []
            for y in list:
                x.append(str(y))
            return x
        except TypeError:
            raise TypeError("Must Be a list")
            return "TypeError: Must be group"
    def fltlist(list):
        final = []
        try:
            for y in list:
                final.append(float(y))
            return final
        except TypeError:
            print("TypeError: Must be group")
            return "TypeError: Must be group"
    def findmatch(database, item,casesensitivity=False,ifnone=None):
        """
            This fucntion is for finding a match of items from a list
        :param list type: item: List of keyname data
        :param bool type: casesensitivity: if the needed name has to be of equal casesettings
        :param show or hide: ifnone: if no string is given or is none will it show all or none
        :return: Matching stric list
        """
        database = myString.strlist(database)
        matched = []

        if (type(database) == list) == True:
            x = 0
            if item == 'ALL':
                return database
            while x < len(database):
                y = 0
                a = ''
                if len(item) == 0 and ifnone == 'hide':
                    return None
                while y < len(item) and len(item) <= len(database[x]):
                    a = a + database[x][y]
                    y += 1
                if item.upper() == a.upper() and casesensitivity == False:
                    matched.append(database[x])
                if item == a and casesensitivity == True:
                    matched.append(database[x])
                x += 1
            if len(matched) == 0:
                return None
            elif len(matched) >= 1:
                return matched
        elif (type(database) == list) == False:
            print('Type Error: Must be a list')
            return
class myTime():
    def sec_to_Timer(time ,seperator=':', remove_if_zero=False):
        hrs, mns, scs = 0, 0, 0
        hrs = time / 3600
        mns = (hrs - int(hrs)) * 60
        scs = (mns - int(mns)) * 60
        hrs = int(hrs)
        mns = int(mns)
        scs = int(scs)
        _3, _2,_1 = f'{hrs}{seperator}', f'{mns}{seperator}',str(scs)
        if hrs < 10:
            _3 = f'0{hrs}{seperator}'
        if mns < 10:
            _2 = f'0{mns}{seperator}'
        if scs < 10:
            _1 = f'0{scs}'
        if hrs == 0 and remove_if_zero:
            _3 = ''
        if mns == 0 and remove_if_zero:
            _2 = ''
        return f'{_3}{_2}{_1}'

    def dateInterpret(date, keepseprator=False, replace='-'):
        final = ['year', 'month', 'day']
        date = date.strip()
        dayreg = '(0[1-9]|[1-2][0-9]|3[0-1])'
        monthbynum = '(0[-9]|1[0-2])'
        constants = MyConstants()
        monthLong = constants.monthDikLong
        monthshort = constants.monthDikShort
        if date.count('-') == 2:
            separator = '-'
            date = date.split('-')
        elif date.count('/') == 2:
            separator = '/'
            date = date.split('-')
        elif date.count(' ') == 2:
            separator = ' '
            date = date.split(' ')
        else:
            raise ValueError('\n\tImproper Date, seperators is unknown\n\tor inconistent')
        for d in date:
            if bool(regex.search('[0-9]{4}', d)):
                final[0] = d
            elif bool(regex.search('[a-zA-Z]+', d)):
                bylong = monthLong.get(d.upper(), None)
                byshort = monthshort.get(d.upper(), None)
                data = myString.findmatch(monthLong, d.upper())
                if bylong != None:
                    final[1] = bylong
                elif byshort != None:
                    final[1] = byshort
                elif type(data) == list and len(data) > 0:
                    final[1] = monthLong.get(data[0])
                else:
                    raise ValueError('Invalid Month')

            elif bool(regex.search(r'(0[1-9]|1[0-2])', d)) and final[1] == 'month':
                final[1] = d
            elif bool(regex.search(r'[0-9]', d)) and final[1] == 'month':
                final[1] = d
            elif bool(regex.search(r'0[1-9]|[1-2][0-9]|3[0-1]', d)) and final[1] != 'month':
                final[2] = d
            elif bool(regex.search(r'[1-9]', d)) and final[1] != 'month':
                final[2] = d
        if final[0] == 'year': raise ValueError(f'Cannot interpret year at {separator.join(date)}')
        if final[1] == 'month': raise ValueError(f'Cannot interpret month at {separator.join(date)}')
        if final[2] == 'day': raise ValueError(f'Cannot interpret day at {separator.join(date)}')
        if keepseprator == False: separator = replace
        return separator.join(final)

    def dateToStr(val, position=((0, 1, 2), (0, 1, 2)), seperator='-', month=None, replace=None):
        if month is None:
            month = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
        elif month is False:
            month = "01 02 03 04 05 06 07 08 09 10 11 12".split()
        if replace == None:
            replace = seperator
        vale = val.split(seperator)
        if regex.search('0[0-9]',str(vale[position[0].index(1)])):
            vale[position[0].index(1)] = str(vale[position[0].index(1)])[1]
        monthI = int(vale[position[0].index(1)]) - 1
        mpos = month[monthI]
        vale[position[0].index(1)] = mpos
        sndpos = position[1]
        fs = vale[position[0].index(position[1][0])]
        ss = vale[position[0].index(position[1][1])]
        td = vale[position[0].index(position[1][2])]
        final = [fs, ss, td]
        return replace.join(final)

    def getclock():
        times = time.localtime()
        times = list(times)
        hour = times[3]
        mins = times[4]
        sign = "AM"
        if hour > 12:
            sign = "PM"
            hour+=-12
        if mins <= 9:
            mins = f'0{mins}'

        return f'{hour}:{mins}{sign}'

    def correctdate(type='numeric',order=(0,1,2),seperator="-"):
        nt = time.localtime()
        nt = list(nt)
        if type=='numeric':
            if len(str(nt[1])) == 1:
                nt[1] = f'0{nt[1]}'
            if len(str(nt[2])) == 1:
                nt[2] = f'0{nt[2]}'
        Monthname = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC"
        Monthname = Monthname.split()
        if type == "numeric":
            date = f'{nt[order[0]]}{seperator}{nt[order[1]]}{seperator}{nt[order[2]]}'
        elif type == "alpha":
            nt[1] = Monthname[nt[1]-1]
            date = f'{nt[order[0]]}{seperator}{nt[order[1]]}{seperator}{nt[order[2]]}'
        return date
class TkinterMethods():
    def buttontoggle(widget,disabled='#D0D0D0',active='white',opposed=None,funcs=None,onlycolor=True):
        if opposed!=None:
            for widg in opposed:
                widg.config(bg=disabled)
                if onlycolor == False:
                    widg.config(state=tkinter.DISABLED)
        if widget.cget('bg') == disabled:
            widget.config(bg=active)
            if onlycolor == False:
                widget.config(state=tkinter.NORMAL)
        if widget.cget('bg') == active:
            widget.config(bg=disabled)
            if onlycolor == False:
                widget.config(state=tkinter.DISABLED)
        if funcs != None:
            for f in funcs:
                if type(funcs) == types.FunctionType:
                    f()


    def DefaultText(widget,default,disabled=('#808080','#D0D0D0'),active=('black','white'),setDis=False,setAct=False):
        if type(widget) == tkinter.Entry:
            if (widget.get() == str(default) and widget.cget('fg') == disabled[0]) or setAct:
                widget.config(fg=active[0], bg=active[1])
                widget.delete(0,tkinter.END)
            elif widget.get() == '' or setDis==True:
                widget.config(fg=disabled[0],bg=disabled[1])
                widget.insert(tkinter.END,str(default))
            else:
                cont = widget.get()
                widget.delete(0,tkinter.END)
                widget.insert(tkinter.END,cont.replace(str(default),''))
                widget.config(fg=active[0], bg=active[1])
        elif type(widget) == tkinter.Text:
            if widget.get('0.0',END).replace('\n','') == '' or setDis==True:
                widget.config(fg=disabled[0],bg=disabled[1])
                widget.insert(tkinter.END,str(default))
            elif (widget.get('0.0',END).replace('\n','') == str(default) and widget.cget('fg') == disabled[0]) or setAct:
                widget.config(fg=active[0], bg=active[1])
                widget.delete('0.0',END)
    def ButtonImage(path,size):
        myimage = PILimageTk.Image.open(path)
        myimage = myimage.resize((size,size),PILimageTk.Image.ANTIALIAS)
        myimage = PILimageTk.PhotoImage(myimage)
        return myimage
class myDictionary():
    def pretty_print(dic):
        for k,v in dic.items():
            try:
                extra = v.__name__
            except AttributeError:
                extra = None
            print(f'{k} == {v}, {extra}')
    def dic_filter(dic, key=None,val=None,not_key=None,not_val=None):
        if type(dic) != dict:
            raise TypeError('dic must be dict')
        result = {}
        for k, v in dic.items():
            execute = True
            by = 0
            if key != None and key not in k:
                by = 1
                execute = False
            if val != None and val not in v:
                by = f'2 {val != None },{ v not in val}{k,v}'
                execute = False
            if not_key != None and not_key in k:
                by = 3
                execute = False
            if not_val != None and not_val in v:
                by = 4
                execute = False
            if execute:
                result[k] = v
        return result
    def fast_dic_inverse(dic):
        return {v: k for k, v in dic.items()}
    def str_val_inverse_dic(dic):
        result = {}
        for key, val in dic.items():
            if type(val) != str:
                val = str(val)
            val_count = " ".join(result.keys()).count(val)
            if val_count == 0:
                result[val] = key
            else:
                result[f'{val}({val_count})'] = key
        return result

    def keyCase(dik,case):
        keys,val = list(dik.keys()),list(val())
    def dikToNlineByValueStr(dik, seperator=":", tabmultiplier=1, TAB='    '):
        tb = TAB * tabmultiplier
        stb = TAB * (int(tabmultiplier) - 1)
        if type(dik) != dict: return dik
        result = ''
        for key, val in dik.items():
            fval = val
            if type(val) is dict:
                fval = ''
                nline = '\n'
                for k, v in val.items():
                    v = str(v).replace('\n', f'\n{TAB}{TAB}')
                    if bool(regex.search('[a-zA-Z]+', k)) == False: k = 'INVALID'
                    tab = tb
                    if len(k) < 2:
                        tab = f'{TAB}'
                    elif len(k) > 4:
                        tab = ' '
                    fval = f'{fval}{tb}{k} {seperator}{tab}{v}\n'
            else:
                if len(key) < 2:
                    tab = f'{TAB}'
                elif len(key) > 4:
                    tab = ''
                nline = ' '
                fval = fval.replace("\n", f'\n{TAB}');
                fval = f'{tab}{fval}\n'
            result = f'{result}{stb}{key}{seperator}{nline}{fval}'
        return result

    def sortedDik(dik, reverse=False):
        if type(dik) != dict: return dik
        dikeys = sorted(list(dik.keys()), reverse=reverse)
        result = {}
        for y in dikeys:
            result[y] = dik[y]
        return result
    def dikToRBitem(dik):
        final = []
        for key,val in dik.items():
            final.append(val);final.append(key)
        return ' '.join(final)
class myRecFuncs():
    def itemcount(item):
        keyitem = []
        quant = []
        summary = {}
        litem = str(item).upper().split()
        fix2 = myRecFuncs.fix(item)
        # function for keyitems
        for x, y in enumerate(fix2):
            if keyitem.count(y) == 0 and (str(y)[0].isalpha() or str(y)[-1].isalpha()):
                keyitem.append(y)
                quant.append(fix2[x - 1])
            elif keyitem.count(y) != 0 and (str(y)[0].isalpha() or str(y)[-1].isalpha()):
                quant[keyitem.index(y)] += fix2[x - 1]
        # function for summary
        for x, y in zip(keyitem, quant):
            summary[x] = y
        setItem = [keyitem, summary]
        return setItem
    def fix(val,case="upper"):
        var = val
        var = str(var).__getattribute__(case)().split()
        final = []
        for I, item in enumerate(var):
            if I == 0 and bool(regex.search(r'[a-zA-Z]', item)):
                if bool(regex.search(r'[a-zA-Z]', item)):
                    final.append('1')
                    final.append(item)
                elif bool(regex.search(r'[a-zA-Z]', item)) == False:
                    final.append(item)
            elif I != 0:
                if bool(regex.search(r'[a-zA-Z]', var[I-1])) == False and bool(regex.search(r'[a-zA-Z]', item)):
                    final.append(var[I-1])
                    final.append(item)
                elif bool(regex.search(r'[a-zA-Z]', var[I-1])) and bool(regex.search(r'[a-zA-Z]', item)):
                    final.append('1')
                    final.append(item)
        return final

    def calcuForm(dik,dataprice,sign='x'):
        st = []
        dat = 0
        for x in dik:
            y = f'{dik[x]} {sign} {dataprice.get(x, 0)}'
            dat+=int(dik[x])*float(dataprice.get(x,0))
            st.append(y)
        st = ") + (".join(st)
        return [dat,f'({st})']
class myFileMethods():
    def getSETTINGS(path,casesettings=None):
        """
            This functions returns a list where index 0 is dictionary and
        index 1 are keywords in the said dictionary a readable file
        in a syntax like 'name' = 12 or age = 12

        :param
            path :          filepath of readable file(txt)
            casesettings:   'upper','lower','title'
        :return:
            list[dictionary, keywordsused]
        """
        data = ''
        with open(path,'r') as f:
            data = f.read()
        dicstart,dicend = data.index('{'),data.index('}')
        data = data[dicstart+1:dicend]
        if casesettings == 'upper':
            data = data.upper()
        elif casesettings == 'lower':
            data = data.lower()
        elif casesettings == 'title':
            data = data.title()
        data = data.strip()
        data = data.split('\n')
        settingsdict = {}
        keyys = []
        for x in data:
            x = x.strip()
            x = x.split(' = ')
            settingsdict[x[0]] = x[1]
            keyys.append(x[0])
        keysettings = [settingsdict,keyys]
        return keysettings

    def cfgSETTINGS(path):
        CFG = ConfigParser()
        CFG.read(path)
        dik = {}
        keys = []
        for x in CFG.sections():
            for y in CFG.options(x):
                israw = False
                if y.count("path") == 1 or y.count("directory") == 1:
                    israw = True
                data = CFG.get(x,y,raw=israw)
                if data.isnumeric():
                    data = float(data)
                dik[y] = data
                keys.append(y)
        return [dik,keys]
class myMainFuncs():
    def isAdmin():
        try:
            is_admin = (os.getuid() == 0)
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return is_admin

    def my_dir(var):
        return list(filter(lambda e: e.count('__') == 0, dir(var)))

    def runfuncs(*args):
        for x in args:
            if type(x) == types.FunctionType:
                x()