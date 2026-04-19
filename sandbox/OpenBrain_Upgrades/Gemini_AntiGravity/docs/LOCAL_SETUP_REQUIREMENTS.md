# AnythingLLM local configuration requirements

To power the internal zero-context queries for OpenBrain, the user must establish a local connection to the AnythingLLM workspace handling the Google Drive index.

## Mapping Google Drive Desktop
1. Download standard [Google Drive for Desktop]
2. Ensure the specific project configuration files or research PDFs are synced locally.
3. Open `AnythingLLM Desktop`.
4. Create a specific workspace matching the OpenBrain `project` flag (e.g. `nautilus_trader`).
5. Select "Local Documents" pointing to the synced Google Drive folders, and "Save to Workspace".

## Exposing the API
1. In AnythingLLM, navigate to **Settings > Developer API**.
2. Press `Generate New API Key`.
3. Set base URL to `http://localhost:3001/api/v1`
4. Use the `/workspace/{slug}/chat` schema in the `query_memory.py` hooks.
