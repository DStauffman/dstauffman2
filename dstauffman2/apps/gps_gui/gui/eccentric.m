function [E] = eccentric(M,e)

% ECCENTRIC [E] = eccentric(M,e)
% Calculates eccentric anomalies given mean anomaly, and eccentricity.
% All angles in radians.  Takes matrices, vectors, or scalar input.

% linear interpolation for starting guess:
E=M+(e.*sin(M)./(1-sin(M+e)+sin(M)));

% Iterate to estimate E:

y=Inf;

while max(max(abs(y)))>1.e-06
        % maximum value in y  < tolerance

   y=M+(e.*sin(E))-E;
        % difference btw prior and new est of E
   dy=e.*cos(E)-1;
        % gradient of y
   correction=y./dy;

   E=E-correction;
end
