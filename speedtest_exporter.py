from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily
import argparse
import subprocess
import time


def perform_test():
    print('Test starting...')
    dl_speed_value, up_speed_value, ping_value, jitter_value = (0, 0, 0, 0)

    if args.server == 0:
        result = subprocess.run(['speedtest', '-u', 'bps'], stdout=subprocess.PIPE).stdout.decode('UTF-8')
    else:
        result = subprocess.run(['speedtest', '-u', 'bps', '-s', str(args.server)], stdout=subprocess.PIPE).stdout.decode('UTF-8')
    print(result)

    if 'ISP' in result:
        lines = result.splitlines()
        for line in lines:
            elements = line.split()
            if 'Latency' in line:
                ping_value = float(elements[1])
                jitter_value = float(elements[3].replace('(', ''))
            elif 'Download' in line:
                dl_speed_value = float(elements[1])
            elif 'Upload' in line:
                up_speed_value = float(elements[1])
    return dl_speed_value, up_speed_value, ping_value, jitter_value


class SpeedtestCollector(object):
    DL_DESC = "How quickly you can pull data from a server on the internet to your device."
    UP_DESC = "How quickly you send data from your device to the internet."
    PING_DESC = "Also called latency, ping is the reaction time of your connection–how quickly your device gets a response after you’ve sent out a request."
    JITTER_DESC = "Also called Packet Delay Variation (PDV), jitter frequency is a measure of the variability in ping over time."

    def collect(self):
        download_bandwidth = GaugeMetricFamily('download_bandwidth', self.DL_DESC)
        upload_bandwidth = GaugeMetricFamily('upload_bandwidth', self.UP_DESC)
        ping = GaugeMetricFamily('ping', self.PING_DESC)
        jitter = GaugeMetricFamily('jitter', self.JITTER_DESC)

        dl_speed_value, up_speed_value, ping_value, jitter_value = perform_test()

        download_bandwidth.add_metric('download_bandwidth', dl_speed_value)
        upload_bandwidth.add_metric('upload_bandwidth', up_speed_value)
        ping.add_metric('ping', ping_value)
        jitter.add_metric('jitter', jitter_value)

        yield download_bandwidth
        yield upload_bandwidth
        yield ping
        yield jitter


def main():
    REGISTRY.register(SpeedtestCollector())
    start_http_server(args.port)
    print('listening on port {}.'.format(args.port))
    while True:
        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Speedtest exporter for prometheus.')
    parser.add_argument('--port', type=int, default=8000,required=False,
                        help='Port to listen for requests.')
    parser.add_argument('--server', type=int, default=0, required=False,
                        help='Number of server to test.')
    args = parser.parse_args()

    main()
    