def flatten_nestedlist(nested_list):
    return list(set([item for sublist in nested_list for item in sublist]))
    