# Spectral-vis

[![Tests](https://github.com/tobias-fritz/Spectral-vis/actions/workflows/python-package.yml/badge.svg)](https://github.com/tobias-fritz/Spectral-vis/actions/workflows/python-package-conda.yml)

Computing and Visualizing Absorption Spectra from Excitation Energies

The procedure is based on [this article](http://gaussian.com/uvvisplot/) from the Gaussian website.

## How to Use

Since the application opportunities for this script are rather broad, an example use case is provided in the [example notebook](./example.ipynb).

You can provide a single excitation energy or a list of energies and their corresponding oscillator strengths.

## Example

Here is a quick example of how to use the `Spectrum` class:

```python
from source.gaussian_broadening import Spectrum

# Initialize the Spectrum class with the path to your CSV file
spectrum = Spectrum('path/to/your/energy.csv')

# Calculate the spectrum in eV
spectrum.calculate_spectrum(unit='eV', sigma=0.2)

# Plot the spectrum
spectrum.plot_spectrum(unit='eV')
```

For more detailed usage, please refer to the [example notebook](./example.ipynb).

## CSV Format

The CSV file should contain pairs of oscillator strengths and excitation energies (row wise). Here is an example:

```csv
oscilator_strength_1, wavelength_1, oscilator_strength_2, wavelength_2
2.32,535.23,0.13,339.79 
2.32,534.57,0.13,344.20 
```

## Try it Online

You can try the example notebook online using Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tobias-fritz/Spectral-vis/HEAD)

## Setup

All dependencies can be installed using either pip or conda:

```sh
pip install -r requirements.txt
```

```sh
conda install --file requirements.txt
```
