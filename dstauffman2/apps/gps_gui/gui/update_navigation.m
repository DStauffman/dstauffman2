function update_navigation(handles)

% UPDATE_NAVIGATION  updates the closest to, navigating to, and distance boxes

% update closest to box
switch handles.closest_poi
    case 'unknown'
        closest_text = 'Unknown';
    case 'main_quad'
        closest_text = 'Main Quad';
    case 'durand'
        closest_text = 'Durand Building';
    case 'tower'
        closest_text = 'Hoover Tower';
    case 'oval'
        closest_text = 'Oval';
    case 'bookstore'
        closest_text = 'Bookstore';
    otherwise
        error('Unexpected landmark');
end
set(handles.edit_closest_to,'String',closest_text);

% update navigating to box
switch handles.navigate_poi
    case 'none'
        navigate_text = 'None';
    case 'main_quad'
        navigate_text = 'Main Quad';
    case 'durand'
        navigate_text = 'Durand Building';
    case 'tower'
        navigate_text = 'Hoover Tower';
    case 'oval'
        navigate_text = 'Oval';
    case 'bookstore'
        navigate_text = 'Bookstore';
    otherwise
        error('Unexpected landmark');
end
set(handles.edit_navigating_to,'String',navigate_text);

% update distance box
if handles.distance_poi == 0
    distance_text = 'N/A';
else
    distance_text = [num2str(handles.distance_poi,'%3.1f'),' meters'];
end
set(handles.edit_distance_to,'String',distance_text);

% update number of satellites box
set(handles.edit_num_sats,'String',int2str(handles.num_sats));