# Financial Markets Customer Offer Affinity
Import the project Financial Markets Customer Offer Affinity
into cloud pak for data as a service from [IBM Cloud Gallery](
https://dataplatform.cloud.ibm.com/exchange/public/entry/view/cab78523832431e767c41527a435e992). <br>

The Financial Markets Customer Offer Affinity accelerator predicts which products the customer is most likely to consider or require next to purchase.  

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
    1. Enter the name `Customer Offer Affinity Space`.
    1. Select your Watson Machine Learning service. If you don't have one, from the **Select machine learning service** pull-down menu, select **Create a new machine learning service**, provision one, and then click the **Create** button.
    1. Click **Create** to create the deployment space.
1. Navigate back to the accelerator project, select the **Assets** tab and scroll to the **Notebooks** section.
1. Edit the  **1-data-preprocessing** notebook by clicking the edit icon that looks like a tiny pencil next to the notebook name. This notebook loads the data and creates and saves the `offer_affinity_prep.py` script to prepare and clean data for model training. It also analyses correlations in the data set. Follow the instructions in the notebook to configure and step through running it.
1. Edit and run the **2-model-training** notebook. This notebook transforms the data, builds machine learning models, and deploys a model. 
1. Edit and run the **3-model-scoring** notebook. This notebook deploys the data assets and the model scoring function.
1. Run the dashboard from RStudio console by completing these steps:
    1. Download the `customer-offer-affinity-analytics-dashboard.zip` file from the Data assets section of the **Assets** page. If you don't see the file, click **View All** to display the full list of assets.
    1. Click **Launch IDE > RStudio** on the menu bar. 
    1. In the **Files** pane, select the **Upload** toolbar button and upload the `customer-offer-affinity-analytics-dashboard.zip` file into RStudio.
    1. Navigate to `customer-offer-affinity-analytics-dashboard`, select the `app.R` file, and click the **Run App** toolbar button to launch the dashboard. If you see a warning message that certain packages are not installed, you can ignore it because the packages will be installed first time you run the app. 
  1. Optional.  You can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. With the **Lite plan** only 5 Business terms can be imported. You must have <a href="https://dataplatform.cloud.ibm.com/docs/content/wsj/catalog/roles-wkcop.html" target="_blank" rel="noopener noreferrer">the permission to create governance artifacts</a>.
    1. Download the `customer-offer-affinity-glossary-categories.csv` and `customer-offer-affinity-glossary-terms.csv` files from the Data assets section of the **Assets** page.
    1. Navigate to **Governance > Categories**.
    1. Click **Add Category > Import From File**. 
    1. Import the `customer-offer-affinity-glossary-categories.csv` file. Select **Replace all values** as your merge option.
    1. Navigate to **Governance > Business Terms**.
    1. Click **Add Business Term > Import From File**. 
    1. Import the `customer-offer-affinity-glossary-terms.csv` file. Select **Replace all values** as your merge option.
    1. Once the Import completes successfully, click on **Go to task** and then click **Publish** in the next page.
    1. Navigate to **Governance > Categories > Industry Accelerators** to explore the business terms.


**Note:** Importing the accelerator and running the notebooks and dashboard consumes approximately 1.5 - 2 Watson Studio CUH and 3 - 3.5 Watson Machine Learning CUH.

 <a id="data-assets"></a>
## Sample data assets
These sample data files that act as dimensional and fact tables are included in the project on the **Assets** page:

- `customer.csv`: Contains customer data, demographic data, temporal data. 
- `customer_product_summary.csv`: Contains combinations and interactions data for each client and product group of interest.
- `customer_summary.csv`: Contains detailed customer transaction data, business metrics, investment and income statistics.
- `customerProductHistory.csv`: Contains a join of the previous three data sets based on Customer ID, Effective Date and Customer Summary End Date. This data set is used as raw data input for the data preparation in the **1-data-preprocessing** notebook. The data set has multiple records per customer, one for each month of summary data and multiple columns for each product, which can be used for modeling purposes. See the `CUSTOMER_PRODUCT_HISTORY.sql` file for the SQL query used to merge the tables. <br>

<a id="notebooks"></a>
## Notebooks
Follow the instructions in the first few cells of the notebook to configure the project token and API key. Then run the notebooks step-by-step.
- **1-data-preprocessing**: This notebook performs the following functions: 
    - Load data
    - Create and save script `offer_affinity_prep.py` to prepare and clean data for model training
    -  Analyze correlations 
- **2-model-training**: This notebook performs the following functions: 
    - Build ML models
    - Analyze and visualize the data
    - Select the best performing ML model and save it
    - Store the model in the deployment space and deploy the model <br>
- **3-model-scoring**: This notebook performs the following functions: 
    - Get the deployment space and deployments
    - Deploy the data assets
    - Create and deploy a pipeline function for model scoring
    - Predict offer affinity  <br>

<a id="dashboard"></a>
## R Shiny dashboard
The R Shiny dashboard displays product statistics and customer summaries, and scores new data. The dashboard has the following tabs:
- Dashboard View: Shows top action clients, trend of the number of offers for each product available, such as cash, education, and brokerage. Provides the percentage statistics of the purchased products that were originally offered.
- Client View: Targets individual client information, depicts the top business metrics, provides an option to run the Model Scoring Web service, predicts and ranks offer affinity, and visualizes the influential factors.

Home page of the dashboard would look like below.
![alt text](https://public.dhe.ibm.com/software/data/sw-library/cognos/mobile/C11/catalog/images/cp4d/OfferAffinityDashboard.PNG)

<a id="glossary"></a>
## Sample business glossary for use with Watson Knowledge Catalog
Optionally, you can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. <br>

The `customer-offer-affinity-glossary-categories.csv` file defines the main and sub categories for the business terms. <br>
The `customer-offer-affinity-glossary-terms.csv` file defines the business terms, category of the business terms and their Related Terms/Part of Terms, if applicable. <br>

**Note:** This optional step requires the Watson Knowledge Catalog service instance. 
## Terms and Conditions
This project contains Sample Materials, provided under this <a href="https://github.com/IBM/Industry-Accelerators/blob/master/CPD%20SaaS/LICENSE" target="_blank" rel="noopener noreferrer">license</a>. <br/>
Licensed Materials - Property of IBM. <br/>
© Copyright IBM Corp. 2019, 2021. All Rights Reserved. <br/>
US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.<br/>
