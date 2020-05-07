%projs = {'raw_data/BLSA', 'raw_data/HCP', 'raw_data/NORMAL'};

%for proj = 1:length(projs)
%    subjs = dir(projs{proj});
%    subjs = subjs(3:end);
%    
%    for s = 1:length(subjs)
%        subj = fullfile(subjs(s).folder, subjs(s).name);
%        if isdir(subj)==1
%            sesss = dir(subj);
%            sesss = sesss(3:end);
%            for ss = 1:length(sesss)
%                sess = fullfile(sesss(ss).folder, sesss(ss).name);

list = '~/Downloads/QA_list.csv';
T = readtable(list,'Delimiter',',','ReadVariableNames',true);
for i = 1:length(T.path_to_sess)
    sess = T.path_to_sess{i};

                if isdir(fullfile(sess, 'reg'))==1 %&& ~isfile(fullfile(sess, 'QA', 'NONRigid_registration.tif'))
                    disp(sess);
                    QA_Registration(sess);
                end
%            end
%        end
%    end
%end
end
