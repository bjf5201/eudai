#!/usr/bin/env bash
#
# Build and run Docker image
#
# Mounts the local project directory to reflect dev workflow
#
# The `docker run` command uses the following options:
#
# --rm                      Remove the container after exiting
# --volume .:/app           Mount the current directory to /app in the container so code changes don't require an image rebuild
# --volume /app/.venv       Mount the virtual environment separately, so the developer's environment doesn't end up in the container
# --publish 8000:8000       Expose port 8000 on the host and map it to port 8000 in the container
# -it $(docker build -q .)  Build the image, then use it as a run target
# $@                        Pass any arguments to the container

if [ -t 1 ]; then
  INTERACTIVE="-it"
else
  INTERACTIVE=""
fi

docker run \
    --rm \
    --volume .:/app \
    --volume /app/.venv \
    --publish 8000:8000 \
    $INTERACTIVE \
    $(docker build -q .) \
    $@