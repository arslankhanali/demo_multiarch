# To Deploy on Argo
### Argo Operator
```sh
cat << EOF | oc apply -f-
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: openshift-gitops-operator
  namespace: openshift-operators
spec:
  channel: latest
  installPlanApproval: Automatic
  name: openshift-gitops-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF
```
### Argo Instance
```sh
# Access Givem: Openshift login user as admin
# rbac:
#   - defaultPolicy: 'role:admin'
oc apply -f argo/argo_instance.yaml
```

### Give Argo Service Account Access to `demo` namespace
```sh
# via CLI
oc create rolebinding argocd-admin-binding \
  --clusterrole=admin \
  --serviceaccount=openshift-gitops:openshift-gitops-argocd-application-controller \
  --namespace=demo

# via Yaml
cat << EOF | oc apply -f-
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: argocd-admin-binding
  namespace: demo
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
subjects:
- kind: ServiceAccount
  name: openshift-gitops-argocd-application-controller
  namespace: openshift-gitops
EOF

# Verify
oc get rolebinding argocd-admin-binding -n demo
```

### Create Application
```sh
oc apply -f argo/application.yaml
```

### Delete Application
```sh
oc delete -f argo/application.yaml
```