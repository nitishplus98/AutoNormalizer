from Relation import *
from time import sleep
import sys
relations=Relations()
print("----------------------------------------------")
print("Attributes of the relation provided as Input: ")
print("----------------------------------------------")
i=0
for ele in relations.relations_dict["test"].relation:
	if(i==0):
		print(ele.name,end="")
	else:
		print(', '+ele.name,end="")
	i=i+1
print()
print()
print("----------------------------------------------")
print("Given functional dependencies: ")
print("----------------------------------------------")
for key in relations.relations_dict["test"].fd_dict["test"]:
	for value in relations.relations_dict["test"].fd_dict["test"][key]:
		print(key+" ---> "+value)
#nf=check_NF("test",relations)

print()
print("----------------------------------------------")
print("Super keys for the relation: ")
print("----------------------------------------------")
print(relations.relations_dict["test"].super_keys)
print()

print("----------------------------------------------")
print("Higest Normal Form Satisfied: "+relations.relations_dict["test"].get_nf(relations,"test"))
print("----------------------------------------------")
print()

print("----------------------------------------------")
print("Functional Dependecies not satisfying BCNF: " )
print("----------------------------------------------")
for key in relations.relations_dict.keys():
	print(key,end=": ")
	for a in relations.relations_dict[key].notvalid[key]:
		print(a+"->[",end=" ")
		for x in relations.relations_dict[key].notvalid[key][a]:
			print(x,end=" ")
		print("]")
	print()
print()
pfds = copy.deepcopy(relations.relations_dict["test"].fd_dict["test"])
while(True):
	for key in relations.relations_dict.keys():
		if(relations.relations_dict[key].get_nf(relations,key)=="1NF"):
			relations.relations_dict[key].oneNF_to_2NF_3NF(relations,key)
			for ke in relations.relations_dict.keys():
				print("----------------------------------------------")
				print(ke)
				print("----------------------------------------------")
				i=0
				for ele in relations.relations_dict[ke].relation:
					if(i==0):
						print(ele.name,end="")
					else:
						print(', '+ele.name,end="")
					i=i+1
				print()
				print()
				print("----------------------------------------------")
				print("Given functional dependencies: ")
				print("----------------------------------------------")
				for keyp in relations.relations_dict[ke].fd_dict[ke]:
					for value in relations.relations_dict[ke].fd_dict[ke][keyp]:
						print(keyp+" ---> "+value)
#nf=check_NF("test",relations)
	
				print()
				print("----------------------------------------------")
				print("Super keys for the relation: ")
				print("----------------------------------------------")
				print(relations.relations_dict[ke].super_keys)
				print(ke)

				print("----------------------------------------------")
				print("Higest Normal Form Satisfied: "+relations.relations_dict[ke].get_nf(relations,ke))
				print("----------------------------------------------")
				print()
				print()
				print()

			obj = Decomposition_Properties(relations,pfds)
			print("----------------------------------------------")
			print("F-closure for the original relation: " )
			print("----------------------------------------------")
			clos = obj.getClosure(pfds)
			for kv in clos:
				print(kv+" ---> "+str(clos[kv]))

			print()
			print("----------------------------------------------")
			print("Properties of Relational Decomposition: " )
			print("----------------------------------------------")
			print("Dependency preserving: "+str(obj.dependency_preserving_after()))
			print("Lossless join: "+str(obj.lossless_join_before()))	
			break
	for key in relations.relations_dict.keys():
		if(relations.relations_dict[key].get_nf(relations,key)=="2NF"):
			relations.relations_dict[key].oneNF_to_2NF_3NF(relations,key)
			for ke in relations.relations_dict.keys():
				print("----------------------------------------------")
				print(ke)
				print("----------------------------------------------")
				i=0
				for ele in relations.relations_dict[ke].relation:
					if(i==0):
						print(ele.name,end="")
					else:
						print(', '+ele.name,end="")
					i=i+1
				print()
				print()
				print("----------------------------------------------")
				print("Given functional dependencies: ")
				print("----------------------------------------------")
				for keyp in relations.relations_dict[ke].fd_dict[ke]:
					for value in relations.relations_dict[ke].fd_dict[ke][keyp]:
						print(keyp+" ---> "+value)
#nf=check_NF("test",relations)
	
				print()
				print("----------------------------------------------")
				print("Super keys for the relation: ")
				print("----------------------------------------------")
				print(relations.relations_dict[ke].super_keys)
				#print(ke)

				print("----------------------------------------------")
				print("Higest Normal Form Satisfied: "+relations.relations_dict[ke].get_nf(relations,ke))
				print("----------------------------------------------")
				print()
			obj = Decomposition_Properties(relations,pfds)
			print("----------------------------------------------")
			print("F-closure for the original relation: " )
			print("----------------------------------------------")
			clos = obj.getClosure(pfds)
			for kv in clos:
				print(kv+" ---> "+str(clos[kv]))

			print()
			print("----------------------------------------------")
			print("Properties of Relational Decomposition: " )
			print("----------------------------------------------")
			print("Dependency preserving: "+str(obj.dependency_preserving_after()))
			print("Lossless join: "+str(obj.lossless_join_before()))	
			break	
		



	for key in relations.relations_dict.keys():
		if(relations.relations_dict[key].get_nf(relations,key)=="3NF"):
			relations.relations_dict[key].threeNF_to_BCNF(relations)
		#break
			for ke in relations.relations_dict.keys():
				print("----------------------------------------------")
				print(ke)
				print("----------------------------------------------")
				i=0
				for ele in relations.relations_dict[ke].relation:
					if(i==0):
						print(ele.name,end="")
					else:
						print(', '+ele.name,end="")
					i=i+1
				print()
				print()
				print("----------------------------------------------")
				print("Given functional dependencies: ")
				print("----------------------------------------------")
				for keyp in relations.relations_dict[ke].fd_dict[ke]:
					for value in relations.relations_dict[ke].fd_dict[ke][keyp]:
						print(keyp+" ---> "+value)
#nf=check_NF("test",relations)
	
				print()
				print("----------------------------------------------")
				print("Super keys for the relation: ")
				print("----------------------------------------------")
				print(relations.relations_dict[ke].super_keys)
				print()

				print("----------------------------------------------")
				print("Higest Normal Form Satisfied: "+relations.relations_dict[ke].get_nf(relations,ke))
				print("----------------------------------------------")
				print()
			obj = Decomposition_Properties(relations,pfds)
			print("----------------------------------------------")
			print("F-closure for the original relation: " )
			print("----------------------------------------------")
			clos = obj.getClosure(pfds)
			for kv in clos:
				print(kv+" ---> "+str(clos[kv]))

			print()
			print("----------------------------------------------")
			print("Properties of Relational Decomposition: " )
			print("----------------------------------------------")
			print("Dependency preserving: "+str(obj.dependency_preserving_after()))
			print("Lossless join: "+str(obj.lossless_join_before()))
			break
	flag=False
	for key in relations.relations_dict.keys():
		if not (relations.relations_dict[key].get_nf(relations,key)=="BCNF"):
			continue
		else:
			flag=True
	if(flag):
		break

			
