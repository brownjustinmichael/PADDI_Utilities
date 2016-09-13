
      program cont
      character*7 tata
      character*2 acc
      real ra,ras,le    
      real x(20,20,3), t(20,20), git(20*20*2)
      integer magic, quality
       acc='w'
       tata = "c__data"
      ierr=icopen(1,tata,acc)
      print*,'Nach dem icopen'
       if(ierr.ne.0) print*,'icopen 1 : ierr=',ierr

       ra = 5.
       ras = 1.
       iddc = 0
       le   = 0.
       numx = 20
       numy = 20
      ierr=icwinfo(1,ra,ras,iddc,le,numx,numy)

       x(:,:,1) = 0.
       x(:,:,2) = -0.5
       x(:,:,3) = 0.
       t(:,:) = 0.5

       nle = 10
       time = 0.001
       dt = 0.01
      ixlen = 20*20*3


!....create grid....................................................
      do i =1,20
         do k = 1,20
            git(k+(i-1)*20)=(i-1)/float(20-1)
            git(k+(i-1)*20+20*20) = (k-1)/float(20-1)
         enddo
      enddo


      ierr=icwrite(1,1,0.0,0.0,git,2*20*20)



      do i=1, 100

      time  = time + dt
! psi, vx, vy//
      ierr = icwrite(1,i,time,dt,x,ixlen)
! t 
      ixlen = 20*20
      ierr = icwrite(1,i,time,dt,t,ixlen)

      enddo

       print*,ra,ras,iddc,le,numx,numy

      end
