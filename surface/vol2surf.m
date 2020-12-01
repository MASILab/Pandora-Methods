% Author: Ilwoo Lyu, ilwoo.lyu@vanderbilt.edu
% this script requires FreeSurfer's MATLAB libraries

% read a list of volumes
flist=dir('*.nii.gz');

% read atlas (template) surfaces
[v_lh,f_lh]=read_surf('surf/lh.white');
[v_rh,f_rh]=read_surf('surf/rh.white');
v_hemi = [v_lh; v_rh];
nv_lh = size(v_lh,1);

for fid = 1: length(flist)
    vol = [flist(fid).folder filesep flist(fid).name];

    surf_data = vol2vert(vol, v_hemi);
    
    [~, fn] = fileparts(flist(fid).name);
    [~, fn] = fileparts(fn);
    fn = [fn '.vtk'];

    lab = dir([flist(fid).folder filesep '*.csv']);
    lab = readtable([flist(fid).folder filesep lab.name]);
    str_lh = struct;
    str_rh = struct;
    nvol = size(surf_data,2);
    for i = 1: nvol
        nlab = lab{i,2}{:};
        nlab = strrep(nlab,'.','_');
        eval(sprintf('str_lh.%s=surf_data(1:nv_lh,i);', nlab));
        eval(sprintf('str_rh.%s=surf_data(nv_lh+1:end,i);', nlab));
    end

    % outputs
    write_property(['atlas/lh.' fn],v_lh,f_lh,str_lh);
    write_property(['atlas/rh.' fn],v_rh,f_rh,str_rh);

    disp('done');
end
