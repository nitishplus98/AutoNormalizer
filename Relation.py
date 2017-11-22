import re
import copy
import time
class Relations:
	def __init__(self):
		file=open("input/schema.txt","r")
		self.relations_dict={}
		str=file.readlines()
		for s in str:
			stri=re.findall(r"[\w']+",s)
			#print(type(s))
			self.relations_dict[stri[0]]=Relation(s)


class Constraints:
	def __init__(self,name,isPKA=False,isNULL=False,isFK=False,isPPKA=False):
		self.name=name
		self.isPKA = isPKA
		self.isNULL = isNULL
		self.isFK = isFK
		self.isPPKA=isPPKA

	

class Relation:

	def __init__(self,s=None,pkey=None,list_of_attributes=None,relation_obj=None,rname=None):
		if(s is None):
			str=[]
			str.append(rname)
			ppkeys=pkey.split("&")
			for x in list_of_attributes:
				#print(x)
				lis=x.split("&")
				for y in relation_obj.relation:
					for z in lis:
						if(z==y.name):
							if (z in ppkeys)&('&' in pkey):
								ok=[y.name,'False',y.isNULL,y.isFK,'True']
								str.extend(ok)
								#print(z+"uyeur")
							elif(z in ppkeys)&('&' not in pkey):
								ok=[y.name,'True',y.isNULL,y.isFK,'False']
								str.extend(ok)
								#print(z+"rtgye") 
							else:
								ok=[y.name,'False',y.isNULL,y.isFK,'False']
								str.extend(ok)
			#print(str)
			#print("abracadabra")					


		else:
			str=re.findall(r"[\w']+",s)	

		self.relation=[]
		self.no=0
		self.ppka=0
		self.super_keys=[]
		self.fd_dict={}
		x=1
		s=None
		while x<=len(str)-5:
			attribute=Constraints(str[x],str[x+1],str[x+2],str[x+3],str[x+4])
			if(str[x+4]=='True'):
				self.ppka=self.ppka+1
				if(self.ppka==1):
					s=str[x]
				else:
					s=s+"&"+str[x]
			if(str[x+1]=='True'):
				self.super_keys.append(str[x])			
			self.relation.append(attribute)
			self.no=self.no+1
			x=x+5
		#print("hello")	
		#print(self.super_keys)	
		if(s is not None):
			self.super_keys.append(s)

	def set_super_keys(self,s):
		if s not in self.super_keys:
			#print("super key"+s)
			self.super_keys.append(s)

	def _set_fds_(self,rname,notvalid_dict=None):
		#self.fd_dict=fd_dict
		if notvalid_dict is None:
			fd_file=open("input/fd2.txt","r")			
			self.fd_dict[rname]={}
			fds=fd_file.readlines()
			str=[]
			for s in fds:
				str.extend(s.split(";"))
			for s in str:
				a,b=s.split("->")
				a=a[1:len(a)-1]
				ls=[]
				ls.extend(a.split("&"))
				ls = sorted(ls)
				a=""
				a='&'.join(ls)
				b=b[1:len(b)-1]
				c=[]
				c=b.split(",")
				ls=[]
				ls.extend(a.split("&"))
				temp=[]
				for ele in c:
					if(ele not in ls):
						temp.append(ele)
				if(a in self.fd_dict[rname] and len(self.fd_dict[rname][a])>0):
					ls = self.fd_dict[rname][a]
					if(len(temp)>0):
						for ele in temp:
							if(ele not in ls):
								ls.append(ele)
					temp = ls
				if(len(temp)>0):
					self.fd_dict[rname][a]=temp
				#print(a,self.fd_dict[rname][a])
		else:
			self.fd_dict[rname]={}
			self.fd_dict[rname].update(notvalid_dict)	

	def _set_composite(self,relations,rname):
		
		for item in relations.relations_dict:
			if(item==rname):
				if len(relations.relations_dict[item].fd_dict[item].keys())==0:
					str=""
					ct=0
					for attr in relations.relations_dict[item].relation:
						if(ct!=0):
							str=str+'&'+attr.name
						else:
							str=attr.name
						ct=ct+1
					relations.relations_dict[rname].super_keys = []	
					relations.relations_dict[rname].set_super_keys(str)
				for fd in relations.relations_dict[item].fd_dict[rname]:
					attr=[]
					attr.extend(fd.split("&"))
					if(len(attr)+len(relations.relations_dict[item].fd_dict[rname][fd])==relations.relations_dict[rname].no):
						str=""
						str='&'.join(attr)
						#print(str,attr)
						relations.relations_dict[rname].set_super_keys(str)
					#print(fds.fd_dict[fd])




class check_NF:
	def __init__(self,rname,relations):
		#self.fds=fds
		self.relations=copy.deepcopy(relations)
		self.relations.relations_dict[rname]._set_composite(self.relations,rname)
		self.notvalid={}
		self.rname=rname

	def getNF_fd(self,fd):
		vkeys=[]
		for key in self.relations.relations_dict[self.rname].super_keys:
			vkeys.extend(key.split("&"))
		k=0
		c=0
		cnf=4
		for item in self.relations.relations_dict:
			if(item==self.rname):
				for key in self.relations.relations_dict[self.rname].super_keys:
					pkeys=key.split("&")
					fdkeys=fd.split("&")
					if(fd==key or set(pkeys).issubset(set(fdkeys))):
						cnf = min(cnf,4)

					elif(set(fdkeys).issubset(set(pkeys))):
						for ele in self.relations.relations_dict[self.rname].fd_dict[self.rname][fd]:
							if ele not in vkeys:
								self.notvalid[fd].append(ele)
								cnf = min(cnf,1)
						cnf = min(cnf,3)
						self.notvalid[fd].append(ele)

					else:
						for ele in self.relations.relations_dict[self.rname].fd_dict[self.rname][fd]:
							if ele not in vkeys:
								self.notvalid[fd].append(ele)
								cnf = min(cnf,2)
						cnf=min(cnf,3)
						self.notvalid[fd].append(ele)
			'''if len(self.notvalid[fd])==0:
				self.notvalid.pop(fd)'''			
		return cnf

	
	def check_2nf(self):
		vkeys=[]
		#print(self.relations.relations_dict[self.rname].super_keys)
		#print("fhuer")
		for key in self.relations.relations_dict[self.rname].super_keys:
			print("super key:"+key)
			vkeys.extend(key.split("&"))  #list of keys.
		k=0
		c=0
		for item in self.relations.relations_dict:
			if(item==self.rname):
				for fd in self.relations.relations_dict[item].fd_dict[self.rname]:
					if item not in self.notvalid.keys():
						self.notvalid[item] = {}
					self.notvalid[item][fd]=[]
					for key in self.relations.relations_dict[self.rname].super_keys:
						pkeys=key.split("&")
						fdkeys=fd.split("&")			
						if(fd==key):
							k=1			
						elif set(fdkeys).issubset((set(pkeys))):
							for x in self.relations.relations_dict[item].fd_dict[self.rname][fd]:
								if x not in vkeys:
									if x not in self.notvalid[item][fd]:
										self.notvalid[item][fd].append(x)
									#print(x+" gh ")
									k=0
									c+=1							
						else:
							k=1
					if len(self.notvalid[item][fd])==0:
						self.notvalid[item].pop(fd)		
		'''for x in self.notvalid:
			if len(self.notvalid[x])==0:
				self.notvalid.pop(x)'''					
		if(c>0):
			return False
		else:
			return True				

	def check_3nf(self):
		
		vkeys=[]
		for key in self.relations.relations_dict[self.rname].super_keys:
			vkeys.extend(key.split("&"))
			#print(vkeys)
		k=0
		c=0
		invalid_list={}
		for item in self.relations.relations_dict:
			if(item==self.rname):
				for fd in self.relations.relations_dict[item].fd_dict[self.rname]:
					if(item not in invalid_list.keys()):
						invalid_list[item]={}
					invalid_list[item][fd]=[]	
					for key in self.relations.relations_dict[self.rname].super_keys:
						pkeys=key.split("&")
						fdkeys=fd.split("&")
						if(fd==key):
							k=1
						elif set(fdkeys).issubset(set(pkeys)):
							k=1
						else:
							for x in self.relations.relations_dict[item].fd_dict[self.rname][fd]:
								if x in vkeys:
									k=1
								else:
									#print(fd+" "+x)
									if x not in invalid_list[item][fd]:
										invalid_list[item][fd].append(x)
									k=0
									c+=1
					if len(invalid_list[item][fd])==0:
						invalid_list[item].pop(fd)
		for item in self.relations.relations_dict:
			for key in invalid_list[item]:
				if key not in self.notvalid[item].keys():
					self.notvalid[item][key]=copy.deepcopy(invalid_list[item][key])
				else:
					self.notvalid[item][key].extend(invalid_list[item][key])

		if(c>0):
			return False
		else:
			return True	

										




	def check_bcnf(self):
		c=0
		#print(self.relations.relations_dict.keys())
		for item in self.relations.relations_dict:
			#print(self.relations.relations_dict[item].fd_dict[self.rname])
			for fd in self.relations.relations_dict[item].fd_dict[item]:
				if fd not in self.relations.relations_dict[item].super_keys:
					for x in self.relations.relations_dict[item].fd_dict[item][fd]:
						if item not in self.notvalid.keys():
							self.notvalid[item]={}
						if fd not in self.notvalid[item].keys():
							self.notvalid[item][fd]=[]
						if x not in self.notvalid[item][fd]:
							self.notvalid[item][fd].append(x)
						c+=1
			# if item in self.notvalid.keys():
			# 	print("not", end=" ")
			# 	print(item,self.notvalid[item])
			'''if len(self.notvalid[fd])==0:
				self.notvalid.pop(fd)'''
		#print(self.notvalid)				
		if(c>0):
			return False
		else:
			return True

	def get_nf(self):
		if(self.check_2nf()==False):
			return "1NF"
		elif(self.check_3nf()==False):
			return "2NF"
		elif(self.check_bcnf()==False):
			return "3NF"
		return "BCNF"
						
	def check_each_fd(self):
		thnf = 4
		for fd in self.relations.relations_dict[self.rname].fd_dict[self.rname]:
			print(fd,self.relations.relations_dict[self.rname].fd_dict[self.rname][fd], end=" ")
			print(self.getNF_fd(fd))
			print()
			thnf = min(self.getNF_fd(fd),thnf)
		return thnf

		
	def oneNF_to_2NF_3NF(self):
		for key in self.relations.relations_dict:
			l=len(self.relations.relations_dict.keys())			
			for x in self.notvalid[key]:				
				list_of_attribute=[]
				lol=[]
				if '&' in x:
					lol.extend(x.split("&"))
					list_of_attribute.extend(lol)
				else:
					list_of_attribute.append(x)
				list_of_attribute.extend(self.notvalid[key][x])		
				l+=1	
				strin=key+str(l)
				print("lstofatr")
				print(list_of_attribute)
				print(x)
				self.relations.relations_dict[strin]=Relation(rname=strin,list_of_attributes=list_of_attribute,relation_obj=self.relations.relations_dict[key],pkey=x)
				for y in self.notvalid[key][x]:
					for z in self.relations.relations_dict[key].relation:
						if(z.name==y):
							self.relations.relations_dict[key].relation.remove(z)

				for x1 in self.relations.relations_dict[key].relation:
					x1.isPKA=False
					x1.isPPKA=False

				#fds1=functional_dependencies(strin,self.notvalid[key])
				keylo={}
				keylo[x]=self.notvalid[key][x]
				self.relations.relations_dict[strin]._set_fds_(strin,keylo)
				#print("strin:"+strin)
				#nf=check_NF(strin,self.relations)
				#print(nf.check_2nf())
			break
		#fds=functional_dependencies(key)
		for a in self.notvalid[self.rname]:
			#print("a:"+a)
			for b in self.notvalid[self.rname][a]:
				for fd in self.relations.relations_dict[key].fd_dict[key]:
					#print(self.relations.relations_dict[key].fd_dict[key][fd])
					#print("notvalid[a]:"+b)
					if b in self.relations.relations_dict[key].fd_dict[key][fd]:
						self.relations.relations_dict[key].fd_dict[key][fd].remove(b)
						#print("fd:"+fd)		
		self.relations.relations_dict[key].fd_dict[key]={k:v for k,v in self.relations.relations_dict[key].fd_dict[key].items() if not len(v)==0}			
		#nf1=check_NF(key,self.relations)
		#print(nf1.check_2nf())

	"""
	Precondition: The Relational Schema at least satisfies the third normal form.
	"""
	def threeNF_to_BCNF(self):
		self.notvalid={}
		self.check_bcnf()
		#print("hdhd")
		#print(self.relations.relations_dict.keys(),self.notvalid.keys(), self.notvalid["test"])
		# print("here\n\n")
		# print(self.notvalid.keys())
		l=len(self.relations.relations_dict.keys())
		i=0
		klist = list(self.relations.relations_dict.keys())
		#print(klist)
		size = len(klist)
		while i < size:
			if klist[i] in self.notvalid.keys():	
				for x in self.notvalid[klist[i]]:				
					list_of_attribute=[]
					lol=[]
					if '&' in x:
						lol.extend(x.split("&"))
						list_of_attribute.extend(lol)
					else:
						list_of_attribute.append(x)
					list_of_attribute.extend(self.notvalid[klist[i]][x])	
					l+=1
					strin=klist[i]+str(l)
					#print("idhar",x,self.notvalid[klist[i]],end=" ")
					self.relations.relations_dict[strin]=Relation(rname=strin,list_of_attributes=list_of_attribute,relation_obj=self.relations.relations_dict[klist[i]],pkey=x)
					for y in self.notvalid[klist[i]][x]:
						if '&' in x:
							lk=x.split('&')
							if y not in lk:
								for z in self.relations.relations_dict[klist[i]].relation:
									if(z.name==y):
										self.relations.relations_dict[klist[i]].relation.remove(z)
						else:
							if x!=y:
								for z in self.relations.relations_dict[klist[i]].relation:
									#print("idhar",x,y,klist[i],z.name)
									if(z.name==y):
										self.relations.relations_dict[klist[i]].relation.remove(z)

					for x1 in self.relations.relations_dict[klist[i]].relation:
						x1.isPKA=False
						x1.isPPKA=False			
					keylo={}
					keylo[x]=self.notvalid[klist[i]][x]
					#print(klist[i],self.notvalid[klist[i]])
					self.relations.relations_dict[strin]._set_fds_(strin,keylo)				
					
				#break
				#print("hello")
				for fd in self.relations.relations_dict[klist[i]].fd_dict[klist[i]]:
					k=0
					print(fd)
					if '&' in fd:
						l=fd.split('&')
						for c in l:
							mn=0
							for x in self.relations.relations_dict[klist[i]].relation:
								if (c==x.name):
									mn=1
							if(mn==0):
								k=1		
								break
						if(k==1):
							del self.relations.relations_dict[klist[i]].fd_dict[klist[i]][fd][:]
					else:
						mn=0
						for x in self.relations.relations_dict[klist[i]].relation:
							if (fd==x.name):
								mn=1
						if(mn==0):
							del self.relations.relations_dict[klist[i]].fd_dict[klist[i]][fd][:]		
					for y in self.relations.relations_dict[klist[i]].fd_dict[klist[i]][fd]:
						mn=0
						for x in self.relations.relations_dict[klist[i]].relation:
							if(y==x.name):
								mn=1
						if(mn==0):
							del self.relations.relations_dict[klist[i]].fd_dict[klist[i]][fd][:]
			self.relations.relations_dict[klist[i]].fd_dict[klist[i]]={k:v for k,v in self.relations.relations_dict[klist[i]].fd_dict[klist[i]].items() if not len(v)==0}	
			i=i+1			






#fds=functional_dependencies(key)
relations=Relations()
relations.relations_dict["test"]._set_fds_("test")
print("Initial dependencies")
#print(relations.relations_dict["test"].fd_dict["test"])
nf=check_NF("test",relations)
pfds = copy.deepcopy(nf.relations.relations_dict["test"].fd_dict["test"])
print(pfds)
print(nf.check_2nf())
print(nf.check_3nf())
print(nf.notvalid)
#print(nf.check_bcnf())
#print(nf.get_nf())
#print(nf.check_each_fd())
nf2=None
for a in nf.notvalid:
	print(a+"->[",end=" ")
	for x in nf.notvalid[a]:
		print(x,end=" ")
	print("]")	
if not nf.check_2nf():
	nf.oneNF_to_2NF_3NF()
	# for x in relations.relations_dict:
	# 	nf2=check_NF(x,relations)
	# 	if not nf2.check_3nf():
	# 		nf2.oneNF_to_2NF_3NF()
elif not nf.check_3nf():
	nf.oneNF_to_2NF_3NF()


for x in relations.relations_dict:
	print(relations.relations_dict[x].fd_dict[x])
	print(x+":",end=" ")
	nf1=check_NF(x,relations)
	print(nf1.check_2nf())
	print(nf1.check_3nf())
	#print(nf1.check_bcnf())
	#print(nf1.get_nf())
	#print(nf1.check_each_fd()
	#print(str(nf.relations.relations_dict.keys()))	

print("Decomposed relations")
for ele in nf.relations.relations_dict.keys():
	print(nf.relations.relations_dict[ele].fd_dict)
	print(nf.relations.relations_dict[ele].super_keys)
	for element in nf.relations.relations_dict[ele].relation:
		print(element.name,end=" ")
	print()




class Decomposition_Properties:
	def __init__(self,relations,pfd_dict):
		self.relations = copy.deepcopy(relations)
		self.pfd_dict = copy.deepcopy(pfd_dict)



	"""
	Computes the closure of a list of functional dependencies, by using Armstrong's inference rules repeatatively.

	@param: list of functional dependencies.
	@return value: Closure of fd list
	"""
	def getClosure(self,fds):
		cdict={}
		tlist=[]
		#print(fds)
		for ele in fds.keys():
			if ele in cdict:
				tlist = fds[ele]
				#print(tlist)
				tlist.extend(cdict[ele])
				tlist = list(set(tlist))
				cdict[ele]=tlist
			else:
				cdict[ele]=fds[ele]

		#print(cdict)

		klist = sorted(set(cdict.keys()));
		for key in klist:
			tlist = cdict[key]
			ksplit = []
			ksplit.extend(key.split("&"))
			for ele in klist:
				if(ele!=key):
					elist=[]
					elist.extend(ele.split("&"))
					flag=True
					for val in elist:
						if(val not in ksplit):
							flag=False
							break
					if(flag==True):
						tlist.extend(cdict[ele])
			tlist = list(set(tlist))
			cdict[key]=tlist

			for ele in klist:
				if(ele!=key):
					elist=[]
					elist.extend(ele.split("&"))
					#print(elist)
					flag=True
					for val in elist:
						if(val not in tlist):
							flag=False
							break
					if(flag==True):
						tlist.extend(cdict[ele])

			tlist = list(set(tlist))
			cdict[key]=tlist
		return cdict

	# fd_dict={}
	# fd_dict['a']=["b"]
	# fd_dict['b']=["c"]
	# fd_dict['c']=["d"]

	# obj = Decomposition_Properties(nf.relations,None)
	# print(obj.getClosure(fd_dict))


	"""
	Finds out if the given relational decomposition is dependency preserving.
	"""
	def dependency_preserving_after(self):
		self.pfd_dict = self.getClosure(self.pfd_dict)
		global_dict={}
		print("each case")
		tlist=[]
		for key in self.relations.relations_dict.keys():
			lfds = self.getClosure(self.relations.relations_dict[key].fd_dict[key])
			print(lfds)
			for ele in lfds:
				if ele in global_dict:
					tlist = global_dict[ele]
					tlist.append(lfds[ele])
					tlist = list(set(tlist))
					global_dict[ele]=tlist

				else:
					global_dict[ele]=lfds[ele]

		print("global")
		global_dict = self.getClosure(global_dict)
		print(global_dict)
		print(self.pfd_dict)
		#print(cmp(self.pfd_dict,global_dict))
		for key in self.pfd_dict:
			if(key not in global_dict):
				return False
			else:
				l1 = copy.deepcopy(self.pfd_dict[key])
				l2 = global_dict[key]
				if(len(l1)!=len(l2)):
					return False
				l1 = sorted(l1)
				l2 = sorted(l2)
				for i in range(len(l1)):
					if(l1[i]!=l2[i]):
						return False
		return True


	def lossless_join_before(self):
		self.pfd_dict = self.getClosure(self.pfd_dict)
		alist = []
		adict={}
		tlist=[]
		for key in self.relations.relations_dict.keys():
			tlist=[]
			for ele in self.relations.relations_dict[key].relation:
				alist.append(ele.name)
				tlist.append(ele.name)
			adict[key]=set(tlist)

		alist = list(sorted(set(alist)))
		klist = sorted(self.relations.relations_dict.keys())
		mats=[]
		print(alist)
		for key in klist:
			row=[]
			for ele in alist:
				if ele in adict[key]:
					row.append(1)
				else:
					row.append(0)
			mats.append(row)
		
		chp = True
		pfd_list=[]
		for key in self.pfd_dict:
			kl = []
			kl.extend(key.split("&"))
			print(kl)
			for i in range(len(kl)):
				kl[i] = alist.index(kl[i])

			for ele in self.pfd_dict[key]:
				ti = alist.index(ele)
				if ti not in kl:
					pfd_list.append((kl,alist.index(ele)))

		print(pfd_list)
		print(mats)
		#print("Idhar")
		while(chp==True):
			chp=False
			for ele in pfd_list:
				rind=[]
				#print(ele)
				for j in range(len(mats)):
					allone=True
					for i in range(len(ele[0])):
						if(mats[j][ele[0][i]]==0):
							allone=False
							break
					if(allone==True):
						rind.append(j)
				
				sflag = False
				cflag = False
				for j in range(len(rind)):
					if(mats[rind[j]][ele[1]]==1):
						sflag=True
					else:
						cflag=True

				if(cflag and sflag):
					chp = True

				if(sflag==True):
					for j in range(len(rind)):
						mats[rind[j]][ele[1]]=1

			vrow=False
			for row in mats:
				allone=True
				for ele in row:
					if(ele==0):
						allone=False
						break
				if(allone):
					vrow=True
					break

			if(vrow==True):
				break

		ans=False
		for row in mats:
			lflag=True
			for ele in row:
				if(ele==0):
					lflag=False
					break
			if(lflag==True):
				ans=True
				break

		return ans


obj = Decomposition_Properties(nf.relations,pfds)
if(obj.dependency_preserving_after()):
	print("The join is dependency preserving")

else:
	print("Decomposition looses out some fds!")


if(obj.lossless_join_before()):
	print("The decomposition has a lossless join")

else:
	print("Decomposition has a lossy join")

for key in nf.relations.relations_dict:
	print(key,nf.relations.relations_dict[key].fd_dict[key],end=" ")
	for ele in nf.relations.relations_dict[key].relation:
		print(ele.name,end=" ")

print()

print("dictionary")
print(nf.notvalid)
if(nf.check_bcnf()==False):
	print(nf.relations.relations_dict["test"].fd_dict)
	print(nf.notvalid)
	nf.threeNF_to_BCNF()

print("finally")
for key in nf.relations.relations_dict:
	nf.relations.relations_dict[key]._set_composite(relations=nf.relations,rname=key)
	print(key,nf.relations.relations_dict[key].fd_dict[key],end=" ")
	for ele in nf.relations.relations_dict[key].relation:
		print(ele.name,end=" ")
	print()
	print(nf.relations.relations_dict[key].super_keys)
print()