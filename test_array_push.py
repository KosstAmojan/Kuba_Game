def push_array(array, starting_index, color):
    """
    This is a helper function that will push the marbles in an array that is provided at the starting index.
    :param starting_index:
    :param array:
    :return:
    """
    result_array = []
    result_array.append('X')
    if starting_index > 0:
        for index in range(0, starting_index):
            result_array.append(array[index])
    for value in range(starting_index, len(array)):
        if len(result_array) == 7:
            break
        if array[value] == 'X' and array[value - 1] == color:
            continue
        result_array.append(array[value])

    return result_array

