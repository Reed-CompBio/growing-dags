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

## To build from k=200 to k=300:

```
python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-stitched ../../data/prepare-G0/pathlinker_round3/ ../../output/pathlinker-G0_round3/ round3_c1.bash -c 1 -k 200

python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-stitched ../../data/prepare-G0/pathlinker_round3/ ../../output/pathlinker-G0_round3/ round3_c2.bash -c 2 -k 200

cat round3_c1.bash round3_c2.bash > round3.bash
bash round3.bash

python stitch.py ../../output/pathlinker-stitched/ ../../output/pathlinker-G0_round3/ ../../output/pathlinker-stitched_round3/ -k1 200 -k2 100
```

You can comment out the runs that are already satisfied.

## To build from k=300 to k=400:

```
python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-stitched_round3/ ../../data/prepare-G0/pathlinker_round4/ ../../output/pathlinker-G0_round4/ round4_c1.bash -c 1 -k 300

python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-stitched_round3/ ../../data/prepare-G0/pathlinker_round4/ ../../output/pathlinker-G0_round4/ round4_c2.bash -c 2 -k 300

cat round4_c1.bash round4_c2.bash > round4.bash
# comment out irrelevant lines
bash round3.bash

python stitch.py ../../output/pathlinker-stitched_round3/ ../../output/pathlinker-G0_round4/ ../../output/pathlinker-stitched_round4/ -k1 300 -k2 100
```

## To build from k=400 to k=600:

```
python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-stitched_round4/ ../../data/prepare-G0/pathlinker_round5/ ../../output/pathlinker-G0_round5/ round5_c1.bash -c 1 -k 400

python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-stitched_round4/ ../../data/prepare-G0/pathlinker_round5/ ../../output/pathlinker-G0_round5/ round5_c2.bash -c 2 -k 400

cat round5_c1.bash round5_c2.bash > round5.bash
# replace -k100 with -k200
# comment out irrelevant lines
bash round5.bash

python stitch.py ../../output/pathlinker-stitched_round4/ ../../output/pathlinker-G0_round5/ ../../output/pathlinker-stitched_round5/ -k1 400 -k2 200
```

## To build from k=600 to k=1000:

```
python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-stitched_round5/ ../../data/prepare-G0/pathlinker_round6/ ../../output/pathlinker-G0_round6/ round6_c1.bash -c 1 -k 600

python build.py ../../data/prepare-G0/pathlinker ../../output/pathlinker-stitched_round5/ ../../data/prepare-G0/pathlinker_round6/ ../../output/pathlinker-G0_round6/ round6_c2.bash -c 2 -k 600

cat round6_c1.bash round6_c2.bash > round6.bash
# replace -k100 with -k400
# comment out irrelevant lines (TGFb C2)
bash round6.bash

python stitch.py ../../output/pathlinker-stitched_round5/ ../../output/pathlinker-G0_round6/ ../../output/pathlinker-stitched_round6/ -k1 600 -k2 400
```

## Finally, finalize iterations.

```
python finalize_iterations.py
```

Final output files for PL, C1, and C2 reconstructions are in `../../output/pathlinker-final/`.
