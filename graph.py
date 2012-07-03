"""
Draw a random wave.
"""

import Image
import ImageDraw
import math
import random


def wave(x, amplitude, wave_length):
    """As x grows, (x, y) coordinates start to shape a wave.
    http://en.wikipedia.org/wiki/Amplitude
    http://en.wikipedia.org/wiki/Wavelength

    Args:
        amplitude: Peak-to-peak amplitude of the wave.
        wave_length: The spatial period of the wave. The distance over which
                     the wave's shape repeats.
    Returns:
        float. Y value of the graph on given x.
    """
    # The multiplier of x defines the wave's length. E.g sin(3x) has 3 times
    # smaller wave length than sin(x).
    x = x * (2 * math.pi / wave_length)

    # Substituting or increasing x moves the wave horizontally.
    # Substituting pi/2 moves the wave, so it's "first" peak is where x=0.
    # sin returns values from -1 to 1, we want from 0 - 1, that's why we
    # add 1 and divide by 2.
    zero_to_one = (math.sin(x - math.pi / 2) + 1) / 2

    return zero_to_one * amplitude


def rotate(x, y, rotation):
    """Rotate coordinates around origin.

    Args:
        x, y: Coordinates.
        rotation: Rotation counter clockwise in radians.
    """
    sin = math.sin
    cos = math.cos
    new_x = (cos(rotation) * x - (sin(rotation) * y))
    new_y = (sin(rotation) * x + cos(rotation) * y)
    return new_x, new_y


def main():
    # Open image.
    size = (3000, 3000)
    width, height = size
    im = Image.new("RGB", size, 'white')
    draw = ImageDraw.Draw(im)

    # Amplitude decreases on every cycle.
    amplitude_factor = 0.999
    starting_dot = (1500, 1500)
    line_count = 300

    # Draw lines.
    for i in xrange(line_count):

        last_dot = starting_dot
        amplitude = random.randint(20, 150)
        wave_length = random.randint(300, 1000)
        rotation = random.uniform(0, 2 * math.pi)
        line_length = random.randint(300, 1500)

        # Draw dots.
        for x in xrange(line_length):
            amplitude = amplitude * amplitude_factor
            y = wave(x, amplitude, wave_length)
            x, y = rotate(x, y, rotation)
            dot = (x + starting_dot[0], y + starting_dot[1])
            draw.line([last_dot, dot], fill='blue')
            last_dot = dot

    im.save("graph.png")

if __name__ == '__main__':
    main()
