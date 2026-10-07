---
name: CreateCloudFlareURL
description: Start or reuse a Cloudflare Quick Tunnel for this Streamlit app and provide a verified public URL. Use when asked to create or share a temporary public link.
---

# Create a public Cloudflare Quick Tunnel URL

Expose this project's local Streamlit app through a temporary Cloudflare Quick Tunnel and return the verified public URL.

## Procedure

1. Identify the project root by locating `app.py`. Use the project's existing Streamlit environment and port when known; this app normally uses port `8501`.
2. Check the local app health endpoint at `http://127.0.0.1:8501/_stcore/health`. If it is not healthy, start Streamlit from the project root using its existing environment. Before stopping or replacing any process, verify its command line and project path; never use broad process-name termination commands.
3. Check for an existing `cloudflared` executable (`command -v cloudflared` and the previously used `/tmp/cloudflared` location). If unavailable, install it only from Cloudflare's official distribution or package manager. Do not download or execute binaries from untrusted sources.
4. Reuse an already-running Quick Tunnel for this app if its public hostname can be identified and its connection is healthy. Avoid starting duplicate tunnels. If a new tunnel is needed, run it detached so it remains available after the command returns:

   ```sh
   cloudflared tunnel --no-autoupdate --protocol http2 --url http://127.0.0.1:8501
   ```

   If using the locally installed binary, invoke its verified absolute path instead. HTTP/2 is preferred because this project's earlier QUIC tunnel experienced intermittent network disconnects.
5. Read the tunnel's startup output and capture the exact `https://<name>.trycloudflare.com` hostname it generated. Keep the tunnel process running.
6. Verify the generated URL externally with an HTTP request and confirm it serves the app (HTTP success); also check its Streamlit health endpoint where reachable. If verification fails, inspect the exact tunnel and app processes/logs, resolve the cause, and retry rather than reporting an unverified URL.
7. Give the user the URL and clearly state that it is a temporary, non-permanent Quick Tunnel address. It is only usable while the local computer, Streamlit app, and tunnel process remain online; restarting the tunnel can create a different URL, and Quick Tunnels have no uptime guarantee.
8. Warn that anyone with the URL can access the app. Visitors may consume the configured Gemini quota and may trigger email delivery if they use the email feature. Do not expose or print `.env` values or credentials. Do not add credentials, enable access control, or publish code unless explicitly requested.
