# Insurance Loss Estimation using Remote Sensing Industry Accelerator
Import the project Insurance Loss Estimation using Remote Sensing
into cloud pak for data as a service from [IBM Cloud Gallery](
https://dataplatform.cloud.ibm.com/exchange/public/entry/view/14ea8dfab582137c695a6630e90cdc32?context=cpdaas). <br>

## Introduction
With the increase in the number of satellite launches and the dramatic improvements in sensing technology (e.g., better cameras with hyper-spectral imaging, synthetic aperture radar, and lidar), remote sensing data now has much better quality in resolution and spatio-temporal coverage. There is demand for using this data to solve business issues across a wide range of industries, including insurance, urban planning, agriculture, climate change, and flood prevention. This creates a need for ML/AI technology solutions for remote sensing data. <br>

Insurance Loss Estimation Using Remote Sensing Data Industry Accelerator shows how to derive insights from remote sensing data, by utilizing an example of studying flooding events for assisting insurance claims. The idea in this accelerator is to study satellite images before and after a certain event, and with the help of spatiotemporal analysis and ML/AI techniques, we can get insights into which regions are affected and to what extent. Such insights provide valuable information to insurance companies on property damage, allowing claims to be processed more efficiently. <br>
For this specific usecase, we picked a category 4 storm event **Hurricane Laura** which caused damage to many areas of Louisiana, United States in August, 2020. Insurance companies can use this accelerator to understand remote sensing capabilities to study the flood event, get insights on impacted regions and then predict estimated claims for individal properties.

Your data scientists can use the sample notebooks, remote sensing analysis, predictive model, and dashboard to accelerate data preparation, machine learning modelling, and data reporting.  All the functionality in this accelerator can be generalized and used towards other use cases for remote sensing data.

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
    1. Enter the name `Insurance Loss Estimation Using Remote Sensing Space`.
    1. Select your Watson Machine Learning service. If you don't have one, from the **Select machine learning service** pull-down menu, select **Create a new machine learning service**, provision one, and then click the **Create** button.
    1. Click **Create** to create the deployment space.
1. Navigate back to the accelerator project, select the **Assets** tab and scroll to the **Notebooks** section.
1. Edit the  **1 - Impact Region Analysis with Remote Sensing** notebook by clicking the edit icon that looks like a tiny pencil next to the notebook name. Follow the instructions in the notebook to configure and step through running it.
1. Edit and run the **2 - Model Training and Deployment** notebook. 
1. Run the dashboard from RStudio console by completing these steps:
    1. Download the `insurance-loss-estimation-using-remote-sensing-analytics-dashboard.zip` file from the Data assets section of the **Assets** page. If you don't see the file, click **View All** to display the full list of assets.
    1. Click **Launch IDE > RStudio** on the menu bar. 
    1. In the **Files** pane, select the **Upload** toolbar button and upload the `insurance-loss-estimation-using-remote-sensing-analytics-dashboard.zip` file into RStudio.
    1. Navigate to `insurance-loss-estimation-using-remote-sensing-analytics-dashboard`, select the `app.R` file, and click the **Run App** toolbar button to launch the dashboard. If you see a warning message that certain packages are not installed, you can ignore it because the packages will be installed first time you run the app. 
    1. Once the app has launched, you can perform model scoring in real time by entering your API key and selecting your region on the **Property View** tab.
1. Optional.  You can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. With the **Lite plan** only 5 Business terms can be imported.  You must have <a href="https://dataplatform.cloud.ibm.com/docs/content/wsj/catalog/roles-wkcop.html" target="_blank" rel="noopener noreferrer">the permission to create governance artifacts</a>.
    1. Download the `insurance-loss-estimation-using-remote-sensing-data-glossary-categories.csv` and  `insurance-loss-estimation-using-remote-sensing-data-glossary-terms.csv` files from the Data assets section of the **Assets** page.
    1. Navigate to **Governance > Categories**.
    1. Click **Add Category > Import From File**. 
    1. Import the `insurance-loss-estimation-using-remote-sensing-data-glossary-categories.csv` file. Select **Replace all values** as your merge option.
    1. Navigate to **Governance > Business Terms**.
    1. Click **Add Business Term > Import From File**. 
    1. Import the `insurance-loss-estimation-using-remote-sensing-data-glossary-terms.csv` file. Select **Replace all values** as your merge option.
    1. Once the Import completes successfully, click on **Go to task** and then click **Publish** in the next page.
    1. Navigate to **Governance > Categories > Industry Accelerators** to explore the business terms.


**Note:** Importing the accelerator and running the notebooks and dashboard consumes approximately 1.5 - 2 Watson Studio CUH and 3 - 3.5 Watson Machine Learning CUH.

 <a id="data-assets"></a>
## Sample data assets
These sample data files that act as dimensional and fact tables are included in the project on the **Assets** page:<br>
`Remote Sensing Input.csv:` Property Ids and property cordinates in Cameron town, Louisiana. <br>
`Insurance Loss Claims.csv:` Customer's property information including property value, construction details, size, property damage amount etc. and insurance information including sum insured limit, previous claims, estimated insurance claim etc. <br>
`b03_before.tif`:  Green band satellite image of Cameron town captured before Hurricane Laura. <br>
`b03_after.tif`: Green band satellite image of Cameron town captured after Hurricane Laura. <br>
`b08_before.tif`: Near infrared band satellite image of Cameron town captured before Hurricane Laura. <br>
`b08_after.tif`: Near infrared band satellite image of Cameron town captured after Hurricane Laura.<br>
Additionally, there are other 2 datasets created via the analytics project: <br>
`Remote Sensing Output.csv:` Flood impact details on the properties provided in Remote Sensing Input.csv. This dataset is generated by the notebook `1-Impact_Region_Analysis_with_Remote_Sensing`.<br>
`model_output_summary.csv`: Consolidated prepped data after combining remote sensing and insurance loss claims datasets for exploratory data analysis and data visualization in the R shiny dashboard. <br>

<a id="notebooks"></a>
## Notebooks
Follow the instructions in the first few cells of the notebook to configure the project token and API key. Then run the notebooks step-by-step.
- **1 - Impact Region Analysis with Remote Sensing**: This notebook performs the following functions: 
    - Study satellite images before and after a certain event (e.g. hurricane Laura) with the help of spatiotemporal analysis and ML/AI techniques.
    - Get insights to understand which regions are affected and to what extent.
    - Read in property cordinates to calculate impact scores on each property and save out the result. <br>

- **2 - Model Training and Deployment**: This notebook performs the following functions: 
    - Load Remote Sensing Output and Insurance Loss Claims.
    - Prepare and clean data for model training.
    - Analyze correlations.
    - Build ML models, Analyze and visualize the data. 
    - Select best performing ML model and save to Cloud Pak for Data.
    - Create a  deployment space and store the pipeline in the space and deploy. <br>

<a id="dashboard"></a>
## R Shiny dashboard
The R Shiny dashboard displays flood impact insights on Cameron town, property details and scores new data. The dashboard has the following tabs:
- Remote Sensing: Displays the impact zones and properties of Cameron town. By clicking on the impact zones in the map the dashboard displays properties and insurance details specific to the impact zone. The tab also shows the satellite images before and after the storm event.

- Property View: Targets individual property and insurance information, displays an impact score calculated by the remote sensing exercise. It provides the option to run the model webservice which predicts the estimated claim amount for the property.

- Simulation Tool : This tab contains a form with all model inputs. The user can change any of these inputs and see the impact that the change has on predicting the estimated claim amount.

Home page of the r-shiny dashboard would look like below
![alt text](https://public.dhe.ibm.com/software/data/sw-library/cognos/mobile/C11/catalog/images/cp4d/Remote-sensing-dashboard1.png)
<a id="glossary"></a>

<a id="glossary"></a>
## Sample business glossary for use with Watson Knowledge Catalog
Optionally, you can import the glossary of business terms into Watson Knowledge Catalog to get started on data governance. <br>

The `insurance-loss-estimation-using-remote-sensing-data-glossary-categories.csv` file defines the main and sub categories for the business terms. <br>
The `insurance-loss-estimation-using-remote-sensing-data-glossary-terms.csv` file defines the business terms, category of the business terms and their Related Terms/Part of Terms, if applicable. <br>
**Note:** This optional step requires the Watson Knowledge Catalog service instance. 

## Terms and Conditions
This project contains Sample Materials, provided under this <a href="https://github.com/IBM/Industry-Accelerators/blob/master/CPD%20SaaS/LICENSE" target="_blank" rel="noopener noreferrer">license</a>. <br/>
Licensed Materials - Property of IBM. <br/>
© Copyright IBM Corp. 2020, 2021. All Rights Reserved. <br/>
US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.<br/>
