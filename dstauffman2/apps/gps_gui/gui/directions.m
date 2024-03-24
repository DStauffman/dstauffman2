function [direction,handles] = directions(pos_save,location_name,location_data,handles)

% Function directs tourist to locations still undiscovered

% initialize output
direction =[];

% setup octants
direct{1} = 'straight';
direct{2} = 'slight left';
direct{3} = 'left';
direct{4} = 'hard left';
direct{5} = 'behind';
direct{6} = 'hard right';
direct{7} = 'right';
direct{8} = 'slight right';

% pull out user position
user = pos_save(1:2,end);

% calculate the heading vector based on a minimum threshold distance traveled
dist_trav = handles.move_limit - 1;  % just below threshold (too little movement)
j = 0;
while dist_trav < handles.move_limit
    dist_trav = distance(user,pos_save(:,end-j));
    j = j + 1;
    if j>100
        % no current heading, because you aren't moving
        draw_bearing('none',handles);
        return
    elseif j >= size(pos_save,2)
        % no current heading, because you haven't moved far enough
        draw_bearing('none',handles);
        break
    end
end

oldvec = [0;0];
if j < size(pos_save,2)
    for q = 1:j
        [crap,newvec] = distance(pos_save(1:2,end), pos_save(1:2,end-q)); %in enu
        oldvec = oldvec + newvec;
    end
    heading = oldvec;
else
    heading = [1;0];
end
poi = location_data;
poi_label = location_name;

% determine closest undiscovered POI
% find distances in meters from user to each POI
dist = zeros(length(poi_label),1);
min_dist = inf;
for i = 1:length(poi_label)
    dist(i,1) = distance(user,poi(i,:));
    if dist(i,1) < min_dist && (all(handles.poi_been~=i) || isempty(handles.poi_been))
        min_dist = dist(i,1);
        closest_new_poi = poi_label(i);
        ind = i;    % index of closest_new_poi
    end
    if length(handles.poi_been) == length(poi_label)
        % all landmarks have been visited
        draw_bearing('none',handles);
        handles.navigate_poi = 'none';
        handles.distance_poi = 0;
        update_navigation(handles);
        return
    end
end

% bearing to closest new poi from current position
[crap,bearing] = distance(poi(ind,:)' , pos_save(1:2,end)); %in enu
dist_to_go = norm(bearing);             % distance to closest new poi
handles.distance_poi = dist_to_go;
a = dot(heading,bearing);
b = det([heading'; bearing']);

% Angle [0,pi) from heading vector to bearing vector
angle_temp = acos(dot(heading,bearing)/(norm(heading)*norm(bearing)));

if a >= 0 && b >= 0
    angle = angle_temp;
elseif a >=0 && b < 0
    angle = -angle_temp;
elseif a < 0 && b >= 0
    angle = angle_temp;
else
    angle = -angle_temp;
end

% Map angles on integer scale from 1 to 8 (corresponding to above directions)
octant = round(angle*8/(2*pi))+1;
if octant >= 9
    octant = octant - 8;
elseif octant <= 0
    octant = octant + 8;
end
direction = direct{octant};

% update closest new poi
handles.navigate_poi = char(closest_new_poi);
draw_bearing(direction,handles);