out_dir = '/nfs/masi/hansencb/WM_Atlas_Learning/visualizations/surfaces_rendering';
mkdir(out_dir);

atlases = {'/nfs/masi/hansencb/t1_tract_data/Atlases/TractSegAtlases/', ...
    '/nfs/masi/hansencb/t1_tract_data/Atlases/TraculaAtlases/', ...
    '/nfs/masi/hansencb/t1_tract_data/Atlases/RecobundlesAtlases/', ...
    '/nfs/masi/hansencb/t1_tract_data/Atlases/XtractAtlases/', ...
    '/nfs/masi/hansencb/t1_tract_data/Atlases/AFQAtlases/', ...
    '/nfs/masi/hansencb/t1_tract_data/Atlases/AFQclippedAtlases/'};

atlas_names = {'TractSeg', 'Tracula', 'Recobundles', 'Xtract', 'AFQ', 'AFQclipped'};

reg_types = {'Linear', 'Nonlinear'};


for at = 1:length(atlases)
    atlas = atlases{at};
    name = atlas_names{at};
    for r = 1:length(reg_types)
        reg = reg_types{r};
        path = fullfile(atlas, [name reg '_ALL.nii.gz']);

        %% Quick demo on how to make a "spinning fiber brain"
        % This version was created by Bennett Landman 
        % April 23, 2020 
        % PLEASE adjust the options and create new demo videos. 
        % Feel free to include public data in this repo. 
        % Save all needed files internally here. 

        %% Set paths (be sure to save all the paths that you need
        addpath(genpath(pwd))

        %% Step 1: Load the data

        %reco = niftiread('RecobundlesNonlinear_ALL.nii.gz');
        %recoInfo = niftiinfo('RecobundlesNonlinear_ALL.nii.gz');
        reco = niftiread(path);
        recoInfo = niftiinfo(path);


        %%Step 2: Start a new figure
        figure(1);
        clf
        clr = distinguishable_colors(size(reco,4));


        %% Step 3: For each volume  make a face/vertex masking

        for j=1:size(reco,4)
            disp([j size(reco,4)])
            L = linspace(0.5,.9,10); %[0.1 0.25 0.5 0.75];
            A = linspace(.01, .1, length(L));



            for i=1:length(L)
                % play with the contours and the cleaning until it makes sense
                lev1 = isosurface(smooth3(reco(:,:,:,j)),L(i));

                % render the face/vertex
                p=patch(reducepatch(reducepatch(lev1,.2),.2));
                set(p,'edgecolor','none','FaceColor',clr(j,:),'facealpha',A(i))
                hold on
            end
            drawnow
        end


        axis off
        axis equal 
        set(gcf,'color','k')



        %% Step 6: Setup the light(s). the l object has lots of options
        % that can be accessed via set/get
        %l = light;
        view(40,30);
        axis off
        %set(gcf,'color','w')
        %lighting GOURAUD
 
        set(gca, 'color', 'black');
        set(gcf, 'InvertHardcopy', 'off')
        view(0,0);
        saveas(gcf, fullfile(out_dir, [name reg '_sagittal.png']));

        view(90,0);
        saveas(gcf,fullfile(out_dir, [name reg '_coronal.png']));

        view(90,90);
        saveas(gcf,fullfile(out_dir, [name reg '_axial.png']));

        % %% Step 7: Be VERY sure to set the data aspect ratio!!!
        % daspect(1./recoInfo.PixelDimensions(1:3))
        % 
        % %% Step 8: Setup the axes. If you dont have this manual settings, 
        % % the video might be jumpy
        % set(gca,'CameraViewAngleMode','Manual');
        % axis([30 202 32 162 5 160])

        % %% Step 9: The options here are super easy. I used to do this by hand
        % % but this library is nice. 
        % OptionZ.FrameRate=30;OptionZ.Duration=20;OptionZ.Periodic=true;
        % CaptureFigVid([-20,10;-110,10;-190,80;-290,10;-380,10], 'DemoVideo-Fibers-v1',OptionZ)
    end
end