#include "inout.h"

#include <joeplib.h>

#ifdef USE12B
#define JMAX 4095.  /*4095*/
#define JDATA  short /*short or unsigned char*/
#else
#define JMAX 255.  /*4095*/
#define JDATA  unsigned char /*short or unsigned char*/
#endif

 


int jcwrite_(iu,magic,niter,time,dt,x,xdim, ydim, zdim, quality)


/****   iu     = file unit
        magic  = data type number 
	niter  = numer of model iteration
	time   = time of last skipped step
	dt     = time step 
        x      = data vector
        xdim   = x-size of data
        ydim   = y-size of data
        zdim   = z-size of data

	RETURNS
	-1      = error, else returns 0

*****/
float *time,*dt,*x;
int   *iu,*magic,*niter,*xdim, *ydim, *zdim, *quality;

{
  int i,ival,i1,i2, k, subimg=1;
  float xmin,xmax;
  extern FILE *fpo[];
  XDR xdrs;
#ifdef F64
  long long start_of_step;
#define ftell ftell64
#define fseek fseek64
#else
  off_t start_of_step, start_of_joep, length_of_joep;
#endif
  struct nlist *mylist, *plist;
  int alreadywritten=0;
  char c1, c2;

  JDATA *image_buffer;
   

  xmin = x[0];
  xmax = x[0];
  for (i=1; i < (*xdim)*(*ydim)*(*zdim); i++){
     if (x[i] < xmin)
	xmin = x[i];
     else if (x[i] > xmax)
	xmax = x[i];
     }
   if(xmax - xmin == 0) xmax = xmin + 0.000000001;

  start_of_step = ftello(fpo[*iu]);

   fputc(74, fpo[*iu]); fputc(*magic, fpo[*iu]);

  if(*quality == 100) xmin = xmax = JXDR;  /* used to mark xdr stream .. a bit dirty .. */

  fprintf(fpo[*iu],"%6d %6e %6e %6e %6e %6d %6d %6d\n",
	  *niter,*time,*dt,xmin,xmax,*xdim, *ydim, *zdim);


      mylist = calcdivisions(*xdim, *ydim, *zdim);
      plist = mylist;



      while(plist != NULL)  {


  start_of_joep = ftello(fpo[*iu]);
  fprintf(fpo[*iu],"%8.8i\n", 0); /** only a dummy */

   printf("  writing subimage   start_of_joep %i   \n", start_of_joep);

  if(*quality != 100) { 
  image_buffer = (JDATA *) malloc(sizeof(JDATA)*(*xdim)*plist->num);

          for(i=0; i< (*xdim)*plist->num; i++)
          image_buffer[i] = (JDATA) (0.5 + JMAX*((x[i + alreadywritten ]-xmin)/(xmax - xmin)  ));

  write_JPEG_file(fpo[*iu], image_buffer, *quality, *xdim, plist->num);
//   for(i=0; i< 30 ; i++) fprintf(fpo[*iu], "C");
  free(image_buffer);
  } else {  /* xdr representation */

         xdrstdio_create(&xdrs, fpo[*iu], XDR_ENCODE);
         for(i=0; i< (*xdim)*plist->num; i++)
         {
         if(!xdr_float(&xdrs, &x[i + alreadywritten])) fprintf(stderr," Error in xdr_float\n");
         }
         xdr_destroy(&xdrs);
         
  }

   alreadywritten += (*xdim)*plist->num;

  length_of_joep = ftello(fpo[*iu]) - start_of_joep;
  if(1) printf(" length_of_joep %d start %d ftell %d \n",length_of_joep, (long)start_of_joep, ftello(fpo[*iu]));
  if(fseeko(fpo[*iu], start_of_joep, SEEK_SET) == -1) fprintf(stderr," error in fseeko\n");
  fprintf(fpo[*iu],"%8.8i\n", length_of_joep);                /**length info at beginning of step **/
  if(fseeko(fpo[*iu], start_of_joep + length_of_joep, SEEK_SET) == -1) fprintf(stderr," error in fseeko 2\n");

  // fprintf(fpo[*iu],"%8.8i\n", ftello(fpo[*iu]) - start_of_step); /**length info at end of step **/
  fprintf(fpo[*iu],"%8.8i\n", ftello(fpo[*iu]) - start_of_step); /**length info at end of step **/

  fflush(fpo[*iu]);

  plist = plist->next;
  }  // subimg

  freemylist(mylist);
  return(0);
}



/** the C interface **/

int jcwrite(int iu, int magic, int *niter,float *time,float *dt,float *x,int *xdim,int *ydim,int *zdim, int *quality)
{
  return(jcwrite_(&iu,&magic,niter,time,dt,x,xdim, ydim, zdim, quality));
}

write_JPEG_file (FILE *outfile,JDATA *image_buffer, int quality, int xdim, int ydimzdim)
{
  struct joep_compress_struct cinfo;
  struct joep_error_mgr jerr;
  JSAMPROW row_pointer[1];      /* pointer to JSAMPLE row[s] */
  int row_stride, i=0;               /* physical row width in image buffer */


  cinfo.err = joep_std_error(&jerr);
  joep_create_compress(&cinfo);


  joep_stdio_dest(&cinfo, outfile);
  cinfo.image_width = xdim;      /* image width and height, in pixels */
  cinfo.image_height = ydimzdim;
  cinfo.input_components = 1;           /* # of color components per pixel */
  cinfo.in_color_space = JCS_GRAYSCALE;       /* colorspace of input image */

  joep_set_defaults(&cinfo);

  joep_set_quality(&cinfo, quality, TRUE /* limit to baseline-JPEG values */);
  joep_start_compress(&cinfo, TRUE);
  row_stride = cinfo.image_width * cinfo.input_components; /* JSAMPLEs per row in im
age_buffer */

  while (cinfo.next_scanline < cinfo.image_height) {
    row_pointer[0] = & image_buffer[cinfo.next_scanline * row_stride];
    (void) joep_write_scanlines(&cinfo, row_pointer, 1);
  }

  joep_finish_compress(&cinfo);
  joep_destroy_compress(&cinfo);



  return;

}

