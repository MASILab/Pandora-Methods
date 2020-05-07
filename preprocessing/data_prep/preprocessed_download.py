import dax
import os
import shutil

download_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA_xnat'

proj_ID = 'BLSA'

assess_resource = 'PREPROCESSED'

xutil = dax.XnatUtils

xnat = xutil.get_interface("http://xnat2.vanderbilt.edu:8080/xnat", "hansencb", "Maliwan12")

assessors = xutil.list_project_assessors(xnat, proj_ID)

if not os.path.exists(os.path.join(download_dir, proj_ID)):
	os.system("mkdir %s" % (os.path.join(download_dir, proj_ID)))

for assessor in assessors:
	assess_label = assessor['assessor_label']
	if 'dtiQA_v6' in assess_label and ('DTI1' not in assess_label and 'DTI2' not in assess_label) and assessor['procstatus'] == 'COMPLETE':
		subj_label = assessor['subject_label']
		sess_label = assessor['session_label']

		#blsa specific scanner id in session label
		scanner = sess_label.split('_')[-1]
		
		subj_dir = os.path.join(download_dir, proj_ID, subj_label)
		if not os.path.exists(subj_dir):
			os.system("mkdir %s" % (subj_dir))
		
		sess_dir = os.path.join(subj_dir, sess_label)
		if not os.path.exists(sess_dir):
			os.system("mkdir %s" % (sess_dir))

		if os.path.exists(os.path.join(sess_dir, 'fixed_{}'.format(assess_label))):
			with open(os.path.join(sess_dir, 'fixed_{}'.format(assess_label)), 'r') as f:
				l = f.readlines()

			if l[0] == 'deleted':
				os.remove(os.path.join(sess_dir, 'fixed_{}'.format(assess_label)))

		if scanner in ['08', '09'] and not os.path.exists(os.path.join(sess_dir, 'fixed_{}'.format(assess_label))):
			if os.path.exists(os.path.join(sess_dir, assess_label)):
				shutil.rmtree(os.path.join(sess_dir, assess_label))
			with open(os.path.join(sess_dir, 'fixed_{}'.format(assess_label)), 'w') as f:
				f.write('deleted')

		if not os.path.exists(os.path.join(sess_dir, assess_label)):
			command = "Xnatdownload -d " + sess_dir + \
					  " -p " + proj_ID + " --ra " + assess_resource + \
					  " --selectionP " + assess_label
			os.system(command)

			if scanner in ['08', '09']:
				with open(os.path.join(sess_dir, 'fixed_{}'.format(assess_label)), 'w') as f:
					f.write('redownloaded')



