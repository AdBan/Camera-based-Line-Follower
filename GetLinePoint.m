function [x, y] = GetLinePoint(frame, height)
    %get reference/prediction pixel height
    y = floor((1 - height) * size(frame, 1));
    
    %take out whole row at calculated height of frame
    row = frame(y, :); 
    
    %get indexes of black (line) pixels
    rowLineIndexes = find(row == 1);
    
    %get index of middle of line
    if (isempty(rowLineIndexes))
        fprintf('%s: Line not found!\n', datestr(now,'HH:MM:SS.FFF'));
        x = -1; y = -1;
        return;
    else
        x = min(rowLineIndexes) + (max(rowLineIndexes) - min(rowLineIndexes)) / 2;
    end
end