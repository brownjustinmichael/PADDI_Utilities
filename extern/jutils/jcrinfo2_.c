#include "inout.h"

int jcrinfo2_(int *iu,int *numx,int *numy,int *numz,int *npde,int *ninfo,float *finfo,char *cinfo,int clen)


{
extern FILE *fpo[MAXFILES];
char buf[100];
int lclen, lninfo, i;
fpos_t pos;
float xx;



  fgetpos( fpo[*iu], &pos);
  if(fscanf(fpo[*iu],"%s",buf) == EOF) { fprintf(stderr," error in jcrinfo_\n"); return(-1);}
  fsetpos( fpo[*iu], &pos);

   fprintf(stderr," in jcrinfo2  buf = %s\n",buf);

  if(strcmp("info2", buf) != 0) { 
          fprintf(stderr," error in jcrinfo2 maybe not an info2 record .. trying old format !!\n", buf); 
          *ninfo = -1;
          return(jcrinfo_(iu,&finfo[0],&finfo[1],npde,&finfo[2],numx,numy,numz));}
  
  if(fscanf(fpo[*iu],"%s %d %d %d %d %d %d",buf, 
	  numx,numy, numz, npde, &lninfo, &lclen) == EOF) { 
                       fprintf(stderr," error in jcrinfo_\n"); return(-1);
                     }
  if(*ninfo == 0) {  /** maybe called from jcwrite .. skip stuff **/
                  for(i=0; i< lninfo; i++) fscanf(fpo[*iu],"%e ",&xx);
                  for(i=0; i< lninfo*lclen; i++)  fgetc(fpo[*iu]);
                  fgetc(fpo[*iu]); /* cr */
                 return(0);
                 }
  if(lninfo > *ninfo) { fprintf(stderr," error in jcrinfo2 .. size of array too small, is %i I need %i \n",
                                *ninfo,lninfo);
                         return(-1);}
  if(lclen > clen) { fprintf(stderr," error in jcrinfo2 .. length of charater array too small, is %i I need %i \n",
                                clen,lclen);
                         return(-1);}

   fprintf(stderr," in jcrinfo2  ninfo = %i  %i\n",*ninfo, lninfo);
  *ninfo = lninfo;
  
  for(i=0; i< *ninfo; i++) fscanf(fpo[*iu],"%e ",&finfo[i]);
  for(i=0; i< *ninfo*(lclen); i++) cinfo[i] = fgetc(fpo[*iu]);
  fgetc(fpo[*iu]); /* cr */


  return(0);
}

/*
int jcrinfo(int iu,float *ra,float *ras,int *iddc,float *le,int *numx,int *numy, int *numz)
{
  return(jcrinfo_(&iu,ra,ras,iddc,le,numx,numy,numz));
}

*/

