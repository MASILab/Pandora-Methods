function [] = QA_Registration(folder)
% takes folder to prokject/subject/sessionm
% has reg/dwi/anat
% will plot several things
% folder='/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA/1512/BLSA_1512_07-0_10'
try

QApath = [folder filesep 'QA'];
mkdir(QApath)

atlaspath='/nfs/masi/schilkg1/LearningWM/data/atlases/mni_icbm152_t1_tal_nlin_asym_09c.nii.gz';

addpath(genpath('/nfs/masi/schilkg1/schillkg/MATLAB/NIFTI_20130306'))


atlas = load_untouch_nii_gz(atlaspath); atlas = double(atlas.img); atlas = atlas./max(atlas(:));
sz = size(atlas);
sag_1 = round(0.5*sz(3));
sag_2 = round(0.6*sz(3));
ax_1 = round(0.3*sz(1));
ax_2 = round(0.6*sz(1));


RIGID_t1 = [folder filesep 'reg' filesep 'T1_norm_lin_atlas.nii.gz'];
RIGID_t1 = load_untouch_nii_gz(RIGID_t1); RIGID_t1 = RIGID_t1.img; RIGID_t1 = RIGID_t1./max(RIGID_t1(:));

NRIGID_t1 = [folder filesep 'reg' filesep 'T1_norm_nonlin_atlas.nii.gz'];
NRIGID_t1 = load_untouch_nii_gz(NRIGID_t1); NRIGID_t1 = NRIGID_t1.img; NRIGID_t1 = NRIGID_t1./max(NRIGID_t1(:));

RIGID_b0 = [folder filesep 'reg' filesep 'b0_lin_atlas.nii.gz'];
RIGID_b0 = load_untouch_nii_gz(RIGID_b0); RIGID_b0 = RIGID_b0.img; RIGID_b0 = RIGID_b0./max(RIGID_b0(:));

NRIGID_b0 = [folder filesep 'reg' filesep 'b0_nonlin_atlas.nii.gz'];
NRIGID_b0 = load_untouch_nii_gz(NRIGID_b0); NRIGID_b0 = NRIGID_b0.img; NRIGID_b0 = NRIGID_b0./max(NRIGID_b0(:));

A = atlas(:,:,sag_1);
B = RIGID_t1(:,:,sag_1);
C = RIGID_b0(:,:,sag_1);
D = atlas(:,:,sag_2);
E = RIGID_t1(:,:,sag_2);
F = RIGID_b0(:,:,sag_2);

G = flipdim(permute(squeeze(atlas(ax_1,:,:)),[2 1]),1);
H = flipdim(permute(squeeze(RIGID_t1(ax_1,:,:)),[2 1]),1);
I = flipdim(permute(squeeze(RIGID_b0(ax_1,:,:)),[2 1]),1);
J = flipdim(permute(squeeze(atlas(ax_2,:,:)),[2 1]),1);
K = flipdim(permute(squeeze(RIGID_t1(ax_2,:,:)),[2 1]),1);
L = flipdim(permute(squeeze(RIGID_b0(ax_2,:,:)),[2 1]),1);

AA = atlas(:,:,sag_1);
BB = NRIGID_t1(:,:,sag_1);
CC = NRIGID_b0(:,:,sag_1);
DD = atlas(:,:,sag_2);
EE = NRIGID_t1(:,:,sag_2);
FF = NRIGID_b0(:,:,sag_2);

GG = flipdim(permute(squeeze(atlas(ax_1,:,:)),[2 1]),1);
HH = flipdim(permute(squeeze(NRIGID_t1(ax_1,:,:)),[2 1]),1);
II = flipdim(permute(squeeze(NRIGID_b0(ax_1,:,:)),[2 1]),1);
JJ = flipdim(permute(squeeze(atlas(ax_2,:,:)),[2 1]),1);
KK = flipdim(permute(squeeze(NRIGID_t1(ax_2,:,:)),[2 1]),1);
LL = flipdim(permute(squeeze(NRIGID_b0(ax_2,:,:)),[2 1]),1);

BLAH = cat(3,A,B,C,D,E,F,G,H,I,J,K,L);
BLAH = reshape(BLAH,[size(BLAH,1), size(BLAH,2), 1, size(BLAH,3)]);
f = figure('visible', 'off'); montage(BLAH,'Size',[4 3]);

save_name=[QApath filesep 'Rigid_registration'];
%pause(1);
print(f,'-dtiff','-r200',save_name); 
%pause(1);
close all;

BLAH = cat(3,AA,BB,CC,DD,EE,FF,GG,HH,II,JJ,KK,LL);
BLAH = reshape(BLAH,[size(BLAH,1), size(BLAH,2), 1, size(BLAH,3)]);
f = figure('visible', 'off'); montage(BLAH,'Size',[4 3]);

save_name=[QApath filesep 'NONRigid_registration'];
%pause(1);
print(f,'-dtiff','-r200',save_name);
%pause(1);
close all;

catch
    disp('fail')
end














