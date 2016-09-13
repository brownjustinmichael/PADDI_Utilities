#include "inout.h"
#include <string.h>

extern FILE *fpo[MAXFILES];
int icopen_(iu,file,acc,flen,acclen)

/***** iu    = file unit
       file  = filename
       acc   = accecs
       flen  = length of 'file', done automaticly
       acclen= length of 'acc', done automaticly

       RETURNS
	0    = erverything fine 
        1    = error

*****/

char *file,*acc;
int *iu,flen,acclen;
{
 char *buf,buf2[180],lacc[1], c;
 extern FILE *fpo[];
  int i,j;
/******************************************
   sprintf(buf2,"%s\0",file);
   for(i=0;i<180;i++) {
#ifdef DEBUG
fprintf(stderr,"%c %i\n",buf2[i] ,buf2[i] ); 
#endif
if((buf2[i] < 33) || (buf2[i] > 127) ) {buf2[i] ='\0';break;}}
#ifdef DEBUG
    fprintf(stderr," icopen:Length: %i %s end \n",i,buf2); 
#endif
     j = *iu;
#ifdef DEBUG
    fprintf(stderr,"icopen unit %i file: %s, acc = %s flen = %i acclen= %i\n",j,file,acc,flen,acclen);
#endif
    *(file+flen)='\0';
     j = *iu;
    if((fpo[j] = fopen(buf2,acc)) == NULL) {
    fprintf(stderr,"error icopen unit %i file: %s, acc = %s flen = %i acclen= %i\n",*iu,buf2,acc,flen,acclen);
    return(1);
      }
    return(0);
*******************************************/
    *(file+flen)='\0';
    if((fpo[*iu] = fopen(file,acc)) == NULL) return(1);
    return(0);

}

/** the c- interface */
int 
icopen(int iu, char *file, char *acc)
{
 int flen, acclen;

 flen = strlen(file);
 acclen =  strlen(acc); 
 return(icopen_(&iu, file, acc, flen, acclen));
}

