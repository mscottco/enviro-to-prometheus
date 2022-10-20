# enviro-to-prometheus

An attempt at a HTTP server that will receive post files from an Enviro board and cache them for reading by a Prometheus server.

## Environmental Variables

- ttl: The time the variables will be pushed to the Prometheus server. Defaults to 15 minutes

## Configuration

A docker image is provided at [mscottco/enviro-to-prometheus](https://hub.docker.com/mscottco/enviro-to-prometheus). You can use it by running something like:

```
docker run -p 8080:8080 -e ttl=15 -d mscottco/enviro-to-prometheus
```

Configure your enviro board to send metrics to:

```
http://[your ip address]:8080/endpoint
```

And configure your Prometheus server to scrape from:
```
http://[your ip address]:8080/metrics
```
