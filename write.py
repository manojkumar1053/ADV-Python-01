"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    # Done: Write the results to a CSV file, following the specification in the instructions.
    with open(filename, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            info = row.serialize() | row.neo.serialize()
            info["name"] = info["name"] if info["name"] is not None else ""
            info["potentially_hazardous"] = (
                "True" if info["potentially_hazardous"] else "False"
            )
            writer.writerow(info)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # done: Write the results to a JSON file, following the specification in the instructions.
    output_data = []
    for row in results:
        d1,d2 = row.serialize(),row.neo.serialize()
        #info = row.serialize() | row.neo.serialize()  # Use python 3.9 or higher
        info = {**d1,**d2}
        info["name"] = info["name"] if info["name"] is not None else ""
        info["potentially_hazardous"] = (
            bool(1) if info["potentially_hazardous"] else bool(0)
        )
        output_data.append(
            {
                "datetime_utc": info["datetime_utc"],
                "distance_au": info["distance_au"],
                "velocity_km_s": info["velocity_km_s"],
                "neo": {
                    "designation": info["designation"],
                    "name": info["name"],
                    "diameter_km": info["diameter_km"],
                    "potentially_hazardous": info["potentially_hazardous"],
                },
            }
        )

    with open(filename, "w") as file:
        json.dump(output_data, file, indent="\t")
