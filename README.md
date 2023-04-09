# Open Data for Public Good: Cycling in Dublin
## Final Year Project

Utilities to support [ArcGIS Experience web application](https://experience.arcgis.com/experience/bd56276abeef4f12ac38bdbffbbf45bc/). 

### Data Sources

Data folder contains python scripts used to parse and reshape data. Data sources detailed below.

| Name & Link | Description | Last Updated  |
| ----------- | ----------- | -------------- |
| [Current Cycle Infrastructure](https://data.gov.ie/dataset/greater-dublin-area-cycle-infrastructure-nta?package_type=dataset) | Current cycle lanes in the Greater Dublin Area | Dec. 2021 |
| [Planned Cycle Infrastructure](https://data.gov.ie/dataset/projected-cycle-lanes?package_type=dataset) | Planned (2021-2026) Cycle Routes in Greater Dublin Area | Oct. 2021 |
| [Cycle Parking](https://data.gov.ie/dataset/dcc_public_cycle_parking_stands?package_type=dataset)   | Parking Stands in Dublin City        | Sep. 2022 |
| [Cycle Counts](https://data.gov.ie/dataset/dublin-city-centre-cycle-counts) | Cycle traffic at specific locations in Dublin City | Updated Monthly, up to date as of Apr. 2023 |
| [Dublinbikes Usage](https://data.gov.ie/dataset/dublinbikes-api?package_type=dataset) | Dublinbike status, link to API for live data & quarterly historic data | Feb. 2022 |
| [Bleeperbike Usage](https://data.gov.ie/dataset/bleeperbike?package_type=dataset) | Various Bleeperbike data, link to API for live data & monthly historic data | Updated Monthly, up to date as of Apr. 2023 |

### Voting API

VotingApplication2 folder contains the code for express api hosted on firebase that counts votes. JSON file `finalyearproject-b132e-a22a1ab9e8e9.json` has been removed as it contained private key; in order to deploy this, the link to `https://finalyearproject-b132e-default-rtdb.firebaseio.com/` in `functions/index.js` would have to be replaced with your firebase database url and `finalyearproject-b132e-a22a1ab9e8e9.json` would have to be populated with the firebase access key.
