class JCrecord;
class JCclass;


class JCrecord {
       public:
            float data(int, int, int);
                  JCrecord(JCclass *parent);
                 ~JCrecord();
            int read_a_record(void);
            int skip_a_record(void);
            float min(void);
            float max(void);
       private:
            int   actuelle;
            float *xdata;
            int magic, niter, xdim, ydim, zdim;
            float mtime, dt;

};

class JCclass {
       friend class JCrecord;
       public:
                 JCclass(char *filename);
                 ~JCclass();
          JCrecord *rec;
          int     read_a_step(void);
          int     skip_step(int);

       private:
          int    xdim, ydim,zdim;
          float  time, dt;
          int    nstep, npde;
          int    magic;
          float  ra, ras, le;
 
          
};

