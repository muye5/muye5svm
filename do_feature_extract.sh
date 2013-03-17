#!/bin/bash
if [ ! -d "./chi/" ]
then
    mkdir "./chi/"
fi

./feature_extract.py ./C000008/ ./chi/8.txt stop_word.txt &
./feature_extract.py ./C000010/ ./chi/10.txt stop_word.txt &
./feature_extract.py ./C000013/ ./chi/13.txt stop_word.txt &
./feature_extract.py ./C000014/ ./chi/14.txt stop_word.txt &
./feature_extract.py ./C000016/ ./chi/16.txt stop_word.txt &
./feature_extract.py ./C000020/ ./chi/20.txt stop_word.txt &
./feature_extract.py ./C000022/ ./chi/22.txt stop_word.txt &
./feature_extract.py ./C000023/ ./chi/23.txt stop_word.txt &
./feature_extract.py ./C000024/ ./chi/24.txt stop_word.txt &
