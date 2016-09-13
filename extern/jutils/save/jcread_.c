#include "inout.h"

#include "joeplib.h"

#ifdef USE12B
#define JMAX 4095  /*4095*/
#define JDATA  short /*short or unsigned char*/
#else
#define JMAX 255  /*4095*/
#define JDATA  unsigned char /*short or unsigned char*/
#endif



int jcread_(iu,niter,time,dt,x,xdim,ydim,zdim)

/****    iu    = file unit

       RETURNS
	niter  = numer of model iteration
	time   = time of last skipped step
	dt     = time step 
        x      = data vector

*****/
float *time,*dt,*x;
int   *iu,*niter,*xdim, *ydim, *zdim;

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
  off_t start_of_joep, length_of_joep;
  char buf2[100];
  double dx;


float ltime,ldt;
int   lniter,lxlen;
extern FILE *fpo[];
register float rjmax, xspan;
   
   if((c1 =  (unsigned char)fgetc(fpo[*iu])) == EOF) return(-1);;
   if((c2 =  (unsigned char)fgetc(fpo[*iu])) == EOF) return(-1);;

      if(c1 != 74) {
                  fprintf(stderr," Wrong magic number .. maybe not a jcpeg file .. c1 = %i c2 = %i\n", c1, c2);
                  return(-1);
                   }
                else magic = (int)c2;

  if((fscanf(fpo[*iu],"%d%e%e%e%e%d%d%d",&lniter,&ltime,&ldt,&xmin,&xmax,xdim, ydim, zdim))
      == EOF) return(-1);
  getc(fpo[*iu]);
	*niter = lniter;
	*time = ltime;
	dt   = &ldt;

     i2 = 0;

#ifdef DEBUG
     fprintf(stderr,"in jcread %i %f  min = %f max = %f \n",lniter,ltime, xmin, xmax);
#endif
     fprintf(stderr,"in jcread %i %f  min = %f max = %f \n",lniter,ltime, xmin, xmax);

     if((int)xmin ==  JXDR && (int)xmax == JXDR) usexdr=1;
     if((int)xmin ==  2*JXDR && (int)xmax == 2*JXDR) { usexdr=1; usexdr_double = 1;}

  start_of_joep = ftello(fpo[*iu]);
  fscanf(fpo[*iu],"%s\n", &buf2);
  length_of_joep = atol(buf2);


     if(!usexdr) { 
     image_out =    (JDATA *) malloc(sizeof(JDATA)*(*xdim)*(*ydim)*(*zdim));
     read_JPEG_file(fpo[*iu], image_out);

     xspan = (xmax-xmin)/JMAX;

     for(i=0; i< (*xdim)*(*ydim)*(*zdim); i++) 
          x[i] = xmin +  xspan * (float)image_out[i];
     free(image_out);
     } else { /* xdr encoded stream */

        printf(" xdrstdio_create ..\n");
        xdrstdio_create(&xdrs, fpo[*iu], XDR_DECODE);
        for(i=0; i< (*xdim)*(*ydim)*(*zdim); i++) 
        {
         if(!usexdr_double) { 
        if(!xdr_float(&xdrs, &x[i])) { fprintf(stderr," Error in xdr_float\n"); return(-1);}
         } else { 
        if(!xdr_double(&xdrs, &dx)) { fprintf(stderr," Error in xdr_double\n"); return(-1);}
           x[i] = (float) dx;
         }
        }
        xdr_destroy(&xdrs);
     }
      fseeko(fpo[*iu], start_of_joep + length_of_joep, SEEK_SET);


     fscanf(fpo[*iu],"%s\n", &buf);
     return(magic);
     }

/* the C interface */
int jcread(int iu,int *niter,float *time,float *dt,float *x,int *xdim,int * ydim,int * zdim
)
{
  return(jcread_(&iu,niter,time,dt,x,xdim, ydim, zdim));
}

int jcdread_(iu,niter,time,dt,x,xdim,ydim,zdim)

/****    iu    = file unit

       RETURNS
        niter  = numer of model iteration
        time   = time of last skipped step
        dt     = time step
        x      = data vector

*****/
double *time,*dt,*x;
int   *iu,*niter,*xdim, *ydim, *zdim;

{
  int i,j,ival,i1,i2;
  unsigned char c1, c2;
  float xmin,xmax;
  extern FILE *fpo[MAXFILES];
  JDATA *image_out;
  char buf[10];
  static int magic;
  int usexdr = 0;
  XDR xdrs;
  off_t start_of_joep, length_of_joep;
  char buf2[100];
 


float ltime,ldt;
int   lniter,lxlen;
extern FILE *fpo[];
register float rjmax, xspan;

   if((c1 =  (unsigned char)fgetc(fpo[*iu])) == EOF) return(-1);;
   if((c2 =  (unsigned char)fgetc(fpo[*iu])) == EOF) return(-1);;

      if(c1 != 74) {
                  fprintf(stderr," Wrong magic number .. maybe not a jcpeg file .. c1 = %i c2 = %i\n", c1, c2);
                  return(-1);
                   }
                else magic = (int)c2;

  if((fscanf(fpo[*iu],"%d%e%e%e%e%d%d%d",&lniter,&ltime,&ldt,&xmin,&xmax,xdim, ydim, zdim))
      == EOF) return(-1);
  getc(fpo[*iu]);
        *niter = lniter;
        *time = ltime;
        dt   = &ldt;

     i2 = 0;

#ifdef DEBUG
     fprintf(stderr,"in jcdread %i %f  min = %f max = %f \n",lniter,ltime, xmin, xmax);
#endif
     fprintf(stderr,"in jcdread %i %f  min = %f max = %f \n",lniter,ltime, xmin, xmax);

     if((int)xmin ==  2*JXDR && (int)xmax == 2*JXDR) usexdr=1;
     else printf(" kein xdr %f %f : %f \n",xmin, xmax,JXDR);

  start_of_joep = ftello(fpo[*iu]);
  fscanf(fpo[*iu],"%s\n", &buf2);
  length_of_joep = atol(buf2);


     if(!usexdr) {
     image_out =    (JDATA *) malloc(sizeof(JDATA)*(*xdim)*(*ydim)*(*zdim));
     read_JPEG_file(fpo[*iu], image_out);

     xspan = (xmax-xmin)/JMAX;

     for(i=0; i< (*xdim)*(*ydim)*(*zdim); i++)
          x[i] = xmin +  xspan * (float)image_out[i];
     free(image_out);
     } else { /* xdr encoded stream */

        printf(" xdrstdio_create ..\n");
        xdrstdio_create(&xdrs, fpo[*iu], XDR_DECODE);
        for(i=0; i< (*xdim)*(*ydim)*(*zdim); i++)
        if(!xdr_double(&xdrs, &x[i])) fprintf(stderr," Error in xdr_float\n");
        xdr_destroy(&xdrs);
     }
      fseeko(fpo[*iu], start_of_joep + length_of_joep, SEEK_SET);


     fscanf(fpo[*iu],"%s\n", &buf);
     return(magic);
}










int
read_JPEG_file (FILE *infile, JDATA *image_out)
{
  struct joep_decompress_struct cinfo;
  struct joep_error_mgr jerr;
  JSAMPARRAY buffer;    
  int row_stride, j=0, i;               /* physical row width in output buffer */


/*
  fprintf(stderr, "read_JPEG_file  fileposition %i --> length %i \n", 
                                                ftello(infile), length_of_joep);
*/

  cinfo.err = joep_std_error(&jerr);
  /* Now we can initialize the JPEG decompression object. */
  joep_create_decompress(&cinfo);

  joep_stdio_src(&cinfo, infile);
  (void) joep_read_header(&cinfo, TRUE);
  (void) joep_start_decompress(&cinfo);
  row_stride = cinfo.output_width * cinfo.output_components;
  /* Make a one-row-high sample array that will go away when done with image */
  buffer = (*cinfo.mem->alloc_sarray)
                ((j_common_ptr) &cinfo, JPOOL_IMAGE, row_stride, 1);

  while (cinfo.output_scanline < cinfo.output_height) {
    (void) joep_read_scanlines(&cinfo, buffer, 1);
/*joerg*/
    for(i=0; i< row_stride; i++) { image_out[j] = (JDATA) *(buffer[0]+i); j++;}
  }
  (void) joep_finish_decompress(&cinfo);
  joep_destroy_decompress(&cinfo);

/** end of joep stuff **/

  return 1;
}


