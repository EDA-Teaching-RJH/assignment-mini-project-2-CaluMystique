import matplotlib.pyplot as plt
import numpy as np
import math

class Speaker:
    def __init__(self, name, resistance, inductance, Resonant_frequency, QES, QMS):
       #section for defining speaker parameters
        self.name = name
        self.resistance = resistance
        self.inductance = inductance
        self.fs = Resonant_frequency
        self.qes = QES
        self.qms = QMS

    def calculate_impedance(self, frequency):
        try:
            #calculations for equivalent and real RLC components 
            Af = 2 * math.pi * frequency
            R = self.resistance
            L1 = self.inductance
            L2 = self.resistance / (2 * math.pi * self.fs * self.qes)
            C = self.qes / (2 * math.pi * self.fs * self.resistance)
            damping_factor = R * (self.qms/self.qes)

            # Parrallel impedance equation
            Z_p = 1 / (math.sqrt((1 / (damping_factor ** 2)) + (((1 / (Af * C)) - (Af * L2)) ** 2)))
            # Series impedance equation
            Z_s = Af * L1 * 0.001

            Z_total = R + Z_s + Z_p
        except ZeroDivisionError:
            print("impossible values")
        except ValueError:
            print("incorrect data format")

        return Z_total

    def plot_impedance(self, freq_range):
        # secction to plot the equation on the graph
        frequencies = np.arange(*freq_range)
        impedances = [self.calculate_impedance(f) for f in frequencies]

        # Extract magnitude and phase of impedance
        magnitudes = [abs(z) for z in impedances]
        

        # section to define parameters of the graph
        plt.figure(figsize=(10, 6))
        plt.plot(frequencies, magnitudes, label='Magnitude (|Z|)')
        plt.xscale("log")
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Impedance Magnitude (Ohms)')
        plt.title(f'Impedance Plot for {self.name}')
        plt.grid(True)
        plt.legend()
        # shows the graph
        plt.show()


# Example Usage
if __name__ == "__main__":
    # Create a speaker object with example parameters
    example_speaker = Speaker(name="Demo Speaker", resistance=6.27, inductance=0.06, QES=0.37, QMS=4.98, Resonant_frequency=61.03)

    # Plot impedance over a frequency range (20 Hz to 20 kHz)
    example_speaker.plot_impedance((20, 20000, 0.5))

