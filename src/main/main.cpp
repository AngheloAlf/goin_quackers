int OS_main(int argc, char* argv[]);
extern "C" void mwExit(void);
extern "C" void mwInit(void);

int main(int argc, char *argv[]) {
    int ret;

    mwInit();
    ret = OS_main(argc, argv);
    mwExit();

    return ret;
}
