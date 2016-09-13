#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <rpc/rpc.h>
#include <jcmagic.h>

#define MAXVAL 65535.
#define MAXVALH 16777215.
#define MAXFILES 25

#define JXDR  1234567

static int debug=0;

/*static int quality=85; */


// single linked list

struct nlist {
             int num;
             struct nlist* next;
};


void freemylist(struct nlist* );
struct nlist * calcdivisions(int , int , int );



