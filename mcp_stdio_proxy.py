# Written for fastmcp v3.0+ (2026 release)

"""
Written to bypass Smithery's broken web scanner by submitting my GitHub repository to Smithery using a local proxy script.

FastMCP includes a built-in proxy feature specifically for this scenario. 
It allows a client's Artificial Intelligence (AI) agent to connect locally via standard input/output (stdio), while the proxy 
securely bridges the connection to your remote Streamable HTTP endpoint.
"""

# Written for FastMCP v2.14 and v3.x (2025-2026 releases)
from fastmcp import FastMCP, Client

# Configure a client to connect to your remote Cloud Run server
backend_client = Client("https://noaa-mcp-free-bly45pyigq-uk.a.run.app/mcp")

# Create the proxy server instance from the client
proxy_server = FastMCP.from_client(backend_client, name="WeatherForensics Proxy")

if __name__ == "__main__":
    # Run the proxy server via stdio
    proxy_server.run(transport="stdio")