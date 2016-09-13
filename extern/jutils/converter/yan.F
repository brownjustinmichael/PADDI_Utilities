#include "jcmagic.h"

      program cont
      parameter (npt=10000000)
      dimension xta(3*npt)
c     dimension x(2,npt),ta(3,npt)
      character*70 data
      character*7 tata
      character*1 acc
      logical ddc,tracer,to8
      real ra,ras,le    
      integer magic, quality
c     print*,'***********************************************'
c     print*,'Character  to  Character....                   '
c     print*,'***********************************************'
c     print* 
c     print*
      j=iargc()
      tracer = .false.
      quality = 65
      to8  = .false.
      if(j.gt.3)  then
       to8 =   .true.
       tracer = .true.
       call getarg(3,tata)
       call getarg(4,data)
       elseif(j.gt.2) then
       tracer = .true.
       call getarg(2,tata)
       call getarg(3,data)
      else

      if(j.gt.0) then
      call getarg(1,tata)
      else
      print*,'character-file =? (7 characters!)'
      read(5,*) tata
      endif
      if(j.gt.1) then
      call getarg(2,data)
      else
      print*,'output data-file =? '
      read(5,*) data
      call iread(" Compression factor ?, default:", quality)
      endif
      endif
      acc='r'
      ierr=icopen(1,tata,acc)
      print*,'Nach dem icopen'
      if(ierr.ne.0) print*,'icopen 1 : ierr=',ierr
      acc='w'
      ierr=jcopen(2,JC2D,data,acc)
      print*,'Nach dem icopen'
      if(ierr.ne.0) print*,'Error icopen 2: ierr=',ierr
      if(.not.tracer) then

      ierr=icrinfo(1,ra,ras,iddc,le,numx,numy)

c     print*
c     call iread("numx = ",numx)
c     call iread("numy = ",numy)
c     call rread('Ra       =',ra)
      ddc=.false.
      if(iddc.eq.1)  then
      ddc=.true.
c     call lread('DDC      =',ddc)
      if(.not.ddc) iddc = 0
c     call rread('Ra c     =',ras)
c     call iread('Le       =',le)   
c     print*   
      endif
      ierr=jcwinfo(2,ra,ras,iddc,le,numx,numy, 1)
      endif

c     print*,'nskip ?  (nskip < 0 : all timesteps )'
c     read(5,*) nskip
c     if(nskip.ge.0) then
c       print*,'nplot ?'
c       read(5,*) nplot
c     else
        nplot = 999999999
        call iread(" Nplot ?, default:", nplot)
c     endif
      numnp = numx*numy
      titer=1.
      nrest=25
      ndm = 2
      abstx = 25.
      niter=0
      time=0
      rewind nrest
      if(ierr.ne.0) print*,'Error icwrite : ierr =',ierr
c     print*,'gitter=',ixlen,' numnp=',numnp,' < ','npt=',npt
       write(6,*) "grid"
        call flush(6)
      if(npt.lt.numnp) then
	print*,'ACHTUNG !!!!! npt zu klein !!!!'
	stop
       endif
c*** Grid ************
      if(.not.tracer) then

      ierr=icread(1,niter,time,0,xta,ixlen)
      print*,'ixlen=',ixlen
      ierr=icwrite(2,niter,time,0,xta,ixlen)
      endif
      
       icount = 0

      do 9997 iplo=1,nplot


         icount =  icount + 1


	niter=nskip+iplo
C ...... read and write stream-fkt...........................
       ixlen = 0
       ierr=icread(1,niter,time,dt,xta,ixlen)
c      print*,'Time = ',time
c      print*,'ixlen=',ixlen,'  3*numnp=',3*numnp
c      print*,'ierr=',ierr
        write(6,'(i5,3H   ,i5,3H   ,f7.5)') icount,niter,time
       call flush(6)
       if(ierr.ne.0) goto 9998
       if(to8) niter = -2
      ierr=jcwrite(2,JCPSI,niter,time,0,xta(1),numx, numy, 1, quality)
      ierr=jcwrite(2,JCPSIDX,niter,time,0,xta(1+numx*numy),numx,numy,1, 
     &     quality)
      ierr=jcwrite(2,JCPSIDY,niter,time,0,xta(1+2*numx*numy),numx,numy,
     &     1, quality)

       if(.not.tracer) then

C........ read and write temp ................................
       ixlen = 0
       ierr=icread(1,iiniter,time,dt,xta,ixlen)
c      print*,'ixlen=',ixlen,'  2*numnp=',2*numnp
       if(ierr.ne.0) goto 9998
       if(to8) niter = -2
       ierr=jcwrite(2,JCTEMP,niter,time,0,xta,numx, numy, 1, quality)
       
C........ read and write chem ................................
      if(ddc) then
       ierr=icread(1,niter,time,dt,xta,ixlen)
       ierr=jcwrite(2,JCCHEM,niter,time,0,xta,numx, numy, 1, quality)
      endif
      endif


9997  continue
 
9998  continue
      write(6,*) "THE END"
      call flush(6)
      ierr=icclose(1)
      ierr=icclose(2)
 9999 continue
      stop
      end
       subroutine iread(text,ival)
       character*(*) text
       character*10 cin
       cin='          '
       write(6,'(a,i10,a3,$)') text,ival,' : '
       call flush(6)
       read(5,'(a10)') cin
       if (cin.ne.'          ') then
	  read(cin,'(i10)') ival
       endif
       return
       end
