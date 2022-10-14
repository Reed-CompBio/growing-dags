#DAG C1
python ../precrec/precrec.py ../../output/pathlinker-stitched/IL1_c1_k200.txt ../../data/prepare-G0/pathlinker/IL1-G0.txt ../../data/netpath/IL1-edges.txt ../../output/pathlinker-stitched/precrec/IL1_c1_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/BCR_c1_k200.txt ../../data/prepare-G0/pathlinker/BCR-G0.txt ../../data/netpath/BCR-edges.txt ../../output/pathlinker-stitched/precrec/BCR_c1_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/TGFbetaReceptor_c1_k200.txt ../../data/prepare-G0/pathlinker/TGFbetaReceptor-G0.txt ../../data/netpath/TGF_beta_Receptor-edges.txt ../../output/pathlinker-stitched/precrec/TGFbetaReceptor_c1_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/TCR_c1_k200.txt ../../data/prepare-G0/pathlinker/TCR-G0.txt ../../data/netpath/TCR-edges.txt ../../output/pathlinker-stitched/precrec/TCR_c1_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/EGFR1_c1_k200.txt ../../data/prepare-G0/pathlinker/EGFR1-G0.txt ../../data/netpath/EGFR1-edges.txt ../../output/pathlinker-stitched/precrec/EGFR1_c1_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/Wnt_c1_k200.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-edges.txt ../../output/pathlinker-stitched/precrec/Wnt_c1_k200-pr

# DAG C2
python ../precrec/precrec.py ../../output/pathlinker-stitched/IL1_c2_k200.txt ../../data/prepare-G0/pathlinker/IL1-G0.txt ../../data/netpath/IL1-edges.txt ../../output/pathlinker-stitched/precrec/IL1_c2_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/BCR_c2_k200.txt ../../data/prepare-G0/pathlinker/BCR-G0.txt ../../data/netpath/BCR-edges.txt ../../output/pathlinker-stitched/precrec/BCR_c2_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/TGFbetaReceptor_c2_k200.txt ../../data/prepare-G0/pathlinker/TGFbetaReceptor-G0.txt ../../data/netpath/TGF_beta_Receptor-edges.txt ../../output/pathlinker-stitched/precrec/TGFbetaReceptor_c2_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/TCR_c2_k200.txt ../../data/prepare-G0/pathlinker/TCR-G0.txt ../../data/netpath/TCR-edges.txt ../../output/pathlinker-stitched/precrec/TCR_c2_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/EGFR1_c2_k200.txt ../../data/prepare-G0/pathlinker/EGFR1-G0.txt ../../data/netpath/EGFR1-edges.txt ../../output/pathlinker-stitched/precrec/EGFR1_c2_k200-pr
python ../precrec/precrec.py ../../output/pathlinker-stitched/Wnt_c2_k200.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-edges.txt ../../output/pathlinker-stitched/precrec/Wnt_c2_k200-pr

# PathLinker k=100
python ../precrec/precrec.py ../../output/pathlinker/IL1-pathlinker.txt none ../../data/netpath/IL1-edges.txt ../../output/pathlinker/IL1-pathlinker-k200-pr -p -k 200
python ../precrec/precrec.py ../../output/pathlinker/BCR-pathlinker.txt none ../../data/netpath/BCR-edges.txt ../../output/pathlinker/BCR-pathlinker-k200-pr -p -k 200
python ../precrec/precrec.py ../../output/pathlinker/TGFbetaReceptor-pathlinker.txt none ../../data/netpath/TGF_beta_Receptor-edges.txt ../../output/pathlinker/TGFbetaReceptor-pathlinker-k200-pr -p -k 200
python ../precrec/precrec.py ../../output/pathlinker/TCR-pathlinker.txt none ../../data/netpath/TCR-edges.txt ../../output/pathlinker/TCR-pathlinker-k200-pr -p -k 200
python ../precrec/precrec.py ../../output/pathlinker/EGFR1-pathlinker.txt none ../../data/netpath/EGFR1-edges.txt ../../output/pathlinker/EGFR1-pathlinker-k200-pr -p -k 200
python ../precrec/precrec.py ../../output/pathlinker/Wnt-pathlinker.txt none ../../data/netpath/Wnt-edges.txt ../../output/pathlinker/Wnt-pathlinker-k200-pr -p -k 200

# PathLinker k=1000
python ../precrec/precrec.py ../../output/pathlinker/IL1-pathlinker.txt none ../../data/netpath/IL1-edges.txt ../../output/pathlinker/IL1-pathlinker-k1000-pr -p -k 1000
python ../precrec/precrec.py ../../output/pathlinker/BCR-pathlinker.txt none ../../data/netpath/BCR-edges.txt ../../output/pathlinker/BCR-pathlinker-k1000-pr -p  -k 1000
python ../precrec/precrec.py ../../output/pathlinker/TGFbetaReceptor-pathlinker.txt none ../../data/netpath/TGF_beta_Receptor-edges.txt ../../output/pathlinker/TGFbetaReceptor-pathlinker-k1000-pr -p -k 1000
python ../precrec/precrec.py ../../output/pathlinker/TCR-pathlinker.txt none ../../data/netpath/TCR-edges.txt ../../output/pathlinker/TCR-pathlinker-k1000-pr -p -k 1000
python ../precrec/precrec.py ../../output/pathlinker/EGFR1-pathlinker.txt none ../../data/netpath/EGFR1-edges.txt ../../output/pathlinker/EGFR1-pathlinker-k1000-pr -p -k 1000
python ../precrec/precrec.py ../../output/pathlinker/Wnt-pathlinker.txt none ../../data/netpath/Wnt-edges.txt ../../output/pathlinker/Wnt-pathlinker-k1000-pr -p -k 1000
