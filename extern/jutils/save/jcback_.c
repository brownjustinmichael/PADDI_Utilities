#include "inout.h"
#include <stdio.h>

int jcback_(iu,n)

/****    iu    = file unit
         n     =  number of steps to  rewind
         len   = length of last step in bytes

       RETURNS
         0     = fine


*****/
int   *iu,*n;

{
   extern FILE *fpo[];
   char buf2[10];
   int i, c1, c2;
   static int magic;

   for(i=0; i< *n; i++) {

#ifdef F64
   fseek64(fpo[*iu],-9,SEEK_CUR);
#else
   fseeko(fpo[*iu],-9,SEEK_CUR);
#endif
   
   fscanf(fpo[*iu],"%s\n", &buf2);

#ifdef F64
   fseek64(fpo[*iu], -atoll(buf2) - 9, SEEK_CUR);
#else
   fseeko(fpo[*iu], -atol(buf2) - 9, SEEK_CUR);
#endif

   if((c1 = fgetc(fpo[*iu])) == EOF) return(-1);; 
   if((c2 = fgetc(fpo[*iu])) == EOF) return(-1);; 
   if(c1 != 74) {
                  fprintf(stderr," Wrong magic number .. maybe not a jcpeg file ..\n");
                  return(-1);
                   }
    else magic = (int)c2;
#ifdef F64
   fseek64(fpo[*iu],-2,SEEK_CUR);
#else
   fseeko(fpo[*iu],-2,SEEK_CUR);
#endif


   }




   return(magic);

 }

int jcback(int iu, int *n)
{
 return(jcback_(&iu,n));
}
