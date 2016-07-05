#Creating animated maps

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

lons = []
lats = []
iterr = 0

my_map = Basemap(llcrnrlon = -130, llcrnrlat = 15, urcrnrlon = -60, urcrnrlat = 60)
          
my_map.drawcoastlines()
my_map.drawcountries(linewidth = 0.4, linestyle = 'solid', color = 'black', antialiased = 1, ax = None, zorder = None)
my_map.fillcontinents(color = 'gray')
my_map.drawstates()
my_map.drawmapboundary()
my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))

x,y = my_map(0, 0)
point = my_map.plot(x, y, 'ro', markersize=5)[0]		

states = [(32.3668, -86.3), (58.3019, -134.4197), (33.4484, -112.0740), (34.7465, -92.2896),
			(38.5816, -121.4944), (39.7392, -104.9903), (41.7637, -72.6851), (39.1582, -75.5244),
			(30.4383, -84.2807), (33.7490, -84.388), (21.3069, -157.8583), (43.6187, -116.2146),
			(39.7817, -89.6501), (39.7684, -86.1581), (41.6005, -93.6091), (39.0558, -95.689),
			(38.2009, -84.8733), (30.4583, -91.1403), (44.3106, -69.7795), (38.9784, -76.4922),
			(42.3601, -71.0589), (42.7325, -84.5555), (44.9537, -93.09), (32.2988, -90.1848),
			(38.5767, -92.1735), (46.5884, -112.0245), (40.8258, -96.6852), (39.1638, -119.7674),
			(43.2081, -71.5376), (40.2171, -74.7429), (35.6870, -105.9378), (42.6526, -73.7562),
			(35.7796, -78.6382), (46.8083, -100.7837), (39.9612, -82.9988), (35.4676, -97.5164),
			(44.9429, -123.0351), (40.2732, -76.8867), (41.824, -71.4128), (34.0007, -81.0348),
			(44.3683, -100.351), (36.1627, -86.7816), (30.2672, -97.7431), (40.7608, -111.891),
			(44.2601, -72.5754), (37.5407, -77.436), (47.0379, -122.9007), (38.3498, -81.6326),
			(43.0731, -89.4012), (41.14, -104.8202), (0, 0)]

def init():
    point.set_data([], [])
    return point,

# animation function.  This is called sequentially
def animate(i):
	global lons
	global lats
	global iterr

	lats.append(states[iterr][0])
	lons.append(states[iterr][1])
	iterr += 1

	if iterr == 51:
		plt.savefig('out.png')
		exit()

	x, y = my_map(lons, lats)
	point.set_data(x, y)
	return point,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=20, interval=500, blit=True)

plt.show()