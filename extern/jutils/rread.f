       subroutine rread(text,val)
       character*(*) text
       character*10 cin
       cin='          '
       write(6,'(a,e10.4,a3,$)') text,val,' : '
       call flush(6)
       read(5,'(a10)') cin
       if (cin.ne.'          ') then
	  read(cin,'(e10.4)') val
       endif
       return
       end
