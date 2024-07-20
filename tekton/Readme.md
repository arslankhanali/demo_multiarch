# To Build on Tekton
### Tekton Operator
```sh
cat << EOF | oc apply -f-
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: openshift-pipelines-operator
  namespace: openshift-operators
spec:
  channel: latest
  installPlanApproval: Automatic
  name: openshift-pipelines-operator-rh
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF
```
### Create a demo Project 
```sh
# oc new-project demo  
cat << EOF | oc apply -f-
apiVersion: v1
kind: Namespace
metadata:
  name: demo
EOF
```
### Create a pvc
```sh
cat << EOF | oc apply -f-
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: demo-pvc
  namespace: demo
  labels:
    app: demo-multiarch
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 2Gi
EOF
```

### Create a quay password
```sh
cat << EOF | oc apply -f-
apiVersion: v1
kind: Secret
metadata:
  labels:
    app: hello
  name: quay-authentication
  annotations:
    tekton.dev/docker-0: https://quay.io
type: kubernetes.io/basic-auth
stringData:
  username: arslankhanali
  password: <pass>
EOF
```
### Give service account 'pipeline' access to the secret
- This service account is automatically created in every project.  
- You can provide it with a secret. This is project specific i.e. pipeline SA in other projects will not have access to it.
```sh
oc patch serviceaccount pipeline -p '{"secrets": [{"name": "quay-authentication"}]}'
```
### Create Tekton Pipeline
- Pipeline to build frontend and backend images
- Images will be pushed to https://quay.io/repository/arslankhanali/skupper-frontend:tekton and https://quay.io/repository/arslankhanali/skupper-backend:tekton
  
```sh
oc apply -f tekton/pipeline_build_images.yaml        
```
![alt text](../images/9-image-pipeline.png)

### Run Pipeline
```sh
oc apply -f tekton/pipelinerun_build_images.yaml   
```
![alt text](../images/10-image-run.png)

### Verify
![alt text](../images/11-image-quay.png)

# Thank You
The End