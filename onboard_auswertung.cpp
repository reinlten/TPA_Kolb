#include <iostream>
#include <fstream>
#include <complex>
#include <vector>
#include <algorithm>


using namespace std;

int main() {
    // Pfad der Anwendung und der Textdateien
	std::string file_path = R"(C:\Users\jonas\Desktop\TPA_Kolb\07.02.2023_1\100kHz - 1MHz\step1.txt)";

	// Textdatei öffnen und lesen
	// Open the file for reading
	std::ifstream file(file_path);
	if (!file) {
		std::cerr << "Error: Could not open file for reading" << std::endl;
		return 1;
	}
	std::vector<string> lines;

	// Read the file line by line
	std::string line;
	while (std::getline(file, line)) {
		lines.push_back(line);
	}

	// Close the file
	file.close();

    // Header und Daten werden geteilt
    std::string header = lines[0];
    std::vector<std::string> data;

    for (int i; i < lines.size(); i++) {
        data.push_back(lines[i]);
    }

    // cout << header << endl;
    // cout << data[0] << endl;
    // cout << data.size() << endl;

    // Header wird ausgelesen und gespeichert
    int current_freq, sample_freq, number_of_periods, number_of_samples_per_period;
    stringstream ss(header);
    ss >> current_freq >> sample_freq >> number_of_periods >> number_of_samples_per_period;

    // cout << current_freq << sample_freq << number_of_periods << number_of_samples_per_period << endl;

    // Anzahl der Dateipunkte wird über Periodenanzahl bestimmt
    int periods_wanted = 10;
    int number_of_samples = periods_wanted * (sample_freq / current_freq);

    // Datenwerte werden in Gesamtspannung (voltage1) und Shuntspannung (voltage2) geteilt
    vector<double> voltage1;
    vector<double> voltage2;
    for (int i = 1; i < number_of_samples + 1; i++) {
        stringstream ss(data[i]);
        int first, second;
        ss >> first >> second;
        voltage1.push_back(first);
        voltage2.push_back(second);
    }

    // cout << voltage1[0] << endl;
    // cout << voltage2[0] << endl;
    // cout << voltage1.size() << endl;
    // cout << voltage2.size() << endl;

    // Kompensationsfaktor für 10 kOhm Widerstand wird berechnet und Spannung wird damit multipliziert
    double factor = 4700.0 / (max_element(voltage1.begin(), voltage1.end())[0] / 2.0);

    for (int i = 0; i < voltage1.size(); i++) {
        voltage1[i] *= factor;
    }

    cout << "Factor: " << factor << endl;

    // Größen for die Visualisierung werden berechnet
    double dt = 1.0 / sample_freq;
    double df = sample_freq / number_of_samples;
    vector<double> time_vector;
    vector<double> frequency_vector;
    for (int i = 0; i < number_of_samples; i++) {
        time_vector.push_back(i * dt);
        frequency_vector.push_back(i * df);
    }

    // Fourierkoeffizienten der beiden Spannungen werden berechnet
    vector<complex<double>> fft_coefficients_voltage_1;
    vector<complex<double>> fft_coefficients_voltage_2;

    fft_coefficients_voltage_1.resize(voltage1.size());
    fft_coefficients_voltage_2.resize(voltage2.size());

    // TO-DO
    // fft(voltage1.data(), fft_coefficients_voltage_1.data(), voltage1.size());
    // fft(voltage2.data(), fft_coefficients_voltage_2.data(), voltage2.size());

    fft_coefficients_voltage_1[0] /= 2.0;
    fft_coefficients_voltage_2[0] /= 2.0;

//     // Fourierkoeffizienten der DUT-Spannung wird berechnet
//     vector<complex<double>> fft_coefficients_voltage_dut;
//     for (int i = 0; i < fft_coefficients_voltage_1.size(); i++) {
//         fft_coefficients_voltage_dut.push_back(fft_coefficients_voltage_1[i] - fft_coefficients_voltage_2[i]);
//     }

//     // Stromstärkewerte durch DUT werden über Ohmsches Gesetz und Shuntspannung berechnet
//     std::vector<double> current;
//     for (int i; i < voltage2.size(); i++) {
//         vector.push_back(voltage2[i] / 100.0);
//     }

//     // Fourrierkoeffizienten des Stroms werden berechnet
//     vector<complex<double>> fft_coefficients_current;

//     fft_coefficients_current.resize(current.size());

//     fft(current.data(), fft_coefficients_current.data(), current.size());

//     fft_coefficients_current[0] /= 2.0;

//     // Amplituden der DUT-Spannung und des DUT-Stroms werden berechnet
//     vector<double> magnitudes_voltage_dut;
//     vector<double> magnitudes_current_dut;
//     for (int i = 0; i < fft_coefficients_voltage_dut.size(); i++) {
//         magnitudes_voltage_dut.push_back(abs(fft_coefficients_voltage_dut[i]));
//         magnitudes_current_dut.push_back(abs(fft_coefficients_current[i]));
//     }

//     // Daten der aktuellen Frequenz werden ausgegeben
//     cout << "Current frequency: " << current_freq << endl;

//     cout << "Magnitude of DC component of voltage: " << magnitudes_voltage_dut[0] << " mV" << endl;
//     cout << "Magnitude of DC component of current: " << magnitudes_current_dut[0] << " mA" << endl;

//     // Position der Werte der aktuellen Frequenz wird berechnet
//     int index = (int)(current_freq / df);

//     // Phasen werden in Grad umgerechnet
//     //double phase_voltage_dut = (360.0 / (2 * M_PI)) * phases_voltage_dut[index];
//     //double phase_current = (360.0 / (2 * M_PI)) * phases_current[index];

//     cout << "Magnitude of voltage: " << magnitudes_voltage_dut[index] << " mV" << endl;
//     cout << "Magnitude of current: " << magnitudes_current_dut[index] << " mA" << endl;
//     //cout << "Phase of voltage: " << phase_voltage_dut << " degrees" << endl;
//     //cout << "Phase of current: " << phase_current << " degrees" << endl;

//     // Berechnet die Amplitude und die Phase der Impedanz bei der aktuellen Frequenz
//     double magnitude_impedance_dut = magnitudes_voltage_dut[index] / magnitudes_current_dut[index];
//     //double phase_impedance_dut = phase_voltage_dut - phase_current;

//     cout << "Magnitude of Impedance: " << magnitude_impedance_dut << " Ohm" << endl;
//     //cout << "Phase of Impedance: " << phase_impedance_dut << " degrees" << endl;

// 	// Impedanz in Array speichern

// 	// Impedanzen ausgeben
}