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
