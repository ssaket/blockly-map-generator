from enum import Enum
from random import randint

# The maximum limit for the random number generator
MAX_LIMIT = 25


def table_1(length=20):
    """Generate a list of numbers that are multiples of 1.
    
    Args:
        length (int, optional): The length of the list. Defaults to 20.
    Returns:
        list: A list of numbers that are multiples of 1.
    """
    start = randint(0, MAX_LIMIT)
    end = MAX_LIMIT + start
    return [x for x in range(start, end)][:length]


def table_2(length=20):
    """Generate a list of numbers that are multiples of 2.
    
    Args:
        length (int, optional): The length of the list. Defaults to 20.
    Returns:
        list: A list of numbers that are multiples of 2.
    """
    start = randint(0, MAX_LIMIT)
    end = 2 * MAX_LIMIT + start
    return [x for x in range(start, end, 2)][:length]


def table_5(length=20):
    """Generate a list of numbers that are multiples of 5.

    Args:
        length (int, optional): The length of the list. Defaults to 20.
    Returns:
        list: A list of numbers that are multiples of 5.
    """
    start = randint(0, MAX_LIMIT)
    end = 5 * MAX_LIMIT + start
    return [x for x in range(start, end, 5)][:length]


def conditions_1(length=20):
    """Generate a list of numbers with a condition. The condition is that the number is less than Max Limit. 
    If the number is greater than Max Limit, then subtract the number from Max Limit. 
     
    Args:
        length (int, optional): The length of the list. Defaults to 20.
        Returns:
        list: A list of numbers with a condition.
    """
    start = 0
    end = MAX_LIMIT
    return [x if x < (MAX_LIMIT) else MAX_LIMIT - x for x in range(start, end)
           ][:length]


def conditions_2(length=20):
    """Generate a list of numbers with a condition. The condition is that the number is less than Max Limit.
    If the number is greater than Max Limit, then subtract a random number from the number.

    Args:
        length (int, optional): The length of the list. Defaults to 20.
    Returns:
        list: A list of numbers with a condition.
    """
    start = 0
    end = MAX_LIMIT
    sub = randint(1, MAX_LIMIT)
    border = randint(1, MAX_LIMIT)
    return [x if x < border else x - sub for x in range(start, end)][:length]


def random_letter_sequence(length=20):
    """Generate a random string of letters.

    Args:
        length (int, optional): The length of the list. Defaults to 20.
    Returns:
        list: A list of random letters.
    """
    start = randint(1, MAX_LIMIT)
    end = MAX_LIMIT + start
    # generate random string of letters
    return [chr(randint(97, 122)) for x in range(start, end)][:length]


class Rewards(Enum):
    """Code block enum. Each code block represents a command for the agent."""
    TABLE_1 = (1, table_1)
    TABLE_2 = (2, table_2)
    TABLE_5 = (3, table_5)
    CONDITIONS_1 = (4, conditions_1)
    CONDITIONS_2 = (4, conditions_2)
    RANDOM_LETTER_SEQUENCE = (5, random_letter_sequence)


if __name__ == "__main__":
    for reward in Rewards:
        print(reward.value[1](5))
