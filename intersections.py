
from networkx.algorithms.bipartite.projection import collaboration_weighted_projected_graph
import requests
import numpy as np
import json
from datetime import datetime
import time
import logging
from requests.sessions import should_bypass_proxies
from shapely.geometry import Polygon, Point




def get_coords(bounds, sleeps=0, dx=50, dy=50, username='raccoonn'):
    """
    Given boundary coordinates discretize and walk through grid
    Store all located intersections, sleep at API call limit

        - Set maximum number of sleeps before exiting
        - Set step size for discretization


    Exit Codes:
        0 :  Entire discretized boundary has been traversed
        1 :  Maximum sleeps reached, discretized boundary incomplete
    """
    ## Setup logging
    logging.basicConfig(filename='gps_intersection.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


    ## Determine min and max boundaries for discretization
    lats, lons = zip(*bounds)
    lat_min, lat_max = min(lats), max(lats)
    lon_min, lon_max = min(lons), max(lons)

    ## Define polygon with given bounds
    B = Polygon(bounds)

    ## Create storage dictionary, initialize sleep iterator
    store = {}
    s_it = 0

    prog = ['|', '/', '-', '\\']
    p_it = 0
    ## Loop through discretized grid
    for lat in np.linspace(lat_min, lat_max, dy):
        for lon in np.linspace(lon_min, lon_max, dx):
            print('Searching for intersections... ' + prog[p_it%4], end='\r')
            p_it += 1
            ## Only call for values within the designated polygon
            if B.contains(Point((lat, lon))):

                try:
                    ## Make an API call
                    search = 'lat='+str(lat)+'&lng='+str(lon)+'&username=' + username
                    url = 'http://api.geonames.org/findNearestIntersectionJSON?' + search
                    response = requests.get(url, timeout=5)
                    response.raise_for_status()
                    data = response.json()
                    logging.info('API call made to: ' + url)
                    logging.info('Response: ' + str(data))
                except:
                    logging.warning('Response failed')
                    time.sleep(1)

                ## Try value extraction
                ## NOTE:  API call always returns, but response is different for limit
                ##        - Just try for value extraction and exception at fail
                try:
                    ix = sorted((data['intersection']['street1'], data['intersection']['street2']))
                    gps = (float(data['intersection']['lat']), float(data['intersection']['lng']))
                    intersection = ix[0] + ' & ' + ix[1]
                    if intersection not in store and B.contains(Point(gps)):
                        logging.info('New intersection: ' + str(intersection) + ' - ' + str(gps))
                        store[intersection] = gps

                ## If failed write current dictionary then quit/sleep accordingly
                except:
                    logging.warning('API Call limit reached, writing current dictionary')
                    fname = datetime.now().strftime('%m%d_%H%M%S') + '_xs_gps_store_xmas.json'
                    with open('xs_gps/' + fname, 'w') as f:
                        json.dump(store, f, indent=4, sort_keys=True)

                    ## If sleep limit reached return Exit Code 1
                    ## Else, sleep and continue loop after API calls reset
                    if s_it == sleeps:
                        logging.info('Maximum sleeps reached')
                        return store, 1

                    else:
                        s_it += 1
                        logging.warning('API call limit reached, sleeping for one hour...')
                        logging.warning('%d sleeps remaining' % (sleeps-s_it))
                        time.sleep(3600)
                        print('API call limit reached.  Sleeping...')


    ## If both loops complete, then entire discretized boundary has been traversed
    ## Return Exit Code 0
    logging.info('Entire discretized boundary has been traversed')
    return store, 0







if __name__ == '__main__':

    ## Load GPS boundaries
    f_bounds = 'bounds_full_grid.txt'
    with open(f_bounds) as f:
        bounds = [[float(n) for n in line.split(', ')] for line in f.read().splitlines()]


    ## Get intersections within boundaries
    sleeps, dx, dy = 500, 200, 200
    store, e_code = get_coords(bounds, sleeps, dx, dy)

    logging.info('Function completed, exit code: %d' % e_code)
 

    ## Write final dictionary
    ## Note:  Check log for boudnary completeness
    fname = datetime.now().strftime('%M%D_%H%M%S') + '_final_xs_gps_store_xmas.json'
    with open('xs_gps/' + fname, 'w') as f:
        json.dump(store, f, indent=4, sort_keys=True)





