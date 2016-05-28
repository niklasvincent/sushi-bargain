

def empty_time_slot_lookup_array():
    return [[] for i in range(7 * 24 * 2)]

def time_slot(day_of_the_week, hours):
    """Calculate time slot for given day of the week and hours"""
    if not hours:
        return -1
    return int(day_of_the_week * 24 * 2 + hours * 2)


def times_to_time_slots(times):
    """Given an array of times, calculate the respective time slots"""
    return [time_slot(i, v) for i, v in enumerate(times)]

