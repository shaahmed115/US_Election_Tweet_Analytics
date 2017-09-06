f=open("Feat1_test.txt")
Feat1 = f.read().splitlines()
f=open("Feat2_test.txt")
Feat2=f.read().splitlines()

#f=open("Feat3_test.txt")
#Feat3=f.read().splitlines()

f=open("testing.txt")
classes=f.read().splitlines()

for i in range(0,40):
	s=classes[i]+ ","
	print s,Feat1[i],Feat2[i]
	



#for i in pmi:
#	for j in distance:
#		for k in pos_neg:
#			#final_features.write(k)
#			print k,print j,print i
#			break
			#final_features.write("\t")
#		break
		#final_features.write(j)
		#print j
		#final_features.write("\t")
		#print "\t"
	#final_features.write(i)
	#print i
	#final_features.write("\n"
	#print "\n"
			
			

	
	







