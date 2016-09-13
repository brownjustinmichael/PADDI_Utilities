
      program cont
      character*70 tata
      character*1 acc
      real ra,ras,le    
      integer magic, quality
      acc='r'
       tata = "c__data"
      ierr=icopen(1,tata,acc)
      print*,'Nach dem icopen'
       if(ierr.ne.0) print*,'icopen 1 : ierr=',ierr

      ierr=icrinfo(1,ra,ras,iddc,le,numx,numy)

       print*,ra,ras,iddc,le,numx,numy

      end
