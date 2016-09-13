FC            = gfortran
CFLAGS        = -O2 -DF64   -Ijpeg12 -DUSE12B -I.
CFLAGS        = -O2 -DF64   -Ijpeg12 -DUSE12B -I. -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE
CFLAGS        = -O2 -g   -Ijpeg12 -D_GNU_SOURCE  -DUSE12B -I.  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE
CFLAGS        = -O2 -g   -Ijpeg12 -D_GNU_SOURCE  -DUSE12B -I. 
FFLAGS	      =  -32 -DHAS_F_MALLOC
FFLAGS	      =  
#CFLAGS        = -O2 -I../jpeg-6a/ 

DEST	      = ${HOME}/bin

EXTHDRS	      = /usr/include/getopt.h \
		/usr/include/sgidefs.h \
		/usr/include/stdio.h \
		/usr/include/stdlib.h \
		/usr/include/string.h

HDRS	      = inout.h \
		jcmagic.h

LDFLAGS	      =

LIBS	      =
CC            = gcc

LINKER	      = $CC

MAKEFILE      = Makefile

OBJS	      = icback_.o \
		icclose_.o \
		icddopen_.o \
		icread_.o \
		icrinfo_.o \
		icskip_.o \
		icwinfo_.o \
		icdwinfo_.o \
		icddwinfo_.o \
		icwrite_.o \
		icdwrite_.o \
		icddwrite_.o \
		icend_.o \
		iread.o \
		jcback_.o \
		jcclose_.o \
		jcopen_.o \
		jcread_.o \
		jctype_.o \
		jcrinfo_.o \
		jcrinfo2_.o \
		jcskip_.o \
		jcwinfo_.o \
		jcwinfo2_.o \
		jcwrite_.o \
		jcend_.o \
		lread.o \
		rread.o \
		divisions.o \
		icopen_.o \
#               jcclass.o

PRINT	      = pr

PROGRAM	      = a.out

SRCS	      = icback_.c \
		icclose_.c \
		icddopen_.c \
		icread_.c \
		icrinfo_.c \
		icskip_.c \
		icwinfo_.c \
		icdwinfo_.c \
		icddwinfo_.c \
		icwrite_.c \
		icdwrite_.c \
		icddwrite_.c \
		icend_.c \
		iread.f \
		jcback_.c \
		jcclose_.c \
		jcopen_.c \
		jcread_.c \
		jctype_.c \
		jcrinfo_.c \
		jcrinfo2_.c \
		jcskip_.c \
		jcwinfo_.c \
		jcwinfo2_.c \
		jcwrite_.c \
		jcend_.c \
		lread.f \
		rread.f \
		divisions.c \
                icopen_.c \
#               jcclass.cpp

.F.o:
	$(FC)  -c -O2 $*.F


all:		libjc.a libjpeg 

$(PROGRAM):     $(OBJS) $(LIBS) jpeg12/libjpeg.a
		$(LINKER) $(LDFLAGS) $(OBJS) $(LIBS) -o $(PROGRAM)

libjpeg:;	cd jpeg12;./configure CC='gcc -D_GNU_SOURCE  '; make
# libjpeg:;	cd jpeg12;./configure CC='icc -D_GNU_SOURCE  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE'; make

libjc.a:         $(OBJS) $(LIBS)
		ar rv libjc.a $(OBJS)

c2j:		 libjc.a c2j.o libjc.a jpeg12/libjpeg.a
		 ifc -o c2j  c2j.o libjc.a  jpeg12/libjpeg.a

j2c:		 libjc.a j2c.o libjc.a jpeg12/libjpeg.a
		 ifc -o j2c  j2c.o libjc.a  jpeg12/libjpeg.a

greg2j: read_greg.o greg2j.o libjc.a jpeg12/libjpeg.a
		$(FC) $(FFLAGS) -o greg2j greg2j.o read_greg.o  libjc.a jpeg12/libjpeg.a

j2greg: write_greg.o j2greg.o
		$(FC) $(FFLAGS) -o j2greg j2greg.o write_greg.o  libjc.a jpeg12/libjpeg.a

read_greg.o:	read_greg.F
		$(FC) -c $(FFLAGS) read_greg.F

fchange:	fchange.o       fchange_cb.o    fchange_main.o
		$(CC) -o fchange fchange.o   fchange_cb.o  fchange_main.o -lforms -lXpm -lX11 -lm

clean:;		rm -f $(OBJS) *.bak *~ libjc.a; cd jpeg12; make clean

depend:;	mkmf -f $(MAKEFILE) PROGRAM=$(PROGRAM) DEST=$(DEST)

tar:;		cd jpeg12; make clean
		tar cvf jutils.tar Makefile *.c *.cpp *.h *.f *.F jpeg12 man converter/*.[c,h,f,F] 
		gzip -fv jutils.tar

install:	$(PROGRAM)
		install -s $(PROGRAM) $(DEST)

print:;		$(PRINT) $(HDRS) $(SRCS)

program:        $(PROGRAM)

tags:           $(HDRS) $(SRCS); ctags $(HDRS) $(SRCS)

update:		$(DEST)/$(PROGRAM)

$(DEST)/$(PROGRAM): $(SRCS) $(LIBS) $(HDRS) $(EXTHDRS)
		@make -f $(MAKEFILE) DEST=$(DEST) install
###
