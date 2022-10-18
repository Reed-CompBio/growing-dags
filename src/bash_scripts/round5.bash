echo BCR cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round5//BCR_c1-G0.txt ../../data/netpath/BCR-nodes.txt -k 200 -c 1 -o ../../output/pathlinker-G0_round5//BCR_c1_k200.txt > ../../output/pathlinker-G0_round5//BCR_c1_k200.log &
echo EGFR1 cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round5//EGFR1_c1-G0.txt ../../data/netpath/EGFR1-nodes.txt -k 200 -c 1 -o ../../output/pathlinker-G0_round5//EGFR1_c1_k200.txt > ../../output/pathlinker-G0_round5//EGFR1_c1_k200.log &
echo TCR cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round5//TCR_c1-G0.txt ../../data/netpath/TCR-nodes.txt -k 200 -c 1 -o ../../output/pathlinker-G0_round5//TCR_c1_k200.txt > ../../output/pathlinker-G0_round5//TCR_c1_k200.log &
echo TGFbetaReceptor cost 1
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round5//TGFbetaReceptor_c1-G0.txt ../../data/netpath/TGF_beta_Receptor-nodes.txt -k 200 -c 1 -o ../../output/pathlinker-G0_round5//TGFbetaReceptor_c1_k200.txt > ../../output/pathlinker-G0_round5//TGFbetaReceptor_c1_k200.log &
#cho Wnt cost 1
#python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round5//Wnt_c1-G0.txt ../../data/netpath/Wnt-nodes.txt -k 200 -c 1 -o ../../output/pathlinker-G0_round5//Wnt_c1_k200.txt > ../../output/pathlinker-G0_round5//Wnt_c1_k200.log &
echo EGFR1 cost 2
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round5//EGFR1_c2-G0.txt ../../data/netpath/EGFR1-nodes.txt -k 200 -c 2 -o ../../output/pathlinker-G0_round5//EGFR1_c2_k200.txt > ../../output/pathlinker-G0_round5//EGFR1_c2_k200.log &
echo TGFbetaReceptor cost 2
python3 ../alg/DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker_round5//TGFbetaReceptor_c2-G0.txt ../../data/netpath/TGF_beta_Receptor-nodes.txt -k 200 -c 2 -o ../../output/pathlinker-G0_round5//TGFbetaReceptor_c2_k200.txt > ../../output/pathlinker-G0_round5//TGFbetaReceptor_c2_k200.log &
