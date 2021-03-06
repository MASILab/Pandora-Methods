function [] = QA_AFQ_clipped(folder)
% takes folder to prokject/subject/sessionm
% will make single montage of TractSeg overlays on b0
% folder='/nfs/masi/hansencb/t1_tract_data/raw_data/BLSA/1512/BLSA_1512_07-0_10'
% folder='/Users/schilling/Downloads/BLSA/1099/BLSA_1099_17-0_10/'

% try
    %%%%%% ADD PATHS
    addpath(genpath('/nfs/masi/schilkg1/schillkg/MATLAB/NIFTI_20130306'))
    addpath(genpath('/nfs/masi/schilkg1/schillkg/MATLAB/programs'))
    
    A={'Callosum\ Forceps\ Major';'Callosum\ Forceps\ Minor';'Left\ Arcuate';'Left\ Cingulum\ Cingulate';'Left\ Cingulum\ Hippocampus';...
        'Left\ Corticospinal';'Left\ IFOF';'Left\ ILF';'Left\ SLF';'Left\ Thalamic\ Radiation'; ...
        'Left\ Uncinate';'Right\ Arcuate';'Right\ Cingulum\ Cingulate';'Right\ Cingulum\ Hippocampus';'Right\ Corticospinal'; ...
        'Right\ IFOF';'Right\ ILF';'Right\ SLF';'Right\ Thalamic\ Radiation';'Right\ Uncinate'};
    paths=A;
    
    bundles_path = [folder filesep 'derivatives' filesep 'AFQ_clipped'];
    b0_path = [folder filesep 'dwi' filesep 'b0.nii.gz'];
    TIFF_NAME = [folder filesep 'QA' filesep 'AFQ_clippedQA'];
    
    %%%%%% LOAD
    b0 = load_untouch_nii_gz(b0_path);
    b0 = b0.img;
    sz=size(b0);
    img = b0(:,:,round(sz(3)/2)); img = permute(img,[2 1]); img = flip(img,1); img = flip(img,2);
    %figure; imagesc(img); colormap gray; axis equal; axis tight; axis off;
    
    %%%%%%%%%%%%% BUNDLES
    overlay_stack = [];
    stack = [];
    
    for i = 1:length(paths)
        %disp(i)
        try
            
            pred = [bundles_path filesep paths{i} '.nii.gz'];
            pred = load_untouch_nii_gz(pred); pred = pred.img;
            pred(pred>=.5) = 1; pred(pred<.5) = 0; %   montage(reshape(truth,[77 91 1 77]))
            
            temp = squeeze(sum(sum(pred,1),2));
            ind = find(temp==max(temp)); ind=ind(1);
            t1_img = b0(:,:,ind); 
            %t1_img=mat2gray(t1_img);
            t1_img=double(t1_img); t1_img=t1_img./max(t1_img(:));
            
            pred_img = pred(:,:,ind);
            
            r = t1_img; r(pred_img==1)=1;
            b = t1_img; b(pred_img==1)=0;
            g = t1_img; g(pred_img==1)=0;
            overlay=cat(3,b,g,r);
            overlay = permute(overlay,[2 1 3]); overlay = flip(overlay,1); overlay = flip(overlay,2);
            
            overlay_stack(:,:,:,i)=overlay;
            
            overlay=cat(3,t1_img,t1_img,t1_img);
            overlay = permute(overlay,[2 1 3]); overlay = flip(overlay,1); overlay = flip(overlay,2);
            
            stack(:,:,:,i)=overlay;
            
            
        catch
            disp('cannot open truth')
            img = zeros(sz(2),sz(1),3);
            overlay = img;
            
            overlay_stack(:,:,:,i)=overlay;
            stack(:,:,:,i)=overlay;
            
        end
        
    end
    
%     MON = zeros(size(stack,1),size(stack,2), 3, size(stack,4)+size(overlay_stack,4));
%     MON(:,:,:,1:5) = overlay_stack(:,:,:,1:5);
%     MON(:,:,:,6:10) = stack(:,:,:,1:5);
%     MON(:,:,:,11:15) = overlay_stack(:,:,:,6:10);
%     MON(:,:,:,16:20) = stack(:,:,:,6:10);
%     MON(:,:,:,21:25) = overlay_stack(:,:,:,11:15);
%     MON(:,:,:,26:30) = stack(:,:,:,11:15);
%     MON(:,:,:,31:35) = overlay_stack(:,:,:,16:20);
%     MON(:,:,:,36:40) = stack(:,:,:,16:20);
    
    
    f = figure('visible', 'off'); montage(overlay_stack,'Size',[4 5]);
    set(f,'PaperPositionMode','auto'); 
    print(f,'-dtiff','-r400',TIFF_NAME);
    close all;
    

%     
% catch
%     disp('fail')
% end
