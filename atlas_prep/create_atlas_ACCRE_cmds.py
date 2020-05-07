import os

def create_atlases_cmds(in_dir, out_dir, prefix, thresh, f):
    blsa_subjs = []
    with open('BLSA_first.csv', 'r') as fin:
        fin.readline()
        for line in fin.readlines():
            subj = line.split(',')[1]
            blsa_subjs.append(subj)
            
    data = {}
    for sess in os.listdir(in_dir):
        parts = sess.split('_')
        sess_name = '_'.join(parts[2:])

        proj = parts[0]
        if parts[1] == 'Morgan' or parts[1] == 'Cutting':
            subj = '_'.join(parts[1:5])
        elif parts[1] == 'Taylor':
            subj = '_'.join(parts[1:4])
        else:
            subj = parts[1]

        include = True
        if proj=='BLSA':
            if not sess_name in blsa_subjs:
                include = False
        
        if include:
            if proj not in data:
                data[proj] = {}

            sess_dir = os.path.join(in_dir, sess)

            for vol in os.listdir(sess_dir):
                path = os.path.join(sess_dir, vol)

                if vol not in data[proj]:
                    data[proj][vol] = [[], []]

                if subj not in data[proj][vol][1]:
                    data[proj][vol][1].append(subj)
                    data[proj][vol][0].append(path)


    for project in data:
        proj_out = os.path.join(out_dir, project)
        if not os.path.isdir(proj_out):
            os.mkdir(proj_out)

        for label in data[project]:
            paths = data[project][label][0]
            out_path = os.path.join(proj_out, '{}_{}'.format(prefix, label))
            if not os.path.isfile(out_path):
                cmd = 'python /scratch/hansencb/tract_preprocessing/atlas/create_atlas_ACCRE.py --paths {} --thresh {} --out {}'.format(' '.join(paths), thresh, out_path)
                f.write('{}\n'.format(cmd))


with open('create_atlas_cmd.txt', 'w') as f:
    out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/TractSegAtlases'
    lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/TractSegLinear'
    nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/TractSegNonlinear'
    
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    create_atlases_cmds(lin_dir, out_dir, 'TractSegLinear', 0.5, f)
    create_atlases_cmds(nonlin_dir, out_dir, 'TractSegNonlinear', 0.5, f)
    
    out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/RecobundlesAtlases'
    lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/RecobundlesLinear'
    nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/RecobundlesNonlinear'
    
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    create_atlases_cmds(lin_dir, out_dir, 'RecobundlesLinear', 0.5, f)
    create_atlases_cmds(nonlin_dir, out_dir, 'RecobundlesNonlinear', 0.5, f)
    
    out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/XtractAtlases'
    lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/XtractLinear'
    nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/XtractNonlinear'
    
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    create_atlases_cmds(lin_dir, out_dir, 'XtractLinear', 0.001, f)
    create_atlases_cmds(nonlin_dir, out_dir, 'XtractNonlinear', 0.001, f)
    
    out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/TraculaAtlases'
    lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/TraculaLinear'
    nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/TraculaNonlinear'
    
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    create_atlases_cmds(lin_dir, out_dir, 'TraculaLinear', 0.5, f)
    create_atlases_cmds(nonlin_dir, out_dir, 'TraculaNonlinear', 0.5, f)

    out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/AFQAtlases'
    lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQcleanLinear'
    nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQcleanNonlinear'

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    create_atlases_cmds(lin_dir, out_dir, 'AFQcleanLinear', 0.5, f)
    create_atlases_cmds(nonlin_dir, out_dir, 'AFQcleanNonlinear', 0.5, f)

    out_dir = '/nfs/masi/hansencb/t1_tract_data/Atlases/AFQclippedAtlases'
    lin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQclippedLinear'
    nonlin_dir = '/nfs/masi/hansencb/t1_tract_data/registered_data/AFQclippedNonlinear'

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    create_atlases_cmds(lin_dir, out_dir, 'AFQclippedLinear', 0.5, f)
    create_atlases_cmds(nonlin_dir, out_dir, 'AFQclippedNonlinear', 0.5, f)
