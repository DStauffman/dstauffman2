function [pos_out,sat_pos_out] = position_finder(rcvr,eph)

%send this script the latest (greatest TOW) ephemeris data for each
%satellite in the receiver file, doesn't have to be in correct order, just
%has to have all of the latest ephemeris for all of the sats the receiver
%sees (and not the ephemeris for sats the receiver does not see)

%send this script the receiver file for the last TOW, number of satellites
%in view long

%for example we would call this function at every time step, and send it
%the corresponding set of data.  For the first time step of data we
%collected at Dave's place the "data files" I would want would be rcvr and
%eph data cut the following way from e79380 and r79380

%note there are no Ionoshere or troposphere corrections yet

tu        = rcvr(:,1);
PRN_rec   = rcvr(:,2);
rho       = rcvr(:,3);

PRN_eph   = eph(:,2);
toc       = eph(:,3);
toe       = eph(:,4);
af0       = eph(:,5);
af1       = eph(:,6);
af2       = eph(:,7);
e         = eph(:,9);
sqrt_a    = eph(:,10);
delta_n   = eph(:,11);
M0        = eph(:,12);
omega     = eph(:,13);
OMEGA_0   = eph(:,14);
i0        = eph(:,15);
OMEGA_dot = eph(:,16);
IDOT      = eph(:,17);
cus       = eph(:,18);
cuc       = eph(:,19);
cis       = eph(:,20);
cic       = eph(:,21);
crs       = eph(:,22);
crc       = eph(:,23);

%Initial position guess in ecef
lat = 37.0; lon = -122.5; h = 0;
x0 = wgslla2xyz(lat, lon, h);

%Find 3D position of Satellite by iteration on transmission time

c = 299792458; %speed of light 

sat_bias = zeros(1,length(PRN_rec));
for j = 1:length(PRN_rec)       %loop over number of sats in receiver file
    dt = rho(j)/c;              %transmission time estimate (receiver file order)
    delta_t = 1;
    while delta_t >.001         %iterate transmission time for each satellite
        t(j) = tu(j) - dt;      %time of transmission

        %pick which data to use together
        for i = 1:length(PRN_rec)
            if PRN_rec(i) == PRN_rec(j)
                sr = i;         %sr = i = j = line of receiver file
            end
            if PRN_eph(i) == PRN_rec(j)
                se= i;          %se = i ~= j = line of ephemeris file
            end
        end

        [sat_pos,sat_clock_bias] = satellite_position_and_bias(t(sr),sqrt_a(se),toe(se), delta_n(se),M0(se),e(se), omega(se), cus(se), cuc(se), crs(se), crc(se), cis(se), cic(se), i0(se), IDOT(se),OMEGA_0(se), OMEGA_dot(se), af0(se), af1(se), af2(se),toc(se));
        Omega_Earth = 7292115.1467e-11; %rad/sec
        theta = Omega_Earth*dt;
        sat_pos_ecef = [cos(theta) sin(theta) 0 ; -sin(theta) cos(theta) 0; 0 0 1]*sat_pos;
        [pred_range, G_row ] = GPS_Range( sat_pos_ecef', x0');
        dt_new = pred_range/c;
        delta_t = dt_new-dt;
        dt = dt_new;
    end
    sat_pos_final(j*3-2:j*3) = sat_pos_ecef;  %row of all satellite positions for this time epoch
    sat_bias(j) = sat_clock_bias;             %row of all satellite clock biases for that time epoch
end

%iterate to find position
b0 = 0; %initial receiver clock bias
delta_matrix = 100*ones(1,4);

clear pred_range G_row del_rho 
while(norm(delta_matrix) > .01) %loop while rss delta is > .01m accuracy

for m = 1:length(sat_pos_final)/3 %number of sats
[ pred_range(m), G_row(m,:) ] = GPS_Range( sat_pos_final(m*3-2:m*3), x0');
end
G = G_row;
del_rho = (rho' - pred_range - repmat(b0,1,length(rho)) + sat_bias)';

%least squares
delta_matrix = inv(G'*G)*G'*del_rho;
%iterate
x0 = x0 + delta_matrix(1:end-1);
b0 = b0+ delta_matrix(end);

end
pos = x0;
[lat, lon, alt] = wgsxyz2lla(pos);

pos_out = [lon; lat; alt];
sat_pos_out = sat_pos_final;