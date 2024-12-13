import pytest
from RLClibrary import Speaker  # Assumes your main program is saved as `speaker.py`
#this program test the library RLCLIbrary. inorder to try it go to RLClibrary and put pytest test_RLC.py


def test_calculate_impedance():
    # Basic test case for 1 khz signal
    speaker = Speaker(name="Test Speaker", resistance=6.27, inductance=0.06, QES=0.37, QMS=4.98, Resonant_frequency=61.03)
    impedance = speaker.calculate_impedance(1000)  # 1 kHz
    assert impedance > 0, "Impedance should be positive for valid inputs"

    # Limit test for low frequencies
    impedance = speaker.calculate_impedance(10)
    assert impedance > 0, "Impedance should be positive for frequency"

    # Limit test for hi frequencies
    impedance = speaker.calculate_impedance(20000)  # 20 kHz
    assert impedance > 0, "Impedance should be positive for high frequency"

    # test case for negative resistances
    invalid_speaker = Speaker(name="Invalid Speaker", resistance=-6.27, inductance=0.06, QES=0.37, QMS=4.98, Resonant_frequency=61.03)
    with pytest.raises(ValueError):
        invalid_speaker.calculate_impedance(1000)

    # test case for zero division errors
    zero_qes_speaker = Speaker(name="Zero QES Speaker", resistance=6.27, inductance=0.06, QES=0, QMS=4.98, Resonant_frequency=61.03)
    with pytest.raises(ZeroDivisionError):
        zero_qes_speaker.calculate_impedance(1000)

def test_plot_impedance():
    # test case for graph plotting
    speaker = Speaker(name="Test Speaker", resistance=6.27, inductance=0.06, QES=0.37, QMS=4.98, Resonant_frequency=61.03)
    try:
        speaker.plot_impedance((20, 20000, 0.5))
    except Exception as e:
        pytest.fail(f"Plotting failed with exception: {e}")

if __name__ == "__main__":
    pytest.main()
