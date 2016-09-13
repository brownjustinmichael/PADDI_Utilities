#include "inout.h"
#include <string.h>

extern FILE *fpo[MAXFILES];

/*
#ifdef CRAY
int JCOPEN(iu,magic,file,flen,acc,acclen)
#else
int jcopen_(iu,magic,file,acc,flen,acclen)
#endif
*/




int jcopen_(int *iu,int *magic,char *file,char *acc,int flen,int acclen)
{
	unsigned char *buf,buf2[180],lacc[180], c, c1, c2;
	extern FILE *fpo[];
	int i,j;


	sprintf(buf2,"%s",file);
	sprintf(lacc,"%s\0",acc);
	for(i=0;i<180;i++) {
		if((buf2[i] < 33) || (buf2[i] > 127) ) {
			buf2[i] ='\0';
			break;
		}
	}

	j = *iu;
	*(file+flen)='\0';
	j = *iu;
	if((fpo[*iu] = fopen(buf2,lacc)) == NULL) {
		fprintf(stderr,"error jcopen unit %i magic %i  file: %s, acc = %s flen = %i acclen= %i\n",
                              *iu,*magic, buf2,lacc,flen,acclen);
		return(-1);
	}
	if(lacc[0] == 'r') {
		if((c1 = fgetc(fpo[j])) == EOF) 
                     {fprintf(stderr,"EOF in jcopen\n"); return(-1);} 
		if((c2 = fgetc(fpo[j])) == EOF) 
                     {fprintf(stderr,"EOF in jcopen\n"); return(-1);} 
		if(c1 != 74) {
			*magic = 0; 
			rewind(fpo[j]);
		}
		else *magic = (int)c2;
	}
	else if(lacc[0] == 'w'  && *magic != 0) {
		fputc(74, fpo[j]); 
		fputc(*magic, fpo[j]);
	}
	else if( lacc[0] == 'a' && *magic != 0) {
                 fprintf(stderr,"Opening for append .. acc = %s\n", lacc);
	}
	else *magic =0;

	return(*magic);
}

int jcopen(int iu,int magic,char *file,char *acc)
{

    return(jcopen_(&iu, &magic, file, acc, strlen(file), strlen(acc)));
}
