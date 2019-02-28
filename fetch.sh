#!/bin/bash
failues=4
start_index_last=$(cat "./fetch_start.txt")
for i in $(seq 1 100)
do  
    if [ "$failues" -le "0" ];
    then break
    fi
    start_index=$(cat "./fetch_start.txt")
    echo "start_index_last"+$start_index_last
    echo "start_index"+$start_index
    if [ "$start_index" == "$start_index_last" ];
    then
        failues=`expr $failues - 1`
    else
        start_index_last=$start_index
    fi
    python fetch_papers.py --start-index=${start_index} --results-per-iteration=200
    date && sleep 5 && date
done
