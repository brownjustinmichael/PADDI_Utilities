#include <sys/time.h>

#include <stdio.h>
#include <sys/stat.h>
#ifndef sun
#include <getopt.h>
#else
#include <stdlib.h>
#endif
#include <math.h>
#include <unistd.h>

#include <jpeglib.h>

#include "jcmagic.h"

#define ABS(A)  ( (A) < 0 ? -(A) : (A) )

#ifdef USE12B
#define MAXVAL 4095  /*4095*/
#define JDATA  short /*short or unsigned char*/
#else
#define MAXVAL 255  
#define JDATA  unsigned char /*short or unsigned char*/
#endif

int xdim, ydim, zdim, niter, iddc;
float mtime, dt, ra, ras, le;
float *data=NULL, *ax=NULL, *ay=NULL;    /* a pointer to the 3d volume of data */
char inp_file[80], out_file[80];		/* name of input file */
struct stat o_data_file, s_data_file;

long interval (const struct timeval *t1, const struct timeval *t2);
struct timeval tv1, tv2, tv3;



int limit=0, dirty=0;

MAIN__() {}
__main() {}

main(argc, argv)
int argc;
char *argv[];
{

	int i, j, k,ierr, errfac, magic=77, quality=85, offset;
        float av, averr, rmserr, maxerr;
        char acc[1]="w";
        float *newdat, *newax, *neway;

        FILE *fff, *f1, *f2;
        fff = fopen("data", "w");
        fprintf(fff,"# (1)quality (2)averr (%)  (3)maxerr (%)  (4)size(byte) (5)compression (\%) (6)comptime(sec) (7)decomptime(sec)\n");

	if (argc <= 2) {
                fprintf(stderr," usage %s  infile outfile -q quality \n",  argv[0]);
		exit(1);
	}

           printf(" for getopt .. \n");
	while((i=getopt(argc,argv,"sdhq:e:q:")) != -1)
	{
		switch(i) {
                case 'e':
                        sscanf(argv[optind-1], "%d", &errfac);
			break;
                case 'h':
                        exit(1);
			break;
                case 's':
                        printf("Restricting temp  values to [0.,1]\n");
                        limit = 1;
			break;
                case 'd':
                        printf(" Dirty hack ... lowest level must be T=1\n");
                        dirty = 1;
			break;
                case 'q':
                        sscanf(argv[optind-1], "%i", &quality);
                        printf(" Quality set to %i\n", quality);
			break;
		}
	}

		sprintf(inp_file,"%s\0",argv[argc-2]);
		sprintf(out_file,"%s\0",argv[argc-1]);

	printf(" inp_file   :  %s\n",inp_file);
	printf(" out_file   :  %s\n",out_file);

        
           printf(" for get_greg_data .. \n");
        get_greg_data();

        newdat = (float *) malloc(sizeof(float)*xdim*ydim*zdim);
        newax = (float *) malloc(sizeof(float)*xdim*ydim*zdim);
        neway = (float *) malloc(sizeof(float)*xdim*ydim*zdim);
quality = 50;
offset = 31*xdim*ydim;
offset = 0;

  zdim = 32;   /*  hack ... test .. */
/* if(1) { */
for(quality = 0; quality <=100; quality +=10) { 
       

  gettimeofday (&tv1, (struct timezone *) NULL);
        

        acc[0] = 'w';
        ierr = jcopen(1,JC3D,out_file,acc);
        printf("vor write ra %f, ras %f , iddc %i, le %f , xdim %i , ydim %i, zdim %i \n",
                                ra, ras, iddc, le, xdim, ydim,zdim);
        ierr = jcwinfo(1, &ra, &ras, &iddc, &le, &xdim, &ydim, &zdim);
while(1) { 
        ierr = jcwrite(1,JPTEMP, &niter, &mtime, &dt, &data[offset], &xdim, &ydim, &zdim, &quality);
        ierr = jcwrite(1,JPAX, &niter, &mtime, &dt, ax, &xdim, &ydim, &zdim, &quality);
        ierr = jcwrite(1,JPAY, &niter, &mtime, &dt, ay, &xdim, &ydim, &zdim, &quality);
}
        ierr = jcclose(1);

        av = 0.;
        for(i=0; i< xdim*ydim*zdim; i++) { 
         av += data[offset+i];
        /*   printf(" data [%i] = %f \n", i, data[offset+i]); */
        }
        printf(" avarage temp = %f \n", av/(float)(xdim*ydim*zdim));



  gettimeofday (&tv2, (struct timezone *) NULL);


        acc[0] = 'r';
        ierr = jcopen(1,&magic,out_file,acc);
        ierr = jcrinfo(1, &ra, &ras, &iddc, &le, &xdim, &ydim, &zdim);
        printf(" vor read ra %f, ras %f , iddc %i, le %f , xdim %i , ydim %i, zdim %i \n",
                                ra, ras, iddc, le, xdim, ydim,zdim);
        ierr = jcread(1, &niter, &mtime, &dt, newdat, &xdim, &ydim, &zdim);
        ierr = jcread(1, &niter, &mtime, &dt, newax, &xdim, &ydim, &zdim);
        ierr = jcread(1, &niter, &mtime, &dt, neway, &xdim, &ydim, &zdim);
        ierr = jcclose(1);

  gettimeofday (&tv3, (struct timezone *) NULL);
        av = 0.;
        for(i=0; i< xdim*ydim*zdim; i++) { 
         av += newdat[i];
        /*   printf(" newdat [%i] = %f \n", i, newdat[i]); */
        }
        printf(" avarage temp = %f \n", av/(float)(xdim*ydim*zdim)); 

        rmserr=0;
        maxerr=0;
        averr=0;
        for(i=0; i< xdim*ydim*zdim; i++) { 
          rmserr+=  pow(newdat[i] - data[offset+i],2);
          averr+=  ABS(newdat[i] - data[offset+i]);
          if(ABS(newdat[i] - data[offset+i]) > maxerr) maxerr = ABS(newdat[i] - data[offset+i]);
          if(ABS(newdat[i] - data[offset+i]) > 0.5) printf(" Housten we are having a problem i= %i data = %f newdat = %f \n", i,data[offset+i], newdat[i]);
          
        }
        rmserr /= xdim*ydim*zdim;
        rmserr = pow(rmserr,0.5);
        averr /= xdim*ydim*zdim;
        printf(" rms error   = %f avarage err = %f maxerr = %f \n", rmserr, averr, maxerr);



        {
        FILE *fff;
        fff = fopen("orgi.pgm", "w");
        fprintf(fff,"P5\n");
        fprintf(fff,"%i %i\n", xdim, ydim*zdim);
        fprintf(fff,"255\n");
        for(i=0; i< xdim*ydim*zdim; i++) fputc((unsigned char) (255.*data[offset+i]), fff);
        fclose(fff);
        }

        {
        FILE *fff;
        fff = fopen("new.pgm", "w");
        fprintf(fff,"P5\n");
        fprintf(fff,"%i %i\n", xdim, ydim*zdim);
        fprintf(fff,"255\n");
        for(i=0; i< xdim*ydim*zdim; i++) fputc((unsigned char) (255.*newdat[i]), fff);
        fclose(fff);
        }

        {
        FILE *fff;
        fff = fopen("diff.pgm", "w");
        fprintf(fff,"P5\n");
        fprintf(fff,"%i %i\n", xdim, ydim*zdim);
        fprintf(fff,"255\n");
        for(i=0; i< xdim*ydim*zdim; i++) fputc((unsigned char) (255.*(ABS(data[offset+i]-newdat[i])/maxerr)), fff);
        fclose(fff);
        }



        stat(out_file,&s_data_file);
        stat(inp_file,&o_data_file);
        printf("  size %ik ---> %ik : compression %f \%%\n",
                           o_data_file.st_size/1000, s_data_file.st_size/1000,
                           (float)(100-100*(float)s_data_file.st_size/(0.75*(float)o_data_file.st_size)));

         fprintf(fff," %i %f %f %i %f %f %f\n", quality, 100*averr, 100*maxerr,  (int)s_data_file.st_size,
                           (float)(100*(float)s_data_file.st_size/(0.75*(float)o_data_file.st_size)),
                            ((float) interval (&tv1, &tv2)) / 1000., ((float) interval (&tv2, &tv3)) / 1000.);
         }

        return(1);
}




get_greg_data()
/* This subroutine will read in the greg data file. */
{
	int iq=0, i;
        float xmin=100000, xmax=-1000000;

	if(access(inp_file, 0)) {  
		perror(inp_file); 
		exit(1);
	}

	readg_(&inp_file,data, ax, ay, &xdim, &ydim, &zdim, &iq, &niter, &mtime, &ra, &dt);

	if ((data = (float *) realloc(data,sizeof(float)*(xdim)*(ydim)*(zdim))) == NULL) {
		fprintf(stderr, "%s: error, not enough memory for the data set\n",
		   inp_file );
		return -1;
	}
	if ((ax = (float *) realloc(ax,sizeof(float)*(xdim)*(ydim)*(zdim))) == NULL) {
		fprintf(stderr, "%s: error, not enough memory for the data set\n",
		   inp_file );
		return -1;
	}
	if ((ay = (float *) realloc(ay,sizeof(float)*(xdim)*(ydim)*(zdim))) == NULL) {
		fprintf(stderr, "%s: error, not enough memory for the data set\n",
		   inp_file );
		return -1;
	}

	iq = 1;
	readg_(&inp_file,data, ax, ay, &xdim, &ydim, &zdim, &iq, &niter, &mtime, &ra, &dt);

        if(dirty) for(i=0; i< xdim*ydim; i++) data[i] = 1;  

                for(i=0; i< xdim*ydim*zdim; i++) {
                           if(data[i] > xmax) xmax = data[i];
                           if(data[i] < xmin) xmin = data[i];
                if(limit) {
                           if(data[i] > 1) data[i] =1.;
                           if(data[i] < 0) data[i] =0.;
                          }
                  }
            printf(" Temp min = %f max = %f ", xmin, xmax);
            if(limit) printf(" --- > changed to 0. 1.");
            printf("\n");

       
                              


	return 0;
}




/* evaluate interval between times. */
long
interval (const struct timeval *t1, const struct timeval *t2)
{
  return (t2->tv_sec - t1->tv_sec) * 1000
    + (t2->tv_usec - t1->tv_usec) / 1000;
}




