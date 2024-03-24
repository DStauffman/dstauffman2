function [sat_pos,sv_clock ] = satellite_position_and_bias(t,sqrt_a,toe, delta_n,M0,e, omega, cus, cuc, crs, crc, cis, cic, i0, IDOT,OMEGA_0, OMEGA_dot, af0, af1, af2,toc )
%Outputs satellite position in ECEF coordinates given satellite ephemeris
%as in IS-GPS-200D.pdf page 98. Also ouputs satellite clock bias in meters.

c = 299792458; %speed of light 
mu = 3.986005e14; %m^3/s^2 (Earth)
omega_earth_dot = 7.2921151467e-5; %rad/s (Earth Rotation)
a = sqrt_a^2;
n0 = sqrt(mu/a^3);          %mean motion
tk = t - toe;               %time from epoch
%correct for week crossovers
if tk>302400
    tk = tk-604800;
elseif tk<-302400
    tk = tk + 604800;
end

n = n0+delta_n;             %corrected mean motion
Mk = M0 +n*tk;              %Mean anomaly

Ek = eccentric(Mk, e);      %Eccentric anomaly
nuk = atan2((sqrt(1-e^2).*sin(Ek)),(cos(Ek)-e));   %True anomaly

%Correct atan2 sign for plotting
if nuk<0
        nuk = nuk+2*pi;
end

Phi_k = nuk+omega;

delta_uk = cus*sin(2*Phi_k) + cuc*cos(2*Phi_k);
delta_rk = crs*sin(2*Phi_k) + crc*cos(2*Phi_k);
delta_ik = cis*sin(2*Phi_k) + cic*cos(2*Phi_k);

uk = Phi_k+delta_uk;
rk = a*(1-e*cos(Ek)) + delta_rk;
ik = i0 + delta_ik + IDOT*tk;

xk_prime = rk*cos(uk);
yk_prime = rk*sin(uk);

OMEGAk = OMEGA_0 + (OMEGA_dot - omega_earth_dot)*tk - omega_earth_dot*toe;

xk = xk_prime*cos(OMEGAk) - yk_prime*cos(ik)*sin(OMEGAk);
yk = xk_prime*sin(OMEGAk) + yk_prime*cos(ik)*cos(OMEGAk);
zk = yk_prime*sin(ik);

sat_pos = [xk;yk;zk];

delta_t = af0+af1*(t - toc)+af2*(t - toc)^2+ -2*sqrt(mu)/(c^2)*e*sqrt_a*sin(Ek);

sv_clock = delta_t*c;