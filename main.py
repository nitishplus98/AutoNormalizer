import sys
sys.path.append("./include/")
import relation

nf=relation.check_NF("test")
print(nf.check_2nf())
print(nf.check_3nf())
print(nf.check_bcnf())
print(nf.get_nf())
print(nf.check_each_fd())
print()
for a in nf.notvalid:
	print(a+"->"+str(nf.notvalid[a]))