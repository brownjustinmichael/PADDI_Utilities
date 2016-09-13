	subroutine writeg(filename,temp,ax,ay,numx,numy,numz,iq,
     &  kstep, xtime, xrayl, xdt)
	character*80 filename
	integer nx(3)
        logical ddc
c*******************************************
      PARAMETER (NWORD1=128)
      COMMON/MESH/MIQX,MIQY,MIQZ,MNX1,MNY1,MNZ1,NX1,NY1,NZ1,JDIMX,JDIMY,
     1 MDUM,MWORD1,MWORD2,JBB(50)
      COMMON/EARTH/RAYL,TIME,NSTEP,EPS,UMAX,VMAX,WMAX,UVWMAX,EKTOT,
     1 VELMA,DT(2),FND,IHEAT,FTOP,FBOT,AVBOX,TMOM,ROTX,ROTY,IRG,
     2 dxp,dyp,IDUMN(41)

c*******************************************
       common/doof/idoof

      dimension a(1),b(1)
      dimension ja(1),jb(1)
      real temp(1), ax(1), ay(1)

      equivalence (ja(1),miqx), (jb(1),rayl)
c     equivalence (a(1),temp(1)), (b(1),ax(1))

c----- new ------------------------
#ifdef HAS_F_MALLOC
	real xta(1)
	pointer (pxta,xta)
#ifdef F90
        real, pointer :: xta(:)
#endif
#else
        real xta(256*256*64)
#endif
c----------------------------------       
        TIME = xtime
        NSTEP = kstep
        RAYL = xrayl
        dt(1) = xdt
        dt(2) = xdt

      WRITE(0,10116)RAYL,TIME,NSTEP

10116 FORMAT(' Rayleigh number =',G12.6,/,' Time            =',
     1G12.6,/,' Nstep           =',I8,/)
C

        
        acc='r'
        MIQX = int(log10(real(numx))/log10(2.))
        MIQY = int(log10(real(numy))/log10(2.))
        MIQZ = int(log10(real(numz))/log10(2.))
        MNX1 =numx
        MNY1 =numy
        MNZ1 =numz
        NX1 =numx-1
        Ny1 =numy-1
        Nz1 =numz-1
        JDIMX = 2**(MIQX-1)+1
        JDIMY = 2**(MIQY-1)+1
        MDUM  = 2**(MIQZ-1)+1
c**************************** ****************
#ifdef HAS_F_MALLOC
        pxta = malloc(4*(numx+1)*(numy+1)*(numz+1) )
#endif
#ifdef F90
        allocate (xta((numx+1)*(numy+1)*(numz+1)))
#endif
c...maybe x * z .... ??? 
      nword2=NZ1*NY1

      MWORD1 = nword1
      MWORD2 = nword2
      nrec=numx*2
      nsize1=nword1/2
      nsize2=numy*numz
      lout = 973

      OPEN(LOUT,FILE=filename,FORM='UNFORMATTED')

      write(LOUT)(ja(i),i=1,nsize1),(jb(i),i=1,nsize1)


       do igit=1,4

       icount = 0
       do ix=1, numx
        do iz=1, numz
         do iy=1, numy
         icount = icount +1
         if(igit.eq.1) 
     &     xta(icount) = temp(ix + (iy-1)*numx + (iz-1)*numx*numy)
         if(igit.eq.3) 
     &     xta(icount) = ax(ix + (iy-1)*numx + (iz-1)*numx*numy)
         if(igit.eq.4) 
     &     xta(icount) = ay(ix + (iy-1)*numx + (iz-1)*numx*numy)
         enddo
        enddo
       enddo
c.... two temp fields
      do 250 kin=1,nrec/2
      ind1=(kin-1)*nsize2 + 1
      ind2=kin*nsize2
      write(LOUT)(xta(i),i=ind1,ind2)
  250 continue
      enddo

      write(*,10333)ldump,nsize1,nsize2,nrec
10333 format(' solution written to unit',i5,' with nsize1 =',
     1i4,', nsize2 =',i5,', nrec =',i4)


#ifdef HAS_F_MALLOC
        call free(pxta)
#elif F90
        deallocate (xta)
#endif

      return
      end

