"""
Draw a wave.
"""

import Image
import ImageDraw
import math


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


def main():
    # Open image.
    size = (1000, 100)
    width, height = size
    im = Image.new("RGB", size, 'white')
    draw = ImageDraw.Draw(im)

    # Draw dots.
    wave_length = 100
    for x in xrange(width):
        y = wave(x, height, wave_length)
        dot = (x, y)
        draw.point(dot, fill='blue')

    im.save("graph.png")

if __name__ == '__main__':
    main()
