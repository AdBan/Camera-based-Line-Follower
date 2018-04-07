clc; clear; close all;
%% User input

loginDataFile = 'raspberry.txt';
camHeight = 240;    %valid: 120, 240, 480, 600, 768, 1080
camWidth = 320;     %valid: 160, 320, 640, 800, 1024, 1920
camFrame = 90;      %valid: 2 to 90


%% Initialize Raspberry

[rpi, cam] = initializePi(loginDataFile, camWidth, camHeight, camFrame);


%% Loop until stop criteria is meet

f1 = figure(1);
stopCriteria = 0; %replace with eg. lost line || end of line || obstacle
while not(stopCriteria)
    %% Process frame
    rgb = snapshot(cam); %capture frame
    grayscale = rgb2gray(rgb);
    binary = imbinarize(grayscale);
    f1; imshowpair(rgb, binary, 'montage');
    drawnow;
end
