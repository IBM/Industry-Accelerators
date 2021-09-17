# Industry Accelerators - Comments Organizer

### Introduction

The accelerator includes a structured glossary of business terms and a set of sample data science assets. Your data scientists can use the sample notebooks, predictive models, and dashboards to accelerate data preparation, machine learning modeling, and data reporting. The provided sample application will be able to automatically group comments/feedback from customers as well as highlight positive and negative sentiment of the comments. This application could be used in the Retail Industry and would allow a central place for retailers to easily review customer feedback in an organized manner. 

#### Usage

- Automatically and dynamically group comments by topics
    - Simultaneously view sentiment analysis of the groups
- View positive, negative, and neutral comments as well as the sentiment of comment's sentences

# Inventory of Artifacts provided

### Sample Datasets

The sample input dataset is obtained from [Data Asset eXchange](https://developer.ibm.com/exchanges/data/)

- thematic-clustering-of-sentences/ : contains the dataset, dataset.csv, from IBM research described in their [paper](https://www.aclweb.org/anthology/P18-2009.pdf), used for clustering.
- sentiment-composition-lexicons/ : contains all the datasets (ADJECTIVES.xlsx, LEXICON_UG.txt, LEXICON_BG.txt, SEMANTIC_CLASSES.xlsx) from IBM research described in their [paper](https://www.aclweb.org/anthology/C18-1189.pdf), used for sentiment analysis.

More information about the thematic clustering dataset can be found [here](https://developer.ibm.com/exchanges/data/all/thematic-clustering-of-sentences/). More information about the lexicons dataset can be found [here](https://developer.ibm.com/exchanges/data/all/sentiment-composition-lexicons/). 

Check `thematic-clustering-glossary-terms.csv`, `adjectives-gloassary-terms.csv`, `lexicon-bg-glossary-terms.csv`, `lexicon-ug-glossary-terms.csv`, `semantic-classes-glossary-terms.csv` for data glossary

### Notebooks

Follow the sequence shown below

* **1_Data_Exploration_and_Model_Training**: Load data; Prepare and clean data for model training; Demonstrates in detail how the clustering and sentiment analysis models work;

* **2_Model_Deployment**: Create a Watson Machine Learning based deployment space; Create and deploy pipeline functions for model scoring (one for clustering, another for sentiment analysis);

## Sequence of steps to run


* Open **1_Data_Exploration_and_Model_Training** notebook & execute step-by-step to understand how the models work.
* Open **2_Model_Deployment** notebook & execute step-by-step to deploy the models.
* Go to `Deployments` and choose `Comments Organizer Space`. Click on `Deployments` tab and choose recent `Sentiment Analysis Deployment` and `Clustering Deployment`.
* Under the `API Reference` tab, copy the endpoint link of both the deployments. This will be used for running the app locally.
* View instructions under **Python Flask App** section to run the example app locally or deploy

### Python Flask App

#### Files
* */comments_organizer_app*: Directory that contains all files for a Flask app, as well as files needed if want to deploy app
  * */static*: Directory that contains static files like css, js (javascript) files needed for the front end of the app. Also has an example input for comments (test_comment_5.txt, test_comment_20.txt)
  * */template*: Directory that contains any html files. index.html is the main file.
  * *Profile*: File that contains command to run app, needed to deploy app on IBM Cloud Foundry
  * *app.py*: Main Flask app file
  * *manifest.yml*: Contains information needed to deploy the app on IBM Cloud Foundry
  * *requirements.txt*: Python libraries and versions used in the app. If more libraries are used, this file should be updated to include them.
  * *setup.py*: Setup for Flask app and deploying the app.


#### Running the App Locally
The app serves as an example of using the functions deployed with Watson Machine Learning.

1. In order to run the Flask app (`comments_organizer_app`) locally, two main functions (1. clustering, 2. sentiment analysis) must be deployed. 

2. In a terminal window (or command prompt in Windows), run the following command to get a token to access the API. Use your Cloud Pak for Data cluster username and password:

```
curl -k -X GET https://<cluster-url>/v1/preauth/validateAuth -u <username>:<password>
```

A json string will be returned. Copy and save the "accessToken".

3. Login to IBM Cloud account, click on `Manage` and choose `Access IAM`. Click on `API Keys`. Either create a new key or copy details from the existing key. Choose endpoint listed in [this](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-overview.html) page.

4. Create a Cloud Object Storage instance using the steps list [here](https://cloud.ibm.com/docs/cloud-object-storage/basics?topic=cloud-object-storage-provision) if not available and service credentails using the steps 
listed [here](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-service-credentials). Copy the credentail under `iam_serviceid_crn`  

2. Then once you have your IBM Cloud API Key, Cloud Object Storage crn link, and endpoint details of two deployments, you can go to `comments_organizer_app/app.py`. Search for 'TODO' and:
     * Replace `wml_credentials` with the credentials you have made in step 3.
     * Replace `space_tag` with Cloud Object Storage crn link you have made in step 4.
     * Replace `clustering_endpoint_url` and `sentiment_analysis_endpoint_url` with the correct urls you obtained from step 4 under `Sequence of steps to run`. 
     
3. Make sure you have all the libraries downdloaded from `requirements.txt`, so run
```
pip install -r requirements.txt
```
4. Now you should be able to run the Flask app. In the directory `comments_organizer_app`, run
```
python app.py
```
The app should be visible on http://0.0.0.0:8000/

5. In the web app, you can load example comments by clicking "Choose File" then comments_organizer_app -> static -> test_comments_20.txt. Now if click "Clustering", "Sentiment Analysis", or "Graphs" you will get dynamic results based on the comments you upload.

**This project contains Sample Materials, provided under license. <br>
Licensed Materials - Property of IBM. <br>
© Copyright IBM Corp. 2019, 2020. All Rights Reserved. <br>
US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.<br>**