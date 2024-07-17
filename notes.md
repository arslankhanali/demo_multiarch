### To Test locally on laptop
```sh
python3 app.py   

uname -m

http://127.0.0.1:5000/architecture
```
#### Podman Build
```sh
# --arch=arch
# Set the architecture of the image to be built, and that of the base image to be pulled, if the build uses one, to the provided value instead of using the architecture of the build host. Unless overridden, subsequent lookups of the same image in the local storage matches this architecture, regardless of the host. (Examples: arm, arm64, 386, amd64, ppc64le, s390x)

# x86 (default)
podman build -t demo-multiarch-x86 -f Containerfile .
podman run -d -p 5000:5000 --name demo-multiarch-container-x86 demo-multiarch-x86

# arm64
podman build -t demo-multiarch-arm64 -f Containerfile . --arch=arm64  
podman run -d -p 5001:5000 --name demo-multiarch-container-arm64 demo-multiarch-arm64

# Z
podman build -t demo-multiarch-s390x -f Containerfile . --arch=s390x  
podman run -d -p 5002:5000 --name demo-multiarch-run-s390x demo-multiarch-s390x

# PPC
podman build -t demo-multiarch-ppc64le -f Containerfile . --arch=ppc64le  
podman run -d -p 5003:5000 --name demo-multiarch-run-ppc64le demo-multiarch-ppc64le

```

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