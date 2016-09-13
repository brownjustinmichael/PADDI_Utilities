# amplitude frequency response
set key
set title "Compression error and file size"
set log y

set xlabel "Compression Factor"
set xrange [0. : 100.0]
set x2range [0. : 100.0]
set ylabel "max/av Error in %"
set y2label "Size of data-file in %"
set ytics nomirror
set y2tics
set tics out
set autoscale  y
set autoscale y2
plot "data" u 1:2  title "av. error"  w lp, "data" u 1:3   title "max. error" w lp,  "data" u 1:5  axes x2y2   title "compression  %", \
    "../../jwutils/converter/data" u 1:2  title "av. error"  w lp, "../../jwutils/converter/data" u 1:3   title "max. error" w lp,  "../../jwutils/converter/data" u 1:5  axes x2y2   title "compression  %"





pause -1 "Hit return to continue"

