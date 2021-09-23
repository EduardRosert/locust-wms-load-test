# OGC Web Map Service (WMS) Load Test
## Git
[![Git Tag](https://img.shields.io/github/v/tag/eduardrosert/locust-wms-load-test)](https://github.com/eduardrosert/locust-wms-load-test/releases)
[![License](https://img.shields.io/github/license/eduardrosert/locust-wms-load-test)](https://github.com/eduardrosert/locust-wms-load-test)
## Docker
[![Docker Automated build](https://img.shields.io/docker/cloud/automated/eduardrosert/locust-wms-test.svg)](https://hub.docker.com/r/eduardrosert/locust-wms-test)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/eduardrosert/locust-wms-test.svg)](https://hub.docker.com/r/eduardrosert/locust-wms-test)
[![Docker Pulls](https://img.shields.io/docker/pulls/eduardrosert/locust-wms-test)](https://hub.docker.com/r/eduardrosert/locust-wms-test)
[![Docker Image Version](https://images.microbadger.com/badges/version/eduardrosert/locust-wms-test.svg)](https://microbadger.com/images/eduardrosert/locust-wms-test "Get your own version badge on microbadger.com")
[![Docker Commit Reference](https://images.microbadger.com/badges/commit/eduardrosert/locust-wms-test.svg)](https://microbadger.com/images/eduardrosert/locust-wms-test "Get your own commit badge on microbadger.com")


Load Tests for WMS servers using the [Locust load testing framework](https://locust.io) packaged in a docker container.
Requests GetCapabilities document and sends GetMap and GetLegendGraphic requests. Picks random layers, bounding boxes, time dimensions (if available) and styles in GetMap and GetLegendGraphic requests from the GetCapabilities document provided by the WMS service.

Supported WMS versions:
 - ``1.1.1``
 - ``1.3.0``

# Run pre-built images with Docker
The pre-built image ``eduardrosert/locust-wms-test`` is available on [Dockerhub](https://hub.docker.com/r/eduardrosert/locust-wms-test). If you already have Docker running on your machine, just do the following to run the image.

```bash
docker run --rm -i -t -p 8089:8089 eduardrosert/locust-wms-test
```
Now you can access the Locust interface at http://localhost:8089 and start the tests.

## Test OGC WMS Endpoint
To load test your WMS server run:
```bash
docker run --rm -i -t -p 8089:8089 \
       eduardrosert/locust-wms-test
```
Then visit the locust interface at http://localhost:8089 and enter you wms endpoint URL as ``host``. 

Examples for WMS endpoint URLs:
- If your WMS capabilities document located at https://example.com/wms?version=1.3.0&request=GetCapabilities then you should enter ``https://example.com/wms`` as host url.
- If your WMS capabilities document located at https://example.com/server/ows?service=wms&version=1.3.0&request=GetCapabilities then you should enter ``https://example.com/server/ows?service=wms`` as host url.


## Run with custom access token
If your WMS server requires a simple authentication using some access token in the request, e.g. ``myauthkey=mysecretaccesstoken``, you can provide that token using the environment variable ``WMS_ACCESS_KEY`` as follows:
```bash
docker run --rm -i -t -p 8089:8089 \
       --env WMS_ACCESS_KEY=myauthkey=mysecretaccesstoken \
       eduardrosert/locust-wms-test
```

## Adjust request weights
If you want to adjust the relative weights of the ``GetCapabilities``,``GetMap`` and ``GetLegendGraphic`` requests, you can do so by configuring the corresponding environment variables:
```bash
docker run --rm -i -t -p 8089:8089 \
       --env WEIGHT_GET_CAPABILITIES=1 \
       --env WEIGHT_GET_LEGEND_GRAPHIC=2 \
       --env WEIGHT_GET_MAP=10 \
       eduardrosert/locust-wms-test
```
The above setting means that for every ``GetCapabilities`` request there will be 2 ``GetLegendGraphic`` requests and 10 ``GetMap`` requests. You can disable a certain request by setting it's weight to ``0``. However you should not disable the ``GetCapabilities`` request, since without it the other requests cannot be generated.

## Enable verbose logging
To enable verbose logging, e.g. log the requested URLs, set the environment variable ``LOG_VERBOSE=1`` (disabled by default):
```bash
docker run --rm -i -t -p 8089:8089 \
       --env LOG_VERBOSE=1 \
       eduardrosert/locust-wms-test
```

# Run pre-build images with Kubernetes
Creates a deployment and a service named of type NodePort named ``locust-wms``:
```bash
kubectl apply -f k8s-locust-wms-test.yaml
```

Run
```bash
kubectl get service
```
to see how to access the service through the ip and port (usually 30000 - 32767) of the kubernetes worker node, e.g. ``http://10.105.111.227:32038``:
```
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
...
locust-wms        NodePort    10.105.111.227   <none>        8089:32038/TCP   2m26s
...
```

## Run with custom access token
If your WMS server requires a simple authentication using some access token in the request, e.g. ``myauthkey=mysecretaccesstoken``, you can provide that token using the environment variable ``WMS_ACCESS_KEY``in the deployment configuration. Edit file ``k8s-locust-wms-test.yaml`` and add the environment variable ``WMS_ACCESS_KEY`` with the key-value pair of your access token, e.g. ``myauthkey=mysecretaccesstoken``:
```
env:
- name: WMS_ACCESS_KEY
  value: "myauthkey=mysecretaccesstoken"
```
After editing, reapply the configuration using ``kubectl apply -f k8s-locust-wms-test.yaml``.
