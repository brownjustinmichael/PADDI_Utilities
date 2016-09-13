#include <stdio.h>
#include <stdlib.h>

#include "jcmagic.h"
#include "jcclass.h"

JCrecord::JCrecord(JCclass *parent)
{
    xdim = parent->xdim; 
    ydim = parent->ydim; 
    zdim = parent->zdim; 
    xdata = new float[xdim*ydim*zdim];
    actuelle=0;
}

JCrecord::~JCrecord(void)
{
    delete[] xdata;
}

int JCrecord::read_a_record()
{
  magic =  jcread(1, &niter, &mtime, &dt, xdata, &xdim, &ydim, &zdim);
  if(magic == -1) { actuelle=0; return(EOF);}
  actuelle=1;
  return 1;
}

int JCrecord::skip_a_record()
{
  magic = jcskip(1, 1 ,&niter,&mtime);
  printf("in skip_a_record %i \n", niter);
  if(magic == -1) return(EOF);
  actuelle=0;
  return 1;
}


float JCrecord::data(int i, int j, int k)
{
   if(!actuelle) read_a_record();
   return(xdata[i + xdim*j + xdim*ydim*k]);
}

float JCrecord::max()
{
   float max=xdata[0];
   for(int i=1; i < xdim*ydim*zdim; i++) if(xdata[i] > max) max=xdata[i];
   return(max);
}

float JCrecord::min()
{
   float min=xdata[0];
   for(int i=1; i < xdim*ydim*zdim; i++) if(xdata[i] < min) min=xdata[i];
   return(min);
}







JCclass::JCclass(char *filename) {
  char acc[2], buf[256];
  sprintf(acc,"r");
  sprintf(buf,filename);
  magic = jcopen(1,magic,buf,acc);
  if(magic == -1) { fprintf(stderr,"error jcopen\n"); exit(0);}
  int ierr = jcrinfo(1, &ra, &ras, &npde, &le, &xdim, &ydim, &zdim);
  if(ierr == -1) { fprintf(stderr,"error jcrinfo\n"); exit(0);}


  rec = new JCrecord[npde](this);

}

JCclass::~JCclass()
{
  delete[] rec;
}

int JCclass::read_a_step()
{
 for(int i=0; i< npde; i++) if(rec[i].read_a_record() == EOF) return(EOF);
 return 1;

}

int JCclass::skip_step(int n)
{
 for(int i=0; i< npde*n; i++) if(rec[i].skip_a_record() == EOF) return(EOF);
 return 1;

}


#ifdef WITHMAIN

main()
{
  JCclass *M = new JCclass("/home/joergs/ctest/j__data");

  while(M->read_a_step() != EOF) { 
      printf(" min %f max %f \n", M->rec[1].min(), M->rec[1].max());
  }

  delete M;

}

#endif
