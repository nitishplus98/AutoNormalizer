import re
import copy
import time
class Relations:
	def __init__(self):
		file=open("schema3.txt","r")
		self.relations_dict={}
		str=file.readlines()
		for s in str:
			stri=re.findall(r"[\w']+",s)
			#print(type(s))
			self.relations_dict[stri[0]]=Relation(s=s)


class Constraints:
	def __init__(self,name,isPKA=False,isNULL=False,isFK=False,isPPKA=False):
		self.name=name
		self.isPKA = isPKA
		self.isNULL = isNULL
		self.isFK = isFK
		self.isPPKA=isPPKA

	

class Relation:

	def __init__(self,s=None,pkey=None,list_of_attributes=None,relation_obj=None,rname="test"):
		self.notvalid={}
		#rname="test"
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
							elif(z in ppkeys)&('&' not in pkey):
								ok=[y.name,'True',y.isNULL,y.isFK,'False']
								str.extend(ok)
							else:
								ok=[y.name,'False',y.isNULL,y.isFK,'False']
								str.extend(ok)
								


		else:
			str=re.findall(r"[\w']+",s)	
		#print("gshjgfkjebfjh")	
		#print(str)
		self.relation=[]
		self.no=0
		self.ppka=0
		self.super_keys=[]
		self.fd_dict={}
		x=1
		#s=None
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
				#print("super_keys",end=" ")
				#print(self.super_keys)			
			self.relation.append(attribute)
			self.no=self.no+1
			x=x+5
		'''if(s is not None):
			self.super_keys.append(s)'''
		x=1
		if s is not  None:
			fd_file=open("fd3.txt","r")			
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
			item=rname
			if len(self.fd_dict[item].keys())==0:
				str=""
				ct=0
				for attr in self.relation:
					if(ct!=0):
						str=str+'&'+attr.name
					else:
						str=attr.name
					ct=ct+1
				self.super_keys = []	
				if str not in self.super_keys:
					self.super_keys.append(s)
			for fd in self.fd_dict[rname]:
				attr=[]
				attr.extend(fd.split("&"))
				if(len(attr)+len(self.fd_dict[rname][fd])==len(self.relation)):
					str=""
					str='&'.join(attr)
					if str not in self.super_keys:
						self.super_keys.append(str)
	def set_super_keys(self,s):
		if s not in self.super_keys:
			self.super_keys.append(s)

	def _set_fds_(self,rname,notvalid_dict=None):
		self.fd_dict[rname]={}
		self.fd_dict[rname].update(notvalid_dict)
		#_set_composite(rname)		

	def _set_composite(self,rname):
		item=rname
		if len(self.fd_dict[item].keys())==0:
			str=""
			ct=0
			for attr in self.relation:
				if(ct!=0):
					str=str+'&'+attr.name
				else:
					str=attr.name
				ct=ct+1
			self.super_keys = []	
			set_super_keys(str)
		for fd in self.fd_dict[rname]:
			attr=[]
			attr.extend(fd.split("&"))
			if(len(attr)+len(self.fd_dict[rname][fd])==len(self.relation)):
				str=""
				str='&'.join(attr)
				#set_super_keys(str)
				if str not in self.super_keys:
					self.super_keys.append(s)


	

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
		return cnf
	
	def check_2nf(self,relations,rname):
		vkeys=[]
		for key in relations.relations_dict[rname].super_keys:
			vkeys.extend(key.split("&"))
		k=0
		c=0
		item=rname
		for fd in relations.relations_dict[item].fd_dict[rname]:
			if item not in self.notvalid.keys():
				self.notvalid[item] = {}
				self.notvalid[item][fd]=[]
				for key in relations.relations_dict[rname].super_keys:
					pkeys=key.split("&")
					fdkeys=fd.split("&")			
					if(fd==key):
						k=1			
					elif set(fdkeys).issubset((set(pkeys))):
						for x in relations.relations_dict[item].fd_dict[rname][fd]:
							if x not in vkeys:
								if x not in self.notvalid[item][fd]:
									self.notvalid[item][fd].append(x)
								k=0
								c+=1							
					else:
						k=1
				if len(self.notvalid[item][fd])==0:
					self.notvalid[item].pop(fd)						
		if(c>0):
			return False
		else:
			return True				

	def check_3nf(self,relations,rname):		
		vkeys=[]
		item=rname
		for key in relations.relations_dict[rname].super_keys:
			vkeys.extend(key.split("&"))
		k=0
		c=0
		invalid_list={}
		for fd in relations.relations_dict[item].fd_dict[item]:
			if(item not in invalid_list.keys()):
				invalid_list[item]={}
			invalid_list[item][fd]=[]

			fdkeys=fd.split("&")
			sflag = False
			for key in relations.relations_dict[item].super_keys:
				pkeys=key.split("&")
				if(fd==key):
					k=1
					sflag = True
					break
				if set(fdkeys).issubset(set(pkeys)) and set(pkeys).issubset(set(fdkeys)):
					k=1
					sflag = True
					break
			if(sflag==False):
				for x in relations.relations_dict[item].fd_dict[item][fd]:
					if x in vkeys:
						k=1
					else:
						if x not in invalid_list[item][fd]:
							invalid_list[item][fd].append(x)
						k=0
						c+=1

			if len(invalid_list[item][fd])==0:
				invalid_list[item].pop(fd)
		if not invalid_list:
			return True		
		for key in invalid_list[item]:
			if item not in self.notvalid.keys():
				self.notvalid[item]={}
			if key not in self.notvalid[item].keys():
				self.notvalid[item][key]=copy.deepcopy(invalid_list[item][key])
			else:
				self.notvalid[item][key].extend(invalid_list[item][key])
				self.notvalid[item][key] = list(set(self.notvalid[item][key]))

		if(c>0):
			return False
		else:
			return True	

										




	def check_bcnf(self,relations,rname):
		c=0
		item=rname
		if not (relations.relations_dict[item].fd_dict):
			return True
		for fd in relations.relations_dict[item].fd_dict[item]:
			if fd not in relations.relations_dict[item].super_keys:
				for x in relations.relations_dict[item].fd_dict[item][fd]:
					if item not in self.notvalid.keys():
						self.notvalid[item]={}
					if fd not in self.notvalid[item].keys():
						self.notvalid[item][fd]=[]
					if x not in self.notvalid[item][fd]:
						self.notvalid[item][fd].append(x)
					c+=1				
		if(c>0):
			return False
		else:
			return True

	def get_nf(self,relations,rname):
		if(self.check_2nf(relations,rname)==False):
			return "1NF"
		elif(self.check_3nf(relations,rname)==False):
			return "2NF"
		elif(self.check_bcnf(relations,rname)==False):
			return "3NF"
		return "BCNF"
						
	def check_each_fd(self,relations,rname):
		thnf = 4
		for fd in relations.relations_dict[rname].fd_dict[rname]:
			print(fd,relations.relations_dict[rname].fd_dict[rname][fd], end=" ")
			print(self.getNF_fd(fd))
			print()
			thnf = min(self.getNF_fd(fd),thnf)
		return thnf

		
	def oneNF_to_2NF_3NF(self,relations,rname):
		for key in relations.relations_dict:
			l=len(relations.relations_dict.keys())			
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
				#print("x: "+x)
				#print(strin)
				relations.relations_dict[strin]=Relation(rname=strin,list_of_attributes=list_of_attribute,relation_obj=relations.relations_dict[key],pkey=x)
				for y in self.notvalid[key][x]:
					for z in relations.relations_dict[key].relation:
						if(z.name==y):
							relations.relations_dict[key].relation.remove(z)

				for x1 in relations.relations_dict[key].relation:
					x1.isPKA=False
					x1.isPPKA=False

				keylo={}
				keylo[x]=self.notvalid[key][x]
				#print("keuhgehrgejhhgj",end=" ")
				#print(keylo)
				relations.relations_dict[strin]._set_fds_(strin,keylo)
				relations.relations_dict[strin]._set_composite(strin)
			break
		for a in self.notvalid[rname]:
			for b in self.notvalid[rname][a]:
				for fd in relations.relations_dict[key].fd_dict[key]:
					if b in relations.relations_dict[key].fd_dict[key][fd]:
						relations.relations_dict[key].fd_dict[key][fd].remove(b)	
		relations.relations_dict[key].fd_dict[key]={k:v for k,v in relations.relations_dict[key].fd_dict[key].items() if not len(v)==0}

	"""
	Precondition: The Relational Schema at least satisfies the third normal form.
	"""
	def threeNF_to_BCNF(self,relations):
		#self.notvalid={}
		#self.check_bcnf()
		l=len(relations.relations_dict.keys())
		i=0
		klist = list(relations.relations_dict.keys())
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
					relations.relations_dict[strin]=Relation(rname=strin,list_of_attributes=list_of_attribute,relation_obj=relations.relations_dict[klist[i]],pkey=x)
					for y in self.notvalid[klist[i]][x]:
						if '&' in x:
							lk=x.split('&')
							if y not in lk:
								for z in relations.relations_dict[klist[i]].relation:
									if(z.name==y):
										relations.relations_dict[klist[i]].relation.remove(z)
						else:
							if x!=y:
								for z in relations.relations_dict[klist[i]].relation:
									if(z.name==y):
										relations.relations_dict[klist[i]].relation.remove(z)

					for x1 in relations.relations_dict[klist[i]].relation:
						x1.isPKA=False
						x1.isPPKA=False			
					keylo={}
					keylo[x]=self.notvalid[klist[i]][x]
					relations.relations_dict[strin]._set_fds_(strin,keylo)
				for fd in relations.relations_dict[klist[i]].fd_dict[klist[i]]:
					k=0
					if '&' in fd:
						l=fd.split('&')
						for c in l:
							mn=0
							for x in relations.relations_dict[klist[i]].relation:
								if (c==x.name):
									mn=1
							if(mn==0):
								k=1		
								break
						if(k==1):
							
							del relations.relations_dict[klist[i]].fd_dict[klist[i]][fd][:]
					else:
						mn=0
						for x in relations.relations_dict[klist[i]].relation:
							if (fd==x.name):
								mn=1
						if(mn==0):
							
							del relations.relations_dict[klist[i]].fd_dict[klist[i]][fd][:]
					ind = 0
					while (ind < len(relations.relations_dict[klist[i]].fd_dict[klist[i]][fd])):
						mn = 0
						for x in relations.relations_dict[klist[i]].relation:
							if(relations.relations_dict[klist[i]].fd_dict[klist[i]][fd][ind]==x.name):
								mn = 1
						if(mn==0):
							relations.relations_dict[klist[i]].fd_dict[klist[i]][fd].pop(ind)
						else:
							ind = ind + 1
			relations.relations_dict[klist[i]].fd_dict[klist[i]]={k:v for k,v in relations.relations_dict[klist[i]].fd_dict[klist[i]].items() if not len(v)==0}	
			i=i+1




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
		for ele in fds.keys():
			if ele in cdict:
				tlist = fds[ele]
				#print(tlist)
				tlist.extend(cdict[ele])
				tlist = list(set(tlist))
				cdict[ele]=tlist
			else:
				cdict[ele]=fds[ele]

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

	"""
	Finds out if the given relational decomposition is dependency preserving.
	"""
	def dependency_preserving_after(self):
		self.pfd_dict = self.getClosure(self.pfd_dict)
		global_dict={}
		#print("each case")
		tlist=[]
		for key in self.relations.relations_dict.keys():
			lfds = self.getClosure(self.relations.relations_dict[key].fd_dict[key])
			print(lfds)
			for ele in lfds:
				if ele in global_dict:
					tlist = global_dict[ele]
					tlist.extend(lfds[ele])
					#print("fnkjehrgkj",end=" ")
					tlist = list(set(tlist))
					global_dict[ele]=tlist
					#print(tlist)

				else:
					global_dict[ele]=lfds[ele]

		global_dict = self.getClosure(global_dict)
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
			#print(kl)
			for i in range(len(kl)):
				kl[i] = alist.index(kl[i])

			for ele in self.pfd_dict[key]:
				ti = alist.index(ele)
				if ti not in kl:
					pfd_list.append((kl,alist.index(ele)))

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