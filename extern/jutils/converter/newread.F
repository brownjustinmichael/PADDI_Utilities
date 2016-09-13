#include "jcmagic.h"

      program cont
      parameter (npt=32*32*32)
      dimension xta(3*npt)
c     dimension x(2,npt),ta(3,npt)
      character*70 data
      character*7 tata
      character*1 acc
      logical ddc,tracer,to8
      real ra,ras,le    
      external real function  rand
      integer magic, quality
c     print*,'***********************************************'
c     print*,'Character  to  Character....                   '
c     print*,'***********************************************'
c     print* 
c     print*
      quality = 100
      acc='w'
      data='j__data'
      ierr=jcopen(2,JC2D,data,acc)
      print*,'Nach dem icopen'
      if(ierr.ne.0) print*,'Error icopen 2: ierr=',ierr


      numx = 32 
      numy = 32 
      numz = 32 
      iddc = 1 
      ierr = -1
      do i=1,numx*numy*numz
      xta(i) = ran1(ierr)
      enddo
      ierr=jcwinfo(2,ra,ras,iddc,le,numx,numy, numz)
      do i=1,10
         print*,i
      ierr=jcdwrite(2,JCPSI,niter,time,0,xta,numx, numy, numz, quality)
      enddo
      ierr=icclose(2)
      end


      FUNCTION ran1(idum)
      INTEGER idum,IA,IM,IQ,IR,NTAB,NDIV
      REAL ran1,AM,EPS,RNMX
      PARAMETER (IA=16807,IM=2147483647,AM=1./IM,IQ=127773,IR=2836,
     *NTAB=32,NDIV=1+(IM-1)/NTAB,EPS=1.2e-7,RNMX=1.-EPS)
      INTEGER j,k,iv(NTAB),iy
      SAVE iv,iy
      DATA iv /NTAB*0/, iy /0/
      if (idum.le.0.or.iy.eq.0) then
        idum=max(-idum,1)
        do 11 j=NTAB+8,1,-1
          k=idum/IQ
          idum=IA*(idum-k*IQ)-IR*k
          if (idum.lt.0) idum=idum+IM
          if (j.le.NTAB) iv(j)=idum
11      continue
        iy=iv(1)
      endif
      k=idum/IQ
      idum=IA*(idum-k*IQ)-IR*k
      if (idum.lt.0) idum=idum+IM
      j=1+iy/NDIV
      iy=iv(j)
      iv(j)=idum
      ran1=min(AM*iy,RNMX)
      return
      END



