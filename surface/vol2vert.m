% Author: Ilwoo Lyu, ilwoo.lyu@vanderbilt.edu
% this script requires FreeSurfer's MATLAB libraries

function surf_data = vol2vert(vol, v_hemi)
    mri=MRIread(vol);

    T = inv(mri.vox2ras)';
    T = [T(1, 1:3) 0; ...
         T(2, 1:3) 0; ...
         T(3, 1:3) 0; ...
         mri.volsize([2,1,3]) / 2 1];
    v=[v_hemi ones(size(v_hemi,1),1)]*T;

    nvol = size(mri.vol,4);
    surf_data = zeros(size(v_hemi,1),nvol);
    for id = 1: nvol
        vol_data = mri.vol(:,:,:,id);

        X = vol_data;
        Y = vol_data;
        Z = vol_data;
        for i = 1:size(X,2)
            X(:, i, :) = i-1;
        end
        for i = 1:size(Y,1)
            Y(i, :, :) = i-1;
        end
        for i = 1:size(Z,3)
            Z(:, :, i) = i-1;
        end

        surf_data(:,id) = interp3(X, Y, Z, vol_data, v(:,1), v(:,2), v(:,3), 'linear');
    end
end
