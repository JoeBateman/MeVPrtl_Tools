#!/bin/bash
# This script assumes you have set up sbndcode and made an MeVPrtl sample 
INPUT_FILE=$1
INPUT_NAME=$(echo $INPUT_FILE | tr ".root" "\n")
OUTPUT_NAME=${INPUT_NAME}_caf.root

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Input file $INPUT_FILE does not exist."
    exit 1
fi

g4_fcl=standard_g4_sbnd.fcl 
detsim_fcl=standard_detsim_sbnd.fcl
reco1_fcl=standard_reco1_sbnd.fcl
reco2_fcl=standard_reco2_sbnd.fcl
ana_fcl=standard_anatree_sbnd.fcl
caf_fcl=cafmakerjob_sbnd.fcl  

lar -c $g4_fcl -s $INPUT_FILE -o ./temp/g4_$INPUT_FILE
lar -c $detsim_fcl -s ./temp/g4_$INPUT_FILE -o ./temp/detsim_$INPUT_FILE -T ./temp/hists_detsim_$INPUT_FILE
lar -c $reco1_fcl -s ./temp/detsim_$INPUT_FILE -o ./temp/reco1_$INPUT_FILE -T ./temp/hists_reco1_$INPUT_FILE
lar -c $reco2_fcl -s ./temp/reco1_$INPUT_FILE -o ./temp/reco2_$INPUT_FILE -T ./temp/hists_reco2_$INPUT_FILE
# lar -c $ana_fcl -s ./temp/reco2_$INPUT_FILE -T ./temp/ana_$INPUT_FILE
lar -c $caf_fcl -s ./temp/reco2_$INPUT_FILE 

# # Clean up cluttering files
# rm ./temp/*
rm hists*
rm larcv*
rm *.db
rm *.log

# Print the output name
echo "Output saved to: reco2_$INPUT_NAME.caf.root & reco2_$INPUT_NAME.flat.caf.root"