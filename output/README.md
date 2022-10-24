```
grep Dijksta pathlinker-G0/*.log | sed 's/:/ /g' | awk '{print $2,$7,1-$2/$7}' > pathlinker-G0/reruns.txt
grep Dijksta ground_truth-G0/*.log | sed 's/:/ /g' | awk '{print $2,$7,1-$2/$7}' > ground_truth-G0/reruns.txt
grep Dijksta omicsintegrator1-G0/*.log | sed 's/:/ /g' | awk '{print $2,$7,1-$2/$7}' > omicsintegrator1-G0/reruns.txt
```

# to copy files from bioinf9 here.
```
scp "aritz@bioinf9.reed.edu:~/2022-GrowingDags/growing-dags/output/pathlinker-G0_round5/*" pathlinker-G0_round5/
```
