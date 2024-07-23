"Module for multithreading."
import concurrent.futures as cf


def multithreading(func, *args, **kwargs):
    """
    concurrent.futures.ThreadPoolExecutor wrapper for multithreading.

    Args:
        func (function): The function to be executed.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        list: Results of the function execution.
    """
    with cf.ThreadPoolExecutor(max_workers=None) as executor:
        results = list(executor.map(func, *args, **kwargs))
    return results