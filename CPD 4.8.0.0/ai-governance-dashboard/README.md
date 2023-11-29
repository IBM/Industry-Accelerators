# Steps to setup the dashboard
## Pre-requisites
#### 1.	Establish your business terms by importing Knowledge Accelerator content
For details about importing a Knowledge Accelerator, see [Getting started with the Knowledge Accelerators](https://www.ibm.com/docs/SSQNUZ_4.8.x/ka/get_started/get_started.html).
#### 2.	Connect your data assets to your business terms
The next step is to associate your data assets to the data classes and business terms, following these steps in IBM Knowledge Catalog:
1.	Create a connection to a data source.
2.	Use the Metadata Import capability to import the metadata on data assets from the data source.
3.	Use the Metadata Enrichment capability to enrich the data assets with data classifications and associations to the business terms that were imported from the Knowledge Accelerator.
4.	Publish the enriched metadata to a catalog.
#### 3. Use Model Inventory with AI Factsheet
1. Create model use case(s) in CPD or IBM Openpages
2. Add related governance artifacts such as data assets to be used by the AI Model.
3. Assign classification to model use case
4. Assign risk level if known
5. Run [notebook](https://github.ibm.com/IndustryModels/ModelsOps/blob/master/dashboards/ai-governance-dashboard) to establish custom data privacy facts for factsheets

These steps are fully described in:
- [Connecting to data sources](https://www.ibm.com/docs/SSQNUZ_4.8.x/cpd/access/connect-data-sources.html)
- [Importing metadata](https://www.ibm.com/docs/SSQNUZ_4.8.x/wsj/manage-data/metadata-import.html)
- [Managing metadata enrichment](https://www.ibm.com/docs/SSQNUZ_4.8.x/wsj/governance/metadata-enrichment.html)
- [Use Model Inventory with AI Factsheet](https://www.ibm.com/docs/SSQNUZ_4.8.x/wsj/analyze-data/factsheets-model-inventory.html)
- [Integrating Factsheets with IBM Openpages](https://ibmdocs-test.dcs.ibm.com/docs/SSQNUZ_4.8.x/wsj/analyze-data/factsheets-openpages-ovr.html)
#### 3.	Create your reporting database 
The metadata from IBM Knowledge Catalog can be sent to a reporting database and can be easily reported on using BI Reporting tools, such as Cognos Analytics, IBM Dashboards, or Tableau. You can also share the metadata using standard SQL queries.

To set up the reporting database:
1.	Create a database to store the data. There are a number of database engines supported. For this example, we created an IBM DB2  database with a pagesize of 32K.
```
db2 create database <DATABASE_NAME> PAGESIZE 32 K
```
2.	Create a schema in this database. For example: 
```
db2 connect to <DATABASE_NAME>
db2 create schema WKCREPORT
```

## Create a platform connection to the database
In Cloud Pak for Data, create a platform connection to the database: 
1. Navigate to Data > Platform connections > New Connection > IBM DB2
2. Enter the connection information, such as host name, port, username, and password
3. Test the connection to make sure it’s working, then click Create

## Setup reporting for IBM Knowledge Catalog and synch your data
####	1. In Cloud Pak for Data, give the user the Reporting Administrator role:
1. Navigate to Administration > Access Control.
2. Select the user, click Assign Roles and from the list of available roles, choose the Reporting Administrator and click Assign 1 Role.
4. Log out and log back in for permissions to become active.
####	2. Enable reporting on IKC Categories and Catalogs:
1. Navigate to Goverance\Categories and select the Knowledge Accelerator categories to be included in the reporting database.
2. Click on the categories Access Control tab and select Allow Reporting/Allow. 
Repeat this for all categories to be included in the reporting database.
3. Navigate to the Catalogs area and select the Catalog where the project assets were pubished.
4. Open the Settings tab, navigate to Reporting on asset metadata and select Allow Reporting/Allow.
####	3. Configure the reporting database:
1. Navigate to Administration > Governance and catalogs > Report setup 
2. Select the database and schema you created in the previous steps
3. Choose which information to report on. Make sure to enable reporting on: 
   - Catalogs: The catalog containing the data assets
   - Categories: the categories containing Knowledge Accelerator business terms and data classes, and the ‘[uncategorized]’ category which contains out of the box classifications
   - Others: any other types of data you may need
####	4. Start reporting to kick off the reporting process. 
This might take some time, depending on the amount of data that is in scope.

For further information, see [Setting up reporting for IBM Knowledge Catalog](https://www.ibm.com/docs/SSQNUZ_4.8.x/wsj/governance/report-setup.html)

## Create a database view
Once reporting has been established, connect to the database, and create the [database view](https://github.com/IBM/Industry-Accelerators/blob/master/CPD%204.8.0.0/ai-governance-dashboard/V_MDLUC_JOINS.sql) to join data across the required tables.

## Create the dashboard
#### Create a dashboard to visualize your data. 
1.	Create a new project for the dashboard.
     1. Navigate to Projects > New Project > Create an empty project.
2.	Add the platform connection created earlier to the project.
     1. On the  Assets tab, click New Asset > Connection > From platform tab. 
     1. Select the connection and click Create.
3.	Import the view created earlier as a data asset using Metadata Import.
     1. On Assets tab New Asset > Metadata Import > Discover.
     1. Select target: this project.
     1. Scope: select the Database Connection > WKCREPORT > V_MDLUC_JOINS view created earlier.
     1. Continue through the process, accepting the defaults.
4.	Create the dashboard
     1. On the Assets tab, click New Asset > Dashboard editor 
     1. Select the V_MDLUC_JOINS view as the data source
     1. Once data preparation is complete, drag and drop fields from the data source to create visualizations on the canvas. Tip: You can also import the pre-defined report. See the next section for steps.

#### If you want to import the pre-defined report into the dashboard you created, follow these steps.
1.	Copy the contents of [JSON dashboard source](https://github.com/IBM/Industry-Accelerators/blob/master/CPD%204.8.0.0/ai-governance-dashboard/AI_Governance_Dashboard.json) to the clipboard
2.	Click on the dashboard then on your keyboard, press the following keys together `ctrl` + `q` + `/` (forward slash) to open the json specification.
3.	Select all and paste to overwrite with the pre-defined dashboard. 
4.	Click Update.
5.	The dashboard will need to be re-linked to the view in the project.
     1. Click the sources icon on the left
     1. Click the ellipse next to V_MDLUC_JOINS and relink.
     1. Choose the data asset and click  Select.
     1. The report will refresh, and data will be displayed.
     1. Select the save icon to save the dashboard.
