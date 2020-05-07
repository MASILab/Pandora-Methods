addpath(genpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/masimatlab/trunk/users/blaberj/matlab/justinlib_v1_7_0'));
addpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/masimatlab/trunk/users/blaberj/dwmri_libraries/dwmri_visualizer_v1_2_0');
addpath('/home-nfs/masi-shared-home/home/local/VANDERBILT/hansencb/NIFTI');


% img_paths = dir('/nfs/masi/hansencb/t1_tract_data/raw_data/HCP/100206/100206/derivatives/tractseg/bundle_segmentations/*.nii.gz');
% slice = 78;
img_paths = dir('/nfs/masi/hansencb/t1_tract_data/Atlases/TractSegAtlases/ALL/TractSegNonlinear*.nii.gz');
slice = 103;

slices = 0;
for i = 1:length(img_paths)
    img = nifti_utils.load_untouch_nii_vol(fullfile(img_paths(i).folder, img_paths(i).name), 'double');
    img = squeeze(img(slice,:,:));
    if i == 1
        slices = img;
    else
        slices = cat(3, slices, img);
    end
end

collapse = zeros(size(img));
for i = 1:size(slices,3)
    slice = slices(:,:,i);
    slice(slice < 0.5) = 0;
    slice(slice >= 0.5) = 1;
    collapse(logical(slice)) = i;
end

figure; imshow(rot90(collapse), [0, 71]);
custom = colorcube;
colormap([[0,0,0]; custom(2:end, :)]);
axis image;
