import json
from google.cloud import pubsub_v1

PROJECT_ID = "sofe4630-ms2-bayan"
TOPIC_ID = "smart-meter"
SUBSCRIPTION_ID = "convert-reading-sub"

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

subscription_path = subscriber.subscription_path(
    PROJECT_ID, SUBSCRIPTION_ID
)
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)


def convert_reading(record):
    record["temperature"] = float(record["temperature"]) * 1.8 + 32
    record["pressure"] = float(record["pressure"]) / 6.895
    return record


def callback(message):
    try:
        record = json.loads(message.data.decode("utf-8"))

        converted = convert_reading(record)

        publisher.publish(
            topic_path,
            json.dumps(converted).encode("utf-8"),
            stage="converted"
        ).result()

        print("Converted record published:", converted)
        message.ack()

    except Exception as e:
        print("Error:", e)
        message.nack()


if __name__ == "__main__":
    print("ConvertReading service started...")
    subscriber.subscribe(subscription_path, callback=callback).result()