import enum
from typing import Callable
import numpy as np
from rtcvis.plf import PLF
from rtcvis.point import Point


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


def get_critical_points(a: PLF, b: PLF, truncate: bool) -> list[float]:
    """Computes an ordered list of all x-offset values by which a must be shifted so that
    one point of a will be at the same x coordinate as another point of b.

    This function is used for computing full convolutions.

    Args:
        a (PLF): Function a
        b (PLF): Function b
        truncate (bool): Whether the result should only contain value >= 0. A new value of 0 will be inserted after truncation if needed.

    Returns:
        list[float]: Ordered list of all x-offset values (unique).
    """
    b_x_cords = [point.x for point in b.points]
    critical_points = []
    for p in a.points:
        new_critical_points = [b_x_cord - p.x for b_x_cord in b_x_cords]
        critical_points += new_critical_points
    result = list(set(critical_points))
    result.sort()
    if len(result) == 0:
        return result

    if truncate:
        if result[0] >= 0:
            return result
        # result needs to be truncated, find the first element >= 0
        for idx, el in enumerate(result):
            if el == 0:
                return result[idx:]
            if el > 0:  # insert a 0 at the beginning
                return [0] + result[idx:]
        # all elements are < 0
        return []
    else:
        return result


class ConvType(enum.Enum):
    """All types of (de-)convolutions."""

    MAX_PLUS_CONV = 0
    MAX_PLUS_DECONV = 1
    MIN_PLUS_CONV = 2
    MIN_PLUS_DECONV = 3

    def get_conv_function(self) -> Callable[[PLF, PLF, float], tuple[PLF, float]]:
        """Returns the function for computing the corresponding (de-)convolution for
        a specific x.

        Returns:
            Callable[[PLF, PLF, float], tuple[PLF, float]]: The corresponding function.
        """
        match self:
            case ConvType.MAX_PLUS_CONV:
                return max_plus_conv
            case ConvType.MAX_PLUS_DECONV:
                return max_plus_deconv
            case ConvType.MIN_PLUS_CONV:
                return min_plus_conv
            case ConvType.MIN_PLUS_DECONV:
                return min_plus_deconv

    def mirrors(self) -> bool:
        """Returns whether this type of (de-)convolution mirrors a before shifting it.
        This is true for the convolutions and false for the deconvolutions.

        Returns:
            bool: Whether a gets mirrored.
        """
        return self == ConvType.MAX_PLUS_CONV or self == ConvType.MIN_PLUS_CONV


def get_full_plus_conv(a: PLF, b: PLF, conv_type: ConvType) -> PLF:
    conv_function = conv_type.get_conv_function()
    if conv_type == ConvType.MAX_PLUS_CONV or conv_type == ConvType.MIN_PLUS_CONV:
        critical_points = get_critical_points(a.transformed(True, 0), b, True)
    else:
        critical_points = get_critical_points(b, a, True)
    points = [Point(x, conv_function(a, b, x)[1]) for x in critical_points]
    return PLF(points)
