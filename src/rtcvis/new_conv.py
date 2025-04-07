from rtcvis.plf import PLF, plf_list_min_max

# from rtcvis.plot_plf import plot_plfs


def min_plus_convolution(a: PLF, b: PLF) -> PLF:
    assert a.x_start == 0 and b.x_start == 0
    assert a.x_end == b.x_end

    # create len(a.points) functions by adding a's points to b
    wsogmm1: list[PLF] = []
    for p in a.points:
        wsogmm1.append(b.add_point(p))

    # now we have to add len(b.points) new functions
    wsogmm2: list[PLF] = []
    for i in range(len(b.points)):
        # iterate over all points of b
        wsogmm2.append(PLF([wsogmm1[j].points[i] for j in range(len(a.points))]))

    # plot_plfs(wsogmm1 + wsogmm2)

    result: PLF = plf_list_min_max(wsogmm1 + wsogmm2, compute_min=True)

    return result.start_truncated(0).end_truncated(a.x_end)
