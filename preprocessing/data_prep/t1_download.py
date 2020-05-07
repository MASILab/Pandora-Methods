import dax
import os

download_dir = '/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA_xnat'

proj_ID = 'BLSA'

resource = 'NIFTI'

xutil = dax.XnatUtils

xnat = xutil.get_interface("http://xnat2.vanderbilt.edu:8080/xnat", "hansencb", "Maliwan12")

scans = xnat.get_project_scans(proj_ID)

if not os.path.exists(proj_ID):
	os.system("mkdir %s" % (proj_ID))

for scan in scans:
	scan_type = scan['scan_type']
	if 'T1' in scan_type:
		#if 'DTI' in assess_label:
		subj_label = scan['subject_label']
		sess_label = scan['session_label']
		
		subj_dir = download_dir + "/" + proj_ID + "/" + subj_label
		if not os.path.exists(subj_dir):
			os.system("mkdir %s" % (subj_dir))
		
		sess_dir = subj_dir + "/" + sess_label
		if not os.path.exists(sess_dir):
			os.system("mkdir %s" % (sess_dir))			
		
		scan_label = scan['scan_label']
		scan_label = proj_ID + '-x-' + subj_label + '-x-' + \
                     sess_label + '-x-' + scan_label
		if not os.path.exists(sess_dir + "/" + scan_label):
			command = "Xnatdownload -d " + sess_dir + \
					  " -p " + proj_ID + " --rs " + resource + \
					  " --selectionS " + scan_label
			os.system(command)
