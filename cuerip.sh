#/bin/bash

ISOFILE=$(grep FILE "$1" | awk "{ print \$2 }" | tr -d \")
echo $ISOFILE
grep "INDEX" "$1" | awk '{ print $3 }' | python "cuerip.py" "$ISOFILE"