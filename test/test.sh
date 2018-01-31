#!/bin/bash
cd test
echo "Test 1"
rm -f Y_N.txt V_K.txt
python3 ../aff3ct_debug_parser.py ./dump_debug_gold.txt --mod Decoder_polar_SC_fast_sys --tsk decode_siho
diff -s Y_N.txt Y_N_gold.txt
diff -s V_K.txt V_K_gold.txt
rm -f Y_N.txt V_K.txt
echo "Test 1 Done."

echo "Test 2"
rm -f Y_N.txt X_N.txt H_N.txt
python3 ../aff3ct_debug_parser.py ./dump_debug_gold2.txt --mod Channel_Rayleigh_LLR --tsk add_noise_wg
diff -s Y_N.txt Y_N_gold2.txt
diff -s X_N.txt X_N_gold2.txt
diff -s H_N.txt H_N_gold2.txt
rm -f Y_N.txt X_N.txt H_N.txt

echo "Test 2 Done."
cd -

