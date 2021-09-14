from flask.wrappers import Response
from flask import Blueprint
from flask import request
from dotenv import load_dotenv
import logging
import os
import json

from geocoder.google import GoogleResult
from geopy import distance
import geocoder


bp = Blueprint("getdistance", __name__, url_prefix="/getdistance")


@bp.route('/getaddress', methods=("GET", "POST"))
def getaddress() -> str:

    logging.basicConfig(filename='result.log', level=logging.INFO)

    load_dotenv()
    address: str = request.args.get('address')

    # Uses google API into geocoder lib to get the latitude and longitude
    g: GoogleResult = geocoder.google(
                        location=address,
                        key=os.environ.get('API_KEY'),
                        )

    if g.latlng is None:
        logging.error("Invalid input, no results")
        return Response(
                "Invalid input, no results",
                status=400
            )

    latlng: dict = {
                    "lat": g.latlng[0],
                    "lng": g.latlng[1]
                    }

    distance: str = caldistance(latlng)

    return distance


# Calculate the distance between the address and MKAD
def caldistance(address: dict) -> str:

    # Open and read the file with the MKAD latitude and longitude
    filename = os.path.join('app', 'static', 'data', 'mkad.json')

    with open(filename) as data:
        mkad = json.load(data)

        shortestdist: float = float('inf')
        closerkm: str = ""

        for km in mkad:

            if km['lat'] == address['lat'] and km['lng'] == address['lng']:
                logging.error("Address is inside MKAD")
                return Response(
                        "Address is inside MKAD",
                        status=400
                    )

            # Uses geopy.distance method to calculate the distance in km
            dist: float = distance.distance(
                                        (address['lat'], address['lng']),
                                        (km['lat'], km['lng'])
                                    ).km

            if dist < shortestdist:

                shortestdist = dist
                closerkm = km

    if shortestdist < 1:
        logging.error("Address is inside MKAD")
        return Response(
                    "Address is inside MKAD",
                    status=400
                )

    logging.info('The distance is {}km to the MKAD km {}'.format(
                    shortestdist,
                    closerkm['km']
                ))
    return str(shortestdist)
