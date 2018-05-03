clc; clear; close all;
%% User input

loginDataFile = 'raspberry.txt';
camHeight = 240;    %valid: 120, 240, 480, 600, 768,  1080
camWidth = 320;     %valid: 160, 320, 640, 800, 1024, 1920
camFrame = 90;      %valid: 2 to 90

% lMotorPin = 'left motor';
% rMotorPin = 'right motor';
lMotorPin = 13;
rMotorPin = 18;

Kp = 20;
Kd = 5;


%% Initialize

[rpi, cam] = InitializePi(loginDataFile, camWidth, camHeight, camFrame, lMotorPin, rMotorPin);

f1 = figure(1); 
stopCriteria = 0; %replace with eg. lost line || end of line || obstacle

errPrev = 0;
errMax = camWidth/2;
 
%% Loop until stop criteria is meet

while not(stopCriteria)
    %% Process frame
    
    %rgb = snapshot(cam); %capture frame
    rgb = imread('training/line_left.png');
    grayscale = rgb2gray(rgb);
    binary = ~imbinarize(grayscale);
    closed = imclose(binary, strel('square', 10));
    frame = closed;
    
    f1; cla; imshowpair(rgb, frame, 'montage'); drawnow; hold on;
    
    
    %% Determine slope based on reference and prediction point
    
    pointsAmount = 3;
    x = zeros(1, pointsAmount); y = zeros(1, pointsAmount);
    for i = 1 : pointsAmount
        [x(i), y(i)] = GetLinePoint(frame, i/(pointsAmount+1));    %get equally distributed points
    end
    if (all(x == -1) && all(y == -1))
        % line not found
        continue;
    end
    x1 = linspace(0, camWidth, 1000);
    p = polyfit(x, y, 1);
    y1 = polyval(p, x1);
    
    plot(x, y, 'rx', 'MarkerSize', 15);
    hold on;
    plot(x1, y1, 'g');
    drawnow;
    
    %% Calculate PD parameters
    err = x(1) - camWidth/2;
    der = errPrev - err;
    u = Kp * err + Kd * der;
    
    if (err < 0)
    % turn left
        fprintf('turning left\n');
        DriveMotor(rpi, lMotorPin, abs(err)/errMax);
        DriveMotor(rpi, rMotorPin, 1 - abs(err)/errMax);
    elseif (err > 0)
    % turn right
        fprintf('turning right\n');
        DriveMotor(rpi, lMotorPin, 1 - abs(err)/errMax);
        DriveMotor(rpi, rMotorPin, abs(err)/errMax);
    else
    % drive forward
        DriveMotor(rpi, lMotorPin, 1);
        DriveMotor(rpi, rMotorPin, 1);
    end
    
    
    errPrev = err;
    
    
end
