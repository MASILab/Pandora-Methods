addpath(genpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/masimatlab/trunk/users/blaberj/matlab/justinlib_v1_7_0'));
addpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/masimatlab/trunk/users/blaberj/dwmri_libraries/dwmri_visualizer_v1_2_0');
addpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/NIFTI');


img1_path = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP/100206/100206/reg/T1_N3_nonlin_atlas.nii.gz';
img2_path = '/nfs/masi/hansencb/t1_tract_data/registered_data/TractSegNonlinear/HCP_100206_100206/CC.nii.gz';
img3_path = '/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz';

img1 = nifti_utils.load_untouch_nii_vol(img1_path, 'double');
img2 = nifti_utils.load_untouch_nii_vol(img2_path, 'double');
img3 = nifti_utils.load_untouch_nii_vol(img3_path, 'double');

slice = 96;

img = cat(2, rot90(img3(:,:,slice)) ./ max(img3(:)), ...
    rot90(img1(:,:,slice)) ./ max(img1(:)), ... 
    rot90(img2(:,:,slice)));

figure;
imshow(img); hold on;
plot((1:length(img)), ones(length(img)).*30,  'c');
plot((1:length(img)), ones(length(img)).*60,  'c');
plot((1:length(img)), ones(length(img)).*90,  'c');
plot((1:length(img)), ones(length(img)).*120, 'c');
plot((1:length(img)), ones(length(img)).*150, 'c');
plot((1:length(img)), ones(length(img)).*180, 'c');
plot((1:length(img)), ones(length(img)).*210, 'c');
