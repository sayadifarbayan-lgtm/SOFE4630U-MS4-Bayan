import csv
import json
from google.cloud import pubsub_v1

PROJECT_ID = "sofe4630-ms2-bayan"
TOPIC_ID = "smart-meter"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def to_float_or_none(value):
    value = value.strip()
    if value == "":
        return None
    return float(value)


with open("Labels.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        for field in ["time", "temperature", "humidity", "pressure"]:
            row[field] = to_float_or_none(row[field])

        publisher.publish(
            topic_path,
            json.dumps(row).encode("utf-8"),
            stage="raw"
        ).result()

        print("Published:", row)

print("All records published successfully.")