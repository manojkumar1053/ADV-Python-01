"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    with open(neo_csv_path, "r") as file:
        reader = csv.DictReader(file)

        near_earth_objects = []
        for line in reader:
            # diameter not always available
            if not line["diameter"]:
                line["diameter"] = None
            else:
                line["diameter"] = float(line["diameter"])

            if not line["name"]:
                line["name"] = None

            line["pha"] = False if line["pha"] in ["N", ""] else True

            try:
                neo = NearEarthObject(
                    pdes=line["pdes"],
                    name=line["name"],
                    diameter=line["diameter"],
                    pha=line["pha"],
                )

            except Exception as e:
                print(e)
                continue

            near_earth_objects.append(neo)

    return near_earth_objects


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, "r") as file:
        reader = json.load(file)
        reader = [dict(zip(reader["fields"], data)) for data in reader["data"]]

        close_approaches = []
        for line in reader:
            try:
                ca = CloseApproach(
                    des=line["des"],
                    cd=line["cd"],
                    dist=float(line["dist"]),
                    v_rel=float(line["v_rel"]),
                )
            except Exception as e:
                print(e)
                continue
            close_approaches.append(ca)

    return close_approaches
