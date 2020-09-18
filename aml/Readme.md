# Working with Azure ML

The file in this folder allow you to interact with the AzureML service.  The main reason for these files to be hear is so that you can set up a Azure DevOps Release Pipeline for Continuous Deployment.  This is demonstrated here: [https://github.com/manashgoswami/AzureDevOps-onnxruntime-jetson/blob/main/README.md](https://github.com/manashgoswami/AzureDevOps-onnxruntime-jetson/blob/main/README.md).

## Create a workspace

Create a json file ``config.json`` with the configuration for your Azure ML workspace.

```
    {
        "subscription_id": "subscription_id",
        "resource_group": "resource_group",
        "workspace_name": "workspace_name",
        "workspace_region": "workspace_region",
        "service_principal_id": "service_principal_id",
        "service_principal_password": "service_principal_password",
        "tenant_id": "tenant_id"
    }
```

Use the file ``create_workspace.py`` to create an AzureML workspace.

## Register model

Register a model in the AzureML workspace with ``model_registration.py``.

## Download a trained model

Use file ``download_model.py``, to download a model that you have registered in the AzureML workspace.

