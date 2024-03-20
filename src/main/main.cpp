#include "types.h"

namespace std {
    template<class T> class allocator;

    template <class T, class Allocator = allocator<T> >
    class deque
    {
    public:
    	void push_back(const T& x);
    };
}



enum GAM_eEngineState {
    GAM_eEngineState_0,
};

template<class T> class ubiSTLAllocator;

class CGameApplication {
public:
    virtual void virtual_08(); // TODO
    virtual void virtual_0C(); // TODO
    virtual void virtual_10(); // TODO
    virtual int virtual_14();
    virtual int64_t virtual_18();
    virtual int virtual_1C();
    virtual int64_t virtual_20();
    virtual void virtual_24();
    virtual void virtual_28();

    //char unk_00[0x14];
    char unk_04;
    char unk_05[0x3];
    char unk_08[0x24];
    std::deque<GAM_eEngineState, ubiSTLAllocator<GAM_eEngineState> > unk_2C;
    char unk_30[0x1C];
    int unk_4C;

    int InitEngine(void);
    int64_t DeInitEngine(void);
    void InitEngineState(void);
    void DeInitEngineState(void);

};


extern "C" void BASE_DeInitModule();                              /* extern */
extern "C" void BASE_InitModule();                                /* extern */

void DeInitGameApplication(void);                      /* extern */
CGameApplication* GAM_GetGameAppInstance();

CGameApplication *InitGameApplication(void);

#if 0
// does not match yet
int OS_main(int argc, char* argv[]) {
    int var_s0;
    CGameApplication* temp_s1;


    BASE_InitModule();

    if (InitGameApplication() == 0) {
        return 1;
    }

    var_s0 = 0;

    temp_s1 = GAM_GetGameAppInstance();

    if (temp_s1->virtual_14() == 0) {
        GAM_eEngineState sp3D;
        temp_s1->unk_04 = 1;
        sp3D = GAM_eEngineState_0;
        temp_s1->unk_2C.push_back(sp3D);
        var_s0 = 1;
    }

    if (temp_s1->InitEngine() == 0) {
        GAM_eEngineState sp3E;
        temp_s1->unk_04 = 1;
        sp3E = GAM_eEngineState_0;
        temp_s1->unk_2C.push_back(sp3E);
        var_s0 = 1;
    }

    if (temp_s1->virtual_1C() == 0) {
        GAM_eEngineState sp3F;
        temp_s1->unk_04 = 1;
        sp3F = GAM_eEngineState_0;
        temp_s1->unk_2C.push_back(sp3F);
        var_s0 = 1;
    }

    while (temp_s1->unk_04 == 0) {
        temp_s1->InitEngineState();
        temp_s1->virtual_28();

        while ((int8_t)(temp_s1->unk_4C != 0 || temp_s1->unk_04 != 0) == 0) {
            temp_s1->virtual_24();
            temp_s1->virtual_28();
        }

        temp_s1->DeInitEngineState();
    }

    var_s0 |= (int8_t)temp_s1->virtual_20() != 1;

    var_s0 |= (int8_t)temp_s1->DeInitEngine() != 1;

    var_s0 |= (int8_t)temp_s1->virtual_18() != 1;

    DeInitGameApplication();

    BASE_DeInitModule();

    return var_s0;
}
#endif


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
