# ONNX Runtime with OpenVINO execution provider using Azure Machine Learning service

This tutorial uses a single container to deploy the TinyYolo model on the Intel UP<sup>2</sup> device.

<p align="center"><img width="100%" src="https://github.com/manashgoswami/byoc/raw/master/ONNXRuntime-AML.png" /></p>

In this example a sample container is built using the Azure Macnhine Learning Service.

## Setup Steps

### 1. An Azure Account Subscription (with pre-paid credits or billing through existing payment channels)

Set up the account in Azure portal using [this tutorial](https://azure.microsoft.com/en-us/free/). 
* Your subscription must have pre-paid credits or bill through existing payment channels. (If you make an account for the first time, you can get 12 months free and $200 in credits to start with.)

### 2. [Setup Jupyter Environment](https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-configure-environment#jupyter) to run this tutorial notebook.

### 2a. You can also use Jupyter Notebooks with NotebookVM in Azure Machine Learning Workspace.

    1. If you have an Azure Machine Learning service workspace, skip to step #2. Otherwise, create one now.
    - Sign in to the [Azure portal](https://portal.azure.com) by using the credentials for the Azure subscription you use.
    - In the upper-left corner of the portal, select __Create a resource__.
    - In the search bar, enter __Machine Learning__. Select the __Machine Learning service workspace__ search result.
    - In the __ML service workspace__ pane, scroll to the bottom and select Create to begin.
    - In the __ML service workspace__ pane, configure your workspace and select __Create__. It can take a few minutes to create the workspace. When the process is finished, a deployment success message appears. It's also present in the notifications section. To view the new workspace, select __Go to resource__.

    2. Create a cloud-based notebook server.
    - Open your Machine Learning workspace in the Azure portal.
    - On your workspace page in the Azure portal, select __Notebook VMs__ on the left.
    - Select __+New__ to create a notebook VM.
    - Provide a name for your VM and select __Create__.
    - Wait approximately 4-5 minutes until the status changes to __Running__
    3. Launch the Jupyter wed interface in your Notebook VM
    - Select __Jupyter__ in the __URI__ column for your VM.
    - On the Jupyter notebook webpage, the top foldername is your username.
    
    More details about quickstart setup instructions are located [here](https://docs.microsoft.com/en-us/azure/machine-learning/service/quickstart-run-cloud-notebook).

#### Clone this repo to your Notebook VM
From the Notebook VM launch the Jupyter web interface as descriped in step #3 above. Click New -> Terminal on the upper right corner of the web interface. You will get a new browser tab with the bash prompt. 
You can use regular `git clone --recursive https://github.com/Azure-Samples/onnxruntime-iot-edge` command line commands to clone this repository into a desired folder.

## Get Started
Open the notebook `AzureML-OpenVINO/AML-BYOC-ONNXRUNTIME-OpenVINO.ipynb` and start executing the cells. 
