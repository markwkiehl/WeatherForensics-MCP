# WeatherForensics MCP

**Past Weather. Present Impact. AI-Ready Intelligence**

WeatherForensics is a Data as a Service (DaaS) that provides comprehensive historical weather data, including standard conditions and severe weather events, relative to a specified target location and timestamp. While most services focus on the "what," our proprietary engine calculates the localized impact of historical weather events—ranging from localized tornadoes to regional hurricanes—at a specific coordinate and datetime.

This repository contains information, documentation, and a sample Python client script (`mcp_client_noaa.py`) to interact with the WeatherForensics Model Context Protocol (MCP) server.  

See also the WeatherForensics website at [WeatherForensics.dev](https://weatherforensics.dev/).


---

## 🚀 Features

- **Developer-Ready Formats:** Responses from all endpoints are delivered as clean JavaScript Object Notation (JSON) data structures, optimized for immediate human and Artificial Intelligence (AI) agent consumption.
- **Transparent Data Provenance:** Every JSON payload explicitly identifies the data content category and its authoritative source dataset.
- **Intelligent Dataset Routing:** The API automatically selects the most appropriate dataset—either the legacy National Oceanic and Atmospheric Administration (NOAA) National Centers for Environmental Information (NCEI) Integrated Surface Database (ISD) hourly dataset or the modern Global Historical Climatology Network hourly (GHCNh) dataset—based on your requested target year.
- **Precision Spatial Querying:** For standard and severe weather requests, the engine automatically identifies the closest active station to your target coordinates that contains the most robust dataset.
- **Advanced Cyclone Impact Analysis:** For tropical cyclone tracking, the API calculates the minimum distance between the storm centroid and your target, evaluating the maximum wind experienced utilizing standard 34, 50, and 64-knot wind radii models.
- **Cross-Platform Compatibility:** Fully supported across Linux, macOS, and Windows environments.

---

## 📊 Data Scope & Available Endpoints

The MCP provides access to standard meteorological data and severe weather tracking via these MCP endpoints.

**Standard Weather Endpoints:** (Sourced from NOAA NCEI)
- `noaa_ncei_hourly_weather_for_location_date`
- `noaa_ncei_daily_weather_for_location_date`
- `noaa_ncei_monthly_weather_for_location_date`

**Severe Weather Endpoints:** (Sourced from NOAA NCEI Severe Weather Data Inventory (SWDI))
- `noaa_swdi_nx3tvs_tornado_impact_to_location`
- `noaa_swdi_supercell_storm_nx3mda_impact_to_location`
- `noaa_swdi_nx3hail_impact_to_location`
- `noaa_swdi_nx3structure_impact_to_location`

**Tropical Cyclone Endpoints:** (Derived from NOAA National Hurricane Center (NHC) HURDAT2)
- `noaa_nhc_tropical_cyclone_for_location_date`

---

## ⚙️ Installation & Configuration

### Prerequisites
The included sample script `mcp_client_noaa.py` requires Python 3.7+ and the following packages:
```bash
pip install fastmcp python-json-logger
```

### Setup
Clone this repository and navigate to the directory containing `mcp_client_noaa.py`.  
Configure your service tier by setting the WeatherForensics_API_KEY environment variable. The script automatically determines the correct Uniform Resource Locator (URL) based on this key.  
- **Forever Free Tier**: Do not set the environment variable. The script will use the default free endpoint.
- **Pro Tier**: Set the environment variable to your 39-character Application Programming Interface (API) key.
- **Enterprise Tier**: Set the environment variable to your 39-character API key (and update the gateway URL (BASE_URL) directly in the script).

### Usage
If you are a Pro or Enterprise tier subscriber, set an environment variable "WeatherForensics_API_KEY" to your API Key.  Not required for the Forever Free tier.
- Linux/macOS: export WeatherForensics_API_KEY="your-key-here"
- Windows (Command Prompt): set WeatherForensics_API_KEY="your-key-here"
- Windows (PowerShell): $env:WeatherForensics_API_KEY="your-key-here"

Execute the client script from your terminal:
```bash
python mcp_client_noaa.py
```

---
## 🤖 AI Agent Integration (Claude Desktop)

To use WeatherForensics MCP directly within Claude Desktop, add the following to your `claude_desktop_config.json`:

{
  "mcpServers": {
    "weatherforensics": {
      "command": "python",
      "args": [
        "/absolute/path/to/WeatherForensics-MCP/mcp_client_noaa.py"
      ],
      "env": {
        "WeatherForensics_API_KEY": "" 
      }
    }
  }
}

Leave `WeatherForensics_API_KEY` blank to use the Forever Free subscription tier.

---

## 📈 Service Tiers & Rate Limits

WeatherForensics is deployed on Google Cloud Run and offers predictable pricing to power your applications. All tiers include access to both the Model Context Protocol (MCP) Server and the Representational State Transfer (REST) Application Programming Interface (API).

| Tier | Price | Rate Limits & Quotas | Infrastructure |
| :--- | :--- | :--- | :--- |
| **Forever Free** | $0/mo | 10 Requests Per Minute (RPM), 500 Req/Day, 1 Concurrent | Shared Community Resource |
| **Pro** | $29/mo | 60 RPM, 10,000 Req/Day, 5 Concurrent | Dedicated Endpoints, Zero Cold Starts |
| **Enterprise** | $279/mo | 500+ RPM, Unlimited Concurrency | Dedicated Instance, Custom Bulk Payloads |

*Note: Free tier users do not need an API key. Excessive volume on the free tier may result in Internet Protocol (IP) throttling or severe latency. Exceeding your tier's rate limits will return a Hypertext Transfer Protocol (HTTP) `429 Too Many Requests` status code.*

---

## 💻 Example Request Responses

All endpoints require target coordinates (latitude,longitude) and local datetime in ISO format.

> Note on Timezones: While all endpoints require your target time as a local datetime (local_datetime_iso), the returned metadata reflects the standard of the underlying dataset. Standard weather responses will echo your input as datetime_local, whereas Severe Weather Data Inventory (SWDI) responses convert and return your target time as datetime_utc to align with radar observation standards.

### Monthly Weather
```
{
    "result": {
        "event_type": "monthly_weather",
        "data_source": "NOAA_NCEI_Search_&_Data_Service_API",
        "target_metadata": {
            "latitude": 40.4407,
            "longitude": -76.12267,
            "datetime_local": "2025-07-10T00:00:00"
        },
        "station_metadata": {
            "distance_from_target_mi": 9.8,
            "STATION": "USW00014712",
            "LATITUDE": 40.37342,
            "LONGITUDE": -75.95924,
            "ELEVATION_ft": 331.9
        },
        "data": [
            {
                "measurement": "Precipitation",
                "value": "6.69",
                "unit": "\"",
                "category": "Precipitation"
            },
            {
                "measurement": "Snowfall",
                "value": "0.0",
                "unit": "\"",
                "category": "Precipitation"
            },
            {
                "measurement": "Maximum temperature",
                "value": "89.2",
                "unit": "\u00b0F",
                "category": "Temperature"
            },
            {
                "measurement": "Average temperature",
                "value": "80.0",
                "unit": "\u00b0F",
                "category": "Temperature"
            },
            {
                "measurement": "Minimum temperature",
                "value": "70.7",
                "unit": "\u00b0F",
                "category": "Temperature"
            },
            {
                "measurement": "Direction of fastest 2-minute wind",
                "value": "300",
                "unit": "\u00b0",
                "category": "Wind"
            },
            {
                "measurement": "Direction of fastest 5-second wind",
                "value": "300",
                "unit": "\u00b0",
                "category": "Wind"
            },
            {
                "measurement": "Fastest 2-minute wind speed",
                "value": "49.0",
                "unit": "mph",
                "category": "Wind"
            },
            {
                "measurement": "Fastest 5-second wind speed",
                "value": "63",
                "unit": "mph",
                "category": "Wind"
            },
            {
                "measurement": "Average daily wind speed",
                "value": "4.5",
                "unit": "mph",
                "category": "Wind"
            }
        ],
        "acknowledgments_and_attributions": {
            "required_attribution": "Weather data derived from NOAA NCEI and NHC. This is not an official NOAA product.",
            "data_sources": [
                "NOAA National Centers for Environmental Information (NCEI)",
                "NOAA National Hurricane Center (NHC) HURDAT2 Database"
            ],
            "software_acknowledgments": "Hurricane parsing utilizes hurdat2parser (MIT License).",
            "usage_policy": "https://weatherforensics.dev/tos.html",
            "attributions_details": "https://weatherforensics.dev/attributions.html"
        }
    },
    "message": "Monthly weather for 2025-07-10 00:00:00 at 40.4407,-76.12267"
}
```

### Daily Weather
```
{
    "result": {
        "event_type": "daily_weather",
        "data_source": "NOAA_NCEI_Search_&_Data_Service_API",
        "target_metadata": {
            "latitude": 40.4407,
            "longitude": -76.12267,
            "datetime_local": "2025-07-10T00:00:00"
        },
        "station_metadata": {
            "distance_from_target_mi": 9.8,
            "STATION": "USW00014712",
            "DATE": "2025-07-10",
            "LATITUDE": 40.37342,
            "LONGITUDE": -75.95924,
            "ELEVATION_ft": 331.9
        },
        "data": [
            {
                "measurement": "Snowfall",
                "value": "0.0",
                "unit": "\"",
                "category": "Precipitation"
            },
            {
                "measurement": "Precipitation",
                "value": "0.00",
                "unit": "\"",
                "category": "Precipitation"
            },
            {
                "measurement": "Snow depth",
                "value": "0.0",
                "unit": "\"",
                "category": "Precipitation"
            },
            {
                "measurement": "Maximum temperature",
                "value": "88",
                "unit": "\u00b0F",
                "category": "Temperature"
            },
            {
                "measurement": "Average temperature",
                "value": "77",
                "unit": "\u00b0F",
                "category": "Temperature"
            },
            {
                "measurement": "Minimum temperature",
                "value": "71",
                "unit": "\u00b0F",
                "category": "Temperature"
            },
            {
                "measurement": "Fog, ice fog, or freezing fog",
                "value": "    1",
                "unit": NaN,
                "category": "Weather Type"
            },
            {
                "measurement": "Fastest 2-minute wind speed",
                "value": "8.9",
                "unit": "mph",
                "category": "Wind"
            },
            {
                "measurement": "Fastest 5-second wind speed",
                "value": "12.1",
                "unit": "mph",
                "category": "Wind"
            },
            {
                "measurement": "Direction of fastest 2-minute wind",
                "value": "  160",
                "unit": "\u00b0",
                "category": "Wind"
            },
            {
                "measurement": "Average daily wind speed",
                "value": "2.91",
                "unit": "mph",
                "category": "Wind"
            },
            {
                "measurement": "Direction of fastest 5-second wind",
                "value": "  150",
                "unit": "\u00b0",
                "category": "Wind"
            }
        ],
        "acknowledgments_and_attributions": {
            "required_attribution": "Weather data derived from NOAA NCEI and NHC. This is not an official NOAA product.",
            "data_sources": [
                "NOAA National Centers for Environmental Information (NCEI)",
                "NOAA National Hurricane Center (NHC) HURDAT2 Database"
            ],
            "software_acknowledgments": "Hurricane parsing utilizes hurdat2parser (MIT License).",
            "usage_policy": "https://weatherforensics.dev/tos.html",
            "attributions_details": "https://weatherforensics.dev/attributions.html"
        }
    },
    "message": "Daily weather for 2025-07-10 00:00:00 at 40.4407,-76.12267"
}
```

### Hourly Weather
```
{
    "result": {
        "event_type": "hourly_weather",
        "data_source": "NOAA_NCEI_Search_&_Data_Service_API",
        "target_metadata": {
            "latitude": 40.4407,
            "longitude": -76.12267,
            "datetime_local": "2025-07-10T13:00:00"
        },
        "station_metadata": {
            "distance_from_target_mi": 9.8,
            "STATION_NAME": "READING RGNL AP",
            "remarks_Source_Station_ID": "725103-14712",
            "remarks": "MET10307/10/25 09:54:02 METAR KRDG 101454Z 19004KT 10SM CLR 26/20 A2999 RMK AO2 SLP158 T02560200 51013 $ (JR)",
            "timestamp_utc": "2025-07-10T09:54:02+00:00",
            "STATION": "USW00014712",
            "LATITUDE": 40.3733,
            "LONGITUDE": -75.9592,
            "ELEVATION_ft": 332.0
        },
        "data": [
            {
                "measurement": "precipitation",
                "value": 0.0,
                "unit": "mm",
                "category": "Moisture"
            },
            {
                "measurement": "relative_humidity",
                "value": 71.0,
                "unit": "%",
                "category": "Moisture"
            },
            {
                "measurement": "station_level_pressure",
                "value": 1002.6,
                "unit": "hPa",
                "category": "Pressure"
            },
            {
                "measurement": "pressure_3hr_change",
                "value": 1.3,
                "unit": "hPa",
                "category": "Pressure"
            },
            {
                "measurement": "altimeter",
                "value": 1015.6,
                "unit": "hPa",
                "category": "Pressure"
            },
            {
                "measurement": "sea_level_pressure",
                "value": 1015.8,
                "unit": "hPa",
                "category": "Pressure"
            },
            {
                "measurement": "dew_point_temperature",
                "value": 20.0,
                "unit": "\u00b0C",
                "category": "Temperature"
            },
            {
                "measurement": "temperature",
                "value": 25.6,
                "unit": "\u00b0C",
                "category": "Temperature"
            },
            {
                "measurement": "wet_bulb_temperature",
                "value": 21.9,
                "unit": "\u00b0C",
                "category": "Temperature"
            },
            {
                "measurement": "visibility",
                "value": 16.093,
                "unit": "km",
                "category": "Visibility"
            },
            {
                "measurement": "wind_speed",
                "value": 2.1,
                "unit": "m/s",
                "category": "Wind"
            },
            {
                "measurement": "wind_direction",
                "value": 190.0,
                "unit": "\u00b0",
                "category": "Wind"
            }
        ],
        "acknowledgments_and_attributions": {
            "required_attribution": "Weather data derived from NOAA NCEI and NHC. This is not an official NOAA product.",
            "data_sources": [
                "NOAA National Centers for Environmental Information (NCEI)",
                "NOAA National Hurricane Center (NHC) HURDAT2 Database"
            ],
            "software_acknowledgments": "Hurricane parsing utilizes hurdat2parser (MIT License).",
            "usage_policy": "https://weatherforensics.dev/tos.html",
            "attributions_details": "https://weatherforensics.dev/attributions.html"
        }
    },
    "message": "Hourly weather for 2025-07-10 13:00:00 at 40.4407,-76.12267"
}
```

### Tropical Cyclone Impact
```
{
    "result": {
        "event_type": "tropical_cyclone",
        "data_source": "NOAA_NHC_HURDAT2_Database",
        "target_metadata": {
            "latitude": 26.674,
            "longitude": -82.248,
            "datetime_local": "2022-09-28T04:00:00+00:00"
        },
        "storm_metadata": {
            "storm_season": 2022,
            "count_of_tropical_cyclones": 35
        },
        "cyclone_report": {
            "STORM_NAME": "IAN (AL092022)",
            "OBSERVATION_TIMESTAMP_LOCAL": "28 Sep 2022 14:00:00",
            "DISTANCE_FROM_STORM_TRACK_CENTROID_TO_TARGET_mi": 3.5,
            "MAX_SUSTAINED_WIND_SPEED_mph": 155.4,
            "IMPACT_ANALYSIS": "CRITICAL wind impact measured"
        },
        "acknowledgments_and_attributions": {
            "required_attribution": "Weather data derived from NOAA NCEI and NHC. This is not an official NOAA product.",
            "data_sources": [
                "NOAA National Centers for Environmental Information (NCEI)",
                "NOAA National Hurricane Center (NHC) HURDAT2 Database"
            ],
            "software_acknowledgments": "Hurricane parsing utilizes hurdat2parser (MIT License).",
            "usage_policy": "https://weatherforensics.dev/tos.html",
            "attributions_details": "https://weatherforensics.dev/attributions.html"
        }
    },
    "message": "Weather conditions from NOAA NHC for tropical cyclone impact at 26.674,-82.248 in 2022:\n"
}
```

### Tornado Impact Analysis (nx3tvs)
```
{
    "result": {
        "event_type": "tornado_vortex_signature",
        "data_source": "NOAA_NCEI_SWDI_NX3TVS",
        "target_metadata": {
            "latitude": 40.7037,
            "longitude": -89.4148,
            "datetime_utc": "2013-11-17T06:00:00Z"
        },
        "impact_analysis": {
            "target_cpa_miles": 1.66,
            "impact_category": "Direct Hit / Core Tornado Impact",
            "threat_level": "Extreme",
            "description": "Target is within 2 miles of the TVS track. High probability of tornadic impact.",
            "required_agent_actions": [
                "Overlay target with active NWS GIS warning polygons."
            ],
            "rankine_estimated_wind_kts": 23.5
        },
        "cpa_radar_metrics": {
            "time_utc": "2013-11-17T17:03:14Z",
            "time_to_cpa_minutes": 663.2,
            "storm_cell_id": "R2",
            "wsr_id": "KILX",
            "maximum_delta_velocity_kts": 146.0,
            "maximum_shear": 69.0,
            "azimuth_deg": 348.0,
            "range_nm": 33.0
        },
        "acknowledgments_and_attributions": {
            "required_attribution": "Weather data derived from NOAA NCEI and NHC. This is not an official NOAA product.",
            "data_sources": [
                "NOAA National Centers for Environmental Information (NCEI)",
                "NOAA National Hurricane Center (NHC) HURDAT2 Database"
            ],
            "software_acknowledgments": "Hurricane parsing utilizes hurdat2parser (MIT License).",
            "usage_policy": "https://weatherforensics.dev/tos.html",
            "attributions_details": "https://weatherforensics.dev/attributions.html"
        }
    },
    "message": "Weather conditions from NOAA NCEI SWDI dataset 'nx3tvs' at 40.7037,-89.4148 on 17 Nov 2013"
}
```

### Supercell Storm (nx3mda)
```
{
    "result": {
        "event_type": "supercell_mesocyclone",
        "data_source": "NOAA_NCEI_SWDI_NX3MDA",
        "target_metadata": {
            "latitude": 40.7037,
            "longitude": -89.4148,
            "datetime_utc": "2013-11-17T06:00:00Z"
        },
        "impact_analysis": {
            "target_cpa_miles": 1.11,
            "impact_category": "Direct Hit / Core Impact",
            "threat_level": "Extreme",
            "description": "Target was within 3 miles of the mesocyclone track. High probability of tornadoes or extreme winds.",
            "dual_pol_warning": null
        },
        "cpa_radar_metrics": {
            "time_utc": "2013-11-17T17:04:52Z",
            "time_to_cpa_minutes": 664.9,
            "storm_cell_id": 499,
            "distance_from_radar_core_mi": 3.95,
            "tornado_vortex_signature": "N",
            "low_level_delta_velocity_kts": 106,
            "strength_rank": 9.0,
            "tornadic_potential": "High"
        },
        "acknowledgments_and_attributions": {
            "required_attribution": "Weather data derived from NOAA NCEI and NHC. This is not an official NOAA product.",
            "data_sources": [
                "NOAA National Centers for Environmental Information (NCEI)",
                "NOAA National Hurricane Center (NHC) HURDAT2 Database"
            ],
            "software_acknowledgments": "Hurricane parsing utilizes hurdat2parser (MIT License).",
            "usage_policy": "https://weatherforensics.dev/tos.html",
            "attributions_details": "https://weatherforensics.dev/attributions.html"
        }
    },
    "message": "Weather conditions from NOAA NCEI SWDI dataset 'nx3mda' at 40.7037,-89.4148 on 17 Nov 2013"
}
```

### Hail Storm (nx3hail)
```
{
    "result": {
        "event_type": "hail_storm",
        "data_source": "NOAA_NCEI_SWDI_NX3HAIL",
        "target_metadata": {
            "latitude": 40.7037,
            "longitude": -89.4148,
            "datetime_utc": "2013-11-17T06:00:00Z"
        },
        "impact_analysis": {
            "target_cpa_miles": 2.3,
            "impact_category": "Near Miss / Hail Impact",
            "threat_level": "High",
            "description": "Target was within 1 to 5 miles of the hail core. Severe probability: 50.0%.",
            "dual_pol_warning": null
        },
        "cpa_radar_metrics": {
            "time_utc": "2013-11-17T17:00:58Z",
            "time_to_cpa_minutes": 661.0,
            "storm_cell_id": "L8",
            "wsr_id": "KLOT",
            "distance_from_radar_core_mi": 3.34,
            "hail_probability_pct": 100.0,
            "severe_probability_pct": 50.0,
            "max_hail_size_in": 1.25
        },
        "acknowledgments_and_attributions": {
            "required_attribution": "Weather data derived from NOAA NCEI and NHC. This is not an official NOAA product.",
            "data_sources": [
                "NOAA National Centers for Environmental Information (NCEI)",
                "NOAA National Hurricane Center (NHC) HURDAT2 Database"
            ],
            "software_acknowledgments": "Hurricane parsing utilizes hurdat2parser (MIT License).",
            "usage_policy": "https://weatherforensics.dev/tos.html",
            "attributions_details": "https://weatherforensics.dev/attributions.html"
        }
    },
    "message": "Weather conditions from NOAA NCEI SWDI dataset 'nx3hail' at 40.7037,-89.4148 on 17 Nov 2013"
}

```

### Storm Cell Structure (nx3structure)
```
{
    "result": {
        "event_type": "storm_cell_structure",
        "data_source": "NOAA_NCEI_SWDI_NX3STRUCTURE",
        "target_metadata": {
            "latitude": 40.7037,
            "longitude": -89.4148,
            "datetime_utc": "2013-11-17T06:00:00Z"
        },
        "impact_analysis": {
            "target_cpa_miles": 0.38,
            "impact_category": "Direct Hit / Core Impact",
            "description": "Target was within 3 miles of the storm core track. High probability of heavy precipitation, large hail, or severe wind."
        },
        "cpa_radar_metrics": {
            "time_utc": "2013-11-17T16:43:46Z",
            "time_to_cpa_minutes": 643.8,
            "storm_cell_id": "Z3",
            "wsr_id": "KMKX",
            "distance_from_radar_core_mi": 55.57,
            "max_reflectivity_dbz": 53,
            "vertically_integrated_liquid_kg_m2": 15
        },
        "acknowledgments_and_attributions": {
            "required_attribution": "Weather data derived from NOAA NCEI and NHC. This is not an official NOAA product.",
            "data_sources": [
                "NOAA National Centers for Environmental Information (NCEI)",
                "NOAA National Hurricane Center (NHC) HURDAT2 Database"
            ],
            "software_acknowledgments": "Hurricane parsing utilizes hurdat2parser (MIT License).",
            "usage_policy": "https://weatherforensics.dev/tos.html",
            "attributions_details": "https://weatherforensics.dev/attributions.html"
        }
    },
    "message": "Weather conditions from NOAA NCEI SWDI dataset 'nx3structure' at 40.7037,-89.4148 on 17 Nov 2013"
}
```

---

## 🛑 Error Handling & HTTP Status Codes

When integrating the API, you may encounter the following standard HTTP status codes:

- **`200 OK`**: The request was successful and the JavaScript Object Notation (JSON) payload is returned.
- **`400 Bad Request`**: The request payload is malformed, missing required fields (`latitude`, `longitude`, `local_datetime_iso`), or contains invalid coordinates/dates.
- **`401 Unauthorized`**: An invalid or missing API Key was provided for a Pro/Enterprise tier endpoint.
- **`429 Too Many Requests`**: You have exceeded the rate limits for your specific subscription tier. Back off and retry later.
- **`500 Internal Server Error`**: An unexpected error occurred on the server (e.g., upstream National Oceanic and Atmospheric Administration (NOAA) API timeouts).

---

## ⚖️ Licensing, Attribution & Terms

When integrating the WeatherForensics Application Programming Interface (API) or Model Context Protocol (MCP) into your applications, you must comply with the following usage and attribution requirements.

*Note: The client scripts in this repository are open-sourced under the [Massachusetts Institute of Technology (MIT) License](LICENSE). Access to the WeatherForensics API and its data is strictly subject to our full [Terms of Service](https://weatherforensics.dev/tos.html).*

### 1. Usage Rights & Restrictions

- **Allowed:** You may use the data for internal analysis, commercial applications, and providing ground-truth context to Artificial Intelligence (AI) models.
- **Restricted:** You may not systematically scrape, bulk-download, resell, or redistribute the raw API/MCP responses as a competing standalone weather data service.

### 2. Required End-User Attribution

To comply with National Oceanic and Atmospheric Administration (NOAA) guidelines, any public-facing application or AI agent interface displaying our data must include the following attribution visibly to the end-user:

> "Weather data derived from NOAA National Centers for Environmental Information (NCEI) and the National Hurricane Center (NHC). This application and its data are not official NOAA products and do not represent any agency determination, view, or policy."

### 3. Acknowledgments & Disclaimers

**Data Sources:** Tropical cyclone impact analysis is derived from the HURDAT2 database *(Landsea, C. W., and J. L. Franklin, 2013)*. Our backend utilizes the `hurdat2parser` library (Copyright © 2019-2021 Kyle S. Gentry), licensed under the MIT License.

**Disclaimer:** The service is provided on an "AS IS" and "AS AVAILABLE" basis. Data should not be used as the sole basis for life-safety decisions, financial trading, or legal determinations.

---


Copyright © 2026 [Mechatronic Solutions LLC](http://mechatronicsolutionsllc.com/). All Rights Reserved. For full terms, visit [WeatherForensics.dev](https://weatherforensics.dev/).

