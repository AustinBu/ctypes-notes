#include "../include/data.h"

Data::Data() {}

Data::Data(const char* name, int value) {
    this->name = strdup(name);
    this->value = value;
}

Data::~Data() {
    delete[] name;
}

extern "C" {
    void del_data(Data* data) {
        delete data;
    }
}