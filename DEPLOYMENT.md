# Deployment

This repository can be deployed as a containerized CLI or as a long-running MCP service.

## Option 1: Deploy `markitdown-mcp` with Docker

1. Build the MCP image:

```bash
docker build -f markitdown-mcp/Dockerfile -t markitdown-mcp:latest .
```

2. Run the MCP service:

```bash
docker run --rm -p 8000:8000 markitdown-mcp:latest
```

3. Configure your MCP client to connect to `http://<host>:8000`.

## Option 2: Deploy the top-level CLI image

1. Build:

```bash
docker build -t markitdown:latest .
```

2. Run for one-shot conversions:

```bash
docker run --rm -i markitdown:latest < input.pdf > output.md
```


## Option 3: Deploy a minimal web app (upload file in browser)

1. Build the web app image:

```bash
docker build -f webapp/Dockerfile -t markitdown-web:latest .
```

2. Run it:

```bash
docker run --rm -p 8080:8080 markitdown-web:latest
```

3. Open `http://localhost:8080` in your browser and upload a file.


## Option 4: Deploy to Vercel (no terminal required)

1. Push this repo to GitHub.
2. In Vercel dashboard, click **Add New...** -> **Project** and import the repo.
3. Keep defaults and deploy. The repository includes `vercel.json` and `api/index.py` so requests are routed to the FastAPI app.
4. Open the generated Vercel URL in your browser.

Files used by this setup:
- `vercel.json`
- `api/index.py`
- `requirements.txt`

## Production notes

- Pin image tags to immutable digests in production.
- Place the service behind HTTPS at the ingress/load balancer layer.
- Limit outbound network access if processing untrusted files.
- For OCR/LLM features, inject API credentials via environment variables at runtime.
