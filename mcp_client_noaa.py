#
#   Written by:  Mark W Kiehl
#   http://mechatronicsolutionsllc.com/
#   http://www.savvysolutions.info/savvycodesolutions/


# Define the script version in terms of Semantic Versioning (SemVer)
# when Git or other versioning systems are not employed.
__version__ = "0.0.0"
# v0.0.0    Release 15 Mar 2026.
# v0.0.1    Revised run_mcp_checks() with retry loop to address GCP Cloud Run cold start delay.

"""

Model Context Protocol (MCP) Client Script for interaction with WeatherForensics MCP Server.

Website:  WeatherForensics.dev

GitHub:  https://github.com/markwkiehl/WeatherForensics-MCP


This script is a template for a client that interacts with an MCP Server that has been deployed to Google Cloud Run service.
Update BASE_URL in this script with the MCP Server URL for the Google Cloud Run service. 


MCP Server Tools:

Name: noaa_ncei_monthly_weather_for_location_date
Description: Returns NOAA NCEI monthly weather conditions for the specified location (latitude,longitude) and local_datetime_iso (in LST).

Name: noaa_ncei_daily_weather_for_location_date
Description: Returns NOAA NCEI daily weather conditions for the specified location (latitude,longitude) and local_datetime_iso (in LST).

Name: noaa_ncei_hourly_weather_for_location_date
Description: Returns NOAA NCEI hourly weather conditions for the specified location (latitude,longitude) and local date and time.

Name: noaa_nhc_tropical_cyclone_for_location_date
Description: Returns NOAA National Hurricane Center (NHC) tropical cyclone wind impact on a specified location (latitude,longitude) and local date.

Name: noaa_swdi_nx3tvs_tornado_impact_to_location
Description: Returns a report on any tornado impact to a specified location (latitude,longitude) and local date using data from NOAA NCEI SWDI API.

Name: noaa_swdi_supercell_storm_nx3mda_impact_to_location
Description: Returns a report on any supercell storm (nx3mda) impact to a specified location (latitude,longitude) and local date using data from NOAA NCEI SWDI API.

Name: noaa_swdi_nx3hail_impact_to_location
Description: Returns a report on any hail (nx3hail) impact to a specified location (latitude,longitude) and local date using data from NOAA NCEI SWDI API.

Name: noaa_swdi_nx3structure_impact_to_location
Description: Returns a report on any nx3structure impact to a specified location (latitude,longitude) and local date using data from NOAA NCEI SWDI API.

"""

from pathlib import Path
import asyncio
import sys
import os
import json
from typing import Dict, Any
from datetime import datetime
# pip install fastmcp
from fastmcp import Client

# ---------------------------------------------------------------------------
# Configure logging

# NOTE:
# Always use logger rather than print.  At scale, you can filter the logs by .info, .warning, and .error.
# By default, print() goes to stdout. Depending on the environment, the Python root logger might be sending logs to stderr. 
# You can set an Environment Variable in Cloud Run LOG_LEVEL=WARNING. Even if the code is full of logger.info() calls, they will be discarded instantly by the logger and never sent to Google Cloud
# While Cloud Run captures both print() and logger, they are often processed by different buffers.
# Google Cloud Logging looks for a field named severity to categorize logs (Blue for Info, Orange for Warning, Red for Error). The python-json-logger uses levelname by default.

# Install with: pip install python-json-logger
import logging

# Use a named logger
logger = logging.getLogger(Path(__file__).stem)
logger.setLevel(logging.INFO)

# Setup a standard Text Handler (Not JSON)
# This is what gcloud CLI "pretty prints" best.
if not logger.handlers:
    # Cloud Run captures everything on stdout
    logHandler = logging.StreamHandler(sys.stdout)
    
    # Use a clean, classic format: [LEVEL] Message
    # This format is highly readable in both the CLI and the Console.
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    logHandler.setFormatter(formatter)
    
    logger.addHandler(logHandler)

# Prevent double-logging
logger.propagate = False

logger.info(f"'{Path(__file__).stem}.py' v{__version__}") 
# logger.info(), logger.warning(), logger.error()


# Force UTF-8 encoding for Windows consoles to handle bullet points (•)
#sys.stdout.reconfigure(encoding='utf-8')

# ----------------------------------------------------------------------

DEBUG = False

# __file__ is /app/src/main.py
# .parent is /app/src
# .parent.parent is /app
PATH_BASE = Path(__file__).resolve().parent.parent
PATH_GCP = PATH_BASE / "gcp"
PATH_SRC = PATH_BASE / "src"
# Define the data directory: /app/data
PATH_DATA = PATH_BASE / "data"

# ----------------------------------------------------------------------
# Configure the WeatherForensics.dev MCP server URL

# The Forever Free Tier clients of the WeatherForensics.dev MCP server will use the following BASE_URL:
BASE_URL = "https://weatherforensics.dev/mcp/free"
API_KEY = None

# If you are a paid subscriber, expose the BASE_URL below and update the API_KEY with the one provided with your subscription:
#BASE_URL = "https://weatherforensics.dev/mcp/pro"
#API_KEY = "your-39-character-api-key-#############"

logger.info(f"BASE_URL: {BASE_URL}")
logger.info(f"API_KEY: {API_KEY}")

# ----------------------------------------------------------------------


def decode_nested_json(data):
    """Recursively parses stringified JSON inside dictionaries or lists.
    
    Usage:

        # Parse the outer layer
        initial_dict = json.loads(json_str)
        # Decode any hidden JSON strings inside
        fully_decoded_dict = decode_nested_json(initial_dict)
        # Print beautifully
        print(json.dumps(fully_decoded_dict, indent=4))

    
    """
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
            # If the decoded string is another dict or list, keep digging
            if isinstance(parsed, (dict, list)):
                return decode_nested_json(parsed)
            return parsed
        except (json.JSONDecodeError, TypeError):
            # It's just a normal string, leave it alone
            return data
    elif isinstance(data, dict):
        return {k: decode_nested_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [decode_nested_json(item) for item in data]
    else:
        return data


async def execute_tool_with_retry(tool_name: str, arguments: dict, max_retries: int = 3, verbose: bool=True):
    """
    Executes a single MCP tool with its own isolated connection and retry loop.
    (Retry loop needed for Forever Free tier with server cold starts).
    """
    base_delay = 2.0
    for attempt in range(max_retries):
        try:
            async with Client(BASE_URL) as client:
                print(f"\nCalling MCP tool '{tool_name}'...")
                result = await client.call_tool(tool_name, arguments)
                
                if result.is_error:
                    print(f"Tool Execution Error: {result.content}")
                elif result.content and len(result.content) > 0:
                    json_str = result.content[0].text
                    # Pass 'json_str' to an LLM.
                    # Pretty print 'json_str' for human consumption (parse it back into a Python dictionary and re-dump it with the indent)
                    try:
                        initial_dict = json.loads(json_str)
                        fully_decoded_dict = decode_nested_json(initial_dict)
                        if verbose: print(json.dumps(fully_decoded_dict, indent=4))
                        return json_str
                    except json.JSONDecodeError:
                        print(f"Server returned plain text instead of JSON:\n{json_str}")
                else:
                    raise Exception("Tool execution error")
                
                return None
                
        except Exception as e:
            logger.warning(f"Connection attempt {attempt + 1} failed for {tool_name}: {e}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logger.info(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                logger.error(f"--- Failed to execute {tool_name} after {max_retries} attempts ---")
                return None


async def run_mcp_checks():
    url = BASE_URL
    
    # Check MCP server status and get available tools.
    try:
        async with Client(url) as client:
            init_data = client.initialize_result

            print("\n--- Server Metadata ---")
            print(f"Connected to MCP Server '{init_data.serverInfo.name}' v{init_data.serverInfo.version} at: {url}")
            
            print(f"Instructions: {getattr(init_data, 'instructions', 'None provided')}")
            
            website = getattr(init_data, 'website_url', getattr(init_data.serverInfo, 'websiteUrl', 'None provided'))
            print(f"Website URL: {website}")

            print("\n--- Available Tools ---")
            tools = await client.list_tools()
            for tool in tools:
                print(f"Name: {tool.name}")
                print(f"Description: {tool.description}")
                print("-" * 20)
    except Exception as e:
        logger.error(f"Failed to fetch server metadata: {e}")
        return

    json_str = await execute_tool_with_retry("noaa_ncei_monthly_weather_for_location_date", {"latitude": 40.4407, "longitude": -76.12267, "local_datetime_iso": datetime(2025, 7, 10).isoformat()})
    if json_str is None: 
        raise Exception("ERROR")
    else:
        pass
        # Pass json_str to LLM

    json_str = await execute_tool_with_retry("noaa_ncei_daily_weather_for_location_date", {"latitude": 40.4407, "longitude": -76.12267, "local_datetime_iso": datetime(2025, 7, 10).isoformat()})
    
    json_str = await execute_tool_with_retry("noaa_ncei_hourly_weather_for_location_date", {"latitude": 40.4407, "longitude": -76.12267, "local_datetime_iso": datetime(2025, 7, 10, 13, 0).isoformat()})
    
    json_str = await execute_tool_with_retry("noaa_nhc_tropical_cyclone_for_location_date", {"latitude": 26.674, "longitude": -82.248, "local_datetime_iso": datetime(2022, 9, 28).isoformat()})
    
    json_str = await execute_tool_with_retry("noaa_swdi_nx3tvs_tornado_impact_to_location", {"latitude": 40.7037, "longitude": -89.4148, "local_datetime_iso": datetime(2013, 11, 17).isoformat()})

    json_str = await execute_tool_with_retry("noaa_swdi_supercell_storm_nx3mda_impact_to_location", {"latitude": 40.7037, "longitude": -89.4148, "local_datetime_iso": datetime(2013, 11, 17).isoformat()})

    json_str = await execute_tool_with_retry("noaa_swdi_nx3hail_impact_to_location", {"latitude": 40.7037, "longitude": -89.4148, "local_datetime_iso": datetime(2013, 11, 17).isoformat()})

    json_str = await execute_tool_with_retry("noaa_swdi_nx3structure_impact_to_location", {"latitude": 40.7037, "longitude": -89.4148, "local_datetime_iso": datetime(2013, 11, 17).isoformat()})



if __name__ == "__main__":
    try:
        asyncio.run(run_mcp_checks())
    except KeyboardInterrupt:
        print("\nClient stopped.")
    except Exception as e:
        print(f"ERROR: {e}")
