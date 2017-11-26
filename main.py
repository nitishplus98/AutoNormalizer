from Relation import *
from time import sleep
import sys
#fds=functional_dependencies(key)
relations=Relations()
relations.relations_dict["test"]._set_fds_("test")
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
#print(relations.relations_dict["test"].fd_dict["test"])
nf=check_NF("test",relations)

print()
print("----------------------------------------------")
print("Super keys for the relation: ")
print("----------------------------------------------")
print(nf.relations.relations_dict["test"].super_keys)
print()

print("----------------------------------------------")
print("Higest Normal Form Satisfied: "+nf.get_nf())
print("----------------------------------------------")
print()

print("----------------------------------------------")
print("Functional Dependecies not satisfying BCNF: " )
print("----------------------------------------------")
for key in relations.relations_dict.keys():
	print(key,end=": ")
	for a in nf.notvalid[key]:
		print(a+"->[",end=" ")
		for x in nf.notvalid[key][a]:
			print(x,end=" ")
		print("]")
	print()
print()

pfds = copy.deepcopy(nf.relations.relations_dict["test"].fd_dict["test"])
flag = None
if not nf.check_2nf():
	nf.oneNF_to_2NF_3NF()
	flag = True
# elif not nf.check_3nf():
# 	nf.oneNF_to_2NF_3NF()
# 	flag = True

if(flag):
	print("----------------------------------------------")
	i=0
	print("Converting to 3NF", end=" ")
	while i<=5:
		sys.stdout.flush()
		sleep(0.08)
		print(".",end="")
		i=i+1
	print("",end=" ")
	print("done")
	print("----------------------------------------------")
	print("Relational Schema: ")
	for key in nf.relations.relations_dict.keys():
		print(key,end=" =	R(")
		i=0
		for element in nf.relations.relations_dict[key].relation:
			if(i==0):
				print(element.name,end="")
			else:
				print(", "+element.name,end="")
			i=i+1
		print(")")
	print()
	print("Functional Dependencies:")
	for key in nf.relations.relations_dict.keys():
		print(key,end=" : ")
		for kv in nf.relations.relations_dict[key].fd_dict[key]:
			print(kv+" ---> "+str(nf.relations.relations_dict[key].fd_dict[key][kv]), end="; ")
		print()
	print()

	obj = Decomposition_Properties(nf.relations,pfds)
	obj = Decomposition_Properties(nf.relations,pfds)
	print("----------------------------------------------")
	print("F-closure for the original relation: " )
	print("----------------------------------------------")
	clos = obj.getClosure(pfds)
	for kv in clos:
		print(kv+" ---> "+str(clos[kv]))

	print()






# for x in relations.relations_dict:
# 	print(relations.relations_dict[x].fd_dict[x])
# 	print(x+":",end=" ")
# 	nf1=check_NF(x,relations)
# 	print(nf1.check_2nf())
# 	print(nf1.check_3nf())
# 	#print(nf1.check_bcnf())
# 	#print(nf1.get_nf())
# 	#print(nf1.check_each_fd()
# 	#print(str(nf.relations.relations_dict.keys()))	

# print("Decomposed relations")
# for ele in nf.relations.relations_dict.keys():
# 	print(nf.relations.relations_dict[ele].fd_dict)
# 	print(nf.relations.relations_dict[ele].super_keys)
# 	for element in nf.relations.relations_dict[ele].relation:
# 		print(element.name,end=" ")
# 	print()


# obj = Decomposition_Properties(nf.relations,pfds)
# if(obj.dependency_preserving_after()):
# 	print("The join is dependency preserving")

# else:
# 	print("Decomposition looses out some fds!")


# if(obj.lossless_join_before()):
# 	print("The decomposition has a lossless join")

# else:
# 	print("Decomposition has a lossy join")

# for key in nf.relations.relations_dict:
# 	print(key,nf.relations.relations_dict[key].fd_dict[key],end=" ")
# 	for ele in nf.relations.relations_dict[key].relation:
# 		print(ele.name,end=" ")

# print()

# print("dictionary")
# print(nf.notvalid)
# if(nf.check_bcnf()==False):
# 	print(nf.relations.relations_dict["test"].fd_dict)
# 	print(nf.notvalid)
# 	nf.threeNF_to_BCNF()

# print("finally")
# for key in nf.relations.relations_dict:
# 	nf.relations.relations_dict[key]._set_composite(relations=nf.relations,rname=key)
# 	print(key,nf.relations.relations_dict[key].fd_dict[key],end=" ")
# 	for ele in nf.relations.relations_dict[key].relation:
# 		print(ele.name,end=" ")
# 	print()
# 	print(nf.relations.relations_dict[key].super_keys)
# print()