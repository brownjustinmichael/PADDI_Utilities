#include "inout.h"

int icback_(iu,n,len)

/****    iu    = file unit
         n     =  number of steps to  rewind
         len   = length of last step in bytes

       RETURNS
         0     = fine


*****/
int   *iu,*n,*len;

{
   extern FILE *fpo[];

   if(fseek(fpo[*iu],(long)(-(*n)*(*len)),1) == 0) {
   return(0);}
   else{
   return(-1);}

     }

/** the c interface **/
int icback(int iu, int *n, int *len)
{
  return(icback_(&iu, n, len));
}
