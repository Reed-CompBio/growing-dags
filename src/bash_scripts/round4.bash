echo BCR cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//BCR_c1-G0.txt ../../data/netpath/BCR-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round4//BCR_c1_k100.txt > ../../output/pathlinker-G0_round4//BCR_c1_k100.log &
echo EGFR1 cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//EGFR1_c1-G0.txt ../../data/netpath/EGFR1-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round4//EGFR1_c1_k100.txt > ../../output/pathlinker-G0_round4//EGFR1_c1_k100.log &
#echo IL1 cost 1
#python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//IL1_c1-G0.txt ../../data/netpath/IL1-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round4//IL1_c1_k100.txt > ../../output/pathlinker-G0_round4//IL1_c1_k100.log &
echo TCR cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//TCR_c1-G0.txt ../../data/netpath/TCR-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round4//TCR_c1_k100.txt > ../../output/pathlinker-G0_round4//TCR_c1_k100.log &
echo TGFbetaReceptor cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//TGFbetaReceptor_c1-G0.txt ../../data/netpath/TGF_beta_Receptor-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round4//TGFbetaReceptor_c1_k100.txt > ../../output/pathlinker-G0_round4//TGFbetaReceptor_c1_k100.log &
echo Wnt cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//Wnt_c1-G0.txt ../../data/netpath/Wnt-nodes.txt -k 100 -c 1 -o ../../output/pathlinker-G0_round4//Wnt_c1_k100.txt > ../../output/pathlinker-G0_round4//Wnt_c1_k100.log &
#echo BCR cost 2
#python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//BCR_c2-G0.txt ../../data/netpath/BCR-nodes.txt -k 100 -c 2 -o ../../output/pathlinker-G0_round4//BCR_c2_k100.txt > ../../output/pathlinker-G0_round4//BCR_c2_k100.log &
echo EGFR1 cost 2
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//EGFR1_c2-G0.txt ../../data/netpath/EGFR1-nodes.txt -k 100 -c 2 -o ../../output/pathlinker-G0_round4//EGFR1_c2_k100.txt > ../../output/pathlinker-G0_round4//EGFR1_c2_k100.log &
#echo TCR cost 2
#python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//TCR_c2-G0.txt ../../data/netpath/TCR-nodes.txt -k 100 -c 2 -o ../../output/pathlinker-G0_round4//TCR_c2_k100.txt > ../../output/pathlinker-G0_round4//TCR_c2_k100.log &
echo TGFbetaReceptor cost 2
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//TGFbetaReceptor_c2-G0.txt ../../data/netpath/TGF_beta_Receptor-nodes.txt -k 100 -c 2 -o ../../output/pathlinker-G0_round4//TGFbetaReceptor_c2_k100.txt > ../../output/pathlinker-G0_round4//TGFbetaReceptor_c2_k100.log &
#echo Wnt cost 2
#python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round4//Wnt_c2-G0.txt ../../data/netpath/Wnt-nodes.txt -k 100 -c 2 -o ../../output/pathlinker-G0_round4//Wnt_c2_k100.txt > ../../output/pathlinker-G0_round4//Wnt_c2_k100.log &
