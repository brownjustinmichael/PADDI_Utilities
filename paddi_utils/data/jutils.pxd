cdef extern from "../../extern/jutils/jcmagic.h":
	int JC2D = 76

	int JCGRID = 10
	int JCTEMP = 11
	int JCCHEM = 12
	int JCSTREAM = 13
	int JCPSI = 14
	int JCPSIDX = 15
	int JCPSIDY = 16


	int JC3D = 77
	int JC3R = 78
	int JC3S = 79

	int JPTEMP = 20
	int JPAX = 21
	int JPAY = 22
	int JPVELX = 23
	int JPVELY = 24
	int JPVELZ = 25
	int JPPRES = 26
	int JPCHEM = 27
	int JPBX = 28
	int JPBY = 29
	int JPBZ = 30

	int jcopen(int iu, int magic, char* file, char* acc)
	int jcwinfo(int ,float *,float *,int *,float *,int *,int *, int *)
	int jcwrite(int , int , int *,float *,float *,float *,int *,int *,int *,int * )
	int jcskip(int , int , int *,float *)
	int jcrinfo(int ,float *,float *,int *,float *,int *,int *, int *)
	int jcrinfo2_(int *iu,int *numx,int *numy,int *numz,int *npde,int *ninfo,float *finfo,char *cinfo,int clen)
	int jcread(int ,int *,float *,float *,float *,int *,int *,int *)
	int jcclose(int )
	