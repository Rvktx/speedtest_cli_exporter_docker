# speedtest_cli_exporter_docker
 This is speedtest.net Prometheus exporter. It checks your network connection. Metrics are :

* Latency
* Download bandwidth
* Upload bandwidth

This is the first exporter using an official more precise and reliable speedtest CLI app (which uses pure sockets instead of HTTP for testing) that I know of.
The last speedtest exporter that I used was giving me inconsistent and inaccurate data.
I couldn't find anything better so I wrote this simple script to run a new official speedtest CLI app and scrapes it's output to Prometheus.

## Usage

### Python

    usage: speedtest_exporter.py [-h] [--port PORT] [--server SERVER]

    Speedtest exporter for prometheus.
    
    optional arguments:
      -h, --help        show this help message and exit
      --port PORT       Port to listen for requests.
      --server SERVER   Number of server to test.
      --license BOOL    You need to set this to True in order to accept Ookla's license and use this exporter.
      --gdpr BOOL       You need to set this to True in order to accept Ookla's GDPR and use this exporter.

### Docker

    docker run -d --name='speedtest_exporter' --net='host' -e TZ="Europe/Warsaw" -e 'TCP_PORT_8000'='8000' 'rvktx/speedtest_exporter:1.1'
    
Environmental variables:

* PORT - Port to listen on; Also change TCP_PORT to expose.
* SERVER - ID number of the server to run the test on.
* LICENSE - You need to set this to True in order to accept Ookla's license and use this exporter.
* GDPR - You need to set this to True in order to accept Ookla's GDPR and use this exporter.

### How to find server ID?

You can get a list of 100 best servers for your location [here](https://www.speedtest.net/speedtest-servers-static.php).

## Acknowledgments

* Ookla - [Speedtest CLI](https://www.speedtest.net/pl/apps/cli)