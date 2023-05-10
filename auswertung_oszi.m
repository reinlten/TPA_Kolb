clear;

f = 5000;

location = ['C:\Users\linus\Uni\Teamprojektarbeit\Messdaten\Oszilloskop Messungen 19.4.23\WA000008.CSV'];
header = readmatrix(location, 'Range', [1, 1, 2, 6]);

fSample = 1/header(2, 2);
dataPoints = fSample/f;

data = readmatrix(location, 'Range', 3);

voltage1 = data(1:dataPoints, 5);
voltage2 = data(1:dataPoints, 6);

current = voltage2/100;
voltageDut = voltage1 - voltage2;

%Erzeugen von Zeit- und Frequenzvektoren
fVector = (0:f:fSample-f)';
dTime = 1/fSample;
obsTime = dataPoints*dTime;
tVector = (0:dTime:obsTime-dTime)';

%Berechnen der Spannungsamplituden
magVoltage1 = (max(voltage1) - min(voltage1))/2;
magVoltage2 = (max(voltage2) - min(voltage2))/2;

%Plotten der gemessenen Spannungen und des Stroms
figure('Name', f + " Hz");
tiledlayout(2, 1);
nexttile;
plot(tVector, voltage1);
title('Gesamtspannung aus OPV in V (Oszi)');
xlabel ('Zeit/s');
ylabel ('Spannung/V');
text(0, -3, "Amplitude: " + magVoltage1 + "V");

nexttile;
plot(tVector, voltage2);
title('Spannung über Shunt in V (Oszi)')
xlabel ('Zeit/s');
ylabel ('Spannung/V');
text(0, -0.3, "Amplitude: " + magVoltage2 + "V");

%Berechnung der Amplituden
magVoltage1 = (max(voltage1) - min(voltage1))/2;
magVoltage2 = (max(voltage2) - min(voltage2))/2;
magVDut = (max(voltageDut) - min(voltageDut))/2;
magCurrent = (max(current) - min(current))/2;

%Berechnung vom Betrag der Impedanz
magImp = magVDut/magCurrent;
