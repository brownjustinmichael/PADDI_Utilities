#include "inout.h"
#include <stdio.h>
#include <stdlib.h>

int icclose_(iu)

int *iu;

{
   extern FILE *fpo[];
   int j;
   j = *iu;
   fprintf(stderr,"\n icclose iu = %i\n",j);
   fclose(fpo[j]);     
   return(0);
    }

/** the C interface */

int icclose(int iu)
{
 return(icclose_(&iu));
}
