from flask import Flask,render_template,request,redirect
from Relation import *
import time

app = Flask(__name__)
saved_query = {}
@app.route("/")
def main():
	return render_template('input.html')

@app.route("/properties",methods=['POST'])
def properties():
	query = request.form['schema']
	sinput = query.strip().split('\n')
	for i in range(len(sinput)):
		sinput[i] = sinput[i].strip()
	query = request.form['fds']
	saved_query['schema'] = request.form['schema']
	saved_query['fds'] = request.form['fds']
	finput = query.strip().split('\n')
	for i in range(len(finput)):
		finput[i] = finput[i].strip()
	relations = Relations(sinput)
	for key in relations.relations_dict:
		relations.relations_dict[key]._set_fds_(key,sinput=finput)
	nf=check_NF("test",relations)
	resp = {}
	resp['schema'] = relations.relations_dict['test'].relation
	resp['fdicts'] = relations.relations_dict['test'].fd_dict['test']
	print(resp['fdicts'])
	resp['skeys'] = nf.relations.relations_dict["test"].super_keys
	resp['hnf'] = nf.get_nf()
	pfds = copy.deepcopy(nf.relations.relations_dict["test"].fd_dict["test"])
	obj = Decomposition_Properties(nf.relations,pfds)
	resp['closure'] = obj.getClosure(pfds)
	nf.check_2nf()
	nf.check_3nf()
	nf.check_bcnf()
	resp['notvalid'] = {}
	for key in nf.notvalid:
		resp['notvalid'][key]={}
		for fdkey in nf.notvalid[key]:
			resp['notvalid'][key][fdkey]=[]
			for rs in nf.notvalid[key][fdkey]:
				resp['notvalid'][key][fdkey].append((rs,nf.getNF_fd(fdkey,rs,key)))
	nf.notvalid = {}
	resp['cvt'] = 0
	return render_template('main.html',res=resp)

@app.route("/normalize",methods=['POST'])
def normalize():
	resp={}
	query = saved_query['schema']
	sinput = query.strip().split('\n')
	for i in range(len(sinput)):
		sinput[i] = sinput[i].strip()
	query = saved_query['fds']
	finput = query.strip().split('\n')
	for i in range(len(finput)):
		finput[i] = finput[i].strip()
	relations = Relations(sinput)
	for key in relations.relations_dict:
		relations.relations_dict[key]._set_fds_(key,sinput=finput)
	nf=check_NF("test",relations)
	pfds = copy.deepcopy(nf.relations.relations_dict["test"].fd_dict["test"])
	obj = Decomposition_Properties(nf.relations,pfds)
	resp['closure'] = copy.deepcopy(obj.getClosure(pfds))
	nf.check_2nf()
	nf.check_3nf()
	nf.check_bcnf()
	resp['notvalid'] = {}
	for key in nf.notvalid:
		resp['notvalid'][key]={}
		for fdkey in nf.notvalid[key]:
			resp['notvalid'][key][fdkey]=[]
			for rs in nf.notvalid[key][fdkey]:
				resp['notvalid'][key][fdkey].append((rs,nf.getNF_fd(fdkey,rs,key)))
	nf.notvalid = {}
	if(request.form['cvt']=="option1"):
		resp['cvt']=1
	elif request.form['cvt']=="option2":
		resp['cvt']=2
	resp['schema'] = copy.deepcopy(relations.relations_dict['test'].relation)
	resp['fdicts'] = copy.deepcopy(relations.relations_dict['test'].fd_dict['test'])
	resp['skeys'] = copy.deepcopy(nf.relations.relations_dict["test"].super_keys)
	resp['hnf'] = copy.deepcopy(nf.get_nf())
	if (not nf.check_2nf()) or (not nf.check_3nf()):
		nf.oneNF_to_2NF_3NF()
	resp['3nfo'] = copy.deepcopy(nf)
	obj = Decomposition_Properties(nf.relations,pfds)
	resp['3lj'] = obj.lossless_join_before()
	resp['3dp'] = obj.dependency_preserving_after()

	if not nf.check_bcnf():
		nf.threeNF_to_BCNF()
	resp['bcnfo'] = copy.deepcopy(nf)
	obj = Decomposition_Properties(nf.relations,pfds)
	resp['blj'] = obj.lossless_join_before()
	resp['bdp'] = obj.dependency_preserving_after()
	return render_template('main.html',res=resp)

if(__name__ == "__main__"):
	app.run()