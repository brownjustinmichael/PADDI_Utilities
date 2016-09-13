#include "jcmagic.h"

program lall

      character data*70, acc*1, cinfo(20)*20
      real finfo(20), xta(50*50*50)
      numx =5
      numy =5
      numz =5
      npde = 4
      ninfo = 20


      do i=1, ninfo
       finfo(i) = float(i)
      enddo
      cinfo = "xxxxxxxxxxx"

      cinfo(1) = "Joerg"
      cinfo(2) = "Schmalzl"
      cinfo(3) = "Spichernstr."
      cinfo(4) = "25"
      cinfo(5) = "48159"
      cinfo(6) = "Muenster"
      
     
      data = "tlall.dat"
      acc = "w"

      ierr=jcopen(2,JC2D,data,acc)
      ierr=jcwinfo2(2,numx,numy, numz, npde, ninfo,  finfo, cinfo)

      xta = 2.5
      iquality = 80;
      niter = 234
      time = 0.0001

      ierr=jcwrite(2,JCPSI,niter,time,0,xta(1),numx, numy, numz, iquality)
      ierr=icclose(2)

      numx = 0
      numy = 0
      numz = 0
      ninfo = 20
      acc = "r"
      xta = 0.
      niter = 0
      time = 0.

      ierr=jcopen(1,magic,data,acc)
!     ierr=jcrinfo2(1,numx,numy, numz, npde, ninfo, finfo, cinfo, 20)
      ierr=jcrinfo(1,ra,ras,iddc,le,numx,numy,numz)
      ierr=jcread(1,niter,time,0,xta(1),numx, numy, numz)
      ierr=icclose(1)

      print*,numx,numy, numz, npde, ninfo
      do i=1, ninfo
!      print*,finfo(i) 
       print*,i, cinfo(i) 
      enddo

      print*,xta(112), niter, time
end



