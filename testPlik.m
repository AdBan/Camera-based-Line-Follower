clc;clear;close all;

myrpi = raspi('192.168.43.74','pi','raspberry');

configurePin(myrpi, 12, 'DigitalOutput');
configurePin(myrpi, 19, 'DigitalOutput');
writeDigitalPin(myrpi, 12, 0);
writeDigitalPin(myrpi, 19, 1);