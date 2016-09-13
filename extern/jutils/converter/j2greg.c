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

#ifdef USE12B
#define MAXVAL 4095  /*4095*/
#define JDATA  short /*short or unsigned char*/
#else
#define MAXVAL 255  /*4095*/
#define JDATA  unsigned char /*short or unsigned char*/
#endif

int xdim, ydim, zdim, niter, iddc;
float mtime, dt, ra, ras, le;
float *data=NULL, *ax=NULL, *ay=NULL;    /* a pointer to the 3d volume of data */
char inp_file[80], out_file[80];		/* name of input file */
struct stat o_data_file, s_data_file;


MAIN__() {}
__main() {}

main(argc, argv)
int argc;
char *argv[];
{

	int i, ierr, errfac, magic=76 ;
        char acc[1]="r";

	if (argc <= 2) {
                fprintf(stderr," usage %s  infile outfile\n",  argv[0]);
		exit(1);
	}

	while((i=getopt(argc,argv,"hq:e:")) != -1)
	{
		switch(i) {
                case 'e':
                        sscanf(argv[optind-1], "%d", &errfac);
			break;
                case 'h':
                        exit(1);
			break;
		}
	}

		sprintf(inp_file,"%s\0",argv[argc-2]);
		sprintf(out_file,"%s\0",argv[argc-1]);

	printf(" inp_file   :  %s\n",inp_file);
	printf(" out_file   :  %s\n",out_file);


        ierr = jcopen(1,&magic,inp_file,acc);

        ierr = jcrinfo(1, &ra, &ras, &iddc, &le, &xdim, &ydim, &zdim);

        data = (float *) malloc(sizeof(float)*xdim*ydim*zdim);
        ax   = (float *) malloc(sizeof(float)*xdim*ydim*zdim);
        ay   = (float *) malloc(sizeof(float)*xdim*ydim*zdim);

        ierr = jcread(1, &niter, &mtime, &dt, data, &xdim, &ydim, &zdim);
        ierr = jcread(1, &niter, &mtime, &dt, ax, &xdim, &ydim, &zdim);
        ierr = jcread(1, &niter, &mtime, &dt, ay, &xdim, &ydim, &zdim);
        ierr = jcclose(1);

        put_greg_data();

        stat(out_file,&s_data_file);
        stat(inp_file,&o_data_file);
        printf("  size %ik --->  %ik : compression %i \%%\n",
                           o_data_file.st_size/1000, s_data_file.st_size/1000,
                           100-100*s_data_file.st_size/o_data_file.st_size);

 return(1);
}




put_greg_data()
/* This subroutine will read in the greg data file. */
{
	int iq=0;

	if(access(inp_file, 0)) {  
		perror(inp_file); 
		exit(1);
	}

	writeg_(&out_file,data, ax, ay, &xdim, &ydim, &zdim, &iq, &niter,
                &mtime, &ra, &dt);



	return 0;
}



