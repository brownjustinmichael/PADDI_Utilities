#include "jcmagic.h"
      program cont
      parameter (npt=300000)
      dimension xta(3*npt)
      dimension x(2,npt),ta(3,npt)
      character*70 data
      character*70 tata
      character*1 acc
      logical ddc,tracer,to8
      real ra,ras,le    
c     print*,'***********************************************'
c     print*,'Character  to  Character....                   '
c     print*,'***********************************************'
c     print* 
c     print*
      j=iargc()
      tracer = .false.
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
      endif
      endif
      acc='r'
      ierr=jcopen(1,magic,tata,acc)
      print*,'Nach dem jcopen .. magic =', magic
c     print*,'Nach dem icopen'
      if(ierr.le.-1) print*,'Error icopen 1 : ierr=',ierr
      acc='w'
      ierr=icopen(2,data,acc)
      if(ierr.ne.0) print*,'Error icopen 2: ierr=',ierr
      if(.not.tracer) then

      ierr=jcrinfo(1,ra,ras,iddc,le,numx,numy,numz)

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
      ierr=icwinfo(2,ra,ras,iddc,le,numx,numy)
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

c     ierr=jcread(1,niter,time,0,xta,numx, numy, numz)
c     ixlen = numx*numy*numz
      print*,'ixlen=',ixlen
       if(to8) niter = -2
      ierr=icwrite(2,niter,time,0,xta, ixlen)
      endif

       icount = 0

      do 9997 iplo=1,nplot

c      read(5,'(a1)') c
c      if(c.eq."q") then 
c       ierr=icclose(1)
c       ierr=icclose(2)
c       stop
c      elseif(c.eq."F") then
c       ierr=icskip(1,1,niter,time)
c        icount =  icount + 1
c       write(6,'(i5,3H   ,i5,3H   ,f7.5)') icount,niter,time
c       call flush(6)
c       if(ierr.lt.2*numnp) goto 9998
c       ierr=icskip(1,1,niter,time)
c       if(ierr.lt.2*numnp) goto 9998
c       if(ddc) ierr=icskip(1,1,niter,time)
c      elseif(c.eq."f") then

         icount =  icount + 1


	niter=nskip+iplo
C ...... read and write stream-fkt...........................
       ixlen = 0
      ierr=jcread(1,niter,time,0,xta(1),numx, numy, numz)
      ierr=jcread(1,niter,time,0,xta(numx*numy),numx, numy, numz)
      ierr=jcread(1,niter,time,0,xta(2*numx*numy),numx,numy,numz)
      ixlen = numx*numy*numz
c      print*,'Time = ',time
c      print*,'ixlen=',ixlen,'  3*numnp=',3*numnp
c      print*,'ierr=',ierr
        write(6,'(i5,3H   ,i5,3H   ,f7.5)') icount,niter,time
       call flush(6)
       if(ierr.le.-1) goto 9998
       if(to8) niter = -2
       ierr=icwrite(2,niter,time,dt,xta,3*ixlen)

       if(.not.tracer) then

C........ read and write temp ................................
       ixlen = 0
      ierr=jcread(1,niter,time,0,xta,numx, numy, numz)
      ixlen = numx*numy*numz
c      print*,'ixlen=',ixlen,'  2*numnp=',2*numnp
       if(ierr.le.-1) goto 9998
       if(to8) niter = -2
       ierr=icwrite(2,niter,time,dt,xta,ixlen)
       
C........ read and write chem ................................
      if(ddc) then
      ierr=jcread(1,niter,time,0,xta,numx, numy, numz)
      if(ierr.le.-1) goto 9998
      ixlen = numx*numy*numz
       if(to8) niter = -2
       ierr=icwrite(2,niter,time,dt,xta,ixlen)
      endif
      endif


c     endif

 9997 continue

 9998 continue
      call flush(6)
      ierr=icclose(1)
      ierr=icclose(2)
 9999 continue
      stop
      end
