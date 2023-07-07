import json
from datetime import datetime

from googlemaps import Client

g = Client(key="AIzaSyBpTac3buTxXFoCNT6gMVBwpMWxKiRLOXI")

origin = "Pachuca, 43870 Hgo., México"
destination = "Polanco I Secc, 11510 Ciudad de México, CDMX, México"
mode = "driving"
departure_time = datetime.now()
avoid = ""
response = g.directions(
    origin, destination, mode=mode, departure_time=departure_time, avoid=avoid
)


with open("response.json", "w") as f:
    json.dump(response, f)
