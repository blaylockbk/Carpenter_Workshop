"""
Tests for toolbox.wind
"""

import toolbox.wind
import numpy as np

def test_wind_power_law():
    """Test wind_power_law"""

    # A 5 m/s wind at 10 m adjusted to 10 m should be 5 m/s
    assert np.isclose(toolbox.wind.wind_profile_power_law(5, 10, 10), 5)

    # A 10 m/s wind at 5 m adjusted to 10 m should be ~11.04 m/s
    assert np.isclose(toolbox.wind.wind_profile_power_law(10, 5, 10), 11.041988471630928)
