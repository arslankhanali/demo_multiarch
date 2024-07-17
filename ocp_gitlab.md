# https://developer.ibm.com/tutorials/build-multi-architecture-x86-and-power-container-images-using-gitlab/#step-7-a-peek-at-the-gitlab-ci-pipeline-yaml-file-10
### Install operator
```sh
cat << EOF | oc apply -f-
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  labels:
    operators.coreos.com/gitlab-runner-operator.openshift-operators: ""
  name: gitlab-runner-operator
  namespace: openshift-operators
spec:
  channel: stable
  installPlanApproval: Automatic
  name: gitlab-runner-operator
  source: certified-operators
  sourceNamespace: openshift-marketplace
EOF
```
# Create Project
```sh
# oc new-project demo  
cat << EOF | oc apply -f-
apiVersion: v1
kind: Namespace
metadata:
  name: demo
EOF
```
# Get Gitlab Token
GR1348941RRBTEzSyzXNnWufxrPxi
echo -n 'GR1348941RRBTEzSyzXNnWufxrPxi' | base64

# Create Secret
``` sh
cat << EOF | oc apply -f-
kind: Secret
apiVersion: v1
metadata:
  name: gitlab-runner-secret
  namespace: demo
data:
  runner-registration-token: R1IxMzQ4OTQxUlJCVEV6U3l6WE5uV3VmeHJQeGk=
type: Opaque
EOF
```

# Create ServiceAccount
``` sh
cat << EOF | oc apply -f-
apiVersion: v1
kind: ServiceAccount
metadata:
  name: gitlab-runner-sa
  namespace: demo
EOF
```

# Create Runner
``` sh
cat << EOF | oc apply -f-
apiVersion: apps.gitlab.com/v1beta2
kind: Runner
metadata:
  name: example-runner
  namespace: demo
spec:
  concurrent: 10
  gitlabUrl: https://gitlab.com
  serviceaccount: gitlab-runner-sa
  tags: openshift, x86
  token: gitlab-runner-secret
EOF
```

# Create Rolebinding
``` sh
cat << EOF | oc apply -f-
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: add-anyuid-to-my-gitlab-sa
  namespace: demo
subjects:
  - kind: ServiceAccount
    name: gitlab-runner-sa
    namespace: demo
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: 'system:openshift:scc:anyuid'
EOF

cat << EOF | oc apply -f-
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: add-my-gitlab-sa-to-runner-app-role
  namespace: demo
subjects:
  - kind: ServiceAccount
    name: gitlab-runner-sa
    namespace: demo
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: gitlab-runner-app-role
EOF
```