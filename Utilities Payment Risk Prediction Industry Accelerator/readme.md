# Utilities Payment Risk Prediction
Import the project Utilities Payment Risk Prediction
into cloud pak for data as a service from [IBM Cloud Gallery](
https://dataplatform.cloud.ibm.com/exchange/public/entry/view/14ea8dfab582137c695a6630e9138d44?context=cpdaas). <br>

## Introduction

The Payment Risk Prediction accelerator helps identify the customers who are likely to miss paying their utility bill by the due date, allowing the business to proactively engage with these customers. The Payment Risk Prediction accelerator includes a structured glossary of business terms and a set of sample data science assets. The glossary provides the information architecture that you need to understand why customers miss their utility bill payment. Your data scientists can use the sample notebooks, the predictive model and the dashboard to accelerate data preparation, machine learning modeling and data reporting.


**Tip:** Download the PDF of these instructions from the Data assets section on the **Assets** page so you can keep these instructions open while you work.

- [Instructions](#instructions)
- [Sample data assets](#data-assets)
- [Notebooks](#notebooks)
- [R Shiny dashboard](#dashboard)
- [Sample business glossary](#glossary)


<a id="instructions"></a>
## Instructions

Follow these steps to implement the industry accelerator:
1. Create a deployment space, which you'll need when you run the notebooks. From the navigation menu, select **Deployments > View All Spaces > New deployment space** and then complete these steps:
    1. Enter the name `Utilities Payment Risk Prediction Space`.
    1. Select your Watson Machine Learning service. If you don't have one, from the **Select machine learning service** pull-down menu, select **Create a new machine learning service**, provision one, and then click the **Create** button.
    1. Click **Create** to create the deployment space.
1. Navigate back to the accelerator project, select the **Assets** tab and scroll to the **Notebooks** section.
1. Edit the `1-model-training` notebook. This notebook prepares the data, builds ML models, and deploys the model. Follow the instructions in the notebook to configure and step through the execution.
1. Edit and run the `2-model-scoring` notebook. This notebook deploys data assets and a model scoring function.
1. Run the dashboard from RStudio console by completing these steps:
    1. Download the `utilities-payment-risk-prediction-analytics-dashboard.zip` file from the Data assets section of the **Assets** page. If you don't see the file, click **View All** to display the full list of assets.
    1. Click **Launch IDE > RStudio** on the menu bar. 
    1. In the **Files** pane, select the **Upload** toolbar button and upload the `utilities-payment-risk-prediction-analytics-dashboard.zip` file into RStudio.
    1. Navigate to `utilities-payment-risk-prediction-analytics-dashboard`, select the `app.R` file, and click the **Run App** toolbar button to launch the dashboard. If you see a warning message that certain packages are not installed, you can ignore it because the packages will be installed first time you run the app. 
    1. Once the app has launched, you can perform model scoring in real time by entering your API key and selecting your region on the **Client View** tab.
1. Optional.  You can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. With the **Lite plan** only 5 Business terms can be imported. You must have <a href="https://dataplatform.cloud.ibm.com/docs/content/wsj/catalog/roles-wkcop.html" target="_blank" rel="noopener noreferrer">the permission to create governance artifacts</a>.
    1. Download the `utilities-payment-risk-prediction-glossary-categories.csv` and `utilities-payment-risk-prediction-glossary-terms.csv` files from the Data assets section of the **Assets** page.
    1. Navigate to **Governance > Categories**.
    1. Click **Add Category > Import From File**. 
    1. Import the `utilities-payment-risk-prediction-glossary-categories.csv` file. Select **Replace all values** as your merge option.
    1. Navigate to **Governance > Business Terms**.
    1. Click **Add Business Term > Import From File**. 
    1. Import the `utilities-payment-risk-prediction-glossary-terms.csv` file. Select **Replace all values** as your merge option.
    1. Once the Import completes successfully, click on **Go to task** and then click **Publish** in the next page.
    1. Navigate to **Governance > Categories > Industry Accelerators** to explore the business terms.

*Note: Importing the accelerator and running the notebooks and dashboard consumes approximately 1.5 - 2 Watson Studio CUH and 3 - 3.5 Watson Machine Learning CUH.

 <a id="data-assets"></a>
## Sample data assets
These sample data files that act as dimensional and fact tables are included in the project on the **Assets** page: <br>
- `CUSTOMER.csv`: Customer demographic data.
- `CST_PROFILES.csv`: Customer profiling information.
- `EMPLOYMENT.csv`: Dimension table with different Employment categories.
- `LOCATION.csv`: Dimension table with location data such as addresses and coordinates.
- `EDUCATION.csv`: Dimension table with different Education categories.
- `MARITAL_STATUS.csv`: Dimension table with marital status categories. M - Married, S - Single, U - Unknown
- `CST_SEGMENT.csv` : Dimension table with segment categories for customers.
- `CST_BUILDING_PROFILES.csv` : Table with building details for each customer.
- `BUILDING_TYPE.csv` : Dimensional table with categories for building type.
- `GENDER.csv'`: Dimensional table with gender status'.
- `INVOICE.csv` : Historical utility bill payment details. Includes monthly billing amounts, energy usage, billing and due dates for each customer.
- `ACCOUNT.csv`: Account details, such as rate start and end dates and credit history for each customer account.
- `Bill Payment View.csv` : Joining the above datasets, we created a csv file that is used as raw data input for the data preparation in `1-model-training` notebook. Refer to `Bill Payment View Creation Query.sql` for the SQL query used to merge the tables.
- `model output summary.csv`: Data file generated in `1-model-training` notebook, contains records for all customers and all billing cycles, including the latest cycle for each customer, where the actual target value is not known.

<a id="notebooks"></a>
## Notebooks
Follow the instructions in the first few cells of the notebook to configure the project token and API key. Then execute the notebooks step-by-step.
- **1-model-training**:  This notebook performs the following functions: 
    - Load data
    - Prepare and clean data for model training
    - Build ML models, Analyze and visualize the data
    - Select best performing ML model and save to Cloud Pak for Data
    - Create a Watson Machine Learning based deployment space
    - Store the model in the space and deploy the model.
- **2-model-scoring**: This notebook performs the following functions: 
    - Get the deployment space and deployments
    - Deploy the data assets
    - Create and deploy a function for model scoring
    -  Predict the probability that a customer will miss their payment. 

<a id="dashboard"></a>
## R Shiny dashboard
The R Shiny dashboard displays model insights, customer summaries and scores new data. The dashboard has the following tabs:
- Billing Cycle View : This tab gives the user a view of the important customer information for the current billing cycle, such as the number of customers billed, total amount owed and overdue amount owed in the period. In our example, the billing cycle is the last month of data that we have, June 2019. The data can be filtered by city, customer segment, if they missed the payment last month, total bill amount range and history of missing payments. The tab also contains charts showing the historical billing cycle number of customers who missed their payment, the overdue amount owed each billing cycle and the frequency of missed payments. Each customer was scored in 1-model-training and assigned a probability of missing this month's bill payment. Summary data for each customer is contained in the table. Clicking on any customer brings the user to the Client View tab for that customer.
- Client View : Provides client information and current billing information for the selected individual. This tab also contains historical billing amounts, usage and predictions for the selected customer. The option to run the model scoring webservice, predicting the risk of the selected customer missing their current bill payment, can also be found in this tab.

Home page of the r-shiny dashboard would look like below
![alt text](https://public.dhe.ibm.com/software/data/sw-library/cognos/mobile/C11/catalog/images/cp4d/Utilities_Payment_Risk_Prediction_Dashboard.png)

<a id="glossary"></a>
## Sample business glossary for use with Watson Knowledge Catalog
Optionally, you can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. <br>

The `utilities-payment-risk-prediction-glossary-categories.csv` file defines the main and sub categories for the business terms. <br>
The `utilities-payment-risk-prediction-glossary-terms.csv` file defines the business terms, category of the business terms and their Related Terms/Part of Terms, if applicable. <br>

### Terms and Conditions
This project contains Sample Materials, provided under this <a href="https://github.com/IBM/Industry-Accelerators/blob/master/CPD%20SaaS/LICENSE" target="_blank" rel="noopener noreferrer">license</a>. <br/>
Licensed Materials - Property of IBM. <br/>
© Copyright IBM Corp. 2020, 2021. All Rights Reserved. <br/>
US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.<br/>
