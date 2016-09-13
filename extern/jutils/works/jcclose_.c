#include "inout.h"
#include <stdio.h>
#include <stdlib.h>

int jcclose_(iu)

int *iu;

{
   extern FILE *fpo[];
   int j;
   j = *iu;
   if(fclose(fpo[j])  == EOF) { fprintf(stderr," error in jcclose_..\n"); return(-1);}    
   return(0);
    }

int jcclose(int iu) { return(jcclose_(&iu));}
