#include "jcmagic.h"
      program cont
      parameter (npt=300000)
      dimension xta(3*npt)
      character*70 data
      character*1 acc
      real ra,ras,le    
      integer magic
      ixlen = 0

      j=iargc()
      if(j.gt.0) then
      call getarg(1,data)
      else
      print*,'character-file =? '
      read(5,*) data
      endif

      acc='r'
      ierr=jcopen(1,magic,data,acc)
      if(ierr.le.-1) print*,'Error icopen 1 : ierr=',ierr

      ierr=icrinfo(1,ra,ras,iddc,le,numx,numy)

      print*,' numx,numy', numx,numy

c.. skip grid ..
      ierr = icskip(1,1, niter, rttime)
      lens = icskip(1, 1, niter, rttime);
      lent = icskip(1, 1, niter, rttime);
      print*,' lens, lent', lens, lent
c     ierr = jend(1);
      do i=1, 10000
      lens = icskip(1, 1, niter, rttime);
      lent = icskip(1, 1, niter, rttime);
      enddo
      lent = icskip(1, 1, niter, rttime);
c     ierr = icback(1, 1, lent);
c     ierr = icback(1, 1, lens);

c..... read temp .............................. 
      ierr=icread(1,niter,time,0,xta,ixlen)


      print*," read ", niter, time
      print*," length ", ixlen

      ierr=icclose(1)
      open(10,file="lasttemp.dat")
      write(10,*) numx, numy
      do i=1,numx*numy
      write(10,*) xta(i)
      enddo
      end
