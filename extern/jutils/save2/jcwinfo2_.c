#include "inout.h"

int jcwinfo2_(int *iu,int *numx,int *numy,int *numz,int *npde,int *ninfo,float *finfo,char *cinfo,int clen)

{
extern FILE *fpo[MAXFILES];
int i;

  fprintf(fpo[*iu],"info2 %4d %4d %4d %4d %4d %4d ",
	  *numx,*numy, *numz, *npde, *ninfo, clen);
  for(i=0; i< *ninfo; i++) fprintf(fpo[*iu],"%6e ",finfo[i]);
  for(i=0; i< *ninfo*clen; i++) fputc(cinfo[i],fpo[*iu]);
  fprintf(fpo[*iu],"\n");
  return(0);
}




/*
int jcwinfo2(int iu,float *ra,float *ras,int *iddc,float *le,int *numx,int *numy, int *numz)
{
  return(jcwinfo2_(&iu,ra,ras,iddc,le,numx,numy, numz));
}
*/


