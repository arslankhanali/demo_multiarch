< WIP >
# For multi arch OCP
Openshift cluster with worker nodes of different CPU architectures. 
```sh
oc -n openshift-config patch cm admin-acks --patch '{"data":{"ack-4.12-kube-1.26-api-removals-in-4.13":"true"}}' --type=merge


oc get clusterversion/version -o=jsonpath="{.status.conditions[?(.type=='RetrievedUpdates')].status}"
oc adm upgrade --to-multi-arch=true
oc adm upgrade

oc adm release info -o jsonpath="{ .metadata.metadata}"

oc adm upgrade channel stable-4.12

oc adm upgrade --to-multi-arch

oc adm upgrade --to-multi-arch=true --allow-upgrade-with-warnings=true
```