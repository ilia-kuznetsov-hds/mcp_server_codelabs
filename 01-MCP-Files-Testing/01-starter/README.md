### `mcp_server.py`

This script runs a local **Model Context Protocol (MCP) server** using `FastMCP`. It acts as a bridge between an AI agent (or any MCP-compatible client) and Google's Gemini and Imagen models, exposing a set of specialized image-generation tools. 

When connected, an agent can use this server to automatically generate and save images to a local `static/` directory. The tools exposed by the server include:

*   **`generate_holiday_scene`**: Creates a customized winter holiday landscape featuring a specific user interest.
*   **`generate_sweater_pattern`**: Designs a seamless, tileable "ugly holiday sweater" texture.
*   **`generate_wearing_sweater`**: Analyzes an uploaded photo (using Gemini 3.5 Flash) to extract physical features, then generates a custom 3D avatar wearing the newly created sweater pattern.
*   **`generate_final_photo`**: Composites the generated scene and avatar into a final, photorealistic image of a cozy fireplace mantle.
