function [howfar,orientation_vector] = distance(user_pos,poi_pos)

ref_point = [-2700326.0126 -4292620.3858 3855138.7591];
[lat_ref, lon_ref, alt_ref] = wgsxyz2lla(ref_point);     

user_enu = wgslla2enu(user_pos(2),user_pos(1),0, lat_ref, lon_ref, alt_ref);
poi_enu = wgslla2enu(poi_pos(2), poi_pos(1),0,lat_ref, lon_ref, alt_ref);

orientation_vector = poi_enu(1:2)-user_enu(1:2); %this is enu
howfar = norm(poi_enu(1:2)-user_enu(1:2));