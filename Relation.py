class Constraints:
	def __init__(self,isPKA=False,isUnique=False,isNULL=False,isNOTNULL=False,isFK=False,FKref=None,a_range=None):
		self.isPKA = isPKA
		self.isUnique = isUnique
		self.isNULL = isNULL
		self.isNOTNULL = isNOTNULL
		self.isFK = isFK
		self.FKref = FKref
		self.a_range = a_range

	def setPK(self):
		self.isPKA = True

	def setUnique(self):
		self.isUnique = True

	def setNULL(self):
		assert self.isNOTNULL==False
		self.isNULL = True

	def setNOTNULL(self):
		assert self.isNULL==False
		self.isNOTNULL = True

	def setFk(self,relation,attribute):
		self.isFK = True
		self.Fkref = (relation,attribute)

	def setRangeConstraints(self,lower,upper):
		self.a_range = (lower,upper)

class Attribute:
	def __init__(self,_id,dtype,name,constraints,relation):
		self._id = _id
		self.dtype=dtype
		self.name=name
		self.constaints=constraints
		self.parent=relation

	def set_id(self,_id):
		self._id = _id

	def setDtype(self,dtype):
		self.dtype = dtype

	def setName(self,name):
		self.name = name

	def setConstraints(self,constraints):
		self.constraints = constraints

	def setParent(self,relation):
		self.parent = relation

class Relation:
	def __init__(self,pkey=None,attributes=[]):
		self.pkey=pkey
		self.attributes=attributes

	def setPK(self,PKAs):
		self.pkey = list(PKAs)

	def setAttributes(self,attributes):
		self.attributes = attributes

	def addColumn(self,attriubte):
		self.attributes.append(attribute)

	def updateColumn(self,attribute):
		index = self.attributes.index(attribute)
		assert index>=0
		assert index<len(self.attributes)
		self.attributes[index] = attribute

	def deleteColumn(self,attribute):
		index = self.attributes.index(attribute)
		assert index>=0
		assert index<len(self.attributes)
		self.attributes.pop(index)