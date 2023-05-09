#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>

using namespace std;

int main() {
    // Pfad der Anwendung und der Textdateien
    string file_path = R"(C:\Users\jonas\Desktop\TPA_Kolb\07.02.2023_1\100kHz - 1MHz\step1.txt)";

    // Textdatei öffnen und lesen
    // Open the file for reading
    ifstream file(file_path);
    if (!file) {
        cerr << "Error: Could not open file for reading" << endl;
        return 1;
    }
    vector<string> lines;

    // Read the file line by line
    string line;
    while (getline(file, line)) {
        lines.push_back(line);
    }

    // Close the file
    file.close();


    // Header und Daten werden geteilt
    string header = lines[0];
    vector<string> data;

    for (int i; i < lines.size(); i++) {
        data.push_back(lines[i]);
    }

    int current_freq, sample_freq, number_of_periods, number_of_samples_per_period;
    stringstream ss(header);
    ss >> current_freq >> sample_freq >> number_of_periods >> number_of_samples_per_period;

    int number_of_samples = data.size();

    vector<double>voltage1;
    vector<double> voltage2;
    for (int i = 1; i < number_of_samples + 1; i++)
    {
        stringstream ss(data[i]);
        int first, second;
        ss >> first >> second;
        voltage1.push_back(first);
        voltage2.push_back(second);
    }

    // Größen for die Visualisierung werden berechnet
    double dt = 1.0 / sample_freq;
    double df = sample_freq / number_of_samples;
    vector<double> time_vector;
    vector<double> frequency_vector;
    for (int i = 0; i < number_of_samples; i++)
    {
        time_vector.push_back(i * dt);
        frequency_vector.push_back(i * df);
    }
}


