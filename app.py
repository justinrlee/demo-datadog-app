#!/usr/local/bin/python3

import os
import argparse
import json
import time
import random
import requests
import threading

import http.server

from urllib import parse


import socketserver

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

class MetricsSender(threading.Thread):
    def __init__(self, interval, batch_size, metric_name, tags, url, mean, standard_dev):
        threading.Thread.__init__(self)
        self.interval = interval
        self.batch_size = batch_size
        self.metric_name = metric_name
        self.tags = tags
        self.url = url
        self.mean = mean
        self.standard_dev = standard_dev
    def run(self):
        print ("Starting " + self.name)
        start_metrics(interval, batch_size, metric_name, tags, url, mean, standard_dev)
        print ("Exiting " + self.name)

class ThreadedHTTPServer(object):
    handler = http.server.SimpleHTTPRequestHandler
    def __init__(self, host, port):
        self.server = socketserver.TCPServer((host, port), self.handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

def start_metrics(interval, batch_size, metric_name, tags, url, mean, standard_dev):
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

if __name__ == '__main__':
    print("Starting demo datadog app.")
    parser = argparse.ArgumentParser(description='Python script that generates dummy metrics and sends them to Datadog')

    parser.add_argument("-i", "--interval",
                        help="Metric reporting interval (in seconds)",
                        type=int,
                        default=os.environ.get('DD_INTERVAL', 1))

    parser.add_argument("-b", "--batch-size",
                        help="Number of metrics to send at a time",
                        type=int,
                        default=os.environ.get('DD_BATCH_SIZE', 60))

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

    parser.add_argument("-p", "--port",
                        default=os.environ.get('DD_PORT', 8000))

    args = parser.parse_args()

    # print(args)

    interval        = args.interval
    batch_size      = args.batch_size
    mean            = args.mean
    standard_dev    = args.standard_dev
    metric_name     = args.metric_name
    app_name        = args.app_name
    env_name        = args.env_name
    version         = args.version
    port            = int(args.port)

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

    # Write file
    hostname = os.environ.get('HOSTNAME')
    text = f"<html>Inside container {hostname} (application:{app_name}, version:{version}, environment:{env_name}), producing metrics every {interval} seconds, with a mean of {mean} and a standard deviation of {standard_dev}</html>\n"
    with open('/var/www/index.html', 'w') as f:
        f.write(text)
    
    os.chdir('/var/www')

    m_thread = MetricsSender(interval, batch_size, metric_name, tags, url, mean, standard_dev)
    s_thread = ThreadedHTTPServer('', port)

    m_thread.start()
    s_thread.start()