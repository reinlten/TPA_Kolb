#include <iostream>
#include <cmath>
#include <vector>

int main() {
    // Set the start and end values
    int start = 1000;
    int end = 1000000;

    // Create a vector to hold the logarithmic space
    std::vector<int> logspace;

    // Calculate the logarithmic spacing between start and end
    double log_start = std::log10(start);
    double log_end = std::log10(end);
    double step = (log_end - log_start) / 999;

    // Populate the vector with whole number values
    for (double i = log_start; i <= log_end; i += step) {
        logspace.push_back(std::round(std::pow(10, i)));
    }

    // Print the resulting vector
    for (int value : logspace) {
        std::cout << value << " ";
    }
    std::cout << std::endl;
    std::cout << logspace.size();

    return 0;
}
