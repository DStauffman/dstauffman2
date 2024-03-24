%% Create GUI window
function varargout = gps_gui(varargin)
% GPS_GUI M-file for gps_gui.fig
%      GPS_GUI, by itself, creates a new GPS_GUI or raises the existing
%      singleton*.
%
%      H = GPS_GUI returns the handle to a new GPS_GUI or the handle to
%      the existing singleton*.
%
%      GPS_GUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GPS_GUI.M with the given input arguments.
%
%      GPS_GUI('Property','Value',...) creates a new GPS_GUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before gps_gui_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to gps_gui_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @gps_gui_OpeningFcn, ...
                   'gui_OutputFcn',  @gps_gui_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


function gps_gui_OpeningFcn(hObject, eventdata, handles, varargin) %#ok
% --- Executes just before gps_gui is made visible.
% add tree logo
tree = importdata(fullfile('..','images','stanford_tree.png'));
stanford_tree = ind2rgb(tree.cdata,tree.colormap);
set(handles.gps_figure,'CurrentAxes',handles.axes_tree_logo);
image(stanford_tree);
axis equal;
axis off;
% add seal logo
seal = importdata(fullfile('..','images','stanford_seal.png'));
stanford_seal = ind2rgb(seal.cdata,seal.colormap);
set(handles.gps_figure,'CurrentAxes',handles.axes_seal_logo);
image(stanford_seal);
axis equal;
axis off;
% draw map
set(handles.gps_figure,'CurrentAxes',handles.axes_map);
plot_map(handles.location_data);
% draw stanford image
stanford_image = importdata(fullfile('..','images','stanford.png'));
set(handles.gps_figure,'CurrentAxes',handles.axes_info);
image(stanford_image);
axis equal;
axis off;
% draw empty compass bearing
bearing = importdata(fullfile('..','images','turn_none.png'));
set(handles.gps_figure,'CurrentAxes',handles.axes_bearing);
image(bearing);
axis equal;
axis off;
% play welcome audio
yy = wavread(fullfile('..','images','intro.wav'));
wavplay(yy,'async');
% update gui
guidata(hObject, handles); % Update handles structure
uiwait(hObject);


function varargout = gps_gui_OutputFcn(hObject, eventdata, handles) %#ok
% --- Outputs from this function are returned to the command line.
varargout{1} = handles;


%% Buttons
function button_start_Callback(hObject, eventdata, handles) %#ok
% --- Executes on Start button
global run_main_loop
run_main_loop = true;
%TODO - figure out how to get the names dynamically
% eph_file = fullfile('..','..','e183524.dat');
% obs_file = fullfile('..','..','r183524.dat');
eph_file = fullfile('..','data','e_test.dat');
obs_file = fullfile('..','data','r_test.dat');
% call the main loop
handles = main_loop(handles,eph_file,obs_file,handles.location_name,handles.location_data);
% update gui
guidata(hObject,handles);


function button_pause_Callback(hObject, eventdata, handles) %#ok
% --- Executes on Pause button
global run_main_loop
run_main_loop = false;
% update gui
guidata(hObject,handles);


function button_reset_Callback(hObject, eventdata, handles) %#ok
% --- Executes on Reset button
global run_main_loop
run_main_loop = false;
clear distancing
% redo initialization
[hObject,handles] = initialize_defaults(hObject,handles);
% update navigation
update_navigation(handles);
% draw map
set(handles.gps_figure,'CurrentAxes',handles.axes_map);
plot_map(handles.location_data);
% draw empty compass bearing
bearing = importdata(fullfile('..','images','turn_none.png'));
set(handles.gps_figure,'CurrentAxes',handles.axes_bearing);
image(bearing);
axis equal;
axis off;
% update gui
guidata(hObject,handles);


function button_replay_last_Callback(hObject, eventdata, handles) %#ok
% --- Executes on Replay Audio button
% replay last location
if ~isempty(handles.poi_been)
    history(handles,handles.location_name{handles.poi_been(end)});
else
    disp('TODO');
%     yy = wavread(fullfile('..','images','no_landmark.wav'));
%     wavplay(yy,'async');
end
% update gui
guidata(hObject,handles);


%% Create functions
function textbox_info_CreateFcn(hObject, eventdata, handles) %#ok
% --- info edit box creation
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
% do initialization once this box is created
[hObject,handles] = initialize_defaults(hObject,handles);
% load text to display at startup
welcome_text = textread(fullfile('..','images','welcome_text.txt'),'%s','delimiter','\n');
set(hObject,'String',welcome_text);
% update gui
guidata(hObject,handles);


function edit_closest_to_CreateFcn(hObject, eventdata, handles) %#ok
% --- closest to edit box creation
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
% update gui
guidata(hObject,handles);


function edit_navigating_to_CreateFcn(hObject, eventdata, handles) %#ok
% --- navigating to edit box creation
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
% update gui
guidata(hObject,handles);


function edit_distance_to_CreateFcn(hObject, eventdata, handles) %#ok
% --- distance to edit box creation
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
% update gui
guidata(hObject,handles);


function edit_num_sats_CreateFcn(hObject, eventdata, handles) %#ok
% --- number of satellites edit box creation
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
% update gui
guidata(hObject,handles);


%% Close functions
function gps_figure_CloseRequestFcn(hObject, eventdata, handles) %#ok
% --- Executes when user attempts to close gps_figure.
global run_main_loop
run_main_loop = false;
uiresume(handles.gps_figure);
% wait one second to delete figure
t = timer('TimerFcn','delete(handles.gps_figure)','StartDelay',1);
start(t);


%% Initialization function
function [hObj_out,hand_out] = initialize_defaults(hObject, handles)
% --- initializes all the handles
global run_main_loop
global quit_gui
run_main_loop         = false;
quit_gui              = false;
handles.location_name = {'main_quad','durand','tower','oval','bookstore'};
handles.location_data = [...
    -122.170352175455 37.4273187226277;...
    -122.173158285714 37.4266529172749;...
    -122.167098714286 37.4275806788321;...
    -122.169552366251 37.429687243309;...
    -122.169240576222 37.4247319051095];
handles.pos_save      = [];
handles.sat_pos_save  = [];
handles.poi_been      = [];
handles.closest_poi   = 'unknown';
handles.navigate_poi  = 'none';
handles.distance_poi  = 0;
handles.manual_choice = false;
handles.prox_limit    = 25;
handles.move_limit    = 15;
handles.num_sats      = 0;
% flag to check if initialization has been executed
handles.initialized     = true;
% update GUI
guidata(hObject,handles);
% pass output back
hObj_out = hObject;
hand_out = handles;

