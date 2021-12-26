import gmplot
import json



def map_intersections(f_bounds, f_coords):
    """
    Extract and plot GPS coordinates for intersections
    """
    ## Load GPS boundaries
    with open(f_bounds) as f:
        bounds = [[float(n) for n in line.split(', ')] for line in f.read().splitlines()]
        bounds.append(bounds[0])

    ## Load Intersection GPS data
    with open(f_coords) as f:
        store = json.load(f)

    ## Extract GPS coordinates from files
    gps_store = []
    for key in store:
        gps_store.append(store[key])


    ## Draw map of intersections and boundaries
    lat, lon = gps_store[0]
    gmap = gmplot.GoogleMapPlotter(lat, lon, 15)
    gmap.plot(*zip(*bounds), edge_width=6, color='blue')
    gmap.scatter(*zip(*gps_store), color='red')
    gmap.draw('maps/big_test.html')






if __name__ == '__main__':

    f_bounds = 'big_bounds.txt'
    f_coords = 'xs_gps/1226_032453_xs_gps_store_xmas.json'
    map_intersections(f_bounds, f_coords)
    print('\nIntersections plotted')

