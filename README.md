## Pasadena Environmental Justice Web Application ([website link](https://pasadena-environmental-justice.onrender.com/))

### Overview
We created this Web App to support the city of Pasadena's Environmental Justice Element. As input, residents can write their street address. The output will be their census tract, which we highlight. Further, residents can decide what metric they are interested in showing: CalEnviroScreen's overall score, the Pollution Burden score, or Population Characteristic scores. An interactive map displays their metric of choice. We show the indicators that comprise the relevant score for the individual's census tract in a table below the map. 

We hope that easy access to environmental justice metrics can help make residents more aware of their vulnerabilities to climate change while providing accessible data for citizens to advocate for themselves.

### Implementation
From a computational perspective, we use the coding package Python Dash for interactive app development, and Plotly for the graphs. The key inputs are:

(1) environmental justice data provided at a consistent geographic resolution

(2) a shape file specifying the boundaries 

(3) code linking one's address to the relevant geographic area

For (1) we use [CalEnviroScreen data](https://oehha.ca.gov/calenviroscreen/report/calenviroscreen-40) available at the Census Tract level. For (2) we use [TIGER/Line Shapefiles](https://www.census.gov/cgi-bin/geo/shapefiles/index.php) from 2018 for California at the Census Tract resolution. For (3) we use a [Python wrapper for the US Census Geocoder API](https://pypi.org/project/censusgeocode/).  

Code by Madeline Kitch. Project advised by Ani Garibyan and Anita Cerna. 
