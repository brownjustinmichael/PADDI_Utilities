#include "inout.h"

int icend_(iu)

int *iu;

{
 
  extern FILE *fpo[];

      fseek(fpo[*iu],0,SEEK_END); 

        return(0);

}
/* the c interface */

int icend(int iu)
{
 return(icend_(&iu));
}

