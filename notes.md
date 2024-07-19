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