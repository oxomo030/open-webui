# Combined OpenAPI Specification

Diese Datei enthält die kombinierte OpenAPI 3.0 Spezifikation für alle API-Router von Open WebUI.

## Dateien

- **openapi.json**: Kombinierte Spezifikation im JSON-Format
- **openapi.yaml**: Kombinierte Spezifikation im YAML-Format

## Verwendung

### Mit Swagger UI

Öffne die JSON-Datei in [Swagger Editor](https://editor.swagger.io/):

```bash
https://editor.swagger.io/?url=https://raw.githubusercontent.com/oxomo030/open-webui/main/docs/api/combined/openapi.json
```

### Mit curl

```bash
# Kombinierte API-Spezifikation abrufen
curl https://raw.githubusercontent.com/oxomo030/open-webui/main/docs/api/combined/openapi.json
```

### Generierung aktualisieren

Die kombinierte Spezifikation kann mit folgendem Befehl neu generiert werden:

```bash
python backend/scripts/generate_openapi_specs.py
```

## Einzelne Router-Spezifikationen

Wenn Sie nur einen bestimmten Router benötigen, finden Sie die einzelnen Spezifikationen im Verzeichnis `../openapi/`.

## Live-API-Dokumentation

Die interaktive API-Dokumentation ist unter folgenden URLs verfügbar:

- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`
- OpenAPI JSON: `http://localhost:8080/openapi.json`
