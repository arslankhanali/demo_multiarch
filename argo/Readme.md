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
Wait couple minutes so that CRDs are installed in previous step.
```sh
# Access Givem: Openshift login user as admin
# rbac:
#   - defaultPolicy: 'role:admin'
oc apply -f argo/argo_instance.yaml
#or
oc apply -f https://raw.githubusercontent.com/arslankhanali/demo_multiarch/main/argo/argo_instance.yaml
```

### Create `demo` namespace
```sh
oc new-project demo
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
oc apply -f argo/application_frontend.yaml
oc apply -f argo/application_backend.yaml
# oc apply -f https://raw.githubusercontent.com/arslankhanali/demo_multiarch/main/argo/application_frontend.yaml
# oc apply -f https://raw.githubusercontent.com/arslankhanali/demo_multiarch/main/argo/application_backend.yaml

# Get App URL
echo "https://$(oc get route frontend -o jsonpath='{.spec.host}')" 

# Stress test. https://<url-from-above>/api/hello
ab -n 100 -c 10 -p skupper-app/payload.json -T application/json https://frontend-demo.apps.cluster-s5cqt.dynamic.redhatworkshops.io/api/hello
```

### Application update
Argo will only update to a new container image if it detects a change in any manifests.
Solution:
1. Automate Tag Update: Use unique tags for each build to ensure Argo CD detects changes.
2. or Manual Update: Add or update an annotation in your deployment manifest to force a redeploy.

### Get password for Argo UI
``` sh
# Argo url
echo "https://$(oc get route openshift-gitops-server -n openshift-gitops -o jsonpath='{.spec.host}')" 
# username in admin
oc get secret openshift-gitops-cluster -n openshift-gitops -o jsonpath='{.data.admin\.password}' | base64 --decode  
```

### Delete Application
```sh
oc delete -f argo/application_frontend.yaml
oc delete -f argo/application_backend.yaml

# oc delete -f https://raw.githubusercontent.com/arslankhanali/demo_multiarch/main/argo/application_frontend.yaml
# oc delete -f https://raw.githubusercontent.com/arslankhanali/demo_multiarch/main/argo/application_backend.yaml

oc delete all -l app=hello
```