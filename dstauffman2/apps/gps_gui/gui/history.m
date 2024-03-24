function [directory,folder] = history(handles,poi_label)

% HISTORY displays the images, audio and text history about the desired landmark

% get information about all the files in the directory
directory = fullfile(cd,['..',filesep],poi_label);
folder = dir(directory);
num = length(folder)-2;

if num < 1
    error('No landmark folders were found');
end

% initial variables
file = cell(1,num);
type = cell(1,num);

% loop through files
for i = 1:num
    file{i} = [directory,filesep,folder(i+2).name];
    % find filetype
    type{i} = file{i}(end-2:end);
end

% find the first txt file, then the first wav file, then loop through the rest
wav_file = find(strcmp(type,'wav'),1,'first');
txt_file = find(strcmp(type,'txt'),1,'first');
ix = [txt_file wav_file setxor(1:num,[txt_file, wav_file])];

for i=ix
    switch type{i}
        case 'wav'
            % play audio
            m = wavfinfo(file{i});
            if ~isempty(m)
                yy = wavread(file{i});
                wavplay(yy,'async');
            end
        case {'jpg','gif','png'}
            % display picture
            picture = importdata(file{i});
            if isfield(picture,'cdata');
                picture = ind2rgb(picture.cdata,picture.colormap);
            end
            set(handles.gps_figure,'CurrentAxes',handles.axes_info);
            image(picture);
            axis off;
            axis equal;
            axis tight;
            pause(3);
        case 'txt'
            % display text to gui
            info_text = textread(file{i},'%s','delimiter','\n');
            set(handles.textbox_info,'String',info_text);
        otherwise
            % nop - skip this file
    end
end

% redraw stanford image
stanford_image = importdata(fullfile('..','images','stanford.png'));
set(handles.gps_figure,'CurrentAxes',handles.axes_info);
image(stanford_image);
axis equal;
axis off;

% put original text back
welcome_text = textread(fullfile('..','images','welcome_text.txt'),'%s','delimiter','\n');
set(handles.textbox_info,'String',welcome_text);