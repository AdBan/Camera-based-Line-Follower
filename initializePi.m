function [rpi, cam] = initializePi(relativePath, camWidth, camHeight, camFrame)

    %read ip address, login and password from file (not included in repository)
    file = fopen(relativePath, 'r');
    piAddress = fgetl(file);
    piLogin = fgetl(file);
    piPassword = fgetl(file);
    fclose(file);

    rpi = raspi(piAddress, piLogin, piPassword);
    cam = cameraboard(rpi, 'Resolution', [num2str(camWidth) 'x' num2str(camHeight)], 'FrameRate', camFrame);

end