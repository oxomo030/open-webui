#!/usr/bin/env python3
"""
Simplified script zur Generierung von OpenAPI-Spezifikationen für jeden Router.
This version uses direct imports to avoid heavy dependencies.
"""
import json
import yaml
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, APIRouter

def import_router_safe(module_name, router_name="router"):
    """Safely import a router, returning None if it fails."""
    try:
        module = __import__(f"open_webui.routers.{module_name}", fromlist=[router_name])
        return getattr(module, router_name)
    except Exception as e:
        print(f"    ⚠ Warning importing {module_name}: {e}")
        return None

# Router-Konfiguration
ROUTERS = [
    {"name": "chats", "module": "chats", "prefix": "/api/v1/chats", "tags": ["chats"]},
    {"name": "notes", "module": "notes", "prefix": "/api/v1/notes", "tags": ["notes"]},
    {"name": "models", "module": "models", "prefix": "/api/v1/models", "tags": ["models"]},
    {"name": "knowledge", "module": "knowledge", "prefix": "/api/v1/knowledge", "tags": ["knowledge"]},
    {"name": "prompts", "module": "prompts", "prefix": "/api/v1/prompts", "tags": ["prompts"]},
    {"name": "tools", "module": "tools", "prefix": "/api/v1/tools", "tags": ["tools"]},
    {"name": "memories", "module": "memories", "prefix": "/api/v1/memories", "tags": ["memories"]},
    {"name": "folders", "module": "folders", "prefix": "/api/v1/folders", "tags": ["folders"]},
    {"name": "groups", "module": "groups", "prefix": "/api/v1/groups", "tags": ["groups"]},
    {"name": "files", "module": "files", "prefix": "/api/v1/files", "tags": ["files"]},
    {"name": "functions", "module": "functions", "prefix": "/api/v1/functions", "tags": ["functions"]},
    {"name": "evaluations", "module": "evaluations", "prefix": "/api/v1/evaluations", "tags": ["evaluations"]},
    {"name": "users", "module": "users", "prefix": "/api/v1/users", "tags": ["users"]},
    {"name": "auths", "module": "auths", "prefix": "/api/v1/auths", "tags": ["auths"]},
    {"name": "configs", "module": "configs", "prefix": "/api/v1/configs", "tags": ["configs"]},
    {"name": "audio", "module": "audio", "prefix": "/api/v1/audio", "tags": ["audio"]},
    {"name": "retrieval", "module": "retrieval", "prefix": "/api/v1/retrieval", "tags": ["retrieval"]},
    {"name": "images", "module": "images", "prefix": "/api/v1/images", "tags": ["images"]},
    {"name": "tasks", "module": "tasks", "prefix": "/api/v1/tasks", "tags": ["tasks"]},
    {"name": "pipelines", "module": "pipelines", "prefix": "/api/v1/pipelines", "tags": ["pipelines"]},
    {"name": "channels", "module": "channels", "prefix": "/api/v1/channels", "tags": ["channels"]},
    {"name": "utils", "module": "utils", "prefix": "/api/v1/utils", "tags": ["utils"]},
    {"name": "ollama", "module": "ollama", "prefix": "/ollama", "tags": ["ollama"]},
    {"name": "openai", "module": "openai", "prefix": "/openai", "tags": ["openai"]},
    {"name": "scim", "module": "scim", "prefix": "/api/v1/scim/v2", "tags": ["scim"]},
]

def generate_router_spec(router_config, router):
    """Generiere OpenAPI-Spezifikation für einen einzelnen Router."""
    app = FastAPI(
        title=f"Open WebUI - {router_config['name'].capitalize()} API",
        description=f"API-Spezifikation für {router_config['name']} Router",
        version="1.0.0",
    )
    
    app.include_router(
        router,
        prefix=router_config['prefix'],
        tags=router_config['tags']
    )
    
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

def generate_combined_spec(routers_list):
    """Generiere kombinierte OpenAPI-Spezifikation für alle Router."""
    app = FastAPI(
        title="Open WebUI - Complete API",
        description="Vollständige API-Spezifikation für alle Open WebUI Router",
        version="1.0.0",
    )
    
    for router_config, router in routers_list:
        if router:
            app.include_router(
                router,
                prefix=router_config['prefix'],
                tags=router_config['tags']
            )
    
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

def main():
    """Hauptfunktion zur Generierung aller Spezifikationen."""
    # Einzelne Router-Spezifikationen
    base_path = Path(__file__).parent.parent.parent / "docs" / "api" / "openapi"
    base_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Generiere OpenAPI-Spezifikationen in: {base_path}")
    
    successful_routers = []
    
    for router_config in ROUTERS:
        name = router_config['name']
        print(f"  Generiere {name}...")
        
        try:
            router = import_router_safe(router_config['module'])
            if not router:
                print(f"    ✗ Router konnte nicht importiert werden")
                continue
                
            spec = generate_router_spec(router_config, router)
            
            # JSON speichern
            json_path = base_path / f"{name}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(spec, f, indent=2, ensure_ascii=False)
            
            # YAML speichern
            yaml_path = base_path / f"{name}.yaml"
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(spec, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"    ✓ {json_path.name}")
            print(f"    ✓ {yaml_path.name}")
            
            successful_routers.append((router_config, router))
            
        except Exception as e:
            print(f"    ✗ Fehler: {e}")
    
    # Kombinierte Spezifikation
    if successful_routers:
        combined_path = Path(__file__).parent.parent.parent / "docs" / "api" / "combined"
        combined_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\nGeneriere kombinierte OpenAPI-Spezifikation in: {combined_path}")
        
        try:
            combined_spec = generate_combined_spec(successful_routers)
            
            # JSON speichern
            json_path = combined_path / "openapi.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(combined_spec, f, indent=2, ensure_ascii=False)
            
            # YAML speichern
            yaml_path = combined_path / "openapi.yaml"
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(combined_spec, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"  ✓ {json_path.name}")
            print(f"  ✓ {yaml_path.name}")
            
        except Exception as e:
            print(f"  ✗ Fehler: {e}")
    
    print(f"\nFertig! {len(successful_routers)}/{len(ROUTERS)} Router erfolgreich generiert.")

if __name__ == "__main__":
    main()
