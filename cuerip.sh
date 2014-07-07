#/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHONSCRIPT="${DIR}/cuerip.py"
ISOFILENAME=$(grep FILE "$1" | awk "{ print \$2 }" | tr -d \")
ISOFILE="$( dirname $1 )/${ISOFILENAME}"
echo $ISOFILE
grep "INDEX" "$1" | awk '{ print $3 }' | python "${PYTHONSCRIPT}" "${ISOFILE}"