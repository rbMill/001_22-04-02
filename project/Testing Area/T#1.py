class baseClass:
    data_type = 'none'
    def __init__(self,data_type,*args):
        if len(args) > 0:
            print('from_person',args)
        self.data_type = data_type

    def other_method(self,*args):
        print( f'{self.data_type} is {" ".join(args)}')

class animalClass(baseClass):
    def __init__(self,*args):
        if len(args) > 0:
            print('from_animal',args)
        super(animalClass, self).__init__('animal')


class personClass(baseClass):
    def __init__(self,*args):
        if len(args) > 0:
            print('from_person',args)
        super(personClass, self).__init__('person')

    def other_method(self,*args):
        print('The person was')
        super(personClass, self).other_method(*args)

class hybridClass(personClass,animalClass):
    def __init__(self,*args):
        super(hybridClass, self).__init__()

a = personClass()
a.other_method('hayasaca')
#
# b = animalClass()
# b.other_method('fluffy')
#
# c = hybridClass()
# print(hybridClass.mro())
# for I,i in enumerate(hybridClass.mro()):
#     try:
#         print(I,i().data_type,i,sep='~')
#     except TypeError:
#         print(I,i('none').data_type, i,sep='~')
#     except AttributeError:
#         print(I,i.__name__)