voltagefunction DriveMotor(rpi, motorPin, percentSpeed)

    if ((percentSpeed < 0) || (percentSpeed > 1))
        fprintf(['Error! Attempted to drive ' motorPin ' with percentage value below 0/above 1!\n']);
        return;
    end

    %calculate voltage [0 - 3,3V] based on percent speed;
    voltage =  percentSpeed *3.3;
    writePWMVoltage(rpi, motorPin, voltage);
    
    fprintf(['Driving ' num2str(motorPin) ' with voltage ' num2str(voltage) '\n']);
    
    %writeDigitalPin(mypi, motorPin , percentSpeed > 0);
    
end

