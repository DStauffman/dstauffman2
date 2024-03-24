function [direction,handles] = distancing(handles,user,location_name,location_data, pos_save)

% DISTANCING  calculates the distance to all landmarks and displays info
%     if within the threshold of any of them.

persistent finished

% initialize finished variable
if isempty(finished)
    finished = true;
end

% only run if finished with the last call
if finished
    finished = false; %#ok - may be used in separate call
    poi = location_data;
    poi_label = location_name;

    % find distances in meters from user to each POI
    dist = zeros(length(poi),1);
    for i = 1:length(poi)
        dist(i,1) = distance(user,poi(i,:));
    end

    % Closest POI to user
    r = find(dist==min(dist));    % r is just an index
    handles.closest_poi = char(poi_label(r));

    % determine if within threshold
    if dist(r) <= handles.prox_limit
        if ~any(handles.poi_been==r)
            handles.navigate_poi = char(poi_label{r});
            handles.distance_poi = dist(r);
            update_navigation(handles);
            history(handles,poi_label{r});
            handles.poi_been = [handles.poi_been r];
            % set map as current figure and change color of landmark
            set(handles.gps_figure,'CurrentAxes',handles.axes_map);
            plot_location(handles.location_data(r,:),'visited');
        end
    end

    % set to know that this loop is finished
    finished = true;
else
    return
end

% update directions
[direction,handles] = directions(pos_save,location_name,location_data,handles);