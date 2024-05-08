class MyClass:
    def __init__(self,value1,value2,value3):
        self.__value1 = value1
        self.__value2 = value2
        self.__value3 = value3

    @property
    def value1(self):
        """The value1 property."""
        return self.__value1

    @value1.setter
    def value1(self, value):
        self.__value1 = value

    @property
    def value2(self):
        """The value2 property."""
        return self.__value2

    @value2.setter
    def value2(self, value):
        self.__value2 = value

    @property
    def value3(self):
        """The value3 property."""
        return self.__value3

    @value3.setter
    def value3(self, value):
        self.__value3 = value

instance = MyClass(1,2,3)
print(instance.value1)
print(instance.value2)
print(instance.value3)
instance.value1 = 2
instance.value2 = 3
instance.value3 = 4
print(instance.value1)
print(instance.value2)
print(instance.value3)

