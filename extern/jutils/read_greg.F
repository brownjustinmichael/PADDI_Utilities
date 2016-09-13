	subroutine readg(filename,temp,ax,ay,numx,numy,numz,iq,
     &  kstep, xtime, xrayl, xdt )
	character*80 filename
	character acc*1
	integer nx(3)
        logical uniform,ddc
c*******************************************
      PARAMETER (NWORD1=128)
      COMMON/MESH/MIQX,MIQY,MIQZ,MNX1,MNY1,MNZ1,NX1,NY1,NZ1,JDIMX,JDIMY,
     1 MDUM,MWORD1,MWORD2,JBB(50)
      COMMON/EARTH/RAYL,TIME,NSTEP,EPS,UMAX,VMAX,WMAX,UVWMAX,EKTOT,
     1 VELMA,DT(2),FND,IHEAT,FTOP,FBOT,AVBOX,TMOM,ROTX,ROTY,IRG,
     2 dxp,dyp,IDUMN(41)

c*******************************************
        common/doof/idoof

	real temp(1), ax(1), ay(1)
	parameter(iunit=1)
c----- new ------------------------
#ifdef HAS_F_MALLOC
	real xta(1)
	pointer (pxta,xta)
#else
        real xta(256*256*64)
#endif
c----------------------------------       
        uniform = .false.

        
        acc='r'

        ixan = 0
        iyan = 0
        izan = 0
        istep = 1

c********************************************
        LDIN=10
      OPEN(LDIN,IOSTAT=IOS,FILE=filename,STATUS='OLD',
     1 FORM='UNFORMATTED')
      IF(IOS.NE.0)THEN
      WRITE(0,10117)IOS,filename
10117 FORMAT(' IOSTAT =',I5,' ON FILE ',A40)
      return
      END IF

      CALL HREAD(NWORD1)
      if(DXP.eq.DYP) uniform = .true.
      kstep = Nstep
      xtime = time
      xrayl = rayl
      xdt   = dt(1)
      if(iq.eq.0) then

      WRITE(0,10116)RAYL,TIME,NSTEP,EPS,FND

10116 FORMAT(' Rayleigh number =',G12.6,/,' Time            =',
     1G12.6,/,' Nstep           =',I8,/,' Internal heating=',
     2G12.6,/,' Basal flux      =',G12.6,/)
C
C
      WRITE(0,*) 'DXP = ', DXP, ' DYP = ',DYP
      WRITE(0,*) 'nx =',NX1,' ny=',ny1,' nz=',nz1
      if(uniform) print*,'>>>>> UNIFORM DATA <<<<<<'

      endif
      RNX=FLOAT(NX1)
      RNY=FLOAT(NY1)
      RNZ=FLOAT(NZ1)
c********************************************

        numx = NX1 +1
        numy = ny1 +1
        numz = nz1 +1
        if(iq.eq.0) then
         close(10)
         return
        endif
c...hack....
        aspx = DXP * RNX / RNZ
        aspy = DYP * RNY / RNZ
        ddc=.false.
        iddc = 0

c........joerg...................................................
        ixend = NX1 +1 
        iyend = NY1 +1 
        izend = NZ1 +1 
        nx(1) = (ixend-ixan) / istep 
        nx(2) = (iyend-iyan) / istep 
        nx(3) = (izend-izan) / istep 
#ifdef HAS_F_MALLOC
 	pxta = malloc(4*(numx+1)*(numy+1)*(numz+1) )
#endif

c///////////////////////////////////////////////////
      nrec=mnx1
      nsize1=nword1/2
      nsize2=mny1*mnz1

      do 111 jjj =1, 4 
c... read 1st temp step................
      do 350 kin=1,nrec
      ind1=(kin-1)*nsize2 + 1
      ind2=kin*nsize2
      read(10,end=100, err=100)(xta(i),i=ind1,ind2)
  350 continue
c///////////////////////////////////////////////////
        xdmin = 1.
        xdmax = 0.

        izz = 0
        icount = 0
        do iz=1+izan,izend,istep
         izz = izz + 1
         iyy = 0 
         do iy=1+iyan,iyend,istep
          iyy = iyy + 1
          ixx = 0
          do ix=1+ixan,ixend,istep
           ixx = ixx + 1
           icount = icount +1
 
           if(jjj.eq.1) 
     &      temp(icount) = xta((ix-1)*numy*numz + iy +(iz-1)*numy)
           if(jjj.eq.3) 
     &      ax(icount) = xta((ix-1)*numy*numz + iy +(iz-1)*numy)
           if(jjj.eq.4) 
     &      ay(icount) = xta((ix-1)*numy*numz + iy +(iz-1)*numy)
          enddo
         enddo
        enddo 
          nx(1) = ixx
          nx(2) = iyy
          nx(3) = izz

 111    continue
c...............................................................
#ifdef HAS_F_MALLOC
        call free(pxta)
#endif
        close(10)
	return
100	continue
	print*,'data file read error'
	return
	end
      SUBROUTINE HREAD(NWORD1)
C
C   Reads the header record
C
      COMMON/MESH/JAA(64)
      COMMON/EARTH/JAB(64)
      COMMON/CONTRO/LMESS,LPLOT,LDIN,LWINT,LIN,LUW
C
      REWIND 10
      NHALF=NWORD1/2
      READ(10,end=999,err=999)(JAA(I),I=1,NHALF),(JAB(I),I=1,NHALF)
c     READ(10)(JAA(I),I=1,NHALF),(JAB(I),I=1,NHALF)
      WRITE(0,10100)
10100 FORMAT(' Header record read from data file.')
 999  RETURN
      END

