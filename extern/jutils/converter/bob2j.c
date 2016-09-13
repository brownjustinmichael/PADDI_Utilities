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

int limit=0, dirty=0, bob=0, x1 =1, istep = 0;

MAIN__() {}
__main() {}

main(argc, argv)
int argc;
char *argv[];
{

	int i, j, ierr, errfac, magic=77, quality=85;
        char acc[1]="w";

        FILE *fff;
        fff = fopen("data", "w");

	if (argc <= 2) {
                fprintf(stderr," usage: %s  -s XDIMxYDIMxZDIM -o outfile -q quality  infile1 infile2 ...\n",  argv[0]);
		exit(1);
	}

	sprintf(out_file,"j_out");
           printf(" for getopt .. \n");
	while((i=getopt(argc,argv,"s:dhq:e:q:o:")) != -1)
	{
		switch(i) {
                case 'e':
                        sscanf(argv[optind-1], "%d", &errfac);
			break;
                case 'h':
                        exit(1);
			break;
                case 's':
                        bob = 1;
                        sscanf(argv[optind-1], "%ix%ix%i", &xdim, &ydim, &zdim);
                        printf(" xdim %i ydim %i zdim %i\n", xdim, ydim, zdim);
                        break;
                case 'd':
                        printf(" Dirty hack ... lowest level must be T=1\n");
                        dirty = 1;
			break;
                case 'q':
                        sscanf(argv[optind-1], "%i", &quality);
                        printf(" Quality set to %i\n", quality);
			break;
                case 'o':
		        sprintf(out_file,"%s\0",argv[optind-1]);
			break;
		}
	}

/*

         printf(" %i filename %s \n", i, argv[i]);
*/
         printf(" %i filename %s   \n", optind, argv[optind]);
        


        ierr = jcopen(1,JC3D,out_file,acc);
        ierr = jcwinfo(1, &ra, &ras, &iddc, &le, &xdim, &ydim, &zdim);

        data = (float *) malloc(xdim*ydim*zdim*sizeof(float));

        for(i=optind; i< argc ; i++) 
        {
         printf(" %s \n", argv[i]);
         fff = fopen(argv[i],"r");
           for(j=0; j < xdim*ydim*zdim; j++) data[j] =1./255. * (float) fgetc(fff);
         fclose(fff);

        istep++;
        niter++;

        ierr = jcwrite(1,JPTEMP, &niter, &mtime, &dt, data, &xdim, &ydim, &zdim, &quality);
        ierr = jcwrite(1,JPAX, &niter, &mtime, &dt, data, &x1, &x1, &x1, &quality);
        ierr = jcwrite(1,JPAY, &niter, &mtime, &dt, data, &x1, &x1, &x1, &quality);

        }

        ierr = jcclose(1);

        return(1);
}


