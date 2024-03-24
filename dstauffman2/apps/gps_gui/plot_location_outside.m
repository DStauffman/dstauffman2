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
    xc = mean(bounds([1 2]));
    yc = mean(bounds([3 4]));
    if loc(1) < bounds(1)
        x = bounds(1);
    elseif loc(1) > bounds(2)
        x = bounds(2);
    else
        x = loc(1);
    end
    if loc(2) < bounds(3)
        y = bounds(3);
    elseif loc(2) > bounds(4)
        y = bounds(4);
    else
        y = loc(2);
    end
    theta = atan2(loc(2),loc(1));
    rx = (x-xc)*cos(theta)/diff(bounds([1 2]))*2;
    ry = (y-yc)*sin(theta)/diff(bounds([3 4]))*2;
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
            out = annotation('arrow',rx*[1 0.8],ry*[1 0.8],'HeadStyle','vback1','Color','r');
        end
    case 'small_user'
        if within
            out = plot(loc(1),loc(2),'x','Color','r','MarkerSize',05,'LineWidth',1.5);
        else
            out = annotation('arrow',rx*[1 0.8],ry*[1 0.8],'HeadStyle','vback1','Color','r');
        end
    case 'path'
        out = plot(loc(1),loc(2),'x','Color','g','MarkerSize',15,'LineWidth',3);
    case 'question'
        out = plot(loc(1),loc(2),'x','Color','k','MarkerSize',15,'LineWidth',3);
    otherwise
        error('Unexpected type');
end