#!/bin/bash
cd test

echo "Test 1..."
rm -f Y_N.txt V_K.txt Y_N.bin V_K.bin
python3 ../aff3ct_debug_parser.py ./dump_debug_gold.txt --mod Decoder_polar_SC_fast_sys --tsk decode_siho
diff -s Y_N.txt Y_N_gold.txt
diff -s V_K.txt V_K_gold.txt
diff -s Y_N.bin Y_N_gold.bin
diff -s V_K.bin V_K_gold.bin
rm -f Y_N.txt V_K.txt Y_N.bin V_K.bin
echo "Test 1 Done."

echo "Test 2..."
rm -f Y_N.txt X_N.txt H_N.txt Y_N.bin X_N.bin H_N.bin
python3 ../aff3ct_debug_parser.py ./dump_debug_gold2.txt --mod Channel_Rayleigh_LLR --tsk add_noise_wg
diff -s Y_N.txt Y_N_gold2.txt
diff -s X_N.txt X_N_gold2.txt
diff -s H_N.txt H_N_gold2.txt
diff -s Y_N.bin Y_N_gold2.bin
diff -s X_N.bin X_N_gold2.bin
diff -s H_N.bin H_N_gold2.bin
rm -f Y_N.txt X_N.txt H_N.txt Y_N.bin X_N.bin H_N.bin
echo "Test 2 Done."

echo "Test 3..."
rm -f Y_N1.txt Y_N2.txt Y_N1.bin Y_N2.bin
python3 ../aff3ct_debug_parser.py ./dump_debug_gold.txt --mod Quantizer_standard --tsk process
diff -s Y_N1.txt Y_N1_gold3.txt
diff -s Y_N1.bin Y_N1_gold3.bin
diff -s Y_N2.txt Y_N2_gold3.txt
diff -s Y_N2.bin Y_N2_gold3.bin
rm -f Y_N1.txt Y_N2.txt Y_N1.bin Y_N2.bin
echo "Test 3 Done."



#Quantizer_standard::process

cd -
