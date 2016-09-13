#include "inout.h"

int icread_(iu,niter,time,dt,x,xlen)

/****    iu    = file unit

       RETURNS
	niter  = numer of model iteration
	time   = time of last skipped step
	dt     = time step 
        x      = data vector
	xlen   = lenght of data vector

*****/
/***   new version !! if niter == -2 short read   **/
float *time,*dt,*x;
int   *iu,*niter,*xlen;

{
  int i,j,ival,i1,i2;
  float xmin,xmax;
  extern FILE *fpo[MAXFILES];

float ltime,ldt;
int   lniter,lxlen;
  extern FILE *fpo[];
   
  if((fscanf(fpo[*iu],"%d%e%e%e%e%d",&lniter,&ltime,&ldt,&xmin,&xmax,xlen))
      == EOF) return(1);
  getc(fpo[*iu]);
	*niter = lniter;
	*time = ltime;
	dt   = &ldt;
/**	xlen = &lxlen; **/

     i2 = 0;

     for (i=0; i < *xlen; i++) {
	 i1=getc(fpo[*iu]);
	 if(*niter != -2 ) i2=getc(fpo[*iu]);
         ival=256*i1+i2;
         *(x+i) = (ival*(xmax-xmin))/MAXVAL+xmin;
         }
     return(0);
     }
/* the C interface */
int icread(int iu,int *niter,float *time,float *dt,float *x,int *xlen)
{
  return(icread_(&iu,niter,time,dt,x,xlen));
}

