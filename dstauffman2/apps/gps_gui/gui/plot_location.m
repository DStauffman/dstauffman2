function out = plot_location(loc,type,bounds)

% PLOT_LOCATION  plots different object types on the GPS map

if ~exist('type','var')
    type = 'question';
end
if ~exist('bounds','var')
    bounds = [-inf inf -inf inf];
end

% determine if location is within bounds of map
if all([loc(1) > bounds(1),loc(1) < bounds(2),loc(2) > bounds(3),loc(2) < bounds(4)])
    within = true;
else
    within = false;
end

switch type
    case 'landmark'
        out = plot(loc(1),loc(2),'.','Color','b','MarkerSize',20);
    case 'visited'
        out = plot(loc(1),loc(2),'.','Color',[0.5 0 1],'MarkerSize',20);
    case 'user'
        if within
            out = plot(loc(1),loc(2),'x','Color','r','MarkerSize',15,'LineWidth',3);
        else
            % TODO: annotate that the user is off the plot
            out = plot(loc(1),loc(2),'x','Color','r','MarkerSize',15,'LineWidth',3);
        end
    case 'small_user'
        if within
            out = plot(loc(1),loc(2),'x','Color','r','MarkerSize',05,'LineWidth',1.5);
        else
            % TODO: annotate that the user is off the plot
            out = plot(loc(1),loc(2),'x','Color','r','MarkerSize',05,'LineWidth',1.5);
        end
    case 'path'
        out = plot(loc(1),loc(2),'x','Color','g','MarkerSize',15,'LineWidth',3);
    case 'question'
        out = plot(loc(1),loc(2),'x','Color','k','MarkerSize',15,'LineWidth',3);
    otherwise
        error('Unexpected type');
end