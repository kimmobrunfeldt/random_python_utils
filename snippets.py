"""
Useful, generic and reusable functions.
"""

import inspect
import os
import re
import subprocess
import sys


def run_command(command):
    """Runs an command and returns the stdout and stderr as a string.

    Args:
        command: Command to execute in Popen's list format.
                 E.g. ['ls', '..']

    Returns:
        tuple. (return_value, stdout, stderr), where return_value is the
        numerical exit code of process and stdout/err are strings containing
        the output. stdout/err is None if nothing has been output.
    """
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return_value = p.wait()
    return return_value, stdout, stderr


def open_with_default_application(file_path):
    """Opens given file with operating system's default application.

    Args:
        file_path: Path to the file that is opened.
    """
    # Mac
    if sys.platform.startswith('darwin'):
        return_value, stdout, stderr = run_command(['open', file_path])
        if return_value > 0:
            raise OSError(repr(stdout) + '\n' + repr(stderr))
    # Windows
    elif os.name == 'nt':
        os.startfile(file_path)
    # *nix(Linux etc.)
    elif os.name == 'posix':
        return_value, stdout, stderr = run_command(['xdg-open', file_path])
        if return_value > 0:
            raise OSError(repr(stdout) + '\n' + repr(stderr))


def split_camel(text):
    """Splits camel cased text to words.
    Works for ASCII, this solution is not reliable, use only for displaying
    purposes.

    See: http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    Also see tests/test_functions.py for examples.
    Args:
        text: str. CamelCasedText.
    Returns:
        list. List of words.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower().split()


def prettify_variable(name):
    """Prettifies variable's name for displaying purposes.
    E.g. _uglyVariable -> Ugly variable

    Args:
        name: Name of the variable to prettify.
    Returns:
        str. Prettified name.
    """
    # Split by n amount of '_' chars
    # '__a_b______c____d_' -> ['a', 'b', 'c', 'd']
    splitted = [x for x in name.split('_') if x]

    all_words = []
    for word in splitted:
        splitted_camel = split_camel(word)
        all_words.append(' '.join(splitted_camel))

    return ' '.join(all_words).capitalize()


def get_methods(obj, filter_func=None):
    """Finds out methods of a given object.

    Args:
        filter_func: Callable function that is used to filter out methodnames.
                     Method's name is given to this function. If the return
                     value is False, method is dropped from list.
    Returns:
        dict. Format: {"methodname": object}
    """
    # Get all methods of the class
    methods = inspect.getmembers(obj, predicate=inspect.ismethod)

    if filter_func is not None:
        # Keep method when filter_func(methodname) == True
        methodlist = [(x, y) for x, y in methods if filter_func(x)]
        methods = dict(methodlist)

    return methods


def get_file_docstring(file_path):
    """Finds out file's docstring.

    Args:
        file_path: Path to the file. Must be importable python file.
    Returns:
        str. A cleaned up docstring.
    """
    file_path = os.path.realpath(os.path.abspath(file_path))
    file_dir, file_name = os.path.split(file_path)

    # Now python can import the file
    sys.path.insert(0, file_dir)

    name, ext = os.path.splitext(file_name)

    docstring = None
    try:
        # Import the module
        imported_module = __import__(name)
        docstring = imported_module.__doc__.strip()
    except Exception, e:
        pass

    sys.path.remove(file_dir)

    return docstring


def dict_depth_call(dictionary, func):
    """Calls a function for all non-dictionary values in an arbitrary deeply
    nested dictionary.
    Note: Remember recursion depth limit.

    Args:
        dicionary: What dictionary to travel.
        func: Function to call for each value.
    """
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            dict_depth_call(value, func)
        else:
            func(value)
