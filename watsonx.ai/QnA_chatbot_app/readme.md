# Sample Streamlit app for QnA with RAG

This is Sample Streamlit app provides a UI interface for the `Q&A with RAG accelerator`. It allows a user to ask questions about a given corpus of documents which are answered using a Retrieval Augmented Generation (RAG) approach. Along with the answer, the app references the source documents used to generate the answer. In addition, the user can provide feedback in a configurable range along with a free text comment. There is also an option to recommend a subject matter expert if the user is not satisfied with the answer.

This app requires an external API which is provided by the `Q&A with RAG accelerator` project template deployed on `Watsonx.ai` `SaaS` or `On Prem`.
For the IBM Cloud SaaS version, please refer to the [IBM Resource Hub](https://dataplatform.cloud.ibm.com/exchange/public/entry/view/75b22cbe-8a20-44a5-ac65-3a927e92cb0e?context=wx). For the CPD On Prem version, access to the `Q&A with RAG accelerator` can be requested through your IBM client team. The `Q&A with RAG accelerator` must be configured and deployed according to the needs of your use case.

## Features
- UI interface that sends user queries to the API and displays the response based on Q&A RAG deployment on watsonx.ai.
- Feedback rating options to select.
- Toggle button to display or hide the source documents.
- Feedback buttons (based on rating options selected) for each response. By default - we have added support from min 2 to 5 max feedback ratings in this app.
- Expert Recommendations are available for each user question based on user rating below 100%. (Optional)

## Requirements
- `Python3` for local setup 
- `Docker` or `Podman` container engine to build your local container image.[Optional]
- `Q&A RAG Accelerator` project setup on `Watsonx.ai` `aaS` or `On Prem` must be deployed.

## Pre - Reqs to run this app
- Please make sure to run Q&A RAG pipeline and copy deployment function url from the deployment space where it is deployed on Watsonx.ai aaS or On Prem environments. 
- Admin user should update the .env file in this folder. Must gather details of watsonx.ai endpoint configuration details before starting this.
- Clone or download this repository.
- Navigate to the project directory `QnA_chatbot_app`
- Please update the .env file according to your specific use case.

   - To configure the endpoint of the Q&A RAG Accelerator for connection with the Streamlit app: [Required]
   
     - `QNA_RAG_DEPLOYMENT_URL` should be set to the public endpoint URL of the QnA RAG function, either on watsonx.ai SaaS or on-prem.
     - To obtain this URL, navigate to the `Deployments` tab. Select the deployment space used in your watsonx.ai project, then click on the Deployments tab to view the online deployments. Look for one named `rag_scoring_function_with_elasticsearch` or `rag_scoring_function_with_milvus`. If these are not available, please run the Q&A RAG pipeline to deploy it quickly.
     - Once deployed, check the deployment details and choose the one with the matching `serving name` based on the `deployment serving name` parameter provided in your watsonx.ai **Q&A with RAG Accelerator** project. Then select the deployment under `API reference` & copy the `Public endpoint` url. For eg: 
       - For SaaS deployments see [link here](https://dataplatform.cloud.ibm.com/ml-runtime/deployments), and the endpoint URL will be in the following format:
       ```
       https://<cloud_region>.ml.cloud.ibm.com/ml/v4/deployments/<serving_name>/predictions?version=2021-05-01
       ```
       - For on-prem deployments, the endpoint URL will be:
       ```
       https://<cpd-watsonx-endpoint-url>/ml-runtime/deployments
       https://<cpd-watsonx-endpoint-url>/ml/v4/deployments/<serving_name>/predictions?version=2021-05-01
       ```
     - Please update your Watsonx-based endpoints accordingly.
   - Please Update `QNA_RAG_ENV_TYPE`, an environment type where your deployed Q&A with RAG Accelerator. Supported values `saas` likely on IBMCloud or `on-prem` based CPD SW clusters. [Required]
   - When `QNA_RAG_ENV_TYPE` to `saas`, please update below
      - `QNA_RAG_SAAS_IAM_APIKEY` is IAM key of watsonx.ai project which has access to the Q&A RAG Accelerator project and its deployment space which you already used in your wx.ai aaS project
   - When `QNA_RAG_ENV_TYPE` to `on-prem`, please update below
      - `QNA_RAG_ONPREM_CPD_USERNAME` is username of your cpd based on prem cluster
      - `QNA_RAG_ONPREM_CPD_APIKEY` is API key generated to access your on prem based cpd cluster. 
   - To initialize the streamlit app for QnA [Optional]. Default values are already set.
      - `FEEDBACK_RATING_OPTIONS` is set to `5` by default, admin user can configure this. app can support feedback rating options from 2 to 7. 
      - `ENABLE_EXPERT_RECOMMENDATION` is set to `True` , disable if you don't need it by default
      - `SAMPLE_EXPERT_RECOMMENDATION` is set to `True`, disable if you have ingested your own expert profiles instead of sample

## How to Run locally

### Pre Reqs 
- To run locally make sure you already installed python3 based environment.

### Steps 
1. Create a virtual environment and activate it (optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run qna_streamlit_chat_app.py --server.port 8080 --client.toolbarMode minimal --theme.base light
   ```
   Note: update port number which is not in use already.
4. Open the app in your browser using the provided URL from above output in your terminal


## How To Run and deploy on IBM Cloud code Engine 

- This procedure uses IBM Code Engine CLI to deploy the application. 
  **NOTE** Please check IBM Code Engine official documentation if you plan to deploy via UI or looking for other deployment options https://cloud.ibm.com/docs/codeengine?topic=codeengine-application-workloads
- please make sure to install `ibmcloud`.Official doc link is https://cloud.ibm.com/docs/cli/reference/ibmcloud?topic=cloud-cli-getting-started
- Make sure you have access to IBM Code engine as well if you are planning to deploy this app there.
- Setup IBM Code engine CLI - https://cloud.ibm.com/docs/codeengine?topic=codeengine-install-cli

### Deploy on IBM Cloud CE from your local source code.

- Admin user can use IBM Cloud Repository and IBM Cloud code engine to deploy their app which is by following below steps from their local source code.
- In this procedure, private IBM cloud repository will be used by Code Engine to build your image and use for deployment automatically via background process in a secure way & this has less pre-reqs to deploy your app.

#### Steps to deploy
- Make sure you have required details below to deploy

1. Logon to IBM Cloud via apikey:
   ```
   ibmcloud login --apikey <your_iam_apikey_based_your_ibmcloudaccount> -r <your region, e.g. eu-de>
   ```
   **Note** for each IBMaccount you have different api key. please make sure to use right account and its apikey which has enough permissions to access IBM Code Engine and IBM Container Repository to deploy this app.
2. Install IBM code engine plugin if not done already
   `ibmcloud plugin install code-engine`
3. Make sure to setup target region, account, resourcegroup on your ibmcloud client.
   `ibmcloud target -g <resourcegroup>`
4. Create project on your code engine account if you don't have existing one -  https://cloud.ibm.com/docs/codeengine?topic=codeengine-manage-project
   `ibmcloud ce project create -n <name_your_project_on_ce>`
    **Note** Make sure you have enough quota to create a project with your IBM cloud account. 
6. Select the project where you want to deploy
   `ibmcloud ce project select -n <name_your_project_on_ce>`
7. Make sure you are in `QnA_chatbot_app` folder location. 
8. Then Create and Deploy your streamlit application on Code Engine & wait for it to complete
   `ibmcloud ce app create --name <name_your_streamlitapp> --build-source .`
   **Note** You might face issues with quota limits with your IBM cloud account. Please run below steps in this scenario.
   - Please make sure that you have enough resource/quota limits on container registry or code engine application to run. If not please increase your quota limits or delete unused older applications/images on ibmcloud.
   - check existing applications with `ibmcloud ce app list` identify any unused apps. if have limited quota limit, either delete by running below cmd or increase your quota limits for application
     `ibmcloud ce app delete --name <name_any_outdated_unused_app_to_delete>`
   - check IBM Container Repository images which were previously created. if have limited quota limit, either delete unused images or increase your quota limits for images storage.
      - [Optional] if you havn't installed plugin for IBM Continer Registry. Please run below
        `ibmcloud plugin install container-registry`
      - To delete any outdated previous images. fetch image details using `ibmcloud cr images` and then retrieve corresponding Repository and tag name of the image created for your app.
        `ibmcloud cr image-rm <repository-image-name>:<tag-name>`
9. Get your public deployment on Code Engine by listing your app name when it is Ready.
   `ibmcloud ce app list | grep <name_of_your_streamlitapp>`
10. Copy the URL and paste on your browser to connect your streamlit app. it may take few secs to bring the app up.
11. To check logs of the application, please run below.
   `ibmcloud ce app logs --name <name_of_your_streamlitapp>`

## Terms of use
**Sample Materials, provided under license.</a> <br>**
Licensed Materials - Property of IBM. <br>
© Copyright IBM Corp. 2024,2025. All Rights Reserved. <br>
US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp. <br>

**The pillow library is used in this application. Pillow is licensed under the open source MIT-CMU License:</a><br>
The Python Imaging Library (PIL) is<br>**
    Copyright © 1997-2011 by Secret Labs AB<br>
    Copyright © 1995-2011 by Fredrik Lundh and contributors<br>
Pillow is the friendly PIL fork. It is<br>
    Copyright © 2010-2024 by Jeffrey A. Clark and contributors<br>
Like PIL, Pillow is licensed under the open source MIT-CMU License:<br>
By obtaining, using, and/or copying this software and/or its associated<br>
documentation, you agree that you have read, understood, and will comply<br>
with the following terms and conditions:<br>
<br>
Permission to use, copy, modify and distribute this software and its<br>
documentation for any purpose and without fee is hereby granted,<br>
provided that the above copyright notice appears in all copies, and that<br>
both that copyright notice and this permission notice appear in supporting<br>
documentation, and that the name of Secret Labs AB or the author not be<br>
used in advertising or publicity pertaining to distribution of the software<br>
without specific, written prior permission.<br>
<br>
SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS<br>
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.<br>
IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL,<br>
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM<br>
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE<br>
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR<br>
PERFORMANCE OF THIS SOFTWARE.<br>
