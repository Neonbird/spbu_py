def combine_with_existing(interval: tuple, intervals: list):
    """
    intersects:
    0 - didn't fell in any interval (if index_... != 0)
    1 - intersect
    2 - right edge
    3 - left edge
    """
    start_combined = False
    stop_combined = False
    start, stop = interval
    # searching for start of new interval
    for index_start, exist_intrvl in enumerate(intervals):
        start_exist, stop_exist = exist_intrvl
        if start_exist <= start <= stop_exist:
            # position of new interval fell into existing interval with index
            start_combined = start_exist
            intersect_start = 1
            break
        elif start < start_exist:
            # position didn't fell in any interval or it's on the left edge (if index_start == 0)
            start_combined = start
            if index_start == 0:
                intersect_start = 3
            else:
                intersect_start = 0
            break
    if not start_combined:
        # position on the right edge
        start_combined = start
        intersect_start = 2
    # searching for stop of new interval
    for index_stop, exist_intrvl in enumerate(intervals[index_start:]):
        start_exist, stop_exist = exist_intrvl
        if stop_exist >= stop >= start_exist:
            # position of new interval fell into existing interval with index
            stop_combined = stop_exist
            intersect_stop = 1
            index_stop += index_start
            break
        elif stop < start_exist:
            # position didn't fell in any interval or it's on the left edge (if index_start == 0)
            stop_combined = stop
            if index_stop == index_start:
                intersect_stop = 3
            else:
                intersect_stop = 0
            break
    if not stop_combined:
        # position on the right edge
        stop_combined = stop
        intersect_stop = 2
    return (start_combined, stop_combined), (index_start, index_stop), (intersect_start, intersect_stop)


def delete_intersections(interval_with_inf: tuple, intervals: list):
    """
    intersects:
    0 - didn't fell in any interval, but not on the edge
    1 - intersect
    2 - right edge
    3 - left edge
    """
    cleared_intervals = []
    combined_interval = interval_with_inf[0]
    index_start, index_stop = interval_with_inf[1]
    intersect_start, intersect_stop = interval_with_inf[2]
    if intersect_start == 2:
        cleared_intervals += intervals + [combined_interval]
    elif intersect_stop == 3:
        cleared_intervals += [combined_interval] + intervals
    else:
        cleared_intervals += intervals[:index_start] + [combined_interval]
        if intersect_stop == 1:
            cleared_intervals += intervals[index_stop + 1:]
        elif intersect_stop == 0:
            cleared_intervals += intervals[index_stop:]
    return cleared_intervals


def add_interval(new_interval: tuple, existing_intervals: list):
    return delete_intersections(combine_with_existing(new_interval, existing_intervals), existing_intervals)


def count_coverage(intervals):
    coverage = 0
    for interval in intervals:
        coverage += interval[1] - interval[0]
    return coverage


intervals = [tuple([int(x) for x in input().split(",")])]
print(count_coverage(intervals))
while True:
    new_interval = tuple([int(x) for x in input().split(",")])
    intervals = add_interval(new_interval, intervals)
    print(intervals)
    print(count_coverage(intervals))
