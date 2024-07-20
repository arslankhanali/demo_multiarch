# Podman arch types
podman build -f Containerfile . --arch=amd64
Set the architecture of the image to be built, and that of the base image to be pulled, if the build uses one, to the provided value instead of using the architecture of the build host. Unless overridden, subsequent lookups of the same image in the local storage matches this architecture, regardless of the host. (Examples: arm, arm64, 386, amd64, ppc64le, s390x)

# Push to both Gitlab and Github
``` sh
git remote                                                                                                                          
> github # github
> origin # gitlab 

# Git LAB
git remote add origin https://gitlab.com/arslankhanali/demo_multiarch.git
git push -u origin main

# Git HUB
git remote add github https://github.com/arslankhanali/demo_multiarch.git
git push -u github main
```

# Dont write repository in quay url
WRONG: https://quay.io/repository/arslankhanali/skupper-backend
RIGHT: https://quay.io/arslankhanali/skupper-backend

# Same robot Account can be shared with multiple repositories in Quay

# Pushing to gitlab will trigger gitlab CI pipeline.


# Combine manifests
podman manifest create mylist-back
podman manifest add mylist-back quay.io/arslankhanali/skupper-backend:latest-ppc64le
podman manifest add mylist-back quay.io/arslankhanali/skupper-backend:latest-x86
podman manifest push mylist-back quay.io/arslankhanali/skupper-backend:latest

podman manifest create mylist-front
podman manifest add mylist-front quay.io/arslankhanali/skupper-frontend:latest-ppc64le
podman manifest add mylist-front quay.io/arslankhanali/skupper-frontend:latest-x86
podman manifest push mylist-front quay.io/arslankhanali/skupper-frontend:latest

# arch in Containerfile
#FROM --platform=linux/arm registry.access.redhat.com/ubi9/python-312
FROM registry.access.redhat.com/ubi9/python-312

# arch in podman build
podman build -t demo-multiarch-arm64 -f Containerfile . --arch=amd64  