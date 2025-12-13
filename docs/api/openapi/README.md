# OpenAPI/Swagger Spezifikationen

Diese Dateien enthalten die OpenAPI 3.0 Spezifikationen für alle API-Router von Open WebUI.

## Verfügbare Router

| Router | Prefix | Beschreibung |
|--------|--------|--------------|
| chats | /api/v1/chats | Chat-Verwaltung |
| notes | /api/v1/notes | Notizen-System |
| models | /api/v1/models | KI-Modell-Verwaltung |
| knowledge | /api/v1/knowledge | Wissensdatenbank |
| prompts | /api/v1/prompts | Prompt-Templates |
| tools | /api/v1/tools | Tool-Integration |
| memories | /api/v1/memories | Speicher-System |
| folders | /api/v1/folders | Ordner-Verwaltung |
| groups | /api/v1/groups | Gruppen-Verwaltung |
| files | /api/v1/files | Datei-Verwaltung |
| functions | /api/v1/functions | Funktions-System |
| evaluations | /api/v1/evaluations | Evaluierungen |
| users | /api/v1/users | Benutzer-Verwaltung |
| auths | /api/v1/auths | Authentifizierung |
| configs | /api/v1/configs | Konfiguration |
| audio | /api/v1/audio | Audio-Verarbeitung |
| retrieval | /api/v1/retrieval | RAG-System |
| images | /api/v1/images | Bild-Generierung |
| tasks | /api/v1/tasks | Task-Verwaltung |
| pipelines | /api/v1/pipelines | Pipeline-System |
| channels | /api/v1/channels | Kanal-System |
| utils | /api/v1/utils | Hilfsfunktionen |
| ollama | /ollama | Ollama-Integration |
| openai | /openai | OpenAI-API |
| scim | /api/v1/scim/v2 | SCIM-Integration |

## Verwendung

### Mit Swagger UI

Öffne eine der JSON-Dateien in [Swagger Editor](https://editor.swagger.io/):

```bash
# Beispiel: chats API
https://editor.swagger.io/?url=https://raw.githubusercontent.com/oxomo030/open-webui/main/docs/api/openapi/chats.json
```

### Mit curl

```bash
# API-Spezifikation abrufen
curl https://raw.githubusercontent.com/oxomo030/open-webui/main/docs/api/openapi/chats.json
```

### Generierung aktualisieren

Die Spezifikationen können mit folgendem Befehl neu generiert werden:

```bash
python backend/scripts/generate_openapi_specs.py
```

## Format

- **JSON**: Maschinenlesbar, ideal für Tools
- **YAML**: Menschenlesbar, ideal für Dokumentation

## Live-API-Dokumentation

Die interaktive API-Dokumentation ist unter folgenden URLs verfügbar:

- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`
- OpenAPI JSON: `http://localhost:8080/openapi.json`
