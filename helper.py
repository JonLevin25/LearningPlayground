def byte_str(n: int, group_len=8):
    if n < 0 or n > 2 ** group_len:
        raise ValueError
    return format(n, f"0{group_len}b")


def grouper(n: int, iterable: iter, filler=None) -> iter:
    iterator = iter(iterable)

    i = 0
    current = []

    while True:
        try:
            current.append(next(iterator))

            # if added last in group
            if i == n - 1:
                yield current
                current = []
                i = 0
                continue
            i += 1
        except StopIteration:
            has_unfinished_group = i != 0
            if has_unfinished_group:
                remaining = n - i
                # if relevant, fill last iteration
                if filler is not None:
                    for i in range(remaining):
                        current.append(filler)
                yield current
            break


def group_str(n, string: str, filler=None):
    for group in grouper(n, string, filler):
        yield "".join(group)


def dict_builder(*tups):
    result = {}
    v_start = 0
    for tup in tups:
        if len(tup) == 2:
            c_start, c_end = tup
        elif len(tup) == 1:
            c_start = c_end = tup
        else:
            raise ValueError(f"Invalid input: {str(tup)}")

        # update result dict
        dic = _dict_range(c_start, c_end, v_start)
        result.update(dic)

        # update start value
        len_added = len(dic.keys())
        v_start += len_added
    return result


def _dict_range(c_start, c_end, v_start):
    v_offset = v_start - ord(c_start)

    chars = (chr(i) for i in range(ord(c_start), ord(c_end) + 1))
    return {c: ord(c) + v_offset for c in chars}
