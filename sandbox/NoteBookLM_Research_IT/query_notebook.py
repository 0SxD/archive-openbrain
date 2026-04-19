"""
NotebookLM Research CLI — OpenBrain Sandbox
============================================
Uses ONLY Python stdlib (subprocess, json, argparse, sys, pathlib).
Delegates to the open-source `notebooklm-mcp-nodejs` binary via stdio MCP protocol.

Source: https://github.com/YassKhazzan/notebooklm-mcp-nodejs (MIT License)
No pip deps. No private/custom code. Approval needed before modifying MCP protocol.

Usage:
    python query_notebook.py --query "What is the architecture?"
    python query_notebook.py --notebook_id <id> --query "..." --output handoffs/out.md
"""
import sys
import json
import argparse
import subprocess
import pathlib


MCP_SERVER_CMD = ["npx", "-y", "notebooklm-mcp-nodejs"]


def build_mcp_request(method: str, params: dict, req_id: int = 1) -> str:
    """Build a JSON-RPC 2.0 request string for the MCP stdio protocol."""
    payload = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method,
        "params": params,
    }
    return json.dumps(payload)


def send_mcp_query(notebook_id: str | None, query: str) -> str:
    """
    Spawn the notebooklm-mcp-nodejs process, send an initialize + ask_question
    over stdio, and return the response text.

    This uses the open MCP JSON-RPC stdio protocol — no custom code, no 3rd party
    Python packages. All communication is via subprocess + JSON-RPC 2.0.
    """
    messages = []

    # 1) initialize
    init_req = build_mcp_request(
        "initialize",
        {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "openbrain-research-cli", "version": "0.1.0"},
        },
        req_id=1,
    )
    messages.append(init_req)

    # 2) ask_question tool call
    tool_args: dict = {"question": query}
    if notebook_id:
        tool_args["notebook_id"] = notebook_id

    tool_req = build_mcp_request(
        "tools/call",
        {"name": "ask_question", "arguments": tool_args},
        req_id=2,
    )
    messages.append(tool_req)

    # Concatenate with newlines — MCP stdio uses newline-delimited JSON
    stdin_payload = "\n".join(messages) + "\n"

    try:
        proc = subprocess.run(
            MCP_SERVER_CMD,
            input=stdin_payload,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        print("ERROR: 'npx' not found. Ensure Node.js is installed and in PATH.")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("ERROR: NotebookLM MCP server timed out after 120s.")
        sys.exit(1)

    # Parse responses — each line is a JSON-RPC message
    response_text = ""
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            # Find the tool result response (id=2)
            if msg.get("id") == 2 and "result" in msg:
                content = msg["result"].get("content", [])
                for block in content:
                    if block.get("type") == "text":
                        response_text += block["text"] + "\n"
        except json.JSONDecodeError:
            continue  # skip non-JSON lines (npm install output, etc.)

    if proc.returncode != 0 and not response_text:
        print(f"MCP server stderr:\n{proc.stderr}")
        sys.exit(1)

    return response_text.strip()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "OpenBrain NotebookLM Research CLI.\n"
            "Queries a NotebookLM notebook via the open-source notebooklm-mcp-nodejs server.\n"
            "Stdlib only — no pip deps."
        )
    )
    parser.add_argument(
        "--notebook_id", type=str, default=None,
        help="Notebook ID to query (optional if active notebook set in MCP config)."
    )
    parser.add_argument(
        "--query", type=str, required=True,
        help="Research query to send to NotebookLM."
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="File path to append results to (e.g. ../../handoffs/notebook_research_output.md)."
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON instead of plain text."
    )

    args = parser.parse_args()

    print(f"[OpenBrain Research CLI] Querying NotebookLM...")
    if args.notebook_id:
        print(f"  Notebook ID : {args.notebook_id}")
    print(f"  Query       : {args.query}")
    print()

    response = send_mcp_query(args.notebook_id, args.query)

    if not response:
        print("WARNING: Empty response received from NotebookLM.")
    else:
        print("=== NOTEBOOKLM RESPONSE ===\n")
        print(response)
        print("\n===========================\n")

    # Optionally persist to handoffs/ for Orchestrator consumption
    if args.output and response:
        out = pathlib.Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("a", encoding="utf-8") as f:
            f.write(
                f"\n## NotebookLM Research Entry\n"
                f"**Query:** {args.query}\n\n"
                f"**Response:**\n{response}\n\n---\n"
            )
        print(f"Results appended to: {args.output}")

    if args.json:
        print(json.dumps({"query": args.query, "response": response}))


if __name__ == "__main__":
    main()
