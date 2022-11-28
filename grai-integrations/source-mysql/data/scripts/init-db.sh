for f in `find '../schema' -type f -name '*.sql'`
  do
    mysql -u grai -p grai -h localhost grai < $f
 done
