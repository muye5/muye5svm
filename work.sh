#!/bin/bash
cd ./libsvm/

if [ ! -e train3000.scale.model -o ! -e test3000.scale ]
then
    echo "Data Not Exist"
    exit -1
fi

./svm-predict test3000.scale train3000.scale.model 3000_output
mv 3000_output ../
echo "done..."
