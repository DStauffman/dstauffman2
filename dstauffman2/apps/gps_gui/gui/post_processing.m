function [] = post_processing(sat_pos, user_pos)

%This function is to be called after collecting data, and passed the handle
%of satellite positions and user positions from the gui over the collected
%data period.  The output is the DOPs over time and the average and
%standard deviation of ENU positions

ref_point = [-2700326.0126 -4292620.3858 3855138.7591];
[lat_ref, lon_ref, alt_ref] = wgsxyz2lla(ref_point);        %reference point near durand

for n = 1:length(user_pos)  %over all time epochs
    clear sat_pos_cut sat_pos_final G_row g
    user_enu(:,n) = wgslla2enu(user_pos(2,n),user_pos(1,n),user_pos(3,n), lat_ref, lon_ref, alt_ref);

    %Find G matrix in ENU frame for all epochs

    sat_pos_cut = sat_pos(n,:)~=0;
    sat_pos_final = sat_pos(n,sat_pos_cut);
    for m = 1:length(sat_pos_final)/3
        enu_sats(m*3-2:m*3) = wgsxyz2enu(sat_pos_final(m*3-2:m*3)', lat_ref, lon_ref, alt_ref);
        [ pred_range(m), G_row(m,:) ] = GPS_Range( enu_sats(m*3-2:m*3), user_enu(:,n)');
    end
    g = inv(G_row'*G_row);
    GDOP(n) = sqrt(g(1,1)+g(2,2)+g(3,3)+g(4,4));
    EDOP(n) = sqrt(g(1,1));
    NDOP(n) = sqrt(g(2,2));
    VDOP(n) = sqrt(g(3,3));
    TDOP(n) = sqrt(g(4,4));
    num_sats(n) = length(sat_pos_final)/3;

end
%Averages over time of sample
ave_num_sats = mean(num_sats)
ave_GDOP = mean(GDOP)
ave_EDOP = mean(EDOP)
ave_NDOP = mean(NDOP)
ave_VDOP = mean(VDOP)
ave_TDOP = mean(TDOP)
ave_user_pos_enu = sum(user_enu')/length(user_enu)
enu_pos_std = std(user_enu')

figure, plot3(user_enu(1,:), user_enu(2,:),user_enu(3,:),'.k')
title('Position from enu reference coordinates')
xlabel('East (m)')
ylabel('North (m)')
zlabel('Up (m)')
axis equal