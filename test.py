import numpy as np

# Set the start and end values
start = 1000
end = 1000000

# Create a logarithmic space with 1000 points
logspace = np.logspace(np.log10(start), np.log10(end), num=1000, base=10, dtype=int)

print(logspace)
