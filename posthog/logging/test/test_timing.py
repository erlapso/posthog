from posthog.logging.timing import (
    timed,
    timed_log,
)
from unittest.mock import (
    Mock,
    call,
    patch,
)


@patch("posthog.logging.timing.statsd.timer")
def test_wrap_with_timing_calls_statsd(mock_timer) -> None:
    timer_instance = Mock()
    mock_timer.return_value = timer_instance

    @timed(name="test")
    def test_func():
        pass

    test_func()
    mock_timer.assert_called_with("test")
    timer_instance.assert_has_calls(calls=[call.start(), call.start().stop()])


@patch("posthog.logging.timing.print")
@patch("posthog.logging.timing.time", side_effect=[100, 100.05])
def test_timed_log_prints_timing_info(mock_time, mock_print):
    """
    Test that the timed_log decorator prints the correct timing information and arguments after function execution.
    This test patches time() to simulate a fixed duration and print() to capture the output.
    """

    @timed_log()
    def sample_function(x, y=None):
        return x + (y if y else 0)

    result = sample_function(10, y=5)
    assert result == 15
    expected_duration = round((100.05 - 100) * 1000, 1)
    expected_message = (
        f"Timed function: sample_function took {expected_duration}ms with args"
    )
    mock_print.assert_called_once_with(
        expected_message, {"args": (10,), "kwargs": {"y": 5}}
    )
