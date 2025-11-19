# Demo Run
## Setup

## Github secrets for quay should be in already.
https://github.com/arslankhanali/demo_multiarch/settings/secrets/actions/QUAY_PASSWORD
https://github.com/arslankhanali/demo_multiarch/settings/secrets/actions/QUAY_PASSWORD

### Setup Tabs  - '86' and 'arm'
```sh
# NOT ACTUAL TOKENS
oc login --token=sha256~yLWMeIq --server=https://api.cluster-2bkw8.2bkw8.sandbox1789.opentlc.com:6443

# NOT ACTUAL TOKENS
oc login --token=sha256~7ifCAhw --server=https://api.cluster-z94pq.z94pq.sandbox1166.opentlc.com:6443

# get contxt
oc config get-contexts

# Rename the long context string to "x86" and "arm"
oc config rename-context default/api-cluster-2bkw8-2bkw8-sandbox1789-opentlc-com:6443/admin x86
oc config rename-context default/api-cluster-z94pq-z94pq-sandbox1166-opentlc-com:6443/kube:admin arm

# Useful aliases
alias oc-which='oc config get-contexts'
alias oc-x86='oc config use-context x86'
alias oc-arm='oc config use-context arm'

# Show architecture under KERNEL-VERSION column
oc get nodes -o wide --context=x86
oc get nodes -o wide --context=arm
```
## Act 1 - Build
``` sh
cd ~/Codes/demo.redhat.com/demo_multiarch
ls # Show App Code

date >> date.txt       
git commit -am "Run demo arch-cop"
git push origin main 

# Show Pipeline
https://github.com/arslankhanali/demo_multiarch/blob/main/.github/workflows/docker-image.yml
# Show Git hub Actions
https://github.com/arslankhanali/demo_multiarch/actions/runs/
# Show Quay - image repository
https://quay.io/repository/arslankhanali/skupper-frontend?tab=tags
```


## Act 2 - Deploy on ARM
``` sh
# Deploy App
oc-arm
oc new-project demo
oc project demo
oc new-app --name=backend -l app=hello quay.io/arslankhanali/skupper-backend:gh
oc new-app --name=frontend -l app=hello quay.io/arslankhanali/skupper-frontend:gh
oc create route edge frontend --service=frontend --port=8080
echo "https://$(oc get route frontend -o jsonpath='{.spec.host}')" 

```

## Act 2 - Deploy on x86
``` sh
# Deploy App
oc-x86
oc new-project demo
oc project demo
oc new-app --name=backend -l app=hello quay.io/arslankhanali/skupper-backend:gh
oc new-app --name=frontend -l app=hello quay.io/arslankhanali/skupper-frontend:gh
oc create route edge frontend --service=frontend --port=8080
echo "https://$(oc get route frontend -o jsonpath='{.spec.host}')" 

```

## Act 3 - Connect
```sh
# Step 1: Initialize Skupper on x86 (where frontend is)
oc-x86
oc project demo
skupper init --enable-console --enable-flow-collector
skupper token create ~/east-west.token
skupper expose deployment/backend --port 8080
skupper status  # Verify it's initialized

# Step 2: Initialize Skupper on ARM and expose backend
oc-arm
oc project demo
oc get deployment backend  
skupper init --ingress none
skupper link create ~/east-west.token
skupper status  
skupper expose deployment/backend --port 8080
skupper service status 


# Verify both backends are available
skupper service status  # Still shows one service entry
oc describe service backend  # Check endpoints - should show pods from both x86 and ARM

```
## Act 4 : Tests - Show HA
```sh
# ----------------
# NAMESPACE x86
# ----------------
oc-x86
oc delete deployment backend -n demo
oc-x86
oc new-app --name=backend -l app=hello quay.io/arslankhanali/skupper-backend:gh -n demo

```

### 5. Clean Up
```sh
# skupper 
skupper delete

# x86
oc-x86
oc project demo
oc delete all --selector app=hello -n demo
skupper delete
oc delete project demo

# arm
oc-arm
oc project demo
oc delete all --selector app=hello -n demo
skupper delete
oc delete project demo
```