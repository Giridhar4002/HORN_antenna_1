# Antenna Radiation Pattern Analysis

This is a Streamlit application designed to analyze and plot the radiation patterns of a high-efficiency multimode horn and a center-fed reflector antenna, based on Gaussian beam analytical models.

## Features
- **Part (b) - Feed Antenna Analysis**: Evaluates a high-efficiency horn operating at 20 GHz with a $3\lambda$ aperture. Plots the normalized Gaussian radiation pattern based on half-power beamwidth ($\theta_b$).
- **Part (c) - Reflector Antenna Analysis**: Calculates the secondary parameters of a center-fed reflector ($D=100\lambda$, $F/D=1.0$) using the feed from Part (b). It derives the edge illumination taper, aperture efficiency, peak directivity, 3dB beamwidth, and side lobe level (SLL), and plots an approximate secondary radiation pattern.

## Prerequisites
Ensure you have Python 3.7+ installed on your system. You will need the following Python libraries:
- `streamlit`
- `numpy`
- `matplotlib`
- `scipy`

## Installation
1. Clone or download this repository.
2. Open your terminal or command prompt and navigate to the folder containing `app.py`.
3. Install the required dependencies by running:
   ```bash
   pip install streamlit numpy matplotlib scipy
