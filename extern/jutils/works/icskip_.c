#include "inout.h"

int icskip_(iu,n,niter,time)

/****    iu    = file unit
         n     =  number of steps to skip

       RETURNS
	niter  = numer of model iteration
	time   = time of last skipped step
        icskip = length of last step in bytes

*****/
/***   new version !! if niter == -2 short read   **/


int *iu,*n,*niter;
float *time;

{
 
  extern FILE *fpo[];
  int i,j,l,len,lniter;
  float x;
   
  for (j=1; j <= *n; j++){
  l = ftell(fpo[*iu]);
  if((fscanf(fpo[*iu],"%d%e%e%e%e%d",&lniter,time,&x,&x,&x,&len))
      == EOF) return(-1);
  getc(fpo[*iu]);

   *niter = lniter;
 
#ifdef DEBUG
  fprintf(stderr,"in icskip !! niter = %d lniter %d\n",niter,lniter);
#endif

     for (i=0; i < len; i++) getc(fpo[*iu]);
     if(*niter != -2 ) for (i=0; i < len; i++) getc(fpo[*iu]);

  }
  l = ftell(fpo[*iu]) - l;
  return(l);
}
/* the c interface */

int icskip(int iu,int *n,int *niter,float *time)
{
 return(icskip_(&iu,&n,niter,time));
}

