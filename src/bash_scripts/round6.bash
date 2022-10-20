echo BCR cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round6//BCR_c1-G0.txt ../../data/netpath/BCR-nodes.txt -k 400 -c 1 -o ../../output/pathlinker-G0_round6//BCR_c1_k400.txt > ../../output/pathlinker-G0_round6//BCR_c1_k400.log &
echo EGFR1 cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round6//EGFR1_c1-G0.txt ../../data/netpath/EGFR1-nodes.txt -k 400 -c 1 -o ../../output/pathlinker-G0_round6//EGFR1_c1_k400.txt > ../../output/pathlinker-G0_round6//EGFR1_c1_k400.log &
echo TCR cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round6//TCR_c1-G0.txt ../../data/netpath/TCR-nodes.txt -k 400 -c 1 -o ../../output/pathlinker-G0_round6//TCR_c1_k400.txt > ../../output/pathlinker-G0_round6//TCR_c1_k400.log &
echo TGFbetaReceptor cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round6//TGFbetaReceptor_c1-G0.txt ../../data/netpath/TGF_beta_Receptor-nodes.txt -k 400 -c 1 -o ../../output/pathlinker-G0_round6//TGFbetaReceptor_c1_k400.txt > ../../output/pathlinker-G0_round6//TGFbetaReceptor_c1_k400.log &
echo EGFR1 cost 2
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round6//EGFR1_c2-G0.txt ../../data/netpath/EGFR1-nodes.txt -k 400 -c 2 -o ../../output/pathlinker-G0_round6//EGFR1_c2_k400.txt > ../../output/pathlinker-G0_round6//EGFR1_c2_k400.log &
#echo TGFbetaReceptor cost 2
#python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round6//TGFbetaReceptor_c2-G0.txt ../../data/netpath/TGF_beta_Receptor-nodes.txt -k 400 -c 2 -o ../../output/pathlinker-G0_round6//TGFbetaReceptor_c2_k400.txt > ../../output/pathlinker-G0_round6//TGFbetaReceptor_c2_k400.log &
