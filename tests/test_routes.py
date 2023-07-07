import json

import requests

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": "AIzaSyBpTac3buTxXFoCNT6gMVBwpMWxKiRLOXI",
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.travelAdvisory.tollInfo,routes.legs.travelAdvisory.tollInfo",
}

json_data = {
    "origin": {
        "address": "2da B Juárez 102, Los Jales, Ex Hacienda de Coscotitlán, 42064 Pachuca de Soto, Hgo., Mexico"
    },
    "destination": {
        "address": "Calz. de Tlalpan 3465, Sta. Úrsula Coapa, Coyoacán, 04650 Ciudad de México, CDMX, Mexico"
    },
    "travelMode": "DRIVE",
    "routingPreference": "TRAFFIC_AWARE",
    "extraComputations": [
        "TOLLS",
    ],
    "routeModifiers": {
        "avoidTolls": False,
        "vehicleInfo": {
            "emissionType": "GASOLINE",
        },
        "tollPasses": [
            "MX_IAVE",
            "MX_PASE",
            "MX_QUICKPASS",
            "MX_SISTEMA_TELEPEAJE_CHIHUAHUA",
            "MX_TAG_IAVE",
            "MX_TAG_TELEVIA",
            "MX_TELEVIA",
            "MX_VIAPASS",
        ],
    },
}
response = requests.post(
    "https://routes.googleapis.com/directions/v2:computeRoutes",
    headers=headers,
    json=json_data,
)
print(response.json())
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
# data = '{\n"origins": [\n  {\n    "waypoint": {\n      "location": {\n        "latLng": {\n          "latitude":42.340173523716736,\n          "longitude":-71.05997968330408\n        }\n      }\n    },\n    "routeModifiers": {\n      "vehicleInfo":{\n        "emissionType": "GASOLINE"\n      },\n      "tollPasses": [\n        "US_MA_EZPASSMA",\n        "US_WA_GOOD_TO_GO"\n      ]\n    }\n  }\n],\n"destinations": [\n  {\n    "waypoint": {\n      "location": {\n        "latLng": {\n          "latitude":42.075698891472804,\n          "longitude": -72.59806562080408\n        }\n      }\n    }\n  }\n],\n"travelMode": "DRIVE",\n"extraComputations": ["TOLLS"]\n}'
# response = requests.post('https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix', headers=headers, data=data)
with open("response_routes.json", "w") as f:
    json.dump(response.json(), f)
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
# data = '{\n  "origin":{\n    "location":{\n      "latLng":{\n        "latitude": 37.419734,\n        "longitude": -122.0827784\n      }\n    }\n  },\n  "destination":{\n    "location":{\n      "latLng":{\n        "latitude": 37.417670,\n        "longitude": -122.079595\n      }\n    }\n  },\n  "travelMode": "DRIVE",\n  "routingPreference": "TRAFFIC_AWARE",\n  "departureTime": "2023-10-15T15:01:23.045123456Z",\n  "computeAlternativeRoutes": false,\n  "routeModifiers": {\n    "avoidTolls": false,\n    "avoidHighways": false,\n    "avoidFerries": false\n  },\n  "languageCode": "en-US",\n  "units": "IMPERIAL"\n}'
# response = requests.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, data=data)
