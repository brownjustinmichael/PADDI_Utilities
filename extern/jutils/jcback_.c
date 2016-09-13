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
   char buf2[20];
   int i, c1, c2;
   static int magic;


   for(i=0; i< *n; i++) {

   if(fseeko(fpo[*iu],-9,SEEK_CUR) == -1) fprintf(stderr,"fseek error in jcback 0\n");
   
   fscanf(fpo[*iu],"%s\n", &buf2);

#define debug 1
if(debug)   printf("\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> jcback %s \n",buf2);


   if(fseeko(fpo[*iu], (off_t)(-atol(buf2) - 9), SEEK_CUR) == -1) fprintf(stderr,"fseek error in jcback 1\n");

   if((c1 = fgetc(fpo[*iu])) == EOF) return(-1);; 
   if((c2 = fgetc(fpo[*iu])) == EOF) return(-1);; 
   if(c1 != 74) {
                  fprintf(stderr," Wrong magic number in jcback .. maybe not a jcpeg file ..\n");
                  return(-1);
                   }
    else magic = (int)c2;
   if(fseeko(fpo[*iu],-2,SEEK_CUR) == -1) fprintf(stderr,"fseek error in jcback 2\n");


   }




   return(magic);

 }

int jcback(int iu, int *n)
{
 return(jcback_(&iu,n));
}
