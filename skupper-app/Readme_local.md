# Build containers
podman build -t frontend -f frontend/Containerfile
podman build -t backend -f backend/Containerfile

# Create a Network
podman network create mynetwork

# Run the Containers in the Pod: Run both the frontend and backend containers within the created Pod:
podman run -d --network mynetwork --name frontend -p 8080:8080 frontend
podman run -d --network mynetwork --name backend -p 8081:8080 backend

# Restart frontend
[frontend](http://localhost:8080/)
refresh tab for new name

# Restart backend
podman restart backend


# Push to quay 
# Make sure repositories are public before pushing
podman push backend quay.io/arslankhanali/skupper-backend:latest-x86
podman push frontend quay.io/arslankhanali/skupper-frontend:latest-x86