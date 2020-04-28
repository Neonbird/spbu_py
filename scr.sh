#!/bin/bash

grep -v "^#" $1 | cut -f 1,4,5 | sort -k1 -nk2,3 | uniq -c | awk '{print $2 "\t" $3"->"$4 "\t" $1}'

