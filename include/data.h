#ifndef ATTRS_H
#define ATTRS_H

#include <iostream>

class Data {
public:
    Data();

    Data(const char* name, int value);

    ~Data();

    const char* name;
    int value;
};

#endif // ATTRS_H