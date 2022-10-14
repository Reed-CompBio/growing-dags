To build from k=100 to k=200:

```
python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-G0 ../../data/prepare-G0/pathlinker_round2/ ../../output/pathlinker-G0_round2/ round2_c1.bash -c 1

python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-G0 ../../data/prepare-G0/pathlinker_round2/ ../../output/pathlinker-G0_round2/ round2_c2.bash -c 2

cat round2_c1.bash round2_c2.bash > round2.bash
bash round2.bash
```

To stitch together:

```
python stitch.py ../../output/pathlinker-G0/ ../../output/pathlinker-G0_round2/ ../../output/pathlinker-stitched/
```
