#include "../include/data.h"

extern "C" {
    int add_one(int in) {
        return in + 1;
    }

    Data* add_data(Data* one, Data* two, const char* name) {
        return new Data(name, one->value + two->value);
    }

    int sum_data(Data* datalist, int length) {
        int sum = 0;
        for (int i = 0; i < length; i++) {
            sum += datalist[i].value;
        }
        return sum;
    }
}