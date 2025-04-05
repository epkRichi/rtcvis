from rtcvis.plf import PLF, plf_min_max
from rtcvis.conv import ConvType, conv


def check_plf_rtc(a: PLF, b: PLF) -> bool:
    """Check whether the PLFs are valid for RTC operations.

    This checks whether both functions start at 0 and end at the same x.

    Args:
        a (PLF): PLF a.
        b (PLF): PLF b.

    Returns:
        bool: Whether an RTC operation can be executed on the curves.
    """
    return a.x_start == 0 and a.x_start == b.x_start and a.x_end == b.x_end


def upper_service_out(upper_service_in: PLF, lower_events_in: PLF) -> PLF:
    assert check_plf_rtc(upper_service_in, lower_events_in)
    length = upper_service_in.x_end
    result = upper_service_in - lower_events_in
    zero_plf = PLF([(0, 0), (length, 0)])
    result = conv(
        a=result, b=zero_plf, conv_type=ConvType.MAX_PLUS_DECONV, start=0, stop=length
    )
    result = plf_min_max(a=result, b=zero_plf, compute_min=False)
    return result


def lower_service_out(lower_service_in: PLF, upper_events_in: PLF) -> PLF:
    assert check_plf_rtc(lower_service_in, upper_events_in)
    length = lower_service_in.x_end
    result = lower_service_in - upper_events_in
    zero_plf = PLF([(0, 0), (length, 0)])
    result = conv(
        a=result, b=zero_plf, conv_type=ConvType.MAX_PLUS_CONV, start=0, stop=length
    )
    return result
