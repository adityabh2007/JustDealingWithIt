import itertools
import random
import math
import matplotlib.pyplot as plt

c1 = random.randrange(15, 2**24)
c2 = random.randrange(0, 2**24)
hex1 = hex(c1)
hex2 = hex(c2)

DEFAULT_START = -1 * math.pi
DEFAULT_STOP = math.pi
DEFAULT_STEP = 0.01

def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += step

range1 = list(float_range(start = DEFAULT_START, stop = DEFAULT_STOP, step = DEFAULT_STEP))
range2 = list(float_range(start = DEFAULT_START, stop = DEFAULT_STOP, step = DEFAULT_STEP))

range_prod = list(itertools.product(range1, range2))

def f1(x, y):
    a1 = random.randint(1, 3)

    result = random.uniform(-1,1) * x**2  - math.sin(y**a1) + abs(y-x)
    return result

def f2(x, y):
    a2 = random.randint(1, 3)
    result = random.uniform(-1,0) * y**3 - math.cos(x**a2) + a2*x
    return result

data1 = []
data2 = []
x = random.randint(1,10000)

for item in range_prod:
    random.seed(x)
    data1.append(f1(item[0], item[1]).real)
    data2.append(f2(item[0], item[1]).real)

from matplotlib import colors as mcolors
VALID_COLORS = list(dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS).keys())
al = ["black", "white", "antiquewhite"]
DEFAULT_COLOR = hex2
DEFAULT_BACKGROUND_COLOR = random.choice(al)
DEFAULT_ALPHA = float(f"0.{str(random.randint(1, 999))}")
DEFAULT_IMAGE_SIZE = (8, 8)
DEFAULT_SPOT_SIZE = 0.01
DEFAULT_PROJECTION = None

def distance_calc(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(
                    1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def filter_color(color):
    if isinstance(color, tuple):
        return color
    if isinstance(color, str):
        distance_list = list(map(lambda x: distance_calc(color, x),
                                 VALID_COLORS))
        min_distance = min(distance_list)
        return VALID_COLORS[distance_list.index(min_distance)]
    return None

color, bgcolor = map(filter_color, [DEFAULT_COLOR, DEFAULT_BACKGROUND_COLOR])

fig = plt.figure()
fig.set_size_inches(DEFAULT_IMAGE_SIZE[0], DEFAULT_IMAGE_SIZE[1])
fig.set_facecolor(bgcolor)
ax = fig.add_subplot(111)
ax.set_facecolor(bgcolor)
ax.scatter(
    data2,
    data1,
    alpha=DEFAULT_ALPHA,
    edgecolors=color,
    s=DEFAULT_SPOT_SIZE)
ax.set_axis_off()
ax.patch.set_zorder(-1)
ax.add_artist(ax.patch)
n = DEFAULT_COLOR
fig.savefig(fname=f"seed_{n}")