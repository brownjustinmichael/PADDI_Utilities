#include "inout.h"
#include <string.h>

extern FILE *fpo[MAXFILES];

int jend_(iu)

int *iu;
{
	extern FILE *fpo[];

         fseek(fpo[*iu],0,SEEK_END); 

	return(0);
}

int jcend(int iu)
{

    return(jend_(&iu));
}
