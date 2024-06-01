#!/bin/bash

# Set the desired context name
CONTEXT_NAME="kind-istio-mono"

# Get the current context
CURRENT_CONTEXT=$(kubectl config current-context)

# Get all contexts
ALL_CONTEXTS=$(kubectl config get-contexts -o name)

# Check if the desired context exists
if echo "$ALL_CONTEXTS" | grep -q "$CONTEXT_NAME"; then
  echo "Context '$CONTEXT_NAME' exists."

  # Check if the desired context is the current context
  if [ "$CURRENT_CONTEXT" == "$CONTEXT_NAME" ]; then
    echo "Current context is '$CONTEXT_NAME'."
  else
    echo "Context '$CONTEXT_NAME' exists but is not currently in use."
    echo "Switching to context '$CONTEXT_NAME'."
    kubectl config use-context "$CONTEXT_NAME"
    if [ $? -ne 0 ]; then
      echo "Failed to switch to context '$CONTEXT_NAME'. Exiting."
      exit 1
    fi
  fi
else
  echo "Context '$CONTEXT_NAME' does not exist. Exiting."
  exit 1
fi
