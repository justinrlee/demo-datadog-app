#!/usr/local/bin/python3

import os
import argparse
import json
import time
import random
import requests

#### Sample Rest API Call:
# curl -X POST \
#   -H 'Content-type: application/json' \
#   -d '{ "series" :
#          [{"metric":"justin.metric",
#           "points":[[1563429850,20], [1563429880,20], [1563429910,20]],
#           "type":"gauge",
#           "tags":["environment:test"]}
#         ]
#       }' \
#   https://api.datadoghq.com/api/v1/series?api_key=XYZ'

if __name__ == '__main__':
    print("Starting demo datadog app.")
    parser = argparse.ArgumentParser(description='Python script that generates dummy metrics and sends them to Datadog')

    parser.add_argument("-i", "--interval",
                        help="Metric reporting interval (in seconds)",
                        type=int,
                        default=os.environ.get('DD_INTERVAL', 5))

    parser.add_argument("-b", "--batch-size",
                        help="Number of metrics to send at a time",
                        type=int,
                        default=os.environ.get('DD_BATCH_SIZE', 24))

    parser.add_argument("-m", "--mean",
                        help="Metric average value",
                        type=int,
                        default=os.environ.get('DD_MEAN', 100))

    parser.add_argument("-s", "--standard-dev",
                        help="Metric standard deviation",
                        type=int,
                        default=os.environ.get('DD_STANDARD_DEV', 20))

    parser.add_argument("-n", "--metric-name",
                        help="Metric name",
                        default=os.environ.get('DD_METRIC_NAME', 'custom.metric'))

    parser.add_argument("-a", "--app-name",
                        help="App name",
                        default=os.environ.get('DD_APP_NAME', 'default'))

    parser.add_argument("-e", "--env-name",
                        help="Environment name",
                        default=os.environ.get('DD_ENV_NAME', 'default'))

    parser.add_argument("-v", "--version",
                        default=os.environ.get('DD_VERSION', '1.0'))

    parser.add_argument("-k", "--api-key",
                        default=os.environ.get('DD_API_KEY', None))

    args = parser.parse_args()

    # print(args)

    interval     = args.interval
    batch_size   = args.batch_size
    mean         = args.mean
    standard_dev = args.standard_dev
    metric_name  = args.metric_name
    app_name     = args.app_name
    env_name     = args.env_name
    version      = args.version

    print("Generating metrics every " + str(interval) + " second(s), batching metrics in groups of " + str(batch_size))

    tags = []
    
    if app_name is not None:
        tags.append("application:" + app_name)
    if env_name is not None:
        tags.append("environment:" + env_name)
    if version is not None:
        tags.append("version:" + version)

    key      = args.api_key
    url      = "https://api.datadoghq.com/api/v1/series?api_key=" + key

    # print(url)
    print(tags)
    
    metrics = []
    while True:
        metric = [time.time(), random.gauss(mean, standard_dev)]
        print(metric)
        metrics.append(metric)
        time.sleep(interval)

        if (len(metrics) >= batch_size):
            print(metrics)
            payload = {
                "series": [{
                    "metric": metric_name,
                    "points": metrics,
                    "type": "gauge",
                    "tags": tags
                }]
            }
            print(json.dumps(payload))
            r = requests.post(url, data=json.dumps(payload))
            print(r)

            metrics = []