#include "inout.h"

int jcrinfo_(iu,ra,ras,iddc,le,numx,numy,numz)


/****   iu    = file unit
	niter  = numer of model iteration
	time   = time of last skipped step
	dt     = time step 
        x      = data vector
        numx   = x dimension of the data
        numy   = y dimension of the data
        numz   = z dimension of the data

	RETURNS
	-1     = error
	0      = fine

*****/
float *ra,*ras,*le;
int   *iu,*numx,*numy,*numz,*iddc;

{
char buf[100];
extern FILE *fpo[MAXFILES];
fpos_t pos;
int ninfo=0;


  fgetpos( fpo[*iu], &pos);
  if(fscanf(fpo[*iu],"%s",buf) == EOF) { fprintf(stderr," error in jcrinfo_\n"); return(-1);}
  fsetpos( fpo[*iu], &pos);

  if(strcmp("info2", buf) == 0) { 
          fprintf(stderr," looks like an  info2 record:%s: !!\n", buf); 
          return(jcrinfo2_(iu,numx,numy,numz,iddc,&ninfo,NULL,NULL,0));}
  




  if(fscanf(fpo[*iu],"%e %e %d %e %d %d %d\n",
	  ra,ras,iddc,le,numx,numy, numz) == EOF) { 
                       fprintf(stderr," error in jcrinfo_\n"); return(-1);
                     }
  return(0);
}

int jcrinfo(int iu,float *ra,float *ras,int *iddc,float *le,int *numx,int *numy, int *numz)
{
  return(jcrinfo_(&iu,ra,ras,iddc,le,numx,numy,numz));
}


