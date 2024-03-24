function draw_bearing(direction,handles)

% DRAW_BEARING  draws the bearing arrows on the GUI

% determine which image to load
fullpath = [fullfile('..','images'),filesep];
switch direction
    case 'none'
        bearing = importdata([fullpath,'turn_none.png']);
    case 'straight'
        bearing = importdata([fullpath,'turn_straight.png']);
    case 'slight right'
        bearing = importdata([fullpath,'turn_slight_right.png']);
    case 'right'
        bearing = importdata([fullpath,'turn_right.png']);
    case 'hard right'
        bearing = importdata([fullpath,'turn_hard_right.png']);
    case 'behind'
        bearing = importdata([fullpath,'turn_around.png']);
    case 'hard left'
        bearing = importdata([fullpath,'turn_hard_left.png']);
    case 'left'
        bearing = importdata([fullpath,'turn_left.png']);
    case 'slight left'
        bearing = importdata([fullpath,'turn_slight_left.png']);
    otherwise
        error('Unexpected direction');
end
% display image on the GUI
set(handles.gps_figure,'CurrentAxes',handles.axes_bearing);
image(bearing);
% turn off axis
axis equal;
axis off;