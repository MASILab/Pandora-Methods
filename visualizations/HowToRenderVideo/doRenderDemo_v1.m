
%% Quick demo on how to make a "spinning brain"
% This version was created by Bennett Landman 
% November 16, 2019. 
% PLEASE adjust the options and create new demo videos. 
% Feel free to include public data in this repo. 
% Save all needed files internally here. 

%% Set paths (be sure to save all the paths that you need
addpath(genpath(pwd))

%% Step 1: Load the data

CT.img = niftiread('CT.nii.gz');
CT.hdr = niftiinfo('CT.nii.gz');
bodymask.img = niftiread('body_seg.nii.gz');
organs.img = niftiread('seg.nii.gz');

%%Step 2: Start a new figure
figure(1);
clf

%% Step 3: For each volume, make a face/vertex masking

% This is a hack to remove the high density skin  leads
bodymask.img = convn(bodymask.img,ones([5 5 2]),'same')==50;

% play with the contours and the cleaning until it makes sense
bones = isosurface(smooth3(CT.img.*bodymask.img),300);

% render the face/vertex
p=patch(bones);

% try to set all render options in 1 call. there are lots of options.
% have fun
set(p,'facecolor',[.5 .5 .5],'edgecolor','none')


%% Step 4 : think about color maps. It's important for clarity
%map = jet(max(organs.img(:)));
map = [255,30,30;255,245,71;112,255,99;9,150,37;30,178,252;132,0,188;...
    255,81,255;158,191,9;255,154,2;102,255,165;0,242,209;255,0,80]/255;
map=parula(max(organs.img(:)));

%% Step 5: Loop over all structures to be rendered
for i=1:max(organs.img(:))
        
    Org = isosurface(smooth3(single(organs.img)==i),.5);
    p=patch(Org);
    set(p,'facecolor',map(i,:),'edgecolor','none')
    if((i>3)||(i<2))
        set(p,'facealpha',.2);
    end
    
end



%% Step 6: Setup the light(s). the l object has lots of options
% that can be accessed via set/get
l = light;
view(40,30);
axis off
set(gcf,'color','w')
lighting GOURAUD

%% Step 7: Be VERY sure to set the data aspect ratio!!!
daspect(1./CT.hdr.PixelDimensions)

%% Step 8: Setup the axes. If you dont have this manual settings, 
% the video might be jumpy
set(gca,'CameraViewAngleMode','Manual');
axis([100 500 0 458 0 140])

%% Step 9: The options here are super easy. I used to do this by hand
% but this library is nice. 
OptionZ.FrameRate=30;OptionZ.Duration=20;OptionZ.Periodic=true;
CaptureFigVid([-20,10;-110,10;-190,80;-290,10;-380,10], 'DemoVideo-NotABrain-v1',OptionZ)