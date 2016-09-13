#include "inout.h"

int icddwinfo_(iu,ra,ras,iddc,le,numx,numy)


/****   iu    = file unit
	niter  = numer of model iteration
	time   = time of last skipped step
	dt     = time step 
        x      = data vector
	xlen   = lenght of data vector

	RETURNS
	0      = fine

*****/
double *ra,*ras,*le;
long   *iu,*numx,*numy,*iddc;

{
extern FILE *fpo[MAXFILES];
  fprintf(fpo[*iu],"%6e %6e %1d %6e %4d %4d\n",
	  *ra,*ras,*iddc,*le,*numx,*numy);
  return(0);
}

/* the c interface */

int icddwinfo(long iu,double *ra,double *ras,long *iddc,double *le,long *numx,long *numy)
{
 return(icddwinfo_(&iu,ra,ras,iddc,le,numx,numy));
}


