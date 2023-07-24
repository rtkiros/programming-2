
def apply_functions(data, *functions):
    """
    Applies multiple functions to the data and returns the results as a list.

    Args:
        data (list): List of data values to apply the functions to.
        *functions (callable): Variable-length argument list of functions to apply.

    Returns:
        list: List of lists containing the results of applying each function to the data.
    """

    result = []
    # Could (should) be in one list comprehension
    for func in functions:
        result.append([func(value) for value in data])
    return result

data = [1, 2, 3, 4, 5]

# Define the functions to be applied
multiply_by_two = lambda x: x * 2
add_five = lambda x: x + 5

# Apply the functions to the data
result = apply_functions(data, multiply_by_two, add_five)

print(result)
