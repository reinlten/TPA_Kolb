#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <filesystem>

#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <dirent.h>
#include <sys/types.h>

struct ComplexNumber
{
    double real;
    double imag;
};

int main()
{
    std::cout << 1 << std::endl;
    #include <iostream>
    #include <fstream>
    #include <vector>
    #include <cmath>
    #include <sys/types.h>
    #include <dirent.h>

    std::vector<double> magImpVector;
    std::vector<double> phaseVector;
    std::vector<ComplexNumber> impCVector;

    std::string folderPath = "/home/debian/";
    std::vector<std::string> fileNames;

    DIR *dir;
    struct dirent *ent;
    if ((dir = opendir(folderPath.c_str())) != nullptr)
    {
        // Iterate over files in the directory
        while ((ent = readdir(dir)) != nullptr)
        {
            if (ent->d_type == DT_REG)
            {
                fileNames.push_back(ent->d_name);
            }
        }
        closedir(dir);
    }
    else
    {
        // Failed to open directory
        std::cout << "Failed to open directory: " << folderPath << std::endl;
    }
    std::cout << 2 << std::endl;
    // std::cout << 1 << std::endl;
    for (const auto &fileName : fileNames)
    {
        std::ifstream file(folderPath + fileName);
        // Extract the header information
        int f, f_sample, number_of_periods, number_of_samples_per_period;
        file >> f >> f_sample >> number_of_periods >> number_of_samples_per_period;

        // Determine the number of data points
        int datapoints = std::round(f_sample / f);

        // Extract the voltage data
        std::vector<double> voltage1(datapoints), voltage2(datapoints);
        for (int i = 0; i < datapoints; ++i)
        {
            file >> voltage1[i];
            file >> voltage2[i];
        }

        // Close the file
        file.close();
        std::cout << 3 << std::endl;

        // Generate the time vector
        double dTime = 1.0 / f_sample;
        double obsTime = datapoints * dTime;
        std::vector<double> tVector(datapoints);
        for (int i = 0; i < datapoints; ++i)
        {
            tVector[i] = i * dTime;
        }

        // Calculate voltage across the DUT
        std::vector<double> voltageDut(datapoints);
        for (int i = 0; i < datapoints; ++i)
        {
            voltageDut[i] = voltage1[i] - voltage2[i];
        }

        // Calculate current: I = U / R
        std::vector<double> current(datapoints);
        for (int i = 0; i < datapoints; ++i)
        {
            current[i] = voltage2[i] / 100.0;
        }

        // Calculation of phase spectrum of impedance
        double phi1, phi2;
        int i, j;
        double maxV1 = voltage1[0];
        double maxV2 = voltage2[0];
        for (int k = 1; k < datapoints; ++k)
        {
            if (voltage1[k] > maxV1)
            {
                maxV1 = voltage1[k];
                i = k;
            }
            if (voltage2[k] > maxV2)
            {
                maxV2 = voltage2[k];
                j = k;
            }
        }
        phi1 = tVector[i];
        phi2 = tVector[j];
        double phase = (phi2 - phi1) * 2 * 3.1415 / (1.0 / f);

        // Calculation of magnitude of voltage across DUT and current
        double maxVDut = voltageDut[0], minVDut = voltageDut[0];
        double maxCurrent = current[0], minCurrent = current[0];
        for (int k = 1; k < datapoints; ++k)
        {
            if (voltageDut[k] > maxVDut)
            {
                maxVDut = voltageDut[k];
            }
            if (voltageDut[k] < minVDut)
            {
                minVDut = voltageDut[k];
            }
            if (current[k] > maxCurrent)
            {
                maxCurrent = current[k];
            }
            if (current[k] < minCurrent)
            {
                minCurrent = current[k];
            }
        }
        double magVDut = (maxVDut - minVDut) / 2.0;
        double magCurrent = (maxCurrent - minCurrent) / 2.0;

        // Calculation of impedance magnitude
        double magImp = magVDut / magCurrent;
        std::cout << magImp << std::endl;

        // Calculation of real and imaginary parts of impedance
        ComplexNumber impC;
        impC.real = magImp * std::cos(phase);
        impC.imag = magImp * std::sin(phase);

        // Store the results for plotting later
        magImpVector.push_back(magImp);
        phaseVector.push_back(phase);
        impCVector.push_back(impC);
        // (code to store results omitted for brevity)
    }

    // Plotting code for Bode diagram
    // (code to plot Bode diagram omitted for brevity)

    // Plotting code for Nyquist diagram
    // (code to plot Nyquist diagram omitted for brevity)

    // Print magnitude values
    std::cout << "Magnitude Values     "
              << "Phase Values" << std::endl;
    for (int i = 0; i < magImpVector.size(); i++)
    {
        std::cout << magImpVector[i] << "                " << phaseVector[i] << std::endl;
    }

    // // Print phase values
    // std::cout << "Phase Values:" << std::endl;
    // for (const auto &phase : phaseVector)
    // {
    //     std::cout << phase << std::endl;
    // }

    return 0;
}
