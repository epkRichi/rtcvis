from typing import Optional
import enum
from rtcvis.plf import PLF
from rtcvis.point import Point


class ConvType(enum.Enum):
    """All types of (de-)convolutions."""

    MAX_PLUS_CONV = 0
    MAX_PLUS_DECONV = 1
    MIN_PLUS_CONV = 2
    MIN_PLUS_DECONV = 3


class ConvAtXResult:
    def __init__(self, transformed_a: PLF, sum: PLF, result: float) -> None:
        """The result of a convolution at a specific x.

        Args:
            transformed_a (PLF): The shifted and optionally mirrored PLF a.
            sum (PLF): The sum or difference between the transformed PLF a and PLF b.
            result (float): The actual result of the convolution.
        """
        self._transformed_a = transformed_a
        self._sum = sum
        self._result = result

    @property
    def transformed_a(self) -> PLF:
        return self._transformed_a

    @property
    def sum(self) -> PLF:
        return self._sum

    @property
    def result(self) -> float:
        return self._result

    def __eq__(self, other) -> bool:
        return self.result == other


def conv_at_x(a: PLF, b: PLF, delta_x: float, conv_type: ConvType) -> ConvAtXResult:
    """Computes the given type of convolution of a and b at the given x.

    Args:
        a (PLF): PLF a
        b (PLF): PLF b
        delta_x (float): The x at which to evaluate the convolution.
        conv_type (ConvType): The type of convolution

    Returns:
        ConvAtXResult: An object containing several properties of the result.
    """
    if conv_type == ConvType.MIN_PLUS_CONV or conv_type == ConvType.MAX_PLUS_CONV:
        transformed_a = a.transformed(mirror=True, offset=delta_x)
        s = transformed_a + b
    else:
        transformed_a = a.transformed(mirror=False, offset=-delta_x)
        s = transformed_a - b
    if conv_type == ConvType.MIN_PLUS_CONV or conv_type == ConvType.MAX_PLUS_DECONV:
        result = s.min
    else:
        result = s.max
    return ConvAtXResult(transformed_a=transformed_a, sum=s, result=result)


def get_critical_points(
    a: PLF,
    b: PLF,
    conv_type: ConvType,
    start: Optional[float] = None,
    stop: Optional[float] = None,
) -> list[float]:
    """Computes an ordered list of all x-offset values by which a must be shifted so that
    one point of a will be at the same x coordinate as another point of b.

    This function is used for computing full convolutions.

    Args:
        a (PLF): PLF a
        b (PLF): PLF b
        truncate (bool): Whether the result should only contain value >= 0. A new value of 0 will be inserted after truncation if needed.

    Returns:
        list[float]: Ordered list of all x-offset values (unique).
    """
    if conv_type == ConvType.MAX_PLUS_CONV or conv_type == ConvType.MIN_PLUS_CONV:
        a = a.transformed(
            True, 0
        )  # a has to be mirrored before being moved to the right
    else:
        a, b = (
            b,
            a,
        )  # a has to be moved to the left which is the same as moving b to the right

    b_x_cords = [point.x for point in b.points]
    critical_points = []
    for p in a.points:
        new_critical_points = [b_x_cord - p.x for b_x_cord in b_x_cords]
        critical_points += new_critical_points
    result = list(set(critical_points))
    result.sort()
    if len(result) == 0:
        return result

    if start is not None and result[0] < start:
        if result[-1] < start:
            # all elements are < start
            return []
        # result needs to be truncated at start, find the first element >= start
        for idx, el in enumerate(result):
            if el == start:
                result = result[idx:]
                break
            if el > start:  # insert a 0 at the beginning
                result = [start] + result[idx:]
                break

    if stop is not None and result[-1] > stop:
        if result[0] > stop:
            # all elements are > stop
            return []
        # result needs to be truncated at end, find the last element < stop
        for idx, el in reversed(list(enumerate(result))):
            if el == stop:
                result = result[: idx + 1]
                break
            if el < stop:  # insert a 0 at the beginning
                result = result[: idx + 1] + [stop]
                break

    return result


def conv(
    a: PLF,
    b: PLF,
    conv_type: ConvType,
    start: Optional[float] = None,
    stop: Optional[float] = None,
) -> PLF:
    """Computes the convolution of given type of a and b.

    Args:
        a (PLF): PLF a
        b (PLF): PLF b
        conv_type (ConvType): The type of convolution
        start (Optional[float], optional): The lowest x value for which the resulting PLF should be defined. Defaults to None.
        stop (Optional[float], optional): The largest x value for which the resulting PLF should be defined. Defaults to None.

    Returns:
        PLF: The result of the convolution.
    """
    critical_points = get_critical_points(a, b, conv_type, start, stop)
    points = [Point(x, conv_at_x(a, b, x, conv_type).result) for x in critical_points]
    return PLF(points)
