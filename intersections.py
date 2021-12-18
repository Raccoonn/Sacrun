import requests
import numpy as np
import json
from datetime import datetime
import time
import logging


"""
Progress --

    CURRENTLY:
        - DOES NOT properly discretize between 4 coordinate boundary

            - Need to add linear interpolation of boundaries
              Allow for an arbitraty 4 sided boundary

"""







def get_coords(nw, ne, sw, se, sleeps=0, dx=50, dy=50, username='raccoonn'):
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


    ## Create storage dictionary, initialize sleep iterator
    store = {}
    s_it = 0

    ## Loop through discretized grid
    for lat in np.linspace(nw[0], sw[0], dy):
        for lon in np.linspace(nw[1], ne[1], dx):

            ## Make an API call
            search = 'lat='+str(lat)+'&lng='+str(lon)+'&username=' + username
            url = 'http://api.geonames.org/findNearestIntersectionJSON?' + search
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            logging.info('API call made to: ' + url)
            logging.info('Response: ' + str(data))

            ## Try value extraction
            ## NOTE:  API call always returns, but response is different for limit
            ##        - Just try for value extraction and exception at fail
            try:
                ix = sorted((data['intersection']['street1'], data['intersection']['street2']))
                gps = (float(data['intersection']['lat']), float(data['intersection']['lng']))
                intersection = ix[0] + ' & ' + ix[1]
                if intersection not in store:
                    logging.info('New intersection: ' + str(intersection) + ' - ' + str(gps))
                    store[intersection] = gps

            ## If failed write current dictionary then quit/sleep accordingly
            except:
                logging.info('API Call limit reached, writing current dictionary')
                fname = datetime.now().strftime('%H%M%S') + '_xs_gps_store.json'
                with open(fname, 'w') as f:
                    json.dump(store, f, indent=4, sort_keys=True)

                ## If sleep limit reached return Exit Code 1
                ## Else, sleep and continue loop after API calls reset
                if s_it == sleeps:
                    logging.info('Maximum sleeps reached')
                    return store, 1

                else:
                    s_it += 1
                    logging.info('API call limit reached, sleeping for one hour...')
                    logging.info('%d sleeps remaining' % (sleeps-s_it))
                    time.sleep(3600)


    ## If both loops complete, then entire discretized boundary has been traversed
    ## Return Exit Code 0
    logging.info('Entire discretized boundary has been traversed')
    return store, 0







if __name__ == '__main__':

    ## GPS boundary coordinates
    nw = (38.583757964220176, -121.49945723851106)
    ne = (38.582065380843446, -121.47462913674272)
    sw = (38.56762038018241, -121.50183900408767)
    se = (38.5636700696355, -121.47607263103154)

    ## Get intersections within boundaries, maximum 5 sleeps
    sleeps, dx, dy = 5, 100, 100
    store, e_code = get_coords(nw, ne, sw, se, sleeps, dx, dy)

    logging.info('Function completed, exit code: %d' % e_code)


    ## Write final dictionary
    ## Note:  Check log for boudnary completeness
    fname = datetime.now().srtftime('%H%M%S') + '_final_xs_gps_store.json'
    with open(fname, 'w') as f:
        json.dump(store, f, indent=4, sort_keys=True)







