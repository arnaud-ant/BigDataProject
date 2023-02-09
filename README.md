# BigDataProject

## Docker

Build image:

`docker build -t package-machine-learning .`

Connect to AWS with credentials:

`aws ecr get-login-password | docker login --username AWS --password-stdin 104264238753.dkr.ecr.us-east-1.amazonaws.com`

Tag image:

`docker tag package-machine-learning:latest 104264238753.dkr.ecr.us-east-1.amazonaws.com/package-machine-learning:latest`

Push image to AWS:

`docker push 104264238753.dkr.ecr.us-east-1.amazonaws.com/package-machine-learning:latest`
