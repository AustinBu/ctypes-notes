from ctypes import *

libcpp = cdll.LoadLibrary('build/libcpp.so')

print(libcpp.add_one(1))

class Data(Structure):
    _fields_ = [("name", c_char_p),
                ("value", c_int)]
    
libcpp.add_data.argtypes = [POINTER(Data), POINTER(Data), c_char_p]
libcpp.add_data.restype = POINTER(Data)

data_one = Data(b"one", 1) # utf-8 encoding
data_two = Data(b"two", 2)

data_three = libcpp.add_data(data_one, data_two, b"three")[0]
print(data_three.name.decode("utf-8"), data_three.value)

libcpp.sum_data.argtypes = [POINTER(Data), c_int]
libcpp.sum_data.restype = c_int

list = [data_one, data_two, data_three]
listtype = Data * len(list)
data_list = listtype(*list)
print(libcpp.sum_data(data_list, len(list)))

libcpp.del_data.argtypes = [POINTER(Data)]
libcpp.del_data(data_three)