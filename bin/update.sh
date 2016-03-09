#!/bin/bash

cd "`dirname $0`"

./create_index_file.py "`pwd`"

echo "
<html>
  <head>
    <meta http-equiv=refresh content='0; url=overview' />
  </head>
  <body>
    <h1><a href=\"overview\">overview</a></h1>
  </body>
</html>
" > ../web/offline-materials/index.html

cd ../web

mkdir -p files
cd files

# CoderDojo logo from https://coderdojo.com/
[ -f logo.png ] || wget https://coderdojo.com/wp-content/themes/coderdojo/images/logo.png

[ -f favicon.ico ] || wget https://coderdojo.com/favicon.ico

cd .. # web
