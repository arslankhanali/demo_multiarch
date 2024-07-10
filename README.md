## General Commands
```sh
python3 app1.py   

uname -m

http://127.0.0.1:5000/architecture
http://127.0.0.1:5002/architecture
http://mac-run-s390x:5002/architecture
```
## Podman Build
```sh
# --arch=arch
# Set the architecture of the image to be built, and that of the base image to be pulled, if the build uses one, to the provided value instead of using the architecture of the build host. Unless overridden, subsequent lookups of the same image in the local storage matches this architecture, regardless of the host. (Examples: arm, arm64, 386, amd64, ppc64le, s390x)

#Create Network
podman network create flask-net


# x86 (default)
podman build -t mac-x86 -f Containerfile .
podman run -d -p 5000:5000 --network flask-net --name mac-container-x86 mac-x86

# arm64
podman build -t mac-arm64 -f Containerfile . --arch=arm64  
podman run -d -p 5001:5000 --network flask-net --name mac-container-arm64 mac-arm64

# Z
podman build -t mac-s390x -f Containerfile . --arch=s390x  
podman run -d -p 5002:5000 --network flask-net --name mac-run-s390x mac-s390x

# PPC
podman build -t mac-ppc64le -f Containerfile . --arch=ppc64le  
podman run -d -p 5003:5000 --network flask-net --name mac-run-ppc64le mac-ppc64le

```
### Install Tekton Operator
``` sh
cat << EOF | oc apply -f-
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  labels:
    operators.coreos.com/openshift-pipelines-operator-rh.openshift-operators: ""
  name: openshift-pipelines-operator-rh
  namespace: openshift-operators
spec:
  channel: latest
  installPlanApproval: Automatic
  name: openshift-pipelines-operator-rh
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF
```
### Add arch64
```sh
# Release Notes
oc adm release info -o jsonpath="{ .metadata.metadata}" 
# Save yaml
oc get configmap/coreos-bootimages -n openshift-machine-config-operator -o yaml >> coreos-bootimages.yaml  
# Extract ami
oc get configmap/coreos-bootimages -n openshift-machine-config-operator -o jsonpath='{.data.stream}' | jq -r '.architectures.aarch64.images.aws.regions."eu-west-3".image'

```

``` sh
oc new-project build-multiarch  

oc create secret docker-registry quay-authentication --docker-email=arskhan@redhat.com --docker-username=arslankhanali --docker-password=jollyJ3lly74 --docker-server=quay.io

oc annotate secret/quay-authentication tekton.dev/docker-0=https://quay.io
```