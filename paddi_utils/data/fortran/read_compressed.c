#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <map>
#include "jcmagic.h"

#define CLEN 20
#define NINFO 7
#define NUMX 128*3
#define NUMY 128*3
#define NUMZ 128*3
#define NTSTEPS 10

extern "C" int jcopen(int iu,int magic,char *file,char *acc);
extern "C" int jcrinfo2_(int *iu,int *numx,int *numy,int *numz,int *npde,int *ninfo,float *finfo,char *cinfo,int clen);
extern "C" int jcread(int iu,int *niter,float *time,float *dt,float *x,int *xdim,int * ydim,int * zdim);
extern "C" int jcclose(int iu);

#define JPTEMP 20   /*** 3D temp field **/
#define JPAX 21     /*** 3D stream x field **/
#define JPAY 22     /*** 3D stream y field **/
#define JPVELX 23   /*** 3D  vel x field **/
#define JPVELY 24   /*** 3D vel y  field **/
#define JPVELZ 25   /*** 3D vel z  field **/
#define JPPRES 26   /*** 3D pressure field **/
#define JPCHEM 27   /*** 3D chem field **/
#define JPBX 28   /*** 3D BX field **/
#define JPBY 29   /*** 3D BY field **/
#define JPBZ 30   /*** 3D BZ field **/

int read_compressed(char* file, int niter) {
	int ierr;
	int iu = 0;
	char acc[2] = "r";
	char cinfo[CLEN*NINFO];
	float finfo[NINFO];

	int numx,numy,numz;
	int ninfo = NINFO;
	int npde;

	std::vector<float> temp_vec(NUMX*NUMY*NUMZ);
	float* temp = &temp_vec[0];
	float time;
	float dt;

	int magic;

	std::map<int,std::vector<float> > data;
	data[JPTEMP] = std::vector<float>(NUMX*NUMY*NUMZ);
	data[JPVELX] = std::vector<float>(NUMX*NUMY*NUMZ);
	data[JPVELY] = std::vector<float>(NUMX*NUMY*NUMZ);
	data[JPVELZ] = std::vector<float>(NUMX*NUMY*NUMZ);
	data[JPPRES] = std::vector<float>(NUMX*NUMY*NUMZ);
	data[JPCHEM] = std::vector<float>(NUMX*NUMY*NUMZ);
	data[JPBX] = std::vector<float>(NUMX*NUMY*NUMZ);
	data[JPBY] = std::vector<float>(NUMX*NUMY*NUMZ);
	data[JPBZ] = std::vector<float>(NUMX*NUMY*NUMZ);

	printf("%i\n", magic);

	jcopen(iu,JC3D,file,acc);

	jcrinfo2_(&iu,&numx,&numy,&numz,&npde,&ninfo,finfo,cinfo,CLEN);
	float* data_ptr;

	for (int q = 0; q < NTSTEPS; ++q)
	{
		for (int i = 0; i < npde; ++i)
		{
			magic = jcread(iu,&q,&time,&dt,temp,&numx,&numy,&numz);
			data_ptr = &data[magic][0];
			for (int j = 0; j < numx*numy*numz; ++j)
			{
				data_ptr[j] = temp[j];
			} 
			printf("%i %f\n", magic, temp[0]);
		}
	}

	jcclose(iu);


	// int jcrinfo2_(&iu,int *numx,int *numy,int *numz,int *npde,int *ninfo,float *finfo,char *cinfo,int clen)


	// #ifdef TWO_DIMENSIONAL
	//         number_of_jc_fields = 3
	// #else
	//         number_of_jc_fields = 6
	// #endif
	// #ifdef TEMPERATURE_FIELD
	//         number_of_jc_fields = number_of_jc_fields + 1 
	// #endif
	// #ifdef CHEMICAL_FIELD
	//         number_of_jc_fields = number_of_jc_fields + 1 
	// #endif
	// #ifdef TWO_DIMENSIONAL
	//         ierr = jcwinfo2(1,nx,nz,1,number_of_jc_fields,ninfo,finfo,cinfo)
}

int main(int argc, char const *argv[])
{
	char file[20] = "j__data03";
	read_compressed(file, 0);
	return 0;
}