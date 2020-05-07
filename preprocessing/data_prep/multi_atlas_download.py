import dax
import os

proj_ID = 'NORMAL'

assess_resource = 'SEG'

xutil = dax.XnatUtils

xnat = xutil.get_interface("http://xnat2.vanderbilt.edu:8080/xnat", "hansencb", "xxx")

assessors = xutil.list_project_assessors(xnat, proj_ID)

if not os.path.exists(proj_ID):
	os.system("mkdir %s" % (proj_ID))

for assessor in assessors:
	assess_label = assessor['assessor_label']
	if 'Multi_Atlas' in assess_label:
		#if 'DTI' in assess_label:
		subj_label = assessor['subject_label']
		sess_label = assessor['session_label']
		
		subj_dir = proj_ID + "/" + subj_label
		if not os.path.exists(subj_dir):
			os.system("mkdir %s" % (subj_dir))
		
		sess_dir = subj_dir + "/" + sess_label
		if not os.path.exists(sess_dir):
			os.system("mkdir %s" % (sess_dir))			
		
		if not os.path.exists(sess_dir + "/" + assess_label):
			command = "Xnatdownload -d " + sess_dir + \
					  " -p " + proj_ID + " --ra " + assess_resource + \
					  " --selectionP " + assess_label
			os.system(command)
