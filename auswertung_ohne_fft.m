clc
clear

%Öffnen der Dateien
files = dir(fullfile('C:\Users\linus\Uni\Teamprojektarbeit\Messdaten\07.02.2023_1kOhm\1kHz - 9kHz', '*.txt*'));


for file = 1:size(files)
    fileId = fopen(fullfile(files(file).folder, files(file).name), 'r');

    %Extrahieren der ersten Zeile
    header = fscanf(fileId, '%d%d', [1, 4]);
    f = header(1, 1);
    fSample = header(1, 2);

    %Bestimmung der Datenpunkte
    dataPoints = round(fSample/f, -0);

    %Extrahieren der Messwerte in zwei Spannungsvektoren
    data = fscanf(fileId, '%d', [dataPoints*2, 1]);
    voltage1 = data(1:2:end)/1000;
    voltage2 = data(2:2:end)/1000;

    fclose(fileId);

    %Erzeugen vom Zeitvektor
    dTime = 1/fSample;
    obsTime = dataPoints*dTime;
    tVector = (0:dTime:obsTime-dTime)';

    %Bestimmung der Spannung, die über dem DUT abfällt
    voltageDut = voltage1 - voltage2;

    %Berechnung des Stroms: I = U/R
    current = voltage2/100;

    % %Plotten der gemessenen Spannungen und des Stroms
    % figure("Name", f + " Hz");
    % tiledlayout(2, 1);
    % nexttile;
    % plot(tVector, voltage1, tVector, voltage2, tVector, voltageDut);
    % title('Spannungen in mV');
    % xlabel ('Zeit/s');
    % ylabel ('Spannung/mV');
    % legend('Uges', 'Ushunt', 'Udut')
    % 
    % nexttile;
    % plot(tVector, current);
    % title('Strom in mA')

    %Berechnung des Phasenspektrums der Impedanz
    [v1Max, i] = max(voltage1);
    [v2Max, j] = max(voltage2);
    phi1 = tVector(i);
    phi2 = tVector(j);
    phase(file, 1) = (phi2 - phi1)*2*pi/(1/f);
    phase(file, 2) = f;

    %Entfernen der Spannungseinbrüche und damit korrektes Berechnen der
    %Amplituden von Spannung und Strom
    magVDut = (max(rmoutliers(voltageDut, "movmedian", 10)) - min(rmoutliers(voltageDut, "movmedian", 10)))/2;
    magCurrent = (max(rmoutliers(current, "movmedian", 10)) - min(rmoutliers(current, "movmedian", 10)))/2;

    %Berechnen des Amplitudenspektrums der Impedanz
    magImp(file, 1) = magVDut ./ magCurrent;
    magImp(file, 2) = f;

    %Berechnung von Real- und Imaginärteil
    ImpC(file, 1) = magImp(file, 1)*cos(phase(file, 1));
    ImpC(file, 2) = magImp(file, 1)*sin(phase(file, 1));
end

    %Plotten von Betragsgang und Phasengang
    figure("Name", "Bode-Diagramm");
    tiledlayout(2,1);
    nexttile;
    plot(magImp(:, 2), magImp(:, 1), "o");
    xlabel("Frequenz/Hz");
    ylabel("Betrag/\Omega");
    title("Betragsgang");

    nexttile;
    plot(phase(:, 2), phase(:, 1), "o");
    axis();
    xlabel("Frequenz/Hz");
    ylabel("Phase");
    title("Phasengang");

    

    %Plotten vom Nyquist-Diagramm
    figure("Name", "Nyquist-Diagramm");
    plot(ImpC(:, 1), ImpC(:, 2), "o");
    xlabel("Re");
    ylabel("Im");
    title("Nyquist-Diagramm")
    
