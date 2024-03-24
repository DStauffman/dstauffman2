
function [ pred_range, G_row ] = GPS_Range( sat_pos, rec_pos)

%AA272C HW#1
%Problem 4
%Tom Chouinard
%Input position vectors of satellite in vector form, followed by receiver
%in vector form, in ECEF coordinates
%function [ pred_range, G ] = GPS_Range( sat_pos, rec_pos)

range = sat_pos - rec_pos;
pred_range = norm(range);
G_row = [-range/pred_range 1];


end
