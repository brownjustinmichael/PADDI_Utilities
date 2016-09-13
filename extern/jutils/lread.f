       subroutine lread(text,lval)
       character*(*) text
       character*1 cin
       logical lval
       cin=' '
       write(6,'(a,l1,a3,$)') text,lval,' : '
       call flush(6)
       read(5,'(a1)') cin
       if (cin.ne.' ') then
	  read(cin,'(l1)') lval
       endif
       return
       end
