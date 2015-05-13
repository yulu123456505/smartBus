from matplotlib import pyplot as plt
from matplotlib import animation
from random import randrange
from matplotlib.patches import Circle

fig = plt.figure()
ax = plt.axes(xlim=(-100, 1000), ylim=(-100, 1000))
line, = plt.plot([], [], 'b.', markersize=14)


def init():
    line.set_data([], [])

    return line

# animation function.  this is called sequentially
def animate(i):
    x = [randrange(1, 1000) for i in range(20)]
    y = [randrange(1, 1000) for i in range(20)]
    line.set_data(x, y)
    c = [[randrange(1, 1000), randrange(1, 1000)] for k in range(randrange(4, 10))]
    for aa, bb in c:
        ax.add_patch(Circle(xy=(aa, bb), radius=40, alpha=0.5))
    return line

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=200)
plt.show()