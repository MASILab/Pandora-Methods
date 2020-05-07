clear; clc; close all;

CSV = 'reg_last_check.csv'
blah = readtable(CSV);

%% run this for RIGID
% change the i=1 to whatever number you were last on
for i = 1:1000
    disp(i);
    foldername=fullfile(blah{i,2:end}{1:end});
    parts = split(foldername, ',');
    if parts{2} == '1'
        foldername = parts{1};
        foldername =  [filesep foldername];
        disp(foldername)
        QAname=[foldername filesep 'QA/Rigid_registration.tif'];

        temp = imread(QAname);
        %figure; imagesc(temp); axis equal; axis off; axis tight;
        figure; imshow(temp); axis equal; axis off; axis tight;
        title(foldername)
        pause;
        close all;
        disp('')
        disp('')
        disp('')
        disp('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx')
    end

end

%% NOTES ON RIGID
% be sure to make an X in colume 6 of table if this sucks, put notes in column 7
% be sure to mostly make sure b0 aligns with T1

%% run this on NONRIGID
for i = 1:3895
    foldername=blah{i,4};
    foldername=char(foldername);
    disp(foldername)
    QAname=[foldername filesep 'QA/NONRigid_registration.tif'];
    
    temp = imread(QAname);
    %figure; imagesc(temp); axis equal; axis off; axis tight;
    figure; imshow(temp); axis equal; axis off; axis tight;
    title(foldername)
    pause;
    close all;
    disp('')
    disp('')
    disp('')
    disp('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx')

end

%% NOTES ON NONRIGID
% be sure to make an X in colume 8 of table if this sucks, put notes in column 9

