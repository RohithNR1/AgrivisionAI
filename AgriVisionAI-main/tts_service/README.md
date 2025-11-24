TTS microservice (Google Cloud Text-to-Speech)

This small Flask service exposes a `/synthesize` endpoint that accepts JSON `{ "text": "...", "lang": "en" }` and returns `{ "audio": "<base64 mp3>" }`.

Setup
1. Create a separate Python virtual environment for the service (recommended):

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Create a Google Cloud service account with `Text-to-Speech` permissions, download the JSON key, and set the environment variable:

   PowerShell:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS = 'C:\path\to\service-account.json'
   ```

   Or add it to a `.env` file in the `tts_service` folder:
   ```text
   GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json
   ```

3. Run the service:

   ```powershell
   python app.py
   ```

4. Configure your main backend to use the service by setting `TTS_SERVICE_URL` to the service URL, e.g. `http://localhost:6000`.

Security
- Keep the Google service account JSON secure and do not commit it to git.
- Run the TTS service behind an authenticated/protected endpoint in production.
