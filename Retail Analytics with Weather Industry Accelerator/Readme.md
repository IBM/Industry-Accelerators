# Retail Analytics with Weather

Download the project `retail-analytics-with-weather-industry-accelerator.tar.gz` from the Releases `CPDv3.5.x` and import it into Cloud Pak for Data v3.5.x. You can also follow the instructions from [Community Page](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/retail-predictive-analytics-with-we) to download and import the project.


Easily visualize which retail locations, products, and weather conditions have higher predicted revenue
uplift in sales based on season to improve product inventory planning and improve marketing campaign
effectiveness.

## What’s Included?

- 4 csv files
    - **Historical Sales.csv** – sample mocked up retailer sales data from the IBM Cognos
       Analytics sample data known as Go Sales.
    - **Historical Weather.csv** – sample mocked up weather data for 38 postal codes in the US
       for 6 historical dates.
    - **All Retail and Weather Data.csv** – Historical Sales.csv and Historical Weather.csv were
       merged into one file. Each row represents a sale and what the weather was at the time
       the sale occurred.
    - **Retail and Weather Model Data.csv** – This csv is the result of pulling historical weather
       and sales into SPSS Modeler 18.1.x (or CP4D Modeler Flow) to generate a scored data
       source that includes the predicted $/% revenue uplift metric coming from a Random
       Forest model.
- 1 SPSS Modeler Stream 18.1.x (Get a trial to SPSS Modeler here.)
    o Retail Model.str
- 1 CP4D Dashboard
    o Retail Weather Dashboard.json

## How does it work?


1) Use the dashboard to visualize the correlation between top and bottom stores, products, and
weather condition by season leveraging historical sales and weather to help an analyst
determine where the most revenue uplift exists when doing marketing or inventory forecasting.
2) Examine the SPSS Model and CP4D Modeler Flow to see how you can ingest and develop code
free models (or bring your code if you like) and prepared data comprised of historical retail sales
and historical weather, in this case, to create a metric called Revenue Uplift representing the
potential upside.

### Learn About The Dashboard Showing Predicted $/% Revenue Uplift By Store, Product and Weather Condition. And, Historical Sales and Weather.

The dashboard answers the questions:

- Which products do we promote by store and weather condition for an upcoming marketing
    campaign or upcoming inventory planning session?
- Which products do we discontinue?
- Which products and stores are our top performers?
- What was the weather when a sale occurred?
- How does weather impact sales?

Use **Retail And Weather README.pdf** to set up and run the accelerator
