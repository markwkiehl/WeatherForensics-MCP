# Written for fastmcp v3.0+ (2026 release)

"""
Written to bypass Smithery's broken web scanner by submitting my GitHub repository to Smithery using a local proxy script.

FastMCP includes a built-in proxy feature specifically for this scenario. 
It allows a client's Artificial Intelligence (AI) agent to connect locally via standard input/output (stdio), while the proxy 
securely bridges the connection to your remote Streamable HTTP endpoint.
"""

import os
from fastmcp import FastMCP

# Fetch the API Key from the environment
API_KEY = os.environ.get("WeatherForensics_API_KEY")

if API_KEY:
    url = f"https://weatherforensics.dev/mcp/pro?key={API_KEY}"
else:
    url = "https://weatherforensics.dev/mcp/free"

# Create a local proxy that bridges to your remote Streamable HTTP server
mcp = FastMCP.as_proxy(url)

if __name__ == "__main__":
    mcp.run(transport="stdio")