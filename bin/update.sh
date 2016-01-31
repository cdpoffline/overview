#!/bin/bash

cd "`dirname $0`"

./create_index_file.py "`pwd`"

echo "
<html>
  <head>
    <meta http-equiv=refresh content='0; url=overview' />
  </head>
  <body>
    <h1><a href="overview">overview</a></h1>
  </body>
</html>
" > ../web/offline-materials/index.html
