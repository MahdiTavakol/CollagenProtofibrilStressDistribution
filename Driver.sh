#!/bin/bash

#Simulations list
Sims=("1-Series1" "2-Series2" "3-Series3" "4-Series4" "5-Series5")
Scripts=("ProtofibrilStressXZDistribution.py" "ProtofibrilStressYZDistribution.py" "ProtofibrilStressZZDistribution.py")

for folder in "${Sims[@]}"
do
	for script in "${Scripts[@]}"
	do
		cp $script $folder/dump/z-cId/$script
	done
done
 


for sim in "${Sims[@]}"
do
	cd $sim/dump/z-cId
	echo "I am in folder" $sim/dump/z-cId
	for script in "${Scripts[@]}"
	do
		./$script & # To turn off the parallel processing remove the "&" sign!!
	done
	cd ../../../
done
wait #To turn off the parallel processing comment this!!

