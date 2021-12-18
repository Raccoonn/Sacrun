import gmplot
import json



## Scatter plot GPS data
with open('store.json') as f:
    store = json.load(f)

gps_store = []
for key in store:
    gps_store.append(store[key])


lat, lon = gps_store[0]
gmap = gmplot.GoogleMapPlotter(lat, lon, 15)

gmap.scatter(*zip(*gps_store), color='red')

gmap.draw('scatter.html')






