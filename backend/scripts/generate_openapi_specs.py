#!/usr/bin/env python3
"""
Script zur Generierung von OpenAPI-Spezifikationen für jeden Router.
"""
import json
import yaml
from pathlib import Path
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

# Importiere die Router
from open_webui.routers import (
    chats, notes, models, knowledge, prompts, tools, 
    memories, folders, groups, files, functions, evaluations,
    users, auths, configs, audio, retrieval, images, tasks,
    pipelines, channels, utils, ollama, openai, scim
)

# Router-Konfiguration
ROUTERS = [
    {"name": "chats", "router": chats.router, "prefix": "/api/v1/chats", "tags": ["chats"]},
    {"name": "notes", "router": notes.router, "prefix": "/api/v1/notes", "tags": ["notes"]},
    {"name": "models", "router": models.router, "prefix": "/api/v1/models", "tags": ["models"]},
    {"name": "knowledge", "router": knowledge.router, "prefix": "/api/v1/knowledge", "tags": ["knowledge"]},
    {"name": "prompts", "router": prompts.router, "prefix": "/api/v1/prompts", "tags": ["prompts"]},
    {"name": "tools", "router": tools.router, "prefix": "/api/v1/tools", "tags": ["tools"]},
    {"name": "memories", "router": memories.router, "prefix": "/api/v1/memories", "tags": ["memories"]},
    {"name": "folders", "router": folders.router, "prefix": "/api/v1/folders", "tags": ["folders"]},
    {"name": "groups", "router": groups.router, "prefix": "/api/v1/groups", "tags": ["groups"]},
    {"name": "files", "router": files.router, "prefix": "/api/v1/files", "tags": ["files"]},
    {"name": "functions", "router": functions.router, "prefix": "/api/v1/functions", "tags": ["functions"]},
    {"name": "evaluations", "router": evaluations.router, "prefix": "/api/v1/evaluations", "tags": ["evaluations"]},
    {"name": "users", "router": users.router, "prefix": "/api/v1/users", "tags": ["users"]},
    {"name": "auths", "router": auths.router, "prefix": "/api/v1/auths", "tags": ["auths"]},
    {"name": "configs", "router": configs.router, "prefix": "/api/v1/configs", "tags": ["configs"]},
    {"name": "audio", "router": audio.router, "prefix": "/api/v1/audio", "tags": ["audio"]},
    {"name": "retrieval", "router": retrieval.router, "prefix": "/api/v1/retrieval", "tags": ["retrieval"]},
    {"name": "images", "router": images.router, "prefix": "/api/v1/images", "tags": ["images"]},
    {"name": "tasks", "router": tasks.router, "prefix": "/api/v1/tasks", "tags": ["tasks"]},
    {"name": "pipelines", "router": pipelines.router, "prefix": "/api/v1/pipelines", "tags": ["pipelines"]},
    {"name": "channels", "router": channels.router, "prefix": "/api/v1/channels", "tags": ["channels"]},
    {"name": "utils", "router": utils.router, "prefix": "/api/v1/utils", "tags": ["utils"]},
    {"name": "ollama", "router": ollama.router, "prefix": "/ollama", "tags": ["ollama"]},
    {"name": "openai", "router": openai.router, "prefix": "/openai", "tags": ["openai"]},
    {"name": "scim", "router": scim.router, "prefix": "/api/v1/scim/v2", "tags": ["scim"]},
]

def generate_router_spec(router_config):
    """Generiere OpenAPI-Spezifikation für einen einzelnen Router."""
    app = FastAPI(
        title=f"Open WebUI - {router_config['name'].capitalize()} API",
        description=f"API-Spezifikation für {router_config['name']} Router",
        version="1.0.0",
    )
    
    app.include_router(
        router_config['router'],
        prefix=router_config['prefix'],
        tags=router_config['tags']
    )
    
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

def generate_combined_spec():
    """Generiere kombinierte OpenAPI-Spezifikation für alle Router."""
    app = FastAPI(
        title="Open WebUI - Complete API",
        description="Vollständige API-Spezifikation für alle Open WebUI Router",
        version="1.0.0",
    )
    
    for router_config in ROUTERS:
        app.include_router(
            router_config['router'],
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
    
    for router_config in ROUTERS:
        name = router_config['name']
        print(f"  Generiere {name}...")
        
        try:
            spec = generate_router_spec(router_config)
            
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
            
        except Exception as e:
            print(f"    ✗ Fehler: {e}")
    
    # Kombinierte Spezifikation
    combined_path = Path(__file__).parent.parent.parent / "docs" / "api" / "combined"
    combined_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nGeneriere kombinierte OpenAPI-Spezifikation in: {combined_path}")
    
    try:
        combined_spec = generate_combined_spec()
        
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
    
    print("\nFertig!")

if __name__ == "__main__":
    main()
