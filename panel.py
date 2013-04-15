"""
Helps to place rectangles on a bigger rectangle. Rectangles are placed
so they form a grid.
"""


class Panel(object):
    """Provides methods to place rectangles on a panel so that the rectangles
    do not overlap.
    """

    def __init__(self, width, height, padding_x=0, padding_y=0):
        """width and height are panel's dimensions."""
        self._width = width
        self._height = height

        self._padding_x = padding_x
        self._padding_y = padding_y

        # The currently maximum y coordinate that a rectangle's bottom has.
        self._current_max_y = 0

        self._current_x = self._padding_x
        self._current_y = self._padding_y

        # Format:
        # [
        #   ((topLeftX, topLeftY), (bottomRightX, bottomRightY))
        # ]
        self._rectangles = []

    def place_rectangle(self, width, height):
        """Places a rectangle to the panel so that it does not overlap with
        another rectangle. Rectangles are placed from left to right as tight
        as they fit taking the padding into account.

        Raises ValueError if placing is not possible.
        """
        if not self._does_rectangle_fit_in_y(height):
            raise ValueError("Rectangle does not fit.")

        if not self._does_rectangle_fit_in_x(width):

            self._start_new_row()
            if not self._does_rectangle_fit_in_x(width) or \
               not self._does_rectangle_fit_in_y(height):
                raise ValueError("Rectangle does not fit.")

        top_left = (self._current_x, self._current_y)
        bottom_right = (self._current_x + width, self._current_y + height)
        self._rectangles.append((top_left, bottom_right))

        self._current_x += width

        if self._current_max_y < bottom_right[1]:
            self._current_max_y = bottom_right[1]

        return self._rectangles[-1]

    def rectangles(self):
        return self._rectangles

    def _start_new_row(self):
        self._current_x = self._padding_x
        self._current_y = self._current_max_y + self._padding_y

    def _does_rectangle_fit_in_x(self, width):
        """width is width of the rectangle."""
        return self._current_x + width <= self._width

    def _does_rectangle_fit_in_y(self, height):
        """height is the height of the rectangle."""
        return self._current_y + height <= self._height


def main():
    panel = Panel(4, 4)
    for x in range(4):
        panel.place_rectangle(2, 2)
        print panel.rectangles()


if __name__ == '__main__':
    main()
