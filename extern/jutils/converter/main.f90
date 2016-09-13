program hi
character buf*70, acc*2

 buf = "lall.xxx"
 acc = "w"
! call clall()
 ierr = icopen(2,buf,acc)
  ra = 0.
  ras = 1.
  iddc = 2
  xle =3. 
  numx = 20
  numy = 20
 ierr=icwinfo(2,ra,ras,iddc,xle,numx,numy)
! ierr=icclose(2)

end
