projs = {'raw_data/NORMAL', 'raw_data/BLSA', 'raw_data/HCP'};

for proj = 1:length(projs)
   subjs = dir(projs{proj});
   subjs = subjs(3:end);
   
   for s = 1:length(subjs)
       subj = fullfile(subjs(s).folder, subjs(s).name);
       if isdir(subj)==1
           sesss = dir(subj);
           sesss = sesss(3:end);
           for ss = 1:length(sesss)
               sess = fullfile(sesss(ss).folder, sesss(ss).name);

                if isdir(fullfile(sess, 'derivatives', 'AFQ_clipped'))==1 && ~isfile(fullfile(sess, 'QA', 'AFQ_clippedQA.tif'))
                    disp(sess);
                    QA_AFQ_clipped(sess);
                end
           end
       end
   end
end
