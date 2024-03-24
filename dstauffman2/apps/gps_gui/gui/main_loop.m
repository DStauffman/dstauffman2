function [handles] = main_loop(handles,eph_file,obs_file,location_name,location_data)

% MAIN_LOOP  runs the main GPS solver loop

% declare global - set to true or false to start or stop this file
global run_main_loop

% Initialize stored vectors of satellite position and user position for post processing
pos_save = zeros(3,0);
sat_pos_save = zeros(0,45);

while run_main_loop
    % read data from file
    obs_full = textread(obs_file);
    tow      = obs_full(end,1);
    row      = find(obs_full(:,1)~=tow,1,'last')+1;
    obs      = obs_full(row:end,:);
    eph_full = textread(eph_file);
    % put newest data on top
    [junk,ix_sort]        = sort(eph_full(:,1),'descend');
    eph_full              = eph_full(ix_sort,:);
    [svid,ix_eph,ix_obs]  = intersect(eph_full(:,2),obs(:,2));
    obs                   = obs(ix_obs,:);
    svid_obs              = obs(:,2);
    handles.num_sats      = length(svid_obs);
    % update number of satellites
    update_navigation(handles);
    eph                   = eph_full(ix_eph,:);
    %avoid sparse matricies with too few sats
    if handles.num_sats > 3
        % pass data to position finder
        % preload satellite vector with zeros b/c # sats changing
        sat_pos_save(end+1,:) = zeros(1,45); %#ok - allow to grow

        % note we are storing the satellite position vector as one row #sats*3
        % long, in ecef xyz coordinates, and user position as 3x1 column vector
        % at each epoch, in lat lon height.
        [pos_save(1:3,end+1), sat_pos_save(end,1:length(svid_obs)*3)] = position_finder(obs,eph);  %#ok - allow to grow

        % set map as current figure and new draw user location
        if exist('user','var')
            delete(user);
        end
        set(handles.gps_figure,'CurrentAxes',handles.axes_map);
        user = plot_location(pos_save(1:2,end),'user');

        % calculate distances to all landmarks and display info on gui
        [direction,handles] = distancing(handles,pos_save(1:2,end),location_name,location_data,pos_save(1:2,:));
        update_navigation(handles);

        % wait for next update cycle
        pause(0.15);

        % set map as current figure and delete user
        set(handles.gps_figure,'CurrentAxes',handles.axes_map);
        delete(user);
        bounds = axis;
        user = plot_location(pos_save(1:2,end),'small_user',bounds);

        % wait for next update cycle
        pause(0.25);
    else
        draw_bearing('none',handles);
        pause(0.3);
    end
    % update gui with most current handles structure
    guidata(handles.gps_figure,handles);
end
if exist('user','var')
    delete(user)
end
% store outputs in handles structure
handles.pos_save     = pos_save;
handles.sat_pos_save = sat_pos_save;