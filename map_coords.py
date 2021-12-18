import gmplot
import json



def map_intersections(fname):
    """
    Extract and plot GPS coordinates for intersections
    """
    ## Scatter plot GPS data
    with open(fname) as f:
        store = json.load(f)

    ## Extract GPS coordinates from files
    gps_store = []
    for key in store:
        gps_store.append(store[key])

    ## Generate google map
    lat, lon = gps_store[0]
    gmap = gmplot.GoogleMapPlotter(lat, lon, 15)
    gmap.scatter(*zip(*gps_store), color='red')
    gmap.draw('scatter.html')






if __name__ == '__main__':

    fname = 'store.json'
    map_intersections(fname)
    print('\nIntersections plotted')


