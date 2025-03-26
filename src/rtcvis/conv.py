from rtcvis.plf import PLF


def min_plus_conv(a: PLF, b: PLF, delta_x: float) -> tuple[PLF, float]:
    a = a.transformed(mirror=True, offset=delta_x)
    s = a + b
    s = s.start_truncated(0).end_truncated(delta_x)
    return s, s.min
