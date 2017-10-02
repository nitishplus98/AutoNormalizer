import re
class Relations:
	def __init__(self):
		file=open("schema.txt","r")
		self.relations_dict={}
		str=file.readlines()
		for s in str:
			stri=re.findall(r"[\w']+",s)
			print(type(s))
			self.relations_dict[stri[0]]=Relation(s)


class Constraints:
	def __init__(self,name,isPKA=False,isNULL=False,isFK=False,isPPKA=False):
		self.name=name
		self.isPKA = isPKA
		self.isNULL = isNULL
		self.isFK = isFK
		self.isPPKA=isPPKA

	

class Relation:
	def __init__(self,s):
		str=re.findall(r"[\w']+",s)		
		self.relation=[]
		self.no=0
		self.ppka=0
		self.super_keys=[]
		x=1
		s=None
		while x<=len(str)-5:
			attribute=Constraints(str[x],str[x+1],str[x+2],str[x+3],str[x+4])
			if(str[x+4]==True):
				self.ppka=self.ppka+1
				if(self.ppka==1):
					s=str[x]
				else:
					s=s+"&"+str[x]
			if(str[x+1]==True):
				self.super_keys.append(str[x])			
			self.relation.append(attribute)
			self.no=self.no+1
			x=x+5

		if(s is not None):
			self.super_keys.append(s)

	def set_super_keys(self,s):
		if s not in self.super_keys:
			#print(s)
			self.super_keys.append(s)

		

class functional_dependencies:
	def __init__(self):
		fd_file=open("fd.txt","r")
		self.fd_dict={}
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
			if(a in self.fd_dict and len(self.fd_dict[a])>0):
				ls = self.fd_dict[a]
				if(len(temp)>0):
					for ele in temp:
						if(ele not in ls):
							ls.append(ele)
				temp = ls
			if(len(temp)>0):
				self.fd_dict[a]=temp
			#print(a,self.fd_dict[a])

	def _set_composite(self,fds,relations,rname):
		
		for item in relations.relations_dict:
			if(item==rname):
				for fd in fds.fd_dict:
					attr=[]
					attr.extend(fd.split("&"))
					if(len(attr)+len(fds.fd_dict[fd])==relations.relations_dict[rname].no):
						str=""
						str='&'.join(attr)
						#print(str,attr)
						relations.relations_dict[rname].set_super_keys(str)
					#print(fds.fd_dict[fd])




class check_NF:
	def __init__(self,rname):
		self.fds=functional_dependencies()
		self.relations=Relations()
		self.fds._set_composite(self.fds,self.relations,rname)
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
						for ele in self.fds.fd_dict[fd]:
							if ele not in vkeys:
								self.notvalid[fd]=ele
								cnf = min(cnf,1)
						cnf = min(cnf,3)
						self.notvalid[fd]=ele

					else:
						for ele in self.fds.fd_dict[fd]:
							if ele not in vkeys:
								self.notvalid[fd]=ele
								cnf = min(cnf,2)
						cnf=min(cnf,3)
						self.notvalid[fd]=ele
		return cnf

	
	def check_2nf(self):
		vkeys=[]
		for key in self.relations.relations_dict[self.rname].super_keys:
			vkeys.extend(key.split("&"))
		k=0
		c=0
		for item in self.relations.relations_dict:
			if(item==self.rname):
				for fd in self.fds.fd_dict:
					for key in self.relations.relations_dict[self.rname].super_keys:
						pkeys=key.split("&")
						fdkeys=fd.split("&")			
						if(fd==key):
							k=1			
						elif set(fdkeys).issubset((set(pkeys))):
							for x in self.fds.fd_dict[fd]:
								if x not in vkeys:
									self.notvalid[fd]=x
									k=0
									c+=1							
						else:
							k=1
		if(c>0):
			return False
		else:
			return True				

	def check_3nf(self):
		
		vkeys=[]
		for key in self.relations.relations_dict[self.rname].super_keys:
			vkeys.extend(key.split("&"))
		k=0
		c=0
		for item in self.relations.relations_dict:
			if(item==self.rname):
				for fd in self.fds.fd_dict:
					for key in self.relations.relations_dict[self.rname].super_keys:
						pkeys=key.split("&")
						fdkeys=fd.split("&")
						if(fd==key):
							k=1
						elif set(fdkeys).issubset(set(pkeys)):
							k=1
						else:
							for x in self.fds.fd_dict[fd]:
								if x in vkeys:
									k=1
								else:
									self.notvalid[fd]=x	
									k=0
									c+=1
		if(c>0):
			return False
		else:
			return True	

										




	def check_bcnf(self):
		c=0
		for item in self.relations.relations_dict:
			if(item==self.rname):
				for fd in self.fds.fd_dict:
					if fd not in self.relations.relations_dict[self.rname].super_keys:
						for x in self.fds.fd_dict[fd]:
							self.notvalid[fd]=x
							c+=1
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
		for fd in self.fds.fd_dict:
			print(fd,self.fds.fd_dict[fd], end=" ")
			print(self.getNF_fd(fd))
			print()
			thnf = min(self.getNF_fd(fd),thnf)
		return thnf



nf=check_NF("test")
print(nf.check_2nf())
print(nf.check_3nf())
print(nf.check_bcnf())
print(nf.get_nf())
print(nf.check_each_fd())
print()
for a in nf.notvalid:
	print(a+"->"+nf.notvalid[a])








				

	