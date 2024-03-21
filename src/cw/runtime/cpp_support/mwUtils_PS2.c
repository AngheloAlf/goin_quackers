typedef    void                (*mwStaticInitializer)(void);
typedef    mwStaticInitializer    mwStaticInitializers[];

extern    mwStaticInitializers    __static_init;
extern    mwStaticInitializers    __static_init_end;

typedef struct ExceptionTableIndex
{
    char*            function_address;
    unsigned int    function_size;
    char*            exception_table;
}    ExceptionTableIndex;
typedef    ExceptionTableIndex    mwExceptionTableIndexes[];

extern    mwExceptionTableIndexes    __exception_table_start__;
extern    mwExceptionTableIndexes    __exception_table_end__;


extern    void    __initialize_cpp_rts(void** si, void** sie, void* ets, void* ete);
extern    void    __destroy_global_chain(void);

void mwInit(void) {
    __initialize_cpp_rts((void**)__static_init, (void **)__static_init_end, __exception_table_start__, __exception_table_end__);
}

void mwExit(void) {
    __destroy_global_chain();
}
