# DEMO - Skupper-example-hello-world
[Skupper-example-hello-world ](https://github.com/skupperproject/skupper-example-hello-world/tree/main)
# Setup tabs in terminal for 3 clusters
- canberra will have a frontend and Skupper console
- sydney and melbourne will have backends
  - You can just have 1 backend as well. We are using 2 to show how skupper automatically routes requests between them during stress testing
  - You will not see difference if you manually send sends usinh UI because 1 backend is wnough to serve you. 
```sh
# canberra: TERMINAL TAB
export KUBECONFIG=$HOME/.kube/config-canberra
oc login --token=sha256~KD3QpUkY-bcngS4yldRq31hsW9c6O-jw9ErhpfLlTJs --server=https://api.cluster-pmvqm.sandbox432.opentlc.com:6443
oc get -o jsonpath='{.status.infrastructureName}' infrastructure cluster

# sydney: TERMINAL TAB
export KUBECONFIG=$HOME/.kube/config-sydney
oc login --token=sha256~Pq8vP_lMbcDI7suI0IOLlb0a4rHug3L7LPQdDuj62pY --server=https://api.cluster-s5cqt.dynamic.redhatworkshops.io:6443
oc get -o jsonpath='{.status.infrastructureName}' infrastructure cluster

# melbourne: TERMINAL TAB
export KUBECONFIG=$HOME/.kube/config-melbourne
oc login --token=sha256~Pq8vP_lMbcDI7suI0IOLlb0a4rHug3L7LPQdDuj62pY --server=https://api.cluster-s5cqt.dynamic.redhatworkshops.io:6443
oc get -o jsonpath='{.status.infrastructureName}' infrastructure cluster
```

# Deploy on clusters
``` sh
# canberra: SETUP - Frontend
oc new-project canberra
oc config set-context --current --namespace canberra
skupper init --enable-console --enable-flow-collector
skupper token create ~/canberra-sydney.token
skupper token create ~/canberra-melbourne.token
oc create deployment frontend --image quay.io/skupper/hello-world-frontend
oc expose deployment/frontend --port 8080 --type LoadBalancer
oc create route edge frontend --service=frontend --port=8080 

# canberra: SETUP - To get Console
echo "https://$(oc get route frontend -o jsonpath='{.spec.host}')"
oc get secret skupper-console-users -n canberra -o jsonpath='{.data.admin}' | base64 --decode # user is admin

# sydney: SETUP - Backend
oc new-project sydney
oc config set-context --current --namespace sydney
skupper init --ingress none
skupper link create ~/canberra-sydney.token
oc create deployment backend --image quay.io/skupper/hello-world-backend --replicas 1
skupper expose deployment/backend --port 8080

# melbourne: SETUP - Backend
oc new-project melbourne
oc config set-context --current --namespace melbourne
skupper init --ingress none
skupper link create ~/canberra-melbourne.token
oc create deployment backend --image quay.io/skupper/hello-world-backend --replicas 1
skupper expose deployment/backend --port 8080

# canberra: TESTING
oc get service/frontend
#[Look up the external IP of the frontend service]
#[Navigate to http://<external-ip>:8080/ in your browser]
a1c0f488da7c24a439acc999ddb5f17d-1105989873.us-east-2.elb.amazonaws.com:8080
#or get the Route
echo "https://$(oc get route frontend -o jsonpath='{.spec.host}')"
# Health
curl -X GET https://frontend-canberra.apps.cluster-pmvqm.sandbox432.opentlc.com/api/health
# data
curl -X GET https://frontend-canberra.apps.cluster-pmvqm.sandbox432.opentlc.com/api/data
# Hello
curl -X POST https://frontend-canberra.apps.cluster-pmvqm.sandbox432.opentlc.com/api/hello \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello! I am Kind Hearted Chameleon.", "name": "Kind Hearted Chameleon"}'


# canberra: STRESS TESTING
# brew intall ab
ab -n 100 -c 10 -p payload.json -T application/json https://frontend-canberra.apps.cluster-pmvqm.sandbox432.opentlc.com/api/hello


# DELETE 
#canberra
skupper delete
oc delete service/frontend
oc delete deployment/frontend
#sydney/melbourne
oc delete
oc delete deployment/backend
```