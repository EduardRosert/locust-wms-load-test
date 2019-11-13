# locust-wms-load-test
Load Tests for WMS servers using the [Locust load testing framework](https://locust.io) packaged in a docker container.
Requests GetCapabilities document and sends GetMap and GetLegendGraphic requests. Picks random layers, bounding boxes, time dimensions (if available) and styles in GetMap and GetLegendGraphic requests from the GetCapabilities document provided by the WMS service.

Supported WMS versions:
 - ``1.1.1``
 - ``1.3.0``

# Run pre-built images with Docker
The pre-built image ``eeduardrosert/locust-wms-load-test`` is available on [Dockerhub](https://hub.docker.com/r/eduardrosert/locust-wms-load-test). If you already have Docker running on your machine, just do the following to run the image.

```bash
docker run --rm -i -t -p 8089:8089 eduardrosert/locust-wms-load-test
```
Now you can access the Locust interface at http://localhost:8089 and start the tests.

## Run with WMS Service URL
To load test your WMS server, e.g. running at https://example.com/wms/ run:
```bash
docker run --rm -i -t -p 8089:8089 eduardrosert/locust-wms-load-test locust -f /app/wms-load-test/locustfile.py --host=https://example.com/wms
```

## Run with custom access token
If your WMS server requires a simple authentication using some access token in the request, e.g. ``myauthkey=mysecretaccesstoken``, you can provide that token using the environment variable ``WMS_ACCESS_KEY``as follows:
```bash
docker run --rm -i -t -p 8089:8089 --env WMS_ACCESS_KEY=myauthkey=mysecretaccesstoken eduardrosert/locust-wms-load-test locust -f /app/wms-load-test/locustfile.py --host=https://example.com/wms
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

## Run with WMS Service URL
Edit the file ``k8s-locust-wms-test.yaml`` to configure the container configuration. Edit the ``value`` for environment variable ``WMS_SERVICE_URL`` to match your wms service url:
```
env:
- name: WMS_SERVICE_URL
  value: "https://example.com/wms"
```
After editing, reapply the configuration using ``kubeclt apply -f k8s-locust-wms-test.yaml``

## Run with custom access token
If your WMS server requires a simple authentication using some access token in the request, e.g. ``myauthkey=mysecretaccesstoken``, you can provide that token using the environment variable ``WMS_ACCESS_KEY``in the deployment configuration. Edit file ``k8s-locust-wms-test.yaml`` and add the environment variable ``WMS_ACCESS_KEY`` with the key-value pair of your access token, e.g. ``myauthkey=mysecretaccesstoken``:
```
env:
- name: WMS_SERVICE_URL
  value: "https://example.com/wms"
- name: WMS_ACCESS_KEY
  value: "myauthkey=mysecretaccesstoken"
```
After editing, reapply the configuration using ``kubeclt apply -f k8s-locust-wms-test.yaml``