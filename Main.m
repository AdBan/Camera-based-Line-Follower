clc; clear; close all;
%% User input

loginDataFile = 'raspberry.txt';
camHeight = 240;    %valid: 120, 240, 480, 600, 768, 1080
camWidth = 320;     %valid: 160, 320, 640, 800, 1024, 1920
camFrame = 90;      %valid: 2 to 90

lMotorPin = 'left motor';
rMotorPin = 'right motor';


%% Initialize

%[rpi, cam] = InitializePi(loginDataFile, camWidth, camHeight, camFrame, lMotorPin, rMotorPin);

f1 = figure(1); 
stopCriteria = 0; %replace with eg. lost line || end of line || obstacle

%% Loop until stop criteria is meet

while not(stopCriteria)
    %% Process frame
    
    %rgb = snapshot(cam); %capture frame
    rgb = imread('training/line_zig.png');
    grayscale = rgb2gray(rgb);
    binary = ~imbinarize(grayscale);
    closed = imclose(binary, strel('square', 10));
    frame = closed;
    
    f1; cla; imshow(rgb); hold on;
    
    
    %% Determine slope based on reference and prediction point
    
    for i = 1 : 9
        [x(i), y(i)] = GetLinePoint(frame, i/10);    %get 10 equally distributed points
    end
    
    x1 = linspace(0, camWidth, 1000);
    p = polyfit(x, y, 1);
    y1 = polyval(p, x1);
    
    plot(x, y, 'rx', 'MarkerSize', 15);
    hold on;
    plot(x1, y1, 'g');
    drawnow;
    
    
end
