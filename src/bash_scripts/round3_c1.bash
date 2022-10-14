echo BCR cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round3//BCR_c1-G0.txt ../../data/netpath/BCR-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round3//BCR_c1_k100.txt > ../../output/pathlinker-G0_round3//BCR_c1_k100.log
echo EGFR1 cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round3//EGFR1_c1-G0.txt ../../data/netpath/EGFR1-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round3//EGFR1_c1_k100.txt > ../../output/pathlinker-G0_round3//EGFR1_c1_k100.log
echo IL1 cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round3//IL1_c1-G0.txt ../../data/netpath/IL1-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round3//IL1_c1_k100.txt > ../../output/pathlinker-G0_round3//IL1_c1_k100.log
echo TCR cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round3//TCR_c1-G0.txt ../../data/netpath/TCR-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round3//TCR_c1_k100.txt > ../../output/pathlinker-G0_round3//TCR_c1_k100.log
echo TGFbetaReceptor cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round3//TGFbetaReceptor_c1-G0.txt ../../data/netpath/TGF_beta_Receptor-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round3//TGFbetaReceptor_c1_k100.txt > ../../output/pathlinker-G0_round3//TGFbetaReceptor_c1_k100.log
echo Wnt cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round3//Wnt_c1-G0.txt ../../data/netpath/Wnt-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round3//Wnt_c1_k100.txt > ../../output/pathlinker-G0_round3//Wnt_c1_k100.log
