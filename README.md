# MCP Workshop Notes

My implementation of [Building Personalized Agents with ADK, MCP, and Memory Bank](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=en#0)

## Part 00: Google Cloud Project Setup

Part 00 is the Google Cloud setup needed for the workshop implementation, including project configuration and API access for Gemini/Imagen.

The [MCP server](https://developers.openai.com/codex/mcp) can also be used locally from Codex by configuring the shared CLI/IDE config file at `.../.codex/config.toml`:

```toml
[mcp_servers.holidays]
command = "uv"
args = [
  "run",
  "--directory",
  "C:\\Users\\user\\Documents\\mcp-server\\01-MCP-Files-Testing\\01-starter",
  "python",
  ".\\mcp_server.py"
]
```


## Part 01: MCP Files Testing

In part 01, we create an MCP server to expose local Python functions to the AI.
The local FastMCP server in `01-MCP-Files-Testing/01-starter/mcp_server.py` exposes holiday image-generation tools:

- `generate_holiday_scene`
- `generate_sweater_pattern`
- `generate_wearing_sweater`
- `generate_final_photo`

Dependencies are managed with `uv` using `pyproject.toml` and `uv.lock`. From `01-MCP-Files-Testing/01-starter`, install dependencies with:

```powershell
uv sync
```

Run the MCP server locally with:

```powershell
uv run python .\mcp_server.py
```

We tested the image-generation flow by calling the local tool implementations from Python. 

<img src="01-MCP-Files-Testing/01-starter/static/generated_selfie.png" alt="Generated Doom Guy selfie" width="400">


