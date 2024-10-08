# ctypes-notes
By Austin Bu

Ctypes is a python library used to interface between C and python. C code is compiled into a .so which python can then load and use functions from. It’s built into python, so there are no external dependencies. To use ctypes with C++, we need to take some extra steps. 

Step 1: Code in C++ and extern desired functions 

Step 2: Compile into .so 

Step 3: Use ctypes to load the library 

Example: 
add.cpp 
```cpp
extern "C" { 
    int add_one(int in) { 
        return in + 1; 
    } 
} 
```

main.py 
```python
from ctypes import * 
libcpp = cdll.LoadLibrary('build/libcpp.so') 
print(libcpp.add_one(1)) 
```

./run.sh 
```bash
 g++ -std=c++17 -shared -o build/libcpp.so -fPIC src/*.cpp 
 python3 python/main.py 
```
### Types
Define the argtypes (Argument types) and restype (Return type) of the functions. Ctypes is limited in what data types it can pass. Namely, it cannot directly pass C++ unique data types such as vectors. All data types need to be native to C. 

Here we can use ctypes to define a Structure to allow passing custom data types. 

data.h 
```cpp
class Data { 
public: 
    Data(const char* name, int value); 

    const char* name; 
    int value; 
}; 
```

data.cpp 
```cpp
#include "../include/data.h" 

Data::Data(const char* name, int value) { 
    this->name = strdup(name); 
    this->value = value; 
} 
```

add.cpp 
```cpp
#include "../include/data.h" 

extern "C" { 
    Data* add_data(Data* one, Data* two, const char* name) { 
        return new Data(name, one->value + two->value); 
    }
} 
```

main.py
```python
class Data(Structure): 
    _fields_ = [("name", c_char_p), 
                ("value", c_int)] 

libcpp.add_data.argtypes = [POINTER(Data), POINTER(Data)] 
libcpp.add_data.restype = POINTER(Data) 

data_one = Data(b"one", 1) # byte data 
data_two = Data(b"two", 2) 

data_three = libcpp.add_data(data_one, data_two, b"three")[0]
print(data_three.name.decode("utf-8"), data_three.value) 
```

You can make a pointer list like this: 
main.py
```python
list = [data_one, data_two, data_three] 
listtype = Data * len(list) 
data_list = listtype(*list) 
print(libcpp.sum_data(data_list, len(list))) 
```

add.cpp
```cpp
extern "C" {
    int sum_data(Data* datalist, int length) {
        int sum = 0;
        for (int i = 0; i < length; i++) {
            sum += datalist[i].value;
        }
        return sum;
    }
}
```
In practice you should bundle the length with the list in a new object 

### Memory Management
Objects made in python are memory managed by python. If you use new to create an object in C++, you will need to manually manage memory there. 

data.cpp
```cpp
Data::~Data() { 
    delete[] name; 
} 

extern "C" { 
    void del_data(Data* data) { 
        delete data; 
    } 
} 
```

main.py
```python
libcpp.del_data.argtypes = [POINTER(Data)] 
... # Don’t need to delete data_one and data_two 
libcpp.del_data(data_three) 
```

### Some other notes
- Since ctypes interacts with C, function overloading is not supported 

- Structs can have functions in them, but are not detected (no autocomplete) 

- You can use a c_void_p instead of an Object pointer, if you keep track of its type 

- Passing by pointer is preferred, else the object will get autodeleted by a destructor 

### Some recommendations
- atexit is a nice library for deleting all the C++ objects at the end. You can just make a super list of objects (helps with keeping a reference too) and delete them atexit 

- Use lots of wrappers, since there a lot of pointers when using ctypes, and none of them have autocomplete 

- Use a debugger, since you'll probably see lots of segfaults 

### Links
https://docs.python.org/3/library/ctypes.html
https://docs.python.org/3/library/atexit.html