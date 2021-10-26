CONDA_NAME := grpc-face-recognition
PYTHON_VERSION := 3.9

DOCKER_TAG := sushantjha/grpc-face-recognition

build-docker:
	docker build . -t $(DOCKER_TAG)

run-docker:
	docker run --gpus all -it --rm -d -p 50052:50052 --name grpc-face-recognition $(DOCKER_TAG)

# create-conda:
# 	conda env create -f environment.yml -n $(CONDA_NAME)

# delete-conda:
# 	conda env remove -y -n $(CONDA_NAME)