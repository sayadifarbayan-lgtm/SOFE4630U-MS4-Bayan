import os
import json
from google.cloud import pubsub_v1

PROJECT_ID = "sofe4630-ms2-bayan"
TOPIC_ID = "smart-meter"
SUBSCRIPTION_ID = "filter-reading-sub"

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

subscription_path = subscriber.subscription_path(
    PROJECT_ID, SUBSCRIPTION_ID
)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def filter_reading(record):
    return (
        record.get("temperature") is not None
        and record.get("humidity") is not None
        and record.get("pressure") is not None
    )


def callback(message):
    try:
        record = json.loads(message.data.decode("utf-8"))

        if filter_reading(record):
            publisher.publish(
                topic_path,
                json.dumps(record).encode("utf-8"),
                stage="filtered"
            ).result()
            print("Filtered record published:", record)
        else:
            print("Removed incomplete record:", record)

        message.ack()

    except Exception as e:
        print("Error:", e)
        message.nack()


if __name__ == "__main__":
    print("FilterReading service started...")
    subscriber.subscribe(subscription_path, callback=callback).result()