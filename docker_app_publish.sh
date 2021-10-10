#!/bin/bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 473200936731.dkr.ecr.us-east-2.amazonaws.com
docker tag mutant_finder:latest 473200936731.dkr.ecr.us-east-2.amazonaws.com/mutant_finder:v1.0.0
docker push 473200936731.dkr.ecr.us-east-2.amazonaws.com/mutant_finder:v1.0.0