# Repository Agent Instructions

When running Python commands in this repository, prefer a local virtual environment over global Python.

Use the closest applicable virtual environment:

- From the repository root, use `.\.venv\Scripts\python.exe` when `.venv` exists.
- From `01-MCP-Files-Testing\01-starter`, use `.\.venv\Scripts\python.exe` from that directory when its local `.venv` exists.

Do not use bare `python` for project commands unless no local virtual environment exists or the user explicitly asks for global Python.

For MCP image-generation work in `01-MCP-Files-Testing\01-starter`, run commands from that directory so relative paths such as `static/generated_scene.png` resolve correctly.
