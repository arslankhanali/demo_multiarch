#!/bin/bash
# Add a A10 Nvidia GPU worker node
# Define variables
################################
ARCH="aarch64" # Possible values: x86_64 or aarch64
AWS_REGION="us-east-2"
GPU="0"
MEMORY="16348"
VCPU="4"
REPLICAS="1"
INSTANCE="m6g.xlarge"

# Fetch AMI ID from the configmap
AMI_ID=$(oc get configmap/coreos-bootimages -n openshift-machine-config-operator -o jsonpath='{.data.stream}' | jq -r ".architectures.$ARCH.images.aws.regions.\"$AWS_REGION\".image")
echo "AMI ID: $AMI_ID"

# Fetch the infrastructure name
INFRASTRUCTURE_NAME=$(oc get -o jsonpath='{.status.infrastructureName}' infrastructure cluster)
echo "Infrastructure Name: $INFRASTRUCTURE_NAME"

# Define the name of the temporary YAML file
TMP_YAML_FILE="tmp_machineset.yaml"

################################

# Get the name of the machineset dynamically
machineset_name=$(oc get -n openshift-machine-api machinesets -o jsonpath='{.items[0].metadata.name}')

# Get YAML and redirect to the temporary file
oc get -n openshift-machine-api machinesets "$machineset_name" -o yaml | oc neat > "$TMP_YAML_FILE"

# Replace 'worker' with 'worker-$ARCH' in all occurrences in the file
sed -i '' "/$machineset_name/s/worker/worker-$ARCH/g" "$TMP_YAML_FILE"

# Update values in the YAML file using variables
sed -i '' "s/machine.openshift.io\/GPU.*/machine.openshift.io\/GPU: \"$GPU\"/" "$TMP_YAML_FILE" 

sed -i '' "s/machine.openshift.io\/memoryMb.*/machine.openshift.io\/memoryMb: \"$MEMORY\"/" "$TMP_YAML_FILE"

sed -i '' "s/machine.openshift.io\/vCPU.*/machine.openshift.io\/vCPU: \"$VCPU\"/" "$TMP_YAML_FILE"

sed -i '' "s/replicas.*/replicas: $REPLICAS/" "$TMP_YAML_FILE"

sed -i '' "s/instanceType.*/instanceType: $INSTANCE/" "$TMP_YAML_FILE"

sed -i '' "s/id: ami-.*/id: $AMI_ID/" "$TMP_YAML_FILE"

# Print the modified lines with updated values
echo "Modified lines with updated values:"
sed -n '/machine.openshift.io\/GPU/p; /machine.openshift.io\/memoryMb/p; /machine.openshift.io\/vCPU/p; /replicas/p; /instanceType/p' "$TMP_YAML_FILE"

# Apply changes
oc apply -f "$TMP_YAML_FILE"


# Clean up temporary file
# rm "$TMP_YAML_FILE"