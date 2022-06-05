


def clear_dict(target_dict: dict, value):
    result = dict()
    for key in target_dict.keys():
        if target_dict[key] != value:
            result[key] = target_dict[key]
    return result