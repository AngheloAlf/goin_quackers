
#define CTORARG_TYPE			short
#define CTORARG_PARTIAL			(0)				//	construct non-virtual bases
#define CTORARG_COMPLETE		(1)				//	construct all bases	

#define CTORCALL_COMPLETE(ctor,objptr)\
	(((void (*)(void *,CTORARG_TYPE))ctor)(objptr,CTORARG_COMPLETE))


#define DTORARG_TYPE			short
#define DTORARG_PARTIAL			(0)				//	destroy non-virtual bases	
#define DTORARG_COMPLETE		(-1)			//	destroy all bases	
#define DTORARG_DELETE			(1)				//	destroy all bases and delete object

#define DTORCALL_COMPLETE(dtor,objptr)\
	(((void (*)(void *,DTORARG_TYPE))dtor)(objptr,DTORARG_COMPLETE))

#define DTORCALL_PARTIAL(dtor,objptr)\
	(((void (*)(void *,DTORARG_TYPE))dtor)(objptr,DTORARG_PARTIAL))



typedef long long address;

extern asm address __getS7(void);
extern asm address __getGP(void);


typedef struct DestructorChain {			//	global destructor chain
	struct DestructorChain	*next;			//	pointer to next destructor chain element
	void					*destructor;	//	pointer to destructor function
	void					*object;		//	pointer to memory location (0L: element is marker)
}	DestructorChain;


extern DestructorChain *__global_destructor_chain;



void __destroy_global_chain(void) {
	DestructorChain	*gdc;

	while((gdc = __global_destructor_chain) != 0) {
		__global_destructor_chain = gdc->next;
		DTORCALL_COMPLETE(gdc->destructor, gdc->object);
	}
}

void *__register_global_object(void *object, void *destructor, void *regmem) {

	((DestructorChain *) regmem)->next = __global_destructor_chain;
	((DestructorChain *) regmem)->destructor = destructor;
	((DestructorChain *) regmem)->object = object;
	__global_destructor_chain = (DestructorChain *) regmem;

	return object;
}

#if 0
static inline void __call_static_initializers(void (**si)(void), void (**sie)(void))
{
	union {
		void (*sifunc)(void);
		address sifuncad;
	} u;
	const address offset = __pc_relative__ ? __getS7() : 0;
	
	for (; si < sie; si++) {
		u.sifunc = *si; 
		u.sifuncad += offset;
		(u.sifunc)();
	}
}

void __initialize_cpp_rts(void (**si)(void), void (**sie)(void), void * , void *) {
	__call_static_initializers(si, sie);
}
#endif
