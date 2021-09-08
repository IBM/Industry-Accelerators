# Utilities Demand Response Program Propensity
Import the project Utilities Demand Response Program Propensity
into cloud pak for data as a service from [IBM Cloud Gallery](
https://dataplatform.cloud.ibm.com/exchange/public/entry/view/14ea8dfab582137c695a6630e9137ea0?context=cpdaas). <br>

## Introduction
The Demand Response Program is what Utilities companies can offer to residential and commercial customers. In exchange for discounted rates, customers agree to reduce or cycle down energy load during periods of peak demand.

The Demand Response (DR) Program Propensity accelerator includes a structured glossary of business terms and a set of sample data science assets. The glossary provides the information architecture that you need to understand which customers are most likely to enroll in the Demand Response Program. Your data scientists can use the sample notebooks, predictive model and dashboard to accelerate data preparation, machine learning modeling and data reporting. Identifying those customers who are most likely to enroll in the Demand Response Program allows your business users or marketers to focus on these prospects.

**Tip:** Download the PDF of these instructions from the Data assets section on the **Assets** page so you can keep these instructions open while you work.

- [Instructions](#instructions)
- [Sample data assets](#data-assets)
- [Cognos Dashboard Embedded](#cognos-dashboard)
- [Notebooks](#notebooks)
- [R Shiny dashboard](#dashboard)
- [Sample business glossary](#glossary)


<a id="instructions"></a>
## Instructions
Follow these steps to implement the industry accelerator:
1. Optional.  You can explore the data and understand various features of Demand Response Program using Cognos Dashboard Embedded. select the **Assets** tab and scroll to the **Dashboard** section.
    1. Edit the **Utilities Demand Response Cognos Dashboard** dashboard by clicking the edit icon  that looks like a tiny pencil next to the dashboard name.
1. Create a deployment space, which you'll need when you run the notebooks. From the navigation menu, select **Deployments > View All Spaces > New deployment space** and then complete these steps:
    1. Enter the name `Utilities Demand Response Propensity Space`.
    1. Select your Watson Machine Learning service. If you don't have one, from the **Select machine learning service** pull-down menu, select **Create a new machine learning service**, provision one, and then click the **Create** button.
    1. Click **Create** to create the deployment space.
1. Navigate back to the accelerator project, select the **Assets** tab and scroll to the **Notebooks** section.
1. Edit the  **1-model-training** notebook by clicking the edit icon that looks like a tiny pencil next to the notebook name. This notebook prepares the data, builds ML models, and deploys the model. Follow the instructions in the notebook to configure and step through running it.
1. Edit and run the **2-model-scoring** notebook. This notebook deploys the data assets and model scoring function.
1. Run the dashboard from RStudio console by completing these steps:
    1. Download the `utilities-demand-response-program-analytics-dashboard.zip` file from the Data assets section of the **Assets** page. If you don't see the file, click **View All** to display the full list of assets.
    1. Click **Launch IDE > RStudio** on the menu bar. 
    1. In the **Files** pane, select the **Upload** toolbar button and upload the `utilities-demand-response-program-analytics-dashboard.zip` file into RStudio.
    1. Navigate to `utilities-demand-response-program-analytics-dashboard`, select the `app.R` file, and click the **Run App** toolbar button to launch the dashboard. If you see a warning message that certain packages are not installed, you can ignore it because the packages will be installed first time you run the app. 
    1. Once the app has launched, you can perform model scoring in real time by entering your API key and selecting your region on the **Client View** tab.
1. Optional.  You can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. With the **Lite plan** only 5 Business terms can be imported. You must have <a href="https://dataplatform.cloud.ibm.com/docs/content/wsj/catalog/roles-wkcop.html" target="_blank" rel="noopener noreferrer">permission to create governance artifacts</a>.
    1. Download the `utilities-demand-response-program-glossary-categories.csv`and `utilities-demand-response-segmentation-glossary-terms.csv` files from the Data assets section of the **Assets** page.
    1. Navigate to **Governance > Categories**.
    1. Click **Add Category > Import From File**. 
    1. Import the `utilities-demand-response-program-glossary-categories.csv` file. Select **Replace all values** as your merge option.
    1. Navigate to **Governance > Business Terms**.
    1. Click **Add Business Term > Import From File**. 
    1. Import the `utilities-demand-response-program-glossary-terms.csv` file. Select **Replace all values** as your merge option.
    1. Once the Import completes successfully, click on **Go to task** and then click **Publish** in the next page.
    1. Navigate to **Governance > Categories > Industry Accelerators** to explore the business terms.

**Note:** Importing the accelerator and running the notebooks and dashboard consumes approximately 1.5 - 2 Watson Studio CUH and 3 - 3.5 Watson Machine Learning CUH.


 <a id="data-assets"></a>
### Sample Data Assets
We provide a number of sample data files which act as dimensional and fact tables. These files can be found in the project's data assets area:
- `CUSTOMER.csv`: Customer demographic data.
- `STANDARD_YEARLY_USAGE.csv`: Historical annual energy usage for each customer for previous 7 years.
- `CST_PROFILES.csv`: Customer profiling information.
- `EMPLOYMENT.csv`: Dimension table with different Employment categories.
- `LOCATION.csv`: Dimension table with location data such as addresses and coordinates.
- `EDUCATION.csv`: Dimension table with different Education categories.
- `MARITAL_STATUS.csv`: Dimension table with marital status categories. M - Married, S - Single, U - Unknown
- `CST_SEGMENT.csv` : Dimension table with segment categories for customers.
-  `GENDER.csv`: Dimensional table with gender status.
- `Demand Response View.csv` : Joining the above datasets, we created a csv file that is used as raw data input for the data preparation in `1-model-training` notebook. Refer to `Demand Response View Creation Query.sql` for the SQL query used to merge the tables.
- `model output summary`: Data file generated in 1-model-training notebook by combining the raw training data with actual and predicted probabilities to display the model insights on the dashboard.

<a id="cognos-dashboard"></a>
## Cognos Dashboard Embedded
Explore the raw data `Demand Response View.csv`using Cognos Embedded Dashboard. The **Utilities Demand Response Cognos Dashboard**  visualizes response for the offer program from different types of customers, different cities etc.The dashboard also displays customer details and an overview of how customer's demographics and usage affect their response to the program.

Note: This optional step requires the **IBM Cognos Dashboard Embedded** service instance.

<a id="notebooks"></a>
## Notebooks
Follow the instructions in the first few cells of the notebook to configure the project token and API key. Then run the notebooks step-by-step.
- **1-model-training**: This notebook performs the following functions: 
    - Load data
    - Prepare and clean data for model training.
    - Analyze correlations.
    - Build ML models, Analyze and visualize the data
    - Select best performing ML model, create the final pipeline and save to Cloud Pak for Data
    - Store the pipeline in the space and deploy the model. <br>

- **2-model-scoring**: This notebook performs the following functions: 
    - Get the deployment space and deployments
    - Deploy the data assets
    - Create and deploy a function for model scoring
    - Predict demand response.  <br>


<a id="dashboard"></a>
## R Shiny dashboard
The R Shiny dashboard displays model insights, customer summaries and scores new data. The dashboard has the following tabs:
- `Model Insights` : This tab contains results from `1-model-training` notebook. The model was applied to the training data and the results on this data is displayed. The user can see how many customers were in the training data, how many were predicted to be interested in enrolling in the Demand Response Program and the propensity rate. The cumulative gains and lift charts for this data are also plotted. This data can be filtered by customer segment, service territory and warranty. The tab also contains a table of data which was the test data in `1-model-training` notebook. This data is used to simulate new data which has just been scored by the model and for which we don't yet know the true target value, whether they actually would be interested in joining the Demand Response Program or not. By clicking on a point on the cumulative gains chart this table is filtered and can be exported. An analyst or marketer can use this to target a specific percentage of customers instead of having to contact all customers.
- `Client View` : Targets individual client information, depicts the top account customer details and summarizes their historical energy usage. It provides the option to run the model scoring webservice, returning the propensity probability for the selected customer.

Home page of the r-shiny dashboard would look like below
![alt text](https://public.dhe.ibm.com/software/data/sw-library/cognos/mobile/C11/catalog/images/cp4d/utilities-demand-response-dashboard.png)

<a id="glossary"></a>
## Sample business glossary for use with Watson Knowledge Catalog
Optionally, you can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. <br>

The `utilities-demand-response-program-glossary-categories.csv` file defines the main and sub categories for the business terms. <br>
The `utilities-demand-response-program-glossary-terms.csv` file defines the business terms, category of the business terms and their Related Terms/Part of Terms if applicable. <br>

**Note:** This optional step requires the Watson Knowledge Catalog service instance. 

### Terms and Conditions
This project contains Sample Materials, provided under this <a href="https://github.com/IBM/Industry-Accelerators/blob/master/CPD%20SaaS/LICENSE" target="_blank" rel="noopener noreferrer">license</a>. <br/>
Licensed Materials - Property of IBM. <br/>
© Copyright IBM Corp. 2020, 2021. All Rights Reserved. <br/>
US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.<br/>
