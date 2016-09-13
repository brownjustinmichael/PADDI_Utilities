#include "inout.h"

int icwinfo_(iu,ra,ras,iddc,le,numx,numy)


/****   iu    = file unit
	niter  = numer of model iteration
	time   = time of last skipped step
	dt     = time step 
        x      = data vector
	xlen   = lenght of data vector

	RETURNS
	0      = fine

*****/
float *ra,*ras,*le;
int   *iu,*numx,*numy,*iddc;

{
extern FILE *fpo[MAXFILES];
  fprintf(fpo[*iu],"%6e %6e %1d %6e %4d %4d\n",
	  *ra,*ras,*iddc,*le,*numx,*numy);
  return(0);
}

/* the c interface */

int icwinfo(int iu,float *ra,float *ras,int *iddc,float *le,int *numx,int *numy)
{
 return(icwinfo_(&iu,ra,ras,iddc,le,numx,numy));
}


