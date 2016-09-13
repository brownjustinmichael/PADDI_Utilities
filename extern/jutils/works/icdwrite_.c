#include "inout.h"

int icdwrite_(iu,niter,time,dt,x,xlen)


/****   iu    = file unit
	niter  = numer of model iteration
	time   = time of last skipped step
	dt     = time step 
        x      = data vector
	xlen   = lenght of data vector

	RETURNS
	0      = fine

*****/
double *time,*dt,*x;
int   *iu,*niter,*xlen;

{
  int i,ival,i1,i2;
  double xmin,xmax;
  extern FILE *fpo[];
   
  /*   New version -> using niter as magic number <-  */
  /*   if niter == -2 short write !!                  */
  /* skalierung des real-feldes auf das integer-intervall*/
  /* [0,65535] und anschliessende ausgabe zweier characters*/

  xmin = x[0];
  xmax = x[0];
  for (i=1; i < *xlen; i++){
     if (x[i] < xmin)
	xmin = x[i];
     else if (x[i] > xmax)
	xmax = x[i];
     }
#ifdef DEBUG
  printf("%6d %6e %6e %6e %6e %6d\n",
	  *niter,*time,*dt,xmin,xmax,*xlen);
#endif
  fprintf(fpo[*iu],"%6d %6e %6e %6e %6e %6d\n",
	  *niter,*time,*dt,(float)xmin,(float)xmax,*xlen);
#ifdef DEBUG
  printf("nach dem fprintf ... \n");
#endif

  for (i=0; i < *xlen; i++) {
      ival =(int)((MAXVAL*(x[i]-xmin))/(xmax-xmin)+.5);
      i1 = ival/256;
      i2 = ival%256;
      putc(i1,fpo[*iu]);
      if(*niter != -2) putc(i2,fpo[*iu]);
      }
  fflush(fpo[*iu]);
  return(0);
}

/** the C interface **/

int icdwrite(int iu, int *niter,double *time,double *dt,double *x,int *xlen)
{
  return(icdwrite_(&iu,niter,time,dt,x,xlen));
}


