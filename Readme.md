# ML Training Job on Azure Machine Learning with custom Docker Container

## Setup Configuration using Azure CLI and Python SDK

Ref: https://docs.microsoft.com/en-us/azure/machine-learning/how-to-train-with-custom-image


[![image size](https://img.shields.io/docker/image-size/johntorrestensor/pyspark-ml/latest)](https://hub.docker.com/r/johntorrestensor/pyspark-ml/ "johntorrestensor/pyspark-ml image size")


Steps: 

- (1) Create a local conda environment with python 3.6 or later and install azure python SDK

```bash
conda create --name azure-env python=3.9
pip install azureml-core
```
- (2) Install Azure CLI and Login with Azure Account

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az login
```

- (3) Create Azure Container Registry Instance and push Docker Image (you must have the image already built locally)

    - Ref: https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli#create-a-container-registry 


```bash
az acr create --resource-group myResourceGroup --name azuremlforecastingcontainer01 --sku Basic

az acr login --name azuremlforecastingcontainer01

docker tag pysparkforecast azuremlforecastingcontainer01.azurecr.io/pypsparkforecast:latest

docker push azuremlforecastingcontainer01.azurecr.io/pypsparkforecast:latest

```