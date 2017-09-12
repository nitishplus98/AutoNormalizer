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
		#print(relations_dict[stri[0]].relation[1].name)	


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
		while x<=len(str)-5:
			attribute=Constraints(str[x],str[x+1],str[x+2],str[x+3],str[x+4])
			if(str[x+4]==True):
				self.ppka=self.ppka+1
				if(self.ppka==1):
					s=str[x]
				else:
					s=s+"&"+str[x]
			if(str[x+1]==True):
				self.super_keys.append(str[x+1])			
			self.relation.append(attribute)
			self.no=self.no+1
			x=x+5
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
			b=b[1:len(b)-1]
			c=[]
			c=b.split(",")
			self.fd_dict[a]=c
			#print(a,fd_dict[a])

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
	def check_2nf(self):
		vkeys=[]		
		for key in self.relations.relations_dict[self.rname].super_keys:
			vkeys.extend(key.split("&"))
		#print(vkeys)	
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

	#def check_3nf():

	#def check_bcnf():	
nf=check_NF("test")
print (nf.check_2nf())
for a in nf.notvalid:
	print(a+"->"+nf.notvalid[a])








				

	
