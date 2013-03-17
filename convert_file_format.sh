#!/bin/bash
if [ $# != 3 ]
then
    echo "Usage: ./convert_file_format.sh dir_name=xxx from_format=xxx to_format=xxx"
    exit -1
fi

eval $*

if [ -z "$dir_name" -o -z "$from_format" -o -z "$to_format" ]
then
    echo "Usage: ./convert_file_format.sh dir_name=xxx from_format=xxx to_format=xxx"
    exit -1
fi

function convert()
{
    target_dir=$1
    files=`echo $target_dir/*`
    for file in $files
    do
        if [ -d $file ]
        then
            convert $file
            continue
        else
            $(iconv -f $from_format -t $to_format -c $file > ${file}"_${to_format}")
        fi
    done
}

if [[ ! -d $dir_name && -f $dir_name ]]
then
    $(iconv -f $from_format -t $to_format -c $dir_name > ${dir_name}"_${to_format}")
else
    convert $dir_name
fi
