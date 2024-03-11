void extern_destroi_mi(void);

class Test {
public:
    int a;

    Test() {
        a = 0;
    }

    ~Test() {
        extern_destroi_mi();
    }

    virtual int get(void) {
        return a;
    }

    virtual void increment(void) {
        a++;
    }
};

Test cpp_object_test;
Test cpp_object_test2;

const char rodata_some_string[] = "this is a string";
const char *data_string_pointer = "this is a pointer to a string";

int data_arr[] = {
    0xA, 0x1, 0xF,
};

short bss_var;

int text_func(int b) {
    return b + cpp_object_test.a;
}
