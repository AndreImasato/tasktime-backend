#!/bin/bash
echo "Importing env variables"
export $(cat envs/docker/.env | xargs)

echo "Building images"
docker-compose -f docker-compose.yaml --compatibility build