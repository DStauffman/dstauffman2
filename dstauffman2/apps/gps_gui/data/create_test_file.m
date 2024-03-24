function [] = create_test_file(obs_orig,obs_file,eph_orig,eph_file,start_line,end_line)

% CREATE_TEST_FILE  reads in the original saved reciever file, and reproduces it in real-time
% 
% Prototype:
%     obs_orig = 'r548582.dat';
%     obs_file = 'r_test.dat';
%     eph_orig = 'e548582.dat';
%     eph_file = 'e_test.dat';
%     start_line = 500;
%     end_line = 750;
%     create_test_file(obs_orig,obs_file,eph_orig,eph_file,start_line,end_line);

% read in the original observation file
strs = textread(obs_orig,'%s','delimiter','\n');
data = textread(obs_orig);

% read in the ephemeris file
eph_strs = textread(eph_orig,'%s','delimiter','\n');
eph_data = textread(eph_orig);

% parse input
if ~exist('start_line','var')
    start_line = 1;
end
if ~exist('end_line','var');
    end_line = length(strs);
end

% delete lines to leave only desired pieces
strs(end_line+1:end)   = [];
data(end_line+1:end,:) = [];
strs(1:start_line-1)   = [];
data(1:start_line-1,:) = [];

% find index to when the times change
times = [1; find(diff(data(:,1))~=0)+1;];

% initialize index to ephemeris file
eph_line = 0;

% loop through lines
for i=1:length(times)-1
    disp(['Writing record ',int2str(i),' of ',int2str(length(times)-1)]);
    if i~= 1
        fid = fopen(obs_file,'a');
    else
        fid = fopen(obs_file,'w');
    end
    rows = times(i):times(i+1)-1;
    for j=1:length(rows)
        fwrite(fid,[char(strs(rows(j))),char(10)]);
    end
    fclose(fid);
    % update ephemeris file if necessary
    temp = find(eph_data(:,1) < data(rows(end),1),1,'last');
    if temp > eph_line
        if eph_line > 0
            fid = fopen(eph_file,'a');
        else
            fid = fopen(eph_file,'w');
        end
        rows = eph_line+1:temp;
        for j=1:length(rows)
            fwrite(fid,[char(eph_strs(rows(j))),char(10)]);
        end
        fclose(fid);
        eph_line = temp;
    end
    pause(0.2);
end