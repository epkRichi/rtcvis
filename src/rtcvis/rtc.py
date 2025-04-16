from typing import Sequence
from rtcvis.plf import PLF, plf_min_max
from rtcvis.conv import ConvType, conv


def check_plf_rtc(plfs: Sequence[PLF]) -> bool:
    """Check whether the PLFs are valid for RTC operations.

    This checks whether both functions start at 0 and end at the same x.

    Args:
        a (PLF): PLF a.
        b (PLF): PLF b.

    Returns:
        bool: Whether an RTC operation can be executed on the curves.
    """
    end = plfs[0].x_end
    return all(plf.x_start == 0 and plf.x_end == end for plf in plfs)


def upper_service_out(upper_service_in: PLF, lower_events_in: PLF) -> PLF:
    assert check_plf_rtc([upper_service_in, lower_events_in])
    length = upper_service_in.x_end
    result = upper_service_in - lower_events_in
    zero_plf = PLF([(0, 0), (length, 0)])
    result = conv(
        a=result, b=zero_plf, conv_type=ConvType.MAX_PLUS_DECONV, start=0, stop=length
    )
    result = plf_min_max(a=result, b=zero_plf, compute_min=False)
    return result


def lower_service_out(lower_service_in: PLF, upper_events_in: PLF) -> PLF:
    assert check_plf_rtc([lower_service_in, upper_events_in])
    length = lower_service_in.x_end
    result = lower_service_in - upper_events_in
    zero_plf = PLF([(0, 0), (length, 0)])
    result = conv(
        a=result, b=zero_plf, conv_type=ConvType.MAX_PLUS_CONV, start=0, stop=length
    )
    return result


def upper_events_out(
    upper_events_in: PLF, lower_service_in: PLF, upper_service_in: PLF
) -> PLF:
    assert check_plf_rtc([upper_events_in, lower_service_in, upper_service_in])
    length = upper_events_in.x_end
    result = conv(
        a=upper_events_in,
        b=upper_service_in,
        conv_type=ConvType.MIN_PLUS_CONV,
        start=0,
        stop=length,
    )
    result = conv(
        a=result,
        b=lower_service_in,
        conv_type=ConvType.MIN_PLUS_DECONV,
        start=0,
        stop=length,
    )
    result = plf_min_max(a=result, b=upper_service_in, compute_min=True)
    result = result.ceiled()
    return result


def lower_events_out(
    lower_events_in: PLF, lower_service_in: PLF, upper_service_in: PLF
) -> PLF:
    assert check_plf_rtc([lower_events_in, lower_service_in, upper_service_in])
    length = lower_events_in.x_end
    result = conv(
        a=lower_events_in,
        b=upper_service_in,
        conv_type=ConvType.MIN_PLUS_DECONV,
        start=0,
        stop=length,
    )
    result = conv(
        a=result,
        b=lower_service_in,
        conv_type=ConvType.MIN_PLUS_CONV,
        start=0,
        stop=length,
    )
    result = plf_min_max(a=result, b=lower_service_in, compute_min=True)
    result = result.floored()

    return result
