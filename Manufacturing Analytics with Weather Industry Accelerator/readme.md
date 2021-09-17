# Manufacturing Analytics With Weather

Download the project `manufacturing-analytics-with-weather-industry-accelerator.tar.gz` from the Releases `CPDv3.5.x` and import it into Cloud Pak for Data v3.5.x. You can also follow the instructions from [Community Page](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/manufacturing-analytics-with-weathe) to download and import the project.


Manufacturers need to quickly identify the reasons why there are high amounts of scrap rate to save
money and deliver quality product. This demonstration shows how weather was the key driver leading
to reducing scrap rate using statistical analysis and dashboards using Cloud Pak For Data (CP4D).

## What’s Included?

- 6 csv files
    - **_Prod_Data.csv_** – mocked up sample historical production data
    - **_WeatherHistory.csv_** – mocked up sample historical weather data
    - **_Scrap_Data.csv_** – mocked up sample historical scrap rate
    - **_All Weather and Manufacturing Data.csv_** – mocked up historical weather and
       production data to determine what the weather was at a particular point in time when
       scrap occurred.
    - **_Manufacturing Weather Forecasts.csv_** – mocked up weather forecast data
    - **_Scrap Rate By Time.csv_** – mocked up historical scrap rate over time
- SPSS Modeler Stream 18.1.
    - **_Scrap_Analysis_Daily_Official.str_**
- 1 Embedded Dashboard
    - **_Manufacturing_Analytics_With_Weather_Dashboard.json_**
- Recording on IBM Community page. **WATCH THIS FIRST!!!**

## How does it work?

The dashboard shows that unless one considers the use of weather and statistical analysis, it is difficult
to determine the reasons why large amounts of scrap rate exist.

The first tab shows that scrap is not a matter of how much you produce, nor is it really about time of
year although it does appear that the summer and spring months are times of the year where higher
scrap rate exists but we still don’t know why.


The second tab shows the high correlation of dewpoint to scrap rate and the third tab some other
correlation results. Back on the second tab, we see that the forecast calls for dewpoint above 10,
therefore, the schedule should be changed to make another product that day or re-allocate resources
where more production can be done.


If you have SPSS Modeler Desktop 18.1.x or greater, then, you’ll be able to see how the data was
combined and correlation analysis was built. If you purchase **Premium Cloud Pak For Data Modeler
Flows** then you’ll be able to build your SPSS Modeler streams in CP4D or upload your streams from
desktop to CP4D!

This was the initial SPSS Modeler stream developed using the desktop version (SPSS Modeler additional)

Here’s the model above imported into our project as a Modeler Flow in CP4D. (Premium)

Use the Readme pdf for detailed instructions to run the model in SPSS Modeler Desktop and as a CP4D Modeler
Flow. The output of the model (both are the same) is **All Weather and Manufacturing Data.csv** , the
merged data set that provides what the weather was for that day when scrap occurred. **Scrap Rate By
Time.csv** and **Manufacturing Weather Forecast.csv** are used in the dashboard to show the existing
problem with scrap rate , the upcoming 15 day forecast and how Dewpoint correlates the most to scrap
rate. The remaining csv files are used in the model as inputs to **All Weather and Manufacturing
Data.csv**. The SPSS Modeler/Modeler Flow also provides additional visualizations and correlation


