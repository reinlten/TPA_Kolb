#include <fstream>
#include <iostream>
#include <vector>
#include <sstream>
#include <cmath>
#include <complex>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

void read_in_file(std::string file_path, std::string& header, std::vector<string>& data)
{
    std::ifstream file(file_path);
    if (!file)
    {
        std::cerr << "Error: Could not open file for reading" << std::endl;
    }
    else{
        std::vector<std::string> lines = {};

        // Read the file line by line
        std::string line = "";
        while (std::getline(file, line))
        {
            lines.push_back(line);
        }

        // Close the file
        file.close();

        // Header und Daten werden geteilt
        header = lines[0];

        for (int i = 1; i < lines.size(); i++)
        {
            data.push_back(lines[i]);
        }
    }
}

void read_header_and_data(std::string header, std::vector<string> data, int& current_freq, int& sample_freq, int& number_of_periods, int& number_of_samples_per_period, 
                            vector<double>& voltage_1, vector<double>& voltage_2, vector<double>& current, int shunt_value, int number_of_samples)
{
    std::stringstream ss(header);
    ss >> current_freq >> sample_freq >> number_of_periods >> number_of_samples_per_period;

    for (int i = 0; i < number_of_samples; i++)
    {
        stringstream ss(data[i]);
        int first, second;
        ss >> first >> second;
        voltage_1.push_back(first);
        voltage_2.push_back(second);
        current.push_back(second / shunt_value);
    }
}

void perform_dft_on_current_frequency(std::vector<double> signal, std::complex<double> &fouriercoefficient, std::complex<double> i, 
                                        double pi, int number_of_samples, int index)
{
    for (double k = 0; k < number_of_samples; k++)
    {
        fouriercoefficient += double(2) * (exp((-2 * pi * i * k * double(index)) / double(number_of_samples)) * signal[k]) / double(number_of_samples);
    }
}

void analyze_file(std::string filename, std::vector<double>& amplitudes, std::vector<double>& phases)
{
    std::string file_path = filename;
    std::string header = "";
    std::vector<std::string> data = {};

    read_in_file(file_path, header, data);

    int current_freq, sample_freq, number_of_periods, number_of_samples_per_period = 0;
    int number_of_samples = data.size();

    vector<double> voltage_1 = {};
    vector<double> voltage_2 = {};
    vector<double> current = {};

    read_header_and_data(header, data, current_freq, sample_freq, number_of_periods, number_of_samples_per_period, voltage_1, voltage_2, current, 100, number_of_samples);

    std::complex<double> fouriercoefficient_1 = 0;
    std::complex<double> fouriercoefficient_2 = 0;
    std::complex<double> fouriercoefficient_voltage = 0;
    std::complex<double> fouriercoefficient_current = 0;
    std::complex<double> i(0.0, 1.0);
    double pi = 3.141592653589793238462643383279;

    int index = (current_freq * number_of_samples) / sample_freq;
    perform_dft_on_current_frequency(voltage_1, fouriercoefficient_1, i, pi, number_of_samples, index);
    perform_dft_on_current_frequency(voltage_2, fouriercoefficient_2, i, pi, number_of_samples, index);
    perform_dft_on_current_frequency(current, fouriercoefficient_current, i, pi, number_of_samples, index);

    fouriercoefficient_voltage = fouriercoefficient_1 - fouriercoefficient_2;

    double amplitude_voltage = std::abs(fouriercoefficient_voltage);
    double amplitude_current = std::abs(fouriercoefficient_current);

    double phase_voltage = std::arg(fouriercoefficient_voltage) * (180 / pi);
    double phase_current = std::arg(fouriercoefficient_current) * (180 / pi);

    std::cout << "magnitude of voltage: " << amplitude_voltage << std::endl;
    std::cout << "magnitude of current: " << amplitude_current << std::endl;
    std::cout << "phase of voltage: " << phase_voltage << std::endl;
    std::cout << "phase of current: " << phase_current << std::endl;

    double amplitude_impedance = amplitude_voltage / amplitude_current;
    double phase_impedance = (phase_voltage - phase_current);

    std::cout << "magnitude of impedance: " << amplitude_impedance << std::endl;
    std::cout << "phase of impedance: " << phase_impedance << std::endl;

    double real = amplitude_impedance * cos(phase_impedance);
    double imag = amplitude_impedance * sin(phase_impedance);

    std::cout << "real part of impedance: " << real << std::endl;
    std::cout << "imaginary part of impedance: " << imag << std::endl << std::endl;

    amplitudes.push_back(amplitude_impedance);
    phases.push_back(phase_impedance);
}

bool isTextFile(const fs::directory_entry &entry)
{
    return entry.path().extension() == ".txt";
}

    int main()
    {
        std::vector<double> amplitudes;
        std::vector<double> phases;
        std::vector<int> frequencies;

        std::string folderPath = R"(C:\Users\jonas\Desktop\Teamprojektarbeit\Aktuell\Messungen BBB\geht\100Ohm)";

        std::string file_path = R"(C:\Users\jonas\Desktop\Teamprojektarbeit\Aktuell\Messungen BBB\geht\100Ohm\step22.txt)";
        std::string header = "";
        std::vector<std::string> data = {};

        read_in_file(file_path, header, data);

        int current_freq, sample_freq, number_of_periods, number_of_samples_per_period = 0;
        int number_of_samples = data.size();

        vector<double> voltage_1 = {};
        vector<double> voltage_2 = {};
        vector<double> current = {};

        read_header_and_data(header, data, current_freq, sample_freq, number_of_periods, number_of_samples_per_period, voltage_1, voltage_2, current, 100, number_of_samples);

        std::complex<double> fouriercoefficient_1 = 0;
        std::complex<double> fouriercoefficient_2 = 0;
        std::complex<double> fouriercoefficient_voltage = 0;
        std::complex<double> fouriercoefficient_current = 0;
        std::complex<double> i(0.0, 1.0);
        double pi = 3.141592653589793238462643383279;

        // int index = (current_freq * number_of_samples) / sample_freq;
        int index = current_freq / 1000;
        cout << current_freq << endl;
        cout << number_of_samples << endl;
        cout << sample_freq << endl;
        cout << "index: " << index << endl;
        perform_dft_on_current_frequency(voltage_1, fouriercoefficient_1, i, pi, number_of_samples, index);
        perform_dft_on_current_frequency(voltage_2, fouriercoefficient_2, i, pi, number_of_samples, index);
        perform_dft_on_current_frequency(current, fouriercoefficient_current, i, pi, number_of_samples, index);

        fouriercoefficient_voltage = fouriercoefficient_1 - fouriercoefficient_2;

        double amplitude_voltage = std::abs(fouriercoefficient_voltage);
        double amplitude_current = std::abs(fouriercoefficient_current);

        double phase_voltage = std::arg(fouriercoefficient_voltage) * (180 / pi);
        double phase_current = std::arg(fouriercoefficient_current) * (180 / pi);

        std::cout << "Current frequency: " << current_freq << std::endl;
        std::cout << "magnitude of voltage: " << amplitude_voltage << std::endl;
        std::cout << "magnitude of current: " << amplitude_current << std::endl;
        std::cout << "phase of voltage: " << phase_voltage << std::endl;
        std::cout << "phase of current: " << phase_current << std::endl;

        double amplitude_impedance = amplitude_voltage / amplitude_current;
        double phase_impedance = phase_voltage - phase_current;

        std::cout << "magnitude of impedance: " << amplitude_impedance << std::endl;
        std::cout << "phase of impedance: " << phase_impedance << std::endl;

        double real = amplitude_impedance * cos(phase_impedance);
        double imag = amplitude_impedance * sin(phase_impedance);

        std::cout << "real part of impedance: " << real << std::endl;
        std::cout << "imaginary part of impedance: " << imag << std::endl << std::endl;

        amplitudes.push_back(amplitude_impedance);
        phases.push_back(phase_impedance);
    }