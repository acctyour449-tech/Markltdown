from __future__ import annotations

from pathlib import Path
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from markitdown import MarkItDown

app = FastAPI(title="MarkItDown Web", version="0.1.0")
md = MarkItDown(enable_plugins=False)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
<!doctype html>
<html>
  <head><meta charset=\"utf-8\"><title>MarkItDown Web</title></head>
  <body style=\"font-family: sans-serif; max-width: 800px; margin: 2rem auto;\">
    <h1>MarkItDown Web</h1>
    <p>Upload a file and get Markdown output.</p>
    <form id=\"f\">
      <input type=\"file\" name=\"file\" required />
      <button type=\"submit\">Convert</button>
    </form>
    <p><small>Result:</small></p>
    <textarea id=\"out\" style=\"width:100%;height:360px;\"></textarea>
    <script>
      const form = document.getElementById('f');
      const out = document.getElementById('out');
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        out.value = 'Converting...';
        const fd = new FormData(form);
        const r = await fetch('/convert', { method: 'POST', body: fd });
        const j = await r.json();
        out.value = j.markdown || (j.error || 'Unknown error');
      });
    </script>
  </body>
</html>
"""


@app.post("/convert")
async def convert(file: UploadFile = File(...)) -> JSONResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp_path = Path(tmp.name)
        data = await file.read()
        tmp.write(data)

    try:
        result = md.convert(str(tmp_path))
        return JSONResponse({"filename": file.filename, "markdown": result.text_content})
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    finally:
        tmp_path.unlink(missing_ok=True)
