from typing import Optional
from rtcvis.plf import PLF, plf_list_min_max
from rtcvis.conv import ConvType


def conv(
    a: PLF,
    b: PLF,
    conv_type: ConvType,
    start: Optional[float] = None,
    stop: Optional[float] = None,
) -> PLF:
    """Computes the convolution of two PLFs.

    Args:
        a (PLF): The first PLF.
        b (PLF): The second PLF.
        conv_type (ConvType): The type of convolution.
        start (Optional[float], optional): Where the resulting PLF's start should be
            truncated. Can be set to None if the result shouldn't be truncated.
            Defaults to None.
        stop (Optional[float], optional): Where the resulting PLF's end should be
            truncated. Can be set to None if the result shouldn't be trunated.
            Defaults to None.

    Returns:
        PLF: The result of the convolution.
    """
    # create len(a.points) functions by adding b's points to a
    wsogmm1: list[PLF] = []
    is_deconv = conv_type in (ConvType.MIN_PLUS_DECONV, ConvType.MAX_PLUS_DECONV)
    # convolutions mirror a first, which is why we need to add the x coordinates
    # deconvolutions dont mirror, which is why we need to subtract the x coordinates
    subtract_x = is_deconv
    # convolutions add the y values, deconvolutions subtract them
    subtract_y = is_deconv
    for p in b.points:
        wsogmm1.append(
            a.add_point(other=p, subtract_x=subtract_x, subtract_y=subtract_y)
        )

    # reverse the list if we're doing a deconvolution because they're currently given
    # in descending of x-coordinates
    if is_deconv:
        wsogmm1 = list(reversed(wsogmm1))

    wsogmm2: list[PLF] = []
    # now we create new PLFs by connecting the i-th point of each function in the
    # correct order and we do this for all points those functions
    for i in range(len(a.points)):
        wsogmm2.append(PLF([wsogmm1[j].points[i] for j in range(len(b.points))]))

    # Now we just need to compute the minimum or maximum over all those PLFs :)
    compute_min = conv_type in (ConvType.MIN_PLUS_CONV, ConvType.MAX_PLUS_DECONV)
    result: PLF = plf_list_min_max(wsogmm1 + wsogmm2, compute_min=compute_min)

    # Optionally truncate the start/end
    if start is not None:
        result = result.start_truncated(start)
    if stop is not None:
        result = result.end_truncated(stop)

    # remove redundant points
    result = result.simplified()

    return result
