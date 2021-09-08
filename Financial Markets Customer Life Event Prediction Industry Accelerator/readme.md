## Financial Markets Customer Life Event Prediction
Import the project Financial Markets Customer Life Event Prediction
into cloud pak for data as a service from [IBM Cloud Gallery](
https://eu-gb.dataplatform.cloud.ibm.com/exchange/public/entry/view/e9c830e3e54b41a6d42efbeb37153f0f?context=cpdaas). <br>
### Introduction

The Customer Life Event Prediction accelerator includes a structured glossary of  business terms and a set of sample data science assets. The glossary provides the information architecture that you need to predict major life events, such as buying a home or relocating. You can use the sample notebooks, predictive models, and dashboards to accelerate data preparation, machine learning modelling, and data reporting. Set your clients on the path to financial success by engaging with them at the right time with relevant investment options.

**Tip:** Download the PDF of these instructions from the Data assets section on the **Assets** page so you can keep these instructions open while you work.

- [Instructions](#instructions)
- [Sample data assets](#data-assets)
- [Notebooks](#notebooks)
- [R Shiny dashboard](#dashboard)
- [Sample business glossary](#glossary)

<a id="instructions"></a>
## Instructions
Follow these steps to implement the industry accelerator:

1 . Create a deployment space, which you'll need when you run the notebooks. From the navigation menu, select **Deployments > View All Spaces > New deployment space** and then complete these steps:
 1. Enter the name `Customer Life Event Space`
 2. Select your Watson Machine Learning service. If you don't have one, click the **Create** button and provision one.
 3. Click on **Create** to create the deployment space.

2 . Navigate back to the accelerator project, select the **Assets** tab and scroll to the **Notebooks** section.

3 . Edit the **1-data-preprocessing** notebook by clicking the edit icon that looks like a tiny pencil next to the notebook name. This notebook loads the data, creates and saves the `life_event_prep.py` script to prepare and clean data for model training. It also selects life events to predict from the data set. Follow the instructions in the notebook to configure and step through running it.

4 . Edit and run the **2-model-training** notebook. This notebook transforms the data, builds ML models  and deploys the models.

5 . Edit and run the **3-model-scoring**. This notebook deploys the data assets and a model scoring function.

6 . Run the dashboard from RStudio console by completing these steps:
 1. Download the `customer-life-event-analytics-dashboard.zip` file from the project's Data assets section of the **Assets** page. If you don't see the file, click **View All** to display the full list of assets.
 2. Click **Launch IDE > RStudio** on the menu bar.
 3. In the **Files** pane, select the **Upload** toolbar button and upload the `customer-life-event-analytics-dashboard.zip` file into RStudio.
 4. Navigate to `customer-life-event-analytics-dashboard`, select the `app.R` file, and click the **Run App** toolbar button to launch the dashboard. If you see a warning message that certain packages are not installed, you can ignore it because the packages will be installed first time you run the app.
 5. Once the app has launched, you can perform model scoring in real time by entering your API key and selecting your region on the **Client View** tab. 

7 . Optional.  You can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. With the **Lite plan** only 5 Business terms can be imported.  You must have <a href="https://dataplatform.cloud.ibm.com/docs/content/wsj/catalog/roles-wkcop.html" target="_blank" rel="noopener noreferrer">permission to create governance artifacts</a>.
 1. Download the `customer-life-event-glossary-categories.csv`and `customer-life-event-glossary-terms.csv` files from the Data assets section of the **Assets** page.
 1. Navigate to **Governance > Categories**.
 1. Click **Add Category > Import From File**. 
 1. Import the `customer-life-event-glossary-categories.csv` file. Select **Replace all values** as your merge option.
 1. Navigate to **Governance > Business Terms**.
 1. Click **Add Business Term > Import From File**. 
 1. Import the `customer-life-event-glossary-terms.csv` file. Select **Replace all values** as your merge option.
 1. Once the Import completes successfully, click on **Go to task** and then click **Publish** in the next page.
 1. Navigate to **Governance > Categories > Industry Accelerators** to explore the business terms.


**Note:** Importing the accelerator and running the notebooks and dashboard consumes approximately 1.5 - 2 Watson Studio CUH and 3 - 3.5 Watson Machine Learning CUH.

 <a id="data-assets"></a>
## Sample data assets
These sample data files that act as dimensional and fact tables are included in the project on the **Assets** page:

- `event.csv`: Event and type data, Temporal data, Life event category etc.
- `customer.csv` : Customer Data, Demographic data.
- `census_probabilities.csv` : Migration, birth, marriage and birth probabilities based on USA census. (This is an optional addition for the user to incorporate census data into the final dataset for modelling.)
- `news.csv`: Contains News information. This information is only used to depict relevant news and life event type information in the analytics dashboard.
- `event_type.csv`:It comprises of event type data, life event type data etc.
- `training_user_inputs_and_prepped_column_names.json` : Used for standardizing the numeric variables for modelling by scaling the values. 

<a id="notebooks"></a>
## Notebooks
Follow the instructions in the first few cells of the notebook to configure the project token and API key. Then run the notebooks step-by-step. <br>
 - **1-data-preprocessing**: This notebook performs the following functions:
    - Load data
    - Create and save script `life_event_prep.py` to prepare and clean data for model training
    - Select life events to predict.

- **2-model-training**: This notebook performs the following functions:
    - Build ML models
    - Analysis and visualization of data
    - Select best performing ML model and save to Cloud Pak for Data
    - Create a Watson Machine Learning based deployment space and store the models in the space and deploy the model.

- **3-model-scoring**: This notebook performs the following functions:
    - Gets the deployment space and deployments
    - Deploys the data assets
    - Creating and deploying a pipeline function for model scoring
    - Prediction of Life Events.

<a id="dashboard"></a>
## R Shiny dashboard

The R Shiny dashboard displays model insights, customer summaries and scores new data. The dashboard has the following tab:

`Dashboard View` : Shows client activity, Top action Clients, Market Action, Recent Life events experienced by clients, and Revenue Opportunities.

`Client View` : Targets individual Client information (personal and financial), Depicts the Top Business Metrics, Visualizes Event distribution, opportunities and Client life event history. It also provides option to run the Model Scoring, Predicts Life Events and Visualizes the influential factors and data fields.

![alt text](https://public.dhe.ibm.com/software/data/sw-library/cognos/mobile/C11/catalog/images/cp4d/LifeEventDashboard.PNG)
<a id="glossary"></a>
## Sample business glossary for use with Watson Knowledge Catalog
Optionally, the glossary of business terms can be imported into Watson Knowledge Catalog to get started on data governance.<br>
The `customer-life-event-glossary-categories.csv` file defines the main and sub categories for the business terms. <br>
The `customer-life-event-glossary-terms.csv` file defines the business terms, category of the business terms and their Related Terms/Part of Terms if applicable. <br>
**Note:** This optional step requires the [Watson Knowledge Catalog](https://cloud.ibm.com/catalog/services/watson-knowledge-catalog) service instance. 

### Terms and Conditions
This project contains Sample Materials, provided under this <a href="https://github.com/IBM/Industry-Accelerators/blob/master/CPD%20SaaS/LICENSE" target="_blank" rel="noopener noreferrer">license</a>. <br/>
Licensed Materials - Property of IBM. <br/>
© Copyright IBM Corp. 2019, 2021. All Rights Reserved. <br/>
US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.<br/>


