def mark_test(function: callable) -> callable:
    """Mark a test function fo pytest can recognize and run it.

    Parameters
    ----------
    function : callable
        Test function to be marked.

    Returns
    -------
    callable
        Marked test function.
    """
    setattr(function, "__test__", True)
    return function
