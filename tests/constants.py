"""Test constants for DellGuard test suite

This module contains all magic numbers and test data constants used across
the test suite. Centralizing these values makes tests more maintainable and
documents the reasoning behind test data choices.
"""

# Baseline test data
# These values represent a typical healthy server baseline
TEST_BASELINE_MEAN = 40.0  # Average CPU usage for healthy server (%)
TEST_BASELINE_STD = 5.0    # Standard deviation of CPU usage

# Alternative baseline values for testing different scenarios
TEST_BASELINE_MEAN_ALT = 50.0
TEST_BASELINE_STD_ALT = 10.0
TEST_BASELINE_MEAN_ALT2 = 45.0
TEST_BASELINE_STD_ALT2 = 7.5

# Threshold calculation
TEST_SIGMA = 3.0  # Standard 3-sigma threshold
TEST_SIGMA_ALT = 2.0  # Alternative sigma for testing
TEST_EXPECTED_THRESHOLD = 55.0  # TEST_BASELINE_MEAN + (TEST_SIGMA * TEST_BASELINE_STD)
TEST_EXPECTED_THRESHOLD_ALT = 70.0  # 50.0 + (2.0 * 10.0)

# Monitoring steps
TEST_STEPS_SHORT = 5   # Short monitoring cycle for quick tests
TEST_STEPS_FULL = 10   # Full monitoring cycle
TEST_BREACH_STEP = 6   # Step at which breach occurs in simulator

# AI call durations (milliseconds)
TEST_AI_DURATION_FAST_MS = 500.0    # Fast AI response
TEST_AI_DURATION_NORMAL_MS = 1000.0  # Normal AI response
TEST_AI_DURATION_SLOW_MS = 1500.0    # Slow AI response

# Test timing
TEST_SLEEP_DURATION_SECONDS = 0.01  # 10ms sleep for timer tests

# Test responses
TEST_AI_RESPONSE_DEFAULT = "Mock AI analysis: CPU threshold breached"
TEST_AI_RESPONSE_CUSTOM = "Test AI diagnosis"
