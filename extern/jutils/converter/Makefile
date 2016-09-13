CFLAGS	      =
FC		= ifc

DEST	      = .

EXTHDRS	      =

HDRS	      = jcmagic.h

INSTALL	      = cp

LD	      = $(FC)

LDFLAGS	      =

LIBS	      = ../libjc.a ../jpeg12/libjpeg.a

MAKEFILE      = Makefile

OBJS	      = \
		test2.o 

PRINT	      = pr

PROGRAM       = test2

SHELL	      = /bin/sh

SRCS	      = \
		test2.f90


all:		$(PROGRAM)

$(PROGRAM):     $(OBJS)
		@echo "Linking $(PROGRAM) ..."
		@$(LD) $(LDFLAGS) $(OBJS) $(LIBS) -o $(PROGRAM)
		@echo "done"

clean:;		@rm -f $(OBJS) core

clobber:;	@rm -f $(OBJS) $(PROGRAM) core tags

depend:;	@mkmf -f $(MAKEFILE)

echo:;		@echo $(HDRS) $(SRCS)

index:;		@ctags -wx $(HDRS) $(SRCS)

install:	$(PROGRAM)
		@echo Installing $(PROGRAM) in $(DEST)
		@-strip $(PROGRAM)
		@if [ $(DEST) != . ]; then \
		(rm -f $(DEST)/$(PROGRAM); $(INSTALL) $(PROGRAM) $(DEST)); fi

print:;		@$(PRINT) $(HDRS) $(SRCS)

tags:           $(HDRS) $(SRCS); @ctags $(HDRS) $(SRCS)

.f90.o:
	$(FC) $(FFLAGS) $(INCLUDES) -c $*.f90


.SUFFIXES: .o .c .y l .a .sh .f .c~ .y~ .l~ .sh~ .f~ .f90 .cpp .C .c++

