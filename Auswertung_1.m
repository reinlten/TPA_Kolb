clearvars;

% specify file path
filePath = 'G:\Meine Ablage\Uni Stuff\WS22 23\TPA\Messungen (neu)\7.12.22\1k - 10k Hz 07.12.22\step1.txt';

% specify length of data to use
dataLength = 100000;

% open file
fileID = fopen(filePath);

% read header
header = textscan(fileID, '%f %f %f %f', 1);

% read data
data = textscan(fileID, '%f %f', dataLength, 'Delimiter', '\t');

% close file
fclose(fileID);

% subtract mean value from first signal
data{1} = data{1} - mean(data{1});

% subtract mean value from second signal
data{2} = data{2} - mean(data{2});

N = length(data{1});
f = (0:N-1)/N*header{1};

%% 

% create figure
figure('Position', [350, 100, 800, 600]);

% create third subplot for original signals
subplot(2,2,[1,2]);

% plot first signal
plot(data{1});

% hold plot
hold on;

% plot second signal
plot(data{2});

% release plot
hold off;

% label axes
xlabel('Data Index');
ylabel('Data Value');

%% 

% create first subplot for first signal
subplot(2,2,3);

% calculate FFT of second signal
fftCoefficients1 = fft(data{1});

% calculate magnitude of FFT coefficients for second signal
fftMagnitude1 = abs(fftCoefficients1);

% plot magnitude of FFT coefficients for second signal
semilogx(f, fftMagnitude1);

% hold plot
hold on;

% calculate FFT of second signal
fftCoefficients2 = fft(data{2});

% calculate magnitude of FFT coefficients for second signal
fftMagnitude2 = abs(fftCoefficients2);

% plot magnitude of FFT coefficients for second signal
semilogx(f, fftMagnitude2);

% release plot
hold off;

% label axes
xlabel('Frequency (Hz)');
ylabel('Magnitude');

%%
% create second subplot for second signal
subplot(2,2,4);

% calculate phase of FFT coefficients for second signal
fftPhase1 = angle(fftCoefficients1);

% plot phase of FFT coefficients for second signal
semilogx(f, fftPhase1);

% hold plot
hold on;

% calculate phase of FFT coefficients for second signal
fftPhase2 = angle(fftCoefficients2);

% plot phase of FFT coefficients for second signal
semilogx(f, fftPhase2);

% release plot
hold off;

% label axes
xlabel('Frequency (Hz)');
ylabel('Phase (rad)');


