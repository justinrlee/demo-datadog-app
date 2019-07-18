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
    parser = argparse.ArgumentParser(description='Python script that generates dummy metrics and sends them to Datadog')

    parser.add_argument("-i", "--interval",
                        help="Metric reporting interval (in seconds)",
                        type=int,
                        default=5)

    parser.add_argument("-b", "--batch",
                        help="Number of metrics to send at a time",
                        type=int,
                        default=12)

    parser.add_argument("-m", "--mean",
                        help="Metric average value",
                        type=int,
                        default=100)

    parser.add_argument("-s", "--standard-dev",
                        help="Metric standard deviation",
                        type=int,
                        default=20)

    parser.add_argument("-n", "--metric-name",
                        help="Metric name")

    parser.add_argument("-a", "--app-name",
                        help="Metric name")

    parser.add_argument("-e", "--env-name",
                        help="Metric name")

    parser.add_argument("-k", "--api-key")

    args = parser.parse_args()

    print(args)

    interval = args.interval
    batch    = args.batch
    mean     = args.mean
    sd       = args.standard_dev
    name     = args.metric_name
    
    tags = []
    app_name = args.app_name
    env_name = args.env_name
    
    if app_name is not None:
        tags.append("application:" + app_name)
    if env_name is not None:
        tags.append("environment:" + env_name)

    key      = args.api_key
    if key == None:
        key = os.environ['DD_API_KEY']
    url      = "https://api.datadoghq.com/api/v1/series?api_key=" + key

    # print(url)
    print(tags)
    
    metrics = []
    while True:
        metrics.append([time.time(), random.gauss(mean, sd)])
        time.sleep(interval)

        if (len(metrics) >= batch):
            print(metrics)
            payload = {
                "series": [{
                    "metric": name,
                    "points": metrics,
                    "type": "gauge",
                    "tags": tags
                }]
            }
            print(json.dumps(payload))
            r = requests.post(url, data=json.dumps(payload))
            print(r)

            metrics = []