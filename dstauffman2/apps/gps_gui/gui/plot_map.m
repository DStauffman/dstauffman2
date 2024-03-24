function [] = plot_map(locations_data)

% PLOT_MAP  plots the Stanford Campus Map

% given (at Stanford)
lat_min =  37.422669;
lat_max =  37.431641;
lng_min = -122.177198;
lng_max = -122.163059;

% load campus map
campus_map = importdata(fullfile('..','images','campus_map.png'));

% create map
image([lng_min lng_max],[lat_min lat_max],campus_map(end:-1:1,:,:));
ax = get(gcf,'CurrentAxes');
set(ax,'YDir','normal');
xlabel('Longitude [\circ]');
ylabel('Latitude [\circ]');
axis off;
hold on;

for i = 1:size(locations_data,1);
    plot_location(locations_data(i,:),'landmark');
end