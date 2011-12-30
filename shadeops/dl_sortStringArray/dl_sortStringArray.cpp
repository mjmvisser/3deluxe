#include <shadeop.h>
#include <string>
#include <algorithm>
#include <math.h>
using namespace std;

extern "C"
{

SHADEOP_TABLE(lm_sortStringArray) = {
		{ "void lm_sortStringArray(string[], float, float[])", "lm_sortStringArray_init", "lm_sortStringArray_cleanup" }, { "" } };

SHADEOP_INIT(lm_sortStringArray_init)
{
	return 0x0; /* No init data */
}

struct st_ex { 
    const char* str;
    float flt;
};

 
/* qsort struct comparision function (str C-string field) */
int struct_cmp_by_str(const void *a, const void *b)
{
    struct st_ex *ia = (struct st_ex *)a;
    struct st_ex *ib = (struct st_ex *)b;
    return strcmp(ia->str, ib->str);
	/* strcmp functions works exactly as expected from
	comparison function */ 
} 

#include <stdio.h>

SHADEOP( lm_sortStringArray )
{
	const char **input1strArray = (const char **)(argv[1]);
	float *input2flt = (float *)(argv[2]);
	float *output3fltArray = (float *)(argv[3]);

    int nElements = (int)floor(*input2flt);

    st_ex *elements = new st_ex[nElements];

    for (int i = 0; i < nElements; i ++) {
        elements[i].str = input1strArray[i];
        elements[i].flt = i;
    }

    qsort(elements, nElements, sizeof(struct st_ex), struct_cmp_by_str);    

    for (int i = 0; i < nElements; i ++) {
        output3fltArray[i] = elements[i].flt;
    }

	return 0;
}

SHADEOP_CLEANUP( lm_sortStringArray_cleanup )
{
	/* Nothing to do */
}

}
