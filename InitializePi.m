function [rpi, cam] = InitializePi(relativePath, camWidth, camHeight, camFrame, lMotorPin, rMotorPin)

    %read ip address, login and password from file (not included in repository)
    file = fopen(relativePath, 'r');
    piAddress = fgetl(file);
    piLogin = fgetl(file);
    piPassword = fgetl(file);
    fclose(file);
    
    
    
    %create handle for raspberry and its camera
    
    rpi = raspi(piAddress, piLogin, piPassword);
    cam = cameraboard(rpi, 'Resolution', [num2str(camWidth) 'x' num2str(camHeight)], 'FrameRate', camFrame);

    %configure GPIO as PWM
     configurePin(rpi, lMotorPin, 'PWM');
     configurePin(rpi, rMotorPin, 'PWM');
     writePWMVoltage(rpi, lMotorPin, 3.3);
     writePWMVoltage(rpi, rMotorPin, 3.3);

    %configure GPIO as DO (just for testing)
%    configureDigitalPin(rpi, lMotorPin, 'output');
%    configureDigitalPin(rpi, rMotorPin, 'output'); 
%    writeDigitalPin(rpi, lMotorPin, 1);
%    writeDigitalPin(rpi, rMotorPin, 1);
end
