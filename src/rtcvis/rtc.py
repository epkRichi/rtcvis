from typing import Sequence
from rtcvis.plf import PLF, plf_min_max
from rtcvis.conv import ConvType, conv

"""
The current approach for PLFs and convolutions is too simple to compute RTC output
curves. The key problem is that event and service curves are assumed to be repeating
periodically, and this has to be respected when computing convolutions. The current
function for computing convolution can only handle finite PLFs.

For deconvolutions, PLF a simply has to be moved to the left. Handling periodic
functions should not be a huge problem since both the transformed a and b are always
defined for all x>=0. Each period of b will always see the same part of a, just with a
different y-offset. This means that we can simply repeat a once and compute the
convolution the way it is done right now and the result just has to be interpreted as a
periodically repeating function as well. The only thing to consider is that for example
for the min-plus-deconvolution, the maximum of the difference between a and b is
computed. If now the y-offset/the difference keeps getting bigger and bigger, the result
would be infinity. We could either introduce a way to represent infinity (technically
this is already possible with floats...) or we could throw an error. If the differnce
does not get bigger, then it gets smaller or stays the same, meaning that the first
period will be where the maximum difference is located and that's why the current
implementation works for many PLFs. For the max-plus-deconvolution, we instead have to
check that the difference (a-b) keeps getting bigger since we're computing the minimum.

Convolutions are unfortunately more tricky. Since we mirror PLF a before offsetting it
on the x-axis, this means that the area of overlap between a and b is finite (and keeps
getting bigger). So when computing convolutions, we'll also have many periods that
fully overlap with a and which will thus all see the same values, just at different y
offsets. The problem is however that the period where the current "end" of a is will
only partially overlap with a and it can thus have a different result (even when
considering the different y-offset) than the other "repetitive" periods. What will
happen is that the extremum we're looking for might be in the non-overlapping period at
first but at some x, it can change and the extremum will then be located in the
overlapping periods. I'm not sure when exactly this switch will happen or how to compute
that. But it will lead to a resulting PLF that starts with an aperiodic part and which
continues with a periodic part. I'm also not sure if the periodic and aperiodic parts
will always have the same length as the periods of a and b or if that might differ.

So, if we really want to compute RTC output curves, we have to support PLFs with an
aperiodic part at the start, followed by a periodic part. Supporting that in all
existing methods like add and match will be a lot of work and after that, the
convolution function still has to be adapted and I'm not sure how complicated this is
going to be. For this reason, I've decided to remove all output-curve related code from
main and put it on a separate branch.

I'm however not sure if I'll even try to add the described features to rtcvis. I've
mainly created this package for visualizing (de-)convolutions with the min-plus-algebra
and this works very well. Computing output functions would be very cool of course, but
it would hardly add anything that the rtctoolbox from ETH Zürich can't do. Using
rtctoolbox, you can also plot every individual step of computing the output curves. The
only thing it can't do is give you an interactive plot for computing the convolutions
of curves (and since these have to be periodic, rtcvis can't do that right now either).
So adding support for periodic functions sounds like a lot of work for very few benefits
(unless we count using matlab as a major disadvantage for rtctoolbox :D)

Anyways, here are two PLFs where if you interpret them as periodic PLFs (without
aperiodic parts), the current convolution function computes an incorrect result for the
min plus deconv:
a = PLF([(0, 0), (9, 9), (15, 9)])
b = PLF([(0, 0), (2, 0), (15, 13)])
The part with slope 0 at the start has to be longer than the following
parts of slope 0, which are all the same length.
"""


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
