import matplotlib.pyplot as plt
import numpy as np
import math

class Speaker:
    def __init__(self, name, resistance, inductance, compliance, damping, Resonant_frequency, QES, QMS):
        """
        Initialize the Speaker object with its RLC parameters.
        
        Parameters:
        - name: str, the name of the speaker.
        - resistance: float, the resistance (R) in ohms.
        - inductance: float, the inductance (L) in henries.
        - compliance: float, the compliance (C) in farads.
        - damping: float, the mechanical damping factor.
        """
        self.name = name
        self.resistance = resistance
        self.inductance = inductance
        self.compliance = compliance
        self.damping = damping
        self.fs = Resonant_frequency
        self.qes = QES
        self.qms = QMS

    def calculate_impedance(self, frequency):
        """
        Compute the impedance of the speaker at a given frequency.

        Parameters:
        - frequency: float, the frequency in Hz.

        Returns:
        - complex, the impedance at the given frequency.
        """
        
        Af = 2 * math.pi * frequency
        R = self.resistance
        L1 = self.inductance
        L2 = self.resistance / (2 * math.pi * self.fs * self.qes)
        C = self.qes / (2 * math.pi * self.fs * self.resistance)
        damping_factor = R * (self.qms/self.qes)

        # Impedance calculation for RLC circuit with damping
        Z_p = 1 / (math.sqrt((1 / (damping_factor ** 2)) + (((1 / (Af * C)) - (Af * L2)) ** 2)))
        Z_s = Af * L1 * 0.001

        Z_total = R + Z_s + Z_p
        
    
        return Z_total

    def plot_impedance(self, freq_range):
        """
        Plot the impedance of the speaker over a range of frequencies.

        Parameters:
        - freq_range: tuple, the range of frequencies (start, stop, step) in Hz.
        """
        frequencies = np.arange(*freq_range)
        impedances = [self.calculate_impedance(f) for f in frequencies]

        # Extract magnitude and phase of impedance
        magnitudes = [abs(z) for z in impedances]
        

        # Plot impedance magnitude
        plt.figure(figsize=(10, 6))
        plt.plot(frequencies, magnitudes, label='Magnitude (|Z|)')
        plt.xscale("log")
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Impedance Magnitude (Ohms)')
        plt.title(f'Impedance Plot for {self.name}')
        plt.grid(True)
        plt.legend()

        plt.show()


# Example Usage
if __name__ == "__main__":
    # Create a speaker object with example parameters
    example_speaker = Speaker(name="Demo Speaker", resistance=6.27, inductance=0.06, compliance=1e-6, damping=0.05, QES=0.37, QMS=4.98, Resonant_frequency=61.03)

    # Plot impedance over a frequency range (20 Hz to 20 kHz)
    example_speaker.plot_impedance((20, 20000, 0.5))

