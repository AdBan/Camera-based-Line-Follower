function DriveMotor(rpi, motorPin, percentSpeed)

    if ((percentSpeed < 0) || (percentSpeed > 1))
        fprintf('Drive motor with percentage value of 0 to 1!');
    end

    %calculate voltage [0 - 3,3V] based on percent speed;
    voltage =  percentSpeed * 3.3;
    
    %writePWMVoltage(rpi, motorPin, voltage);
    fprintf(['Driving ' motorPin ' with voltage ' num2str(voltage) '\n']);   %simulate PWM
    
end

