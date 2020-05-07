addpath(genpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/masimatlab/trunk/users/blaberj/matlab/justinlib_v1_7_0'));
addpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/masimatlab/trunk/users/blaberj/dwmri_libraries/dwmri_visualizer_v1_2_0');
addpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/NIFTI');


img1_path = '/nfs/masi/hansencb/t1_tract_data/raw_data/HCP/100206/100206/reg/T1_N3_nonlin_atlas.nii.gz';
seg_path = '/nfs/masi/hansencb/t1_tract_data/registered_data/TractSegNonlinear/HCP_100206_100206/CC.nii.gz';
img2_path = '/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz';

img1 = nifti_utils.load_untouch_nii_vol(img1_path, 'double');
seg = nifti_utils.load_untouch_nii_vol(seg_path, 'double');
img2 = nifti_utils.load_untouch_nii_vol(img2_path, 'double');

slice = 96;

slice1 = rot90(img1(:,:,slice));
slice1 = slice1 ./ max(slice1(:));
slice1 = cat(3, slice1, slice1, slice1);

seg_slice = rot90(seg(:,:,slice));
seg_slice = seg_slice>=0.5;

slice2 = rot90(img2(:,:,slice));
slice2 = slice2 ./ max(slice2(:));
slice2 = cat(3, slice2, slice2, slice2);

color_slice = ones(size(slice1,1), size(slice1,2), 3);
color_slice(:,:,1) = 12/256;
color_slice(:,:,2) = 232/256;
color_slice(:,:,3) = 232/256;

color_seg_slice = color_slice .* seg_slice;

half_alpha = zeros(size(slice1,1), size(slice1,2));
half_alpha(:, floor(size(half_alpha,2)/2):end) = 1;
half_alpha = half_alpha .* seg_slice;

figure;
h = imagesc(slice1, [0, 1]);

[M,N,tmp] = size(slice1); 
block_size = 50; 
P = ceil(M / block_size); 
Q = ceil(N / block_size); 
alpha = checkerboard(block_size, P, Q) > 0; 
alpha = alpha(1:M, 1:N); 
set(h, 'AlphaData', alpha);

hold on;
h = imagesc(slice2, [0, 1]);
set(h, 'AlphaData', ~alpha);


hold on;
h = imagesc(color_seg_slice, [0,1]);
set(h, 'AlphaData', seg_slice .* alpha .* 0.35);
% set(h, 'AlphaData', half_alpha .* 0.5);

axis image;
xticks([]);
yticks([]);