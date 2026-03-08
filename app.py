import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1

def calculate_feed_pattern(theta, theta_b):
    """Calculate the normalized Gaussian radiation pattern for the feed."""
    # E(θ) = e^(-0.3467 * (θ/θb)^2)
    # In dB, this is approx -3 * (θ/θb)^2
    pattern_linear = np.exp(-0.3467 * (theta / theta_b)**2)
    pattern_db = 20 * np.log10(pattern_linear + 1e-10)
    return pattern_db

def approximate_reflector_pattern(theta, theta_3, sll_db, d_peak):
    """
    Approximate the secondary reflector pattern using a modified Bessel/Sinc envelope
    that roughly matches the 3dB beamwidth and SLL.
    """
    # Convert theta to radians for calculation
    theta_rad = np.radians(theta)
    
    # Scale factor to match the 3dB beamwidth
    # For a circular aperture, 2*J1(u)/u drops to -3dB at u approx 1.616
    u = 1.616 * 2 * theta / theta_3
    u = np.where(u == 0, 1e-10, u) # Avoid division by zero
    
    # Base pattern (similar to uniform illumination, but we adjust SLL)
    pattern_linear = np.abs(2 * j1(u) / u)
    pattern_db = 20 * np.log10(pattern_linear + 1e-10)
    
    # Adjust SLL to match the calculated theoretical SLL
    # The first sidelobe of 2*J1(u)/u is at -17.6 dB. We shift it to match the requested SLL.
    sll_diff = sll_db - (-17.6)
    pattern_db_adjusted = np.where(pattern_db < -3, pattern_db + sll_diff * (pattern_db / -17.6), pattern_db)
    
    # Normalize to Peak Directivity
    return d_peak + pattern_db_adjusted

def main():
    st.set_page_config(page_title="Antenna Radiation Patterns", layout="wide")
    st.title("Antenna Radiation Pattern Analysis")
   

    st.header("Part (b): High-Efficiency Horn at 20 GHz")
    
    col1, col2 = st.columns((1, 2))
    
    with col1:
        st.subheader("Given Parameters")
        st.write("- Frequency (f) = 20 GHz")
        st.write("- Wavelength (λ) = 15 mm")
        st.write("- Aperture Diameter ($d_m$) = $3\lambda$ = 45 mm")
        st.write("- Horn Type: High-efficiency multimode (A = 63, $\eta_e \\approx 85\\%$)")
        
        theta_b = 63 * (1/3)
        directivity_feed = 10 * np.log10(0.85 * (np.pi * 3)**2)
        
        st.subheader("Calculated Results")
        st.latex(r"\theta_b = 63 \times \frac{\lambda}{d_m} = 21^\circ")
        st.latex(r"D_e = 10 \log_{10}(0.85 \times (\pi \times 3)^2) = " + f"{directivity_feed:.2f} \\text{{ dBi}}")
    
    with col2:
        # Plotting Feed Pattern
        theta_feed = np.linspace(-60, 60, 500)
        pattern_feed_db = calculate_feed_pattern(theta_feed, theta_b)
        
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.plot(theta_feed, pattern_feed_db, label=f"Gaussian Model ($\\theta_b={theta_b}^\circ$)")
        ax1.axhline(-3, color='r', linestyle='--', label="-3 dB Level")
        ax1.axvline(21, color='g', linestyle=':', label="$\\theta = 21^\circ$")
        ax1.axvline(-21, color='g', linestyle=':')
        ax1.set_ylim(-30, 2)
        ax1.set_xlim(-60, 60)
        ax1.set_xlabel("Angle $\\theta$ (degrees)")
        ax1.set_ylabel("Normalized Pattern (dB)")
        ax1.set_title("High-Efficiency Horn Radiation Pattern ")
        ax1.grid(True)
        ax1.legend()
        st.pyplot(fig1)

    st.divider()

    st.header("Part (c): Center-Fed Reflector")
    
    col3, col4 = st.columns((1, 2))
    
    with col3:
        st.subheader("Given Parameters")
        st.write("- Reflector Diameter (D) = $100\lambda$")
        st.write("- F/D Ratio = 1.0")
        
        # Calculations
        theta_0 = 2 * np.degrees(np.arctan(100/400)) # 28.07 deg
        taper = 3 * (theta_0 / theta_b)**2 # 5.36 dB
        eta_f = 69.7 # %
        d_peak = 48.37 # dBi
        theta_3 = 0.625 # degrees
        sll = -20.68 # dB
        
        st.subheader("Calculated Results")
        st.latex(r"\theta_0 = 2 \arctan\left(\frac{D}{4F}\right) = " + f"{theta_0:.2f}^\circ")
        st.latex(r"T = 3 \left(\frac{28.07}{21}\right)^2 = " + f"{taper:.2f} \\text{{ dB}}")
        st.write(f"**Aperture Efficiency ($\eta_f$):** {eta_f}%")
        st.write(f"**Peak Directivity ($D_{{peak}}$):** {d_peak} dBi")
        st.write(f"**3dB Beamwidth ($\\theta_3$):** {theta_3}$^\circ$")
        st.write(f"**Side Lobe Level (SLL):** {sll} dB")
        
    with col4:
        # Plotting Reflector Pattern
        theta_ref = np.linspace(-3, 3, 1000)
        pattern_ref_db = approximate_reflector_pattern(theta_ref, theta_3, sll, d_peak)
        
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(theta_ref, pattern_ref_db, color='purple', label="Reflector Secondary Pattern")
        ax2.axhline(d_peak - 3, color='r', linestyle='--', label=f"-3 dB Level ({d_peak - 3:.2f} dBi)")
        ax2.axhline(d_peak + sll, color='orange', linestyle='--', label=f"SLL ({d_peak + sll:.2f} dBi)")
        
        ax2.set_ylim(d_peak - 40, d_peak + 5)
        ax2.set_xlim(-3, 3)
        ax2.set_xlabel("Angle $\\theta$ (degrees)")
        ax2.set_ylabel("Directivity (dBi)")
        ax2.set_title("Center-Fed Reflector Radiation Pattern ")
        ax2.grid(True)
        ax2.legend()
        st.pyplot(fig2)

if __name__ == "__main__":
    main()
