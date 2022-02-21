from enum import Enum
from colormaps import turbo_colormap, viridis_colormap, magma_colormap, inferno_colormap, plasma_colormap, green_colormap, red_colormap, blue_colormap
from copy import deepcopy


class Color(Enum):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 102)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    GREEN = (0, 255, 0)
    BLUE = (50, 153, 213)
    GREY = (128, 128, 128)

# I made this function because I didn't want to surround the colormaps in the colormaps dict with the make_continuous function. Maybe that is the better option though
# Is there a third way?

def extend_colormaps(colormaps):
    for name, colormap in colormaps.items():
        colormaps[name] = make_continuous(colormap)

def make_continuous(colormap):
    tail = deepcopy(colormap)
    tail.reverse()
    return colormap + tail

colormaps = {
    "Turbo" : turbo_colormap, 
    "Magma" : magma_colormap, 
    "Viridis" : viridis_colormap,
    "Inferno" : inferno_colormap, 
    "Plasma" : plasma_colormap,
    "Green" : green_colormap,
    "Red" : red_colormap,
    "Blue" : blue_colormap,
    }

extend_colormaps(colormaps)

# TODO replace all instances of this color with the next color_from_map function
def color(colormap, i):
    return to_rgb(colormap[i % len(colormap)])

def color_from_map(colormap, i):
    return to_rgb(colormap[i % len(colormap)])

def rgb_color(r,g,b,a = 255):
    return ()

def to_rgb(color_floats):
    return tuple(x * 255.0 for x in color_floats)

def turbo_color(i):
    return to_rgb(turbo_colormap[i%len(turbo_colormap)])

# Copyright 2019 Google LLC.
# SPDX-License-Identifier: Apache-2.0

# Author: Anton Mikhailov


# The look-up table contains 256 entries. Each entry is a floating point sRGB triplet.
# To use it with matplotlib, pass cmap=ListedColormap(turbo_colormap_data) as an arg to imshow() (don't forget "from matplotlib.colors import ListedColormap").
# If you have a typical 8-bit greyscale image, you can use the 8-bit value to index into this LUT directly.
# The floating point color values can be converted to 8-bit sRGB via multiplying by 255 and casting/flooring to an integer. Saturation should not be required for IEEE-754 compliant arithmetic.
# If you have a floating point value in the range [0,1], you can use interpolate() to linearly interpolate between the entries.
# If you have 16-bit or 32-bit integer values, convert them to floating point values on the [0,1] range and then use interpolate(). Doing the interpolation in floating point will reduce banding.
# If some of your values may lie outside the [0,1] range, use interpolate_or_clip() to highlight them.

def fade_colors(from_color, to_color, steps, current_step):
    return [x + ((y - x)/steps) * current_step for x, y in zip(from_color, to_color)]

def interpolate(colormap, x):
  x = max(0.0, min(1.0, x))
  a = int(x*255.0)
  b = min(255, a + 1)
  f = x*255.0 - a
  return [colormap[a][0] + (colormap[b][0] - colormap[a][0]) * f,
          colormap[a][1] + (colormap[b][1] - colormap[a][1]) * f,
          colormap[a][2] + (colormap[b][2] - colormap[a][2]) * f]

def interpolate_or_clip(colormap, x):
  if   x < 0.0: return [0.0, 0.0, 0.0]
  elif x > 1.0: return [1.0, 1.0, 1.0]
  else: return interpolate(colormap, x)
