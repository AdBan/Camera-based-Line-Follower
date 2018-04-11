clc; clear; close all;
%% User input

loginDataFile = 'raspberry.txt';
camHeight = 240;    %valid: 120, 240, 480, 600, 768, 1080
camWidth = 320;     %valid: 160, 320, 640, 800, 1024, 1920
camFrame = 90;      %valid: 2 to 90

lMotorPin = 'left motor';
rMotorPin = 'right motor';

referencePoint = 0.2;   %valid: 0 to 1
predictionPoint = 0.6;  %valid: 0 to 1


%% Initialize

[rpi, cam] = InitializePi(loginDataFile, camWidth, camHeight, camFrame, lMotorPin, rMotorPin);

f1 = figure(1); 
stopCriteria = 0; %replace with eg. lost line || end of line || obstacle

%% Loop until stop criteria is meet

while not(stopCriteria)
    %% Process frame
    
    rgb = snapshot(cam); %capture frame
    grayscale = rgb2gray(rgb);
    binary = ~imbinarize(grayscale);
    closed = imclose(binary, strel('square', 10));
    frame = closed;
    
    f1; cla; imshow(rgb); hold on;
    
    
    %% Determine slope based on reference and prediction point
    
    %get reference/prediction pixel height
    referenceHeight = (1 - referencePoint) * camHeight;
    predictionHeight = (1 - predictionPoint) * camHeight;
    
    %take out whole row at calculated height of frame
    referenceRow = frame(referenceHeight, :); 
    predictionRow = frame(predictionHeight, :);
    
    %get indexes of black (line) pixels
    referenceRowLineIndexes = find(referenceRow == 1); 
    predictionRowLineIndexes = find(predictionRow == 1);
    
    %get index of middle of line
    referenceMiddleIndex = min(referenceRowLineIndexes) + (max(referenceRowLineIndexes) - min(referenceRowLineIndexes)) / 2;
    predictionMiddleIndex = min(predictionRowLineIndexes) + (max(predictionRowLineIndexes) - min(predictionRowLineIndexes)) / 2;
    
    plot(referenceMiddleIndex, referenceHeight, 'rs', 'MarkerSize', 15);
    plot(predictionMiddleIndex, predictionHeight, 'ro', 'MarkerSize', 15);
    legend('reference point', 'prediction point');
    drawnow;
    
    
end
