#include "inout.h"

#include "joeplib.h"

#ifdef USE12B
#define JMAX 4095  /*4095*/
#define JDATA  short /*short or unsigned char*/
#else
#define JMAX 255  /*4095*/
#define JDATA  unsigned char /*short or unsigned char*/
#endif



int jctype_(iu)

/****    iu    = file unit

       RETURNS
         type of step .. 0 = joep,  1= xdr

*****/
int   *iu;

{
  int i,j,ival,i1,i2;
  unsigned char c1, c2;
  float xmin,xmax;
  extern FILE *fpo[MAXFILES];
  JDATA *image_out;
  char buf[10];
  static int magic;
  int usexdr = 0, usexdr_double = 0;
  XDR xdrs;
  long start_of_joep, length_of_joep;
  char buf2[100];
  double dx;
  fpos_t start;

  int  xdim, ydim, zdim;


float ltime,ldt;
int   lniter,lxlen;
extern FILE *fpo[];
register float rjmax, xspan;
   
   fgetpos(fpo[*iu],&start);
   if((c1 =  (unsigned char)fgetc(fpo[*iu])) == EOF) return(-1);;
   if((c2 =  (unsigned char)fgetc(fpo[*iu])) == EOF) return(-1);;

      if(c1 != 74) {
                  fprintf(stderr," Wrong magic number .. maybe not a jcpeg file .. c1 = %i c2 = %i\n", c1, c2);
                  return(-1);
                   }
                else magic = (int)c2;

  if((fscanf(fpo[*iu],"%d%e%e%e%e%d%d%d",&lniter,&ltime,&ldt,&xmin,&xmax,&xdim, &ydim, &zdim))
      == EOF) return(-1);
  getc(fpo[*iu]);



   fsetpos(fpo[*iu],&start);

     if((int)xmin ==  JXDR && (int)xmax == JXDR) return(1);
     if((int)xmin ==  2*JXDR && (int)xmax == 2*JXDR) return(2);
     else return (0);

     }



