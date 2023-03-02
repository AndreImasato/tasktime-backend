#!/bin/bash
echo "Importing env variables"
export $(cat envs/docker/.env | xargs)

echo "Shutting containers down"
docker-compose -f docker-compose.yaml --compatibility down