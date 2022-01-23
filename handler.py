import os
import pyhiveapi
import json
import logging

from pyhiveapi.helper.hive_exceptions import NoApiToken
from newrelic_telemetry_sdk import GaugeMetric, MetricClient
from os.path import exists

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

__tokens_file = "/tmp/tokens.json"


def lambda_handler(event, context):
    tokens = {
        "token": os.environ.get("ID_TOKEN", ""),
        "refreshToken": os.environ.get("REFRESH_TOKEN", ""),
        "accessToken": os.environ.get("ACCESS_TOKEN", "")
    }

    tokens.update(_read_tokens())

    if os.environ.get("NEWRELIC_REGION") == "EU":
        metric_client = MetricClient(insert_key=os.environ["NEWRELIC_INSERT_KEY"],
                                     host="insights-collector.eu01.nr-data.net")
    else:
        metric_client = MetricClient(insert_key=os.environ["NEWRELIC_INSERT_KEY"])

    logger.debug("Refreshing tokens")
    api = pyhiveapi.API()
    new_tokens = api.refreshTokens(tokens)
    if new_tokens["original"] == 200:
        api.token = new_tokens["parsed"]["token"]
        tokens.update({"token": new_tokens["parsed"]["token"]})
        tokens.update({"refreshToken": new_tokens["parsed"]["refreshToken"]})
        tokens.update({"accessToken": new_tokens["parsed"]["accessToken"]})
        _write_tokens(tokens)
    else:
        raise NoApiToken

    products = api.getProducts()
    logger.debug("Response received: %s", json.dumps(products, indent=2))

    for product in products["parsed"]:
        if product["type"] == "heating":
            tags = {
                "id": product["id"],
                "productName": product["state"]["name"],
                "model": product["props"]["model"],
                "modelVariant": product["props"]["modelVariant"],
                "version": product["props"]["version"],
                "pmz": product["props"]["pmz"]
            }
            temperature = GaugeMetric("hive.heating.temperature", product["props"]["temperature"], tags)
            target = GaugeMetric("hive.heating.target", product["state"]["target"], tags)
            online = GaugeMetric("hive.heating.online", 1 if product["props"]["online"] else 0, tags)
            working = GaugeMetric("hive.heating.working", 1 if product["props"]["working"] else 0, tags)

            response = metric_client.send_batch((temperature, target, online, working))
            response.raise_for_status()
    print("Sent metrics successfully!")


def _read_tokens():
    tokens = {}
    if exists(__tokens_file):
        with open(__tokens_file, encoding="utf-8") as tokens_file:
            tokens = json.loads(tokens_file.read())
    return tokens


def _write_tokens(tokens):
    with open(__tokens_file, "w") as tokens_file:
        tokens_file.write(json.dumps(tokens, indent = 4))
