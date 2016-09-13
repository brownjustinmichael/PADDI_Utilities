#include "inout.h"

#define _FILE_OFFSET_BITS 64

#include <stdio.h>
#include <unistd.h>
#include <joeplib.h>


int jcskip_(iu,n,niter,time)

/****    iu    = file unit
         n     =  number of steps to skip


       RETURNS
	niter  = numer of model iteration
	time   = time of last skipped step

*****/
float *time;
int   *iu,*niter,*n;

{
  int i,j,ival,i1,i2, c1, c2;
  float xmin,xmax;
  off_t  start_of_joep, length_of_joep;
  off_t  xxx;
  extern FILE *fpo[MAXFILES];
  float ltime,ldt;
  int  lniter,xdim, ydim, zdim,subimg=1,k;
  extern FILE *fpo[];
  char buf2[30];
  static int magic;


   
   if((c1 = fgetc(fpo[*iu])) == EOF) return(-1);;
   if((c2 = fgetc(fpo[*iu])) == EOF) return(-1);;

      if(c1 != 74) {
                  fprintf(stderr," JCSKIP Wrong magic number .. maybe not a jcpeg file %i ..\n", c2);
                  return(-1);
                   }
                else magic = (int)c2;

  if((fscanf(fpo[*iu],"%d%e%e%e%e%d%d%d",&lniter,&ltime,&ldt,&xmin,&xmax,&xdim, &ydim, &zdim))
      == EOF) return(-1);
  getc(fpo[*iu]);
	*niter = lniter;
	*time = ltime;

     i2 = 0;

   while(ydim*zdim/subimg > 256*256-1) subimg++;

   for(k=0; k < subimg; k++) {


  start_of_joep = ftello64(fpo[*iu]);
  fscanf(fpo[*iu],"%s\n", &buf2);
  if(debug)printf(">> %s \n", buf2);
  length_of_joep = (off_t)atol(buf2);
  xxx = start_of_joep + length_of_joep;
  if(fseeko64(fpo[*iu], xxx, SEEK_SET) != 0) fprintf(stderr," error in fseeko64\n");;
  if(debug)printf("start_of_joep %i length_of_joep %i .. -> set %i  \n", start_of_joep , (int)length_of_joep ,  start_of_joep + length_of_joep);
  if(length_of_joep < 0) exit(0);
  fscanf(fpo[*iu],"%s\n", &buf2);

  }

     return(magic);
     }

/* the C interface */
int jcskip(int iu, int n,int *niter,float *time)
{
  return(jcskip_(&iu,&n,niter,time));
}

