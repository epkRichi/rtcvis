from rtcvis.plf import PLF


def plus_conv(a: PLF, b: PLF, delta_x: float) -> PLF:
    r"""Computes the resulting PLF of the plus convolution of a and b.
    This function does not return the minimum or maximum of the resulting
    PLF, it instead returns the PLF itself. The returned function will
    also be truncated so it is only defined for 0 <= x <= delta_x.

    Returned PLF: f(x) = a(delta_x - x) + b(x)

    Args:
        a (PLF): Function a.
        b (PLF): Function b.
        delta_x (float): The x for which to compute the plus convolution.

    Returns:
        PLF: The result of the plus convolution.
    """
    a = a.transformed(mirror=True, offset=delta_x)
    s = a + b
    s = s.start_truncated(0).end_truncated(delta_x)
    return s


def plus_deconv(a: PLF, b: PLF, delta_x: float) -> PLF:
    r"""Computes the resulting PLF of the plus deconvolution of a and b.
    This function does not return the minimum or maximum of the resulting
    PLF, it instead returns the PLF itself. The returned function will
    also be truncated so it is only defined for x > 0.

    Returned PLF: f(x) = a(delta_x + x) - b(x)

    Args:
        a (PLF): Function a.
        b (PLF): Function b.
        delta_x (float): The x for which to compute the plus deconvolution.

    Returns:
        PLF: The result of the plus convolution.
    """
    a = a.transformed(mirror=False, offset=-delta_x)
    s = a - b
    s = s.start_truncated(0)
    return s


def min_plus_conv(a: PLF, b: PLF, delta_x: float) -> tuple[PLF, float]:
    r"""Computes the min plus convolution of a and b at delta_x. Returns
    the result as well as the resulting function before taking the minimum.

    Args:
        a (PLF): Function a.
        b (PLF): Function b.
        delta_x (float): The x for which to compute the min plus convolution.

    Returns:
        tuple[PLF, float]: The resulting PLF and its minimum.
    """
    f = plus_conv(a=a, b=b, delta_x=delta_x)
    return f, f.min


def min_plus_deconv(a: PLF, b: PLF, delta_x: float) -> tuple[PLF, float]:
    r"""Computes the min plus deconvolution of a and b at delta_x. Returns
    the result as well as the resulting function before taking the maximum.

    Args:
        a (PLF): Function a.
        b (PLF): Function b.
        delta_x (float): The x for which to compute the min plus deconvolution.

    Returns:
        tuple[PLF, float]: The resulting PLF and its maximum.
    """
    f = plus_deconv(a=a, b=b, delta_x=delta_x)
    return f, f.max


def max_plus_conv(a: PLF, b: PLF, delta_x: float) -> tuple[PLF, float]:
    r"""Computes the max plus convolution of a and b at delta_x. Returns
    the result as well as the resulting function before taking the maximum.

    Args:
        a (PLF): Function a.
        b (PLF): Function b.
        delta_x (float): The x for which to compute the max plus convolution.

    Returns:
        tuple[PLF, float]: The resulting PLF and its maximum.
    """
    f = plus_conv(a=a, b=b, delta_x=delta_x)
    return f, f.max


def max_plus_deconv(a: PLF, b: PLF, delta_x: float) -> tuple[PLF, float]:
    r"""Computes the max plus deconvolution of a and b at delta_x. Returns
    the result as well as the resulting function before taking the minimum.

    Args:
        a (PLF): Function a.
        b (PLF): Function b.
        delta_x (float): The x for which to compute the max plus deconvolution.

    Returns:
        tuple[PLF, float]: The resulting PLF and its minimum.
    """
    f = plus_deconv(a=a, b=b, delta_x=delta_x)
    return f, f.min
