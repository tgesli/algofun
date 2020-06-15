def dayRange(days):
    dayNames = ["Sun", "M", "Tu", "W", "Th", "F", "Sat"]

    if not days:
        return ""

    segments = []
    last = 0
    for i in range(len(days)-1):
        if days[i + 1] - days[i] > 1:
            segments.append(days[last:i + 1])
            last = i+1

    segments.append(days[last:])

    res = ""
    delim = ""
    for seg in segments:
        if len(seg) > 1:
            res += delim + dayNames[seg[0]] + '-' + dayNames[seg[-1]]
        else:
            res += delim + dayNames[seg[0]]
        delim = ","

    return res


print(dayRange([1, 2, 3, 5]))