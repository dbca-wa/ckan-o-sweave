#! /bin/bash
grep -rn "\cpr{" ../reports/assets/ | grep -v "%" | grep -v "template | sort -u > ../reports/cpr.txt