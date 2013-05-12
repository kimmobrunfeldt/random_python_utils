"""
Contains convenient list type which can be used in history lists.
"""


class HistoryList(object):
    """List that keeps a history of objects in chronological order. If
    existing object is appended again, it is moved to be most recently added.

    First item of the list is the newet, last is the oldest.
    Note: The internal list keeps the data in reversed order. So first item
          of that list is actually the oldest.
    """
    def __init__(self, max_length=None):
        self.max_length = max_length
        self._history = []

    def newest(self):
        """Returns the newest item in the list."""
        return self._history[-1]

    def oldest(self):
        """Returns the oldest item in the list."""
        return self._history[0]

    def append(self, obj):
        """Appends an object to the list."""
        # Item already exists in the list, move it to last
        if obj in self._history:
            self._history.remove(obj)
            self._history.append(obj)
        else:
            self._history.append(obj)

            # If maximum length is exceeded, drop the first item(oldest).
            if self._is_too_long():
                self._history.pop(0)

    def remove(self, obj):
        """Removes an object from the list."""
        self._history.remove(obj)

    def _is_too_long(self):
        """Returns True if the list is too long."""
        is_infinite = self.max_length is None
        is_too_long = len(self._history) > self.max_length
        return not is_infinite and is_too_long

    def __iter__(self):
        """Iterating the list will iterate the list from newest to oldest."""
        for item in reversed(self._history):
            yield item

    def __repr__(self):
        # This is not very efficient with big lists.
        return repr(self._history[::-1])

    def __str__(self):
        return str(self._history[::-1])

    def __len__(self):
        return len(self._history)

    def __contains__(self, item):
        """Operator 'in'. For example 'x in historylist'."""
        return item in self._history
