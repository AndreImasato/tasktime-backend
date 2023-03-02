#!/bin/bash
echo "Importing env variables"
export $(cat envs/docker/.env | xargs)

echo "Bringing containers up"
docker-compose -f docker-compose.yaml --compatibility up -d