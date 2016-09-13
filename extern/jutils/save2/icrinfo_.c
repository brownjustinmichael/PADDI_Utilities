#include "inout.h"

int icrinfo_(iu,ra,ras,iddc,le,numx,numy)


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
  fscanf(fpo[*iu],"%e %e %d %e %d %d\n",
	  ra,ras,iddc,le,numx,numy);
/***     getc(fpo[*iu]); ***/
  return(0);
}

/* the c interface */

int icrinfo(int iu,float *ra,float *ras,int *iddc,float *le,int *numx,int *numy)
{
  return(icrinfo_(&iu,ra,ras,iddc,le,numx,numy));
}


