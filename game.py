import random


def generateNumber(k=4):
    """

    :param k:
    :return: a list of k random digits (excluding 0)
    """
    return random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], k)


def evaluateSolution(solution: list, answer: list):
    if type(solution) != list or type(answer) != list:
        raise TypeError('Solution or/and answer of the wrong type')
    if len(solution) != 4 or len(answer) != 4:
        raise Exception('Solution and/or answer do not have 4 elements')

    centered_numbers = 0
    uncentered_numbers = 0

    for key, value in enumerate(answer):
        if value == solution[key]:
            centered_numbers = centered_numbers + 1
        elif value in solution:
            uncentered_numbers = uncentered_numbers + 1

    return (centered_numbers, uncentered_numbers)
