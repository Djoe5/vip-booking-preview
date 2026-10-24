import json
import requests
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

URL = "https://connect.composio.dev/mcp"
API_KEY = "ck_6yQCwO4FN5FqvTwDgyv8"

def send_mcp_request(method: str, params: dict = None, request_id: str = "1"):
    headers = {
        "x-consumer-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method
    }
    if params is not None:
        payload["params"] = params
        
    resp = requests.post(URL, json=payload, headers=headers, timeout=60)
    text = resp.text
    
    data_lines = []
    for line in text.splitlines():
        if line.startswith("data:"):
            data_lines.append(line[5:].strip())
            
    if data_lines:
        combined_json = "".join(data_lines)
        try:
            return json.loads(combined_json)
        except Exception:
            return {"raw_data": combined_json, "status_code": resp.status_code}
            
    try:
        return resp.json()
    except Exception:
        return {"raw": text, "status_code": resp.status_code}

def call_tool(tool_name: str, arguments: dict):
    res = send_mcp_request("tools/call", {
        "name": tool_name,
        "arguments": arguments
    })
    return res

if __name__ == "__main__":
    # Test checking active connections
    print("[*] Checking connections via COMPOSIO_MANAGE_CONNECTIONS...")
    conn_res = call_tool("COMPOSIO_MANAGE_CONNECTIONS", {})
    print(json.dumps(conn_res, indent=2))
