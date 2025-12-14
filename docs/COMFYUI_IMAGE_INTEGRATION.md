# ComfyUI Image Integration - Architecture Overview

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [ComfyUI Workflow Position Mapping](#comfyui-workflow-position-mapping)
4. [Image Edit Function Integration](#image-edit-function-integration)
5. [Technical Implementation Guide](#technical-implementation-guide)
6. [AI Agent TODO List](#ai-agent-todo-list)

---

## Executive Summary

This document provides a comprehensive analysis of the ComfyUI integration within the Open WebUI chat component. ComfyUI is integrated as one of four image generation engines (alongside OpenAI DALL-E, Automatic1111, and Google Gemini), with specific emphasis on:

- **Workflow Position Mapping**: How workflow node IDs and parameters are mapped from the ComfyUI JSON workflow to dynamic runtime values
- **Image Edit Integration**: How the image editing function leverages ComfyUI workflows for image-to-image transformations
- **Architecture**: Event-driven, WebSocket-based communication between frontend and backend

### Key Features
- ✅ Dynamic workflow node mapping system
- ✅ Support for both image generation and image editing
- ✅ WebSocket-based real-time communication
- ✅ Multiple image engine support with unified API
- ✅ Configurable workflow templates

---

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Chat.svelte                                                    │
│  ├── MessageInput.svelte                                        │
│  │   └── imageGenerationEnabled toggle                          │
│  ├── Messages/ResponseMessage.svelte                            │
│  │   └── generateImage() function                               │
│  └── WebSocket Event Listeners                                  │
│      ├── 'files' event → message.files update                   │
│      └── 'status' event → loading indicators                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                         Backend Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FastAPI Routers                                                │
│  ├── /api/images/generations (POST)                             │
│  │   └── image_generations()                                    │
│  ├── /api/images/edit (POST)                                    │
│  │   └── image_edits()                                          │
│  └── /api/images/config (GET/POST)                              │
│                                                                 │
│  Engine Selection Logic                                         │
│  ├── OpenAI DALL-E                                              │
│  ├── Automatic1111                                              │
│  ├── Google Gemini                                              │
│  └── ComfyUI ← Focus of this document                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                      ComfyUI Integration                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  utils/images/comfyui.py                                        │
│  ├── comfyui_create_image()                                     │
│  │   ├── Load workflow JSON                                     │
│  │   ├── Map workflow nodes                                     │
│  │   ├── WebSocket connection                                   │
│  │   └── Get generated images                                   │
│  │                                                              │
│  ├── comfyui_edit_image()                                       │
│  │   ├── Upload input image(s)                                 │
│  │   ├── Load edit workflow                                     │
│  │   ├── Map image nodes                                        │
│  │   └── Process workflow                                       │
│  │                                                              │
│  └── comfyui_upload_image()                                     │
│      └── Upload to ComfyUI server                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                      ComfyUI Server                             │
├─────────────────────────────────────────────────────────────────┤
│  ├── /prompt (POST) - Queue workflow                            │
│  ├── /ws (WebSocket) - Execution status                         │
│  ├── /history/{prompt_id} (GET) - Get results                   │
│  ├── /view (GET) - Retrieve generated image                     │
│  └── /api/upload/image (POST) - Upload input images             │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Sequence

#### Image Generation Flow
```
1. User enables imageGenerationEnabled in MessageInput
2. User sends message with prompt
3. Chat.svelte → getFeatures() returns { image_generation: true }
4. POST /api/chat/completions with features object
5. Backend middleware detects image_generation flag
6. Middleware calls image_generations()
7. Router selects engine based on IMAGE_GENERATION_ENGINE
8. If ComfyUI selected:
   a. comfyui_create_image() loads workflow
   b. Maps node positions (prompt, model, width, height, etc.)
   c. Connects to ComfyUI WebSocket
   d. Queues prompt via /prompt endpoint
   e. Listens for completion on WebSocket
   f. Retrieves image URLs from /history endpoint
   g. Downloads images and uploads to Open WebUI storage
9. Returns image URLs to frontend
10. WebSocket emits 'files' event
11. ResponseMessage.svelte displays images
```

#### Image Edit Flow
```
1. User uploads image(s) to chat
2. User enables image edit mode
3. User enters edit prompt
4. POST /api/images/edit with image data
5. If ComfyUI selected:
   a. comfyui_upload_image() uploads to ComfyUI
   b. comfyui_edit_image() loads edit workflow
   c. Maps image node positions
   d. Maps prompt and other parameters
   e. Executes workflow on ComfyUI
   f. Retrieves edited images
   g. Filters for output-type images
6. Returns edited image URLs
7. Displays in chat
```

---

## ComfyUI Workflow Position Mapping

### Overview

ComfyUI workflows are JSON-based graph structures where each node has:
- **Node ID**: Unique identifier (e.g., "3", "4", "5")
- **Node Type**: Class type (e.g., "KSampler", "CheckpointLoaderSimple")
- **Inputs**: Parameters and connections to other nodes
- **Metadata**: Title and other info

The mapping system allows Open WebUI to inject dynamic values (prompts, dimensions, seeds, etc.) into specific workflow nodes at runtime.

### Workflow Node Structure

#### Default ComfyUI Workflow Example
```json
{
  "3": {
    "inputs": {
      "seed": 0,
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "model.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "5": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "6": {
    "inputs": {
      "text": "positive prompt",
      "clip": ["4", 1]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive)"
    }
  },
  "7": {
    "inputs": {
      "text": "negative prompt",
      "clip": ["4", 1]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Negative)"
    }
  }
}
```

### Node Mapping Configuration

#### Required Workflow Nodes (Image Generation)

Located in: `src/lib/components/admin/Settings/Images.svelte`

```javascript
let REQUIRED_WORKFLOW_NODES = [
  {
    type: 'prompt',        // Maps to positive prompt text
    key: 'text',           // Input parameter name
    node_ids: ''           // Comma-separated node IDs (e.g., "6")
  },
  {
    type: 'model',         // Maps to model selection
    key: 'ckpt_name',      // Input parameter name
    node_ids: ''           // e.g., "4"
  },
  {
    type: 'width',         // Maps to image width
    key: 'width',          // Input parameter name
    node_ids: ''           // e.g., "5"
  },
  {
    type: 'height',        // Maps to image height
    key: 'height',         // Input parameter name
    node_ids: ''           // e.g., "5"
  },
  {
    type: 'steps',         // Maps to sampling steps
    key: 'steps',          // Input parameter name
    node_ids: ''           // e.g., "3"
  },
  {
    type: 'seed',          // Maps to random seed
    key: 'seed',           // Input parameter name
    node_ids: ''           // e.g., "3"
  }
];
```

#### Required Edit Workflow Nodes (Image Editing)

```javascript
let REQUIRED_EDIT_WORKFLOW_NODES = [
  {
    type: 'image',         // Maps to input image filename
    key: 'image',          // Input parameter name
    node_ids: ''           // Node ID for image input
  },
  {
    type: 'prompt',        // Maps to edit prompt
    key: 'prompt',         // Input parameter name
    node_ids: ''
  },
  {
    type: 'model',         // Maps to model selection
    key: 'unet_name',      // Input parameter name (different for edit)
    node_ids: ''
  },
  {
    type: 'width',         // Maps to output width
    key: 'width',
    node_ids: ''
  },
  {
    type: 'height',        // Maps to output height
    key: 'height',
    node_ids: ''
  }
];
```

### Mapping Implementation

#### Backend Implementation

Located in: `backend/open_webui/utils/images/comfyui.py`

```python
async def comfyui_create_image(
    model: str, 
    payload: ComfyUICreateImageForm, 
    client_id, 
    base_url, 
    api_key
):
    # Load workflow JSON
    workflow = json.loads(payload.workflow.workflow)
    
    # Iterate through configured node mappings
    for node in payload.workflow.nodes:
        if node.type:
            if node.type == "model":
                # Map model to all specified node IDs
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][node.key] = model
                    
            elif node.type == "prompt":
                # Map prompt to all specified node IDs
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][
                        node.key if node.key else "text"
                    ] = payload.prompt
                    
            elif node.type == "negative_prompt":
                # Map negative prompt
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][
                        node.key if node.key else "text"
                    ] = payload.negative_prompt
                    
            elif node.type == "width":
                # Map width
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][
                        node.key if node.key else "width"
                    ] = payload.width
                    
            elif node.type == "height":
                # Map height
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][
                        node.key if node.key else "height"
                    ] = payload.height
                    
            elif node.type == "n":
                # Map batch size (number of images)
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][
                        node.key if node.key else "batch_size"
                    ] = payload.n
                    
            elif node.type == "steps":
                # Map sampling steps
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][
                        node.key if node.key else "steps"
                    ] = payload.steps
                    
            elif node.type == "seed":
                # Map seed (generate random if not provided)
                seed = (
                    payload.seed
                    if payload.seed
                    else random.randint(0, 1125899906842624)
                )
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][node.key] = seed
        else:
            # Custom node mapping with fixed value
            for node_id in node.node_ids:
                workflow[node_id]["inputs"][node.key] = node.value
    
    # Execute workflow...
```

### Mapping Process Visualization

```
Configuration Step (Admin UI):
┌─────────────────────────────────────────────────┐
│ Admin configures node mappings:                 │
│ - type: "prompt"                                │
│ - key: "text"                                   │
│ - node_ids: "6"                                 │
└─────────────────────────────────────────────────┘
                    ↓
Runtime Step (Backend):
┌─────────────────────────────────────────────────┐
│ User prompt: "A beautiful sunset"               │
│                                                 │
│ Mapping logic finds node_id "6"                 │
│ workflow["6"]["inputs"]["text"] = "A beautiful  │
│                                    sunset"      │
└─────────────────────────────────────────────────┘
                    ↓
Execution Step (ComfyUI):
┌─────────────────────────────────────────────────┐
│ Node "6" (CLIPTextEncode) receives:             │
│ {                                               │
│   "text": "A beautiful sunset",                 │
│   "clip": ["4", 1]                              │
│ }                                               │
│ → Encodes prompt into latent space              │
└─────────────────────────────────────────────────┘
```

### Multi-Node Mapping

One mapping type can target **multiple nodes**. This is useful for:

1. **Duplicate prompts**: Apply same prompt to multiple CLIP encoders
2. **Consistent dimensions**: Apply same width/height to multiple nodes
3. **Shared parameters**: Apply same settings across parallel branches

Example:
```javascript
{
  type: 'width',
  key: 'width',
  node_ids: '5,8,12'  // Applies width to nodes 5, 8, and 12
}
```

Backend processing:
```python
for node_id in ['5', '8', '12']:
    workflow[node_id]["inputs"]["width"] = 1024
```

---

## Image Edit Function Integration

### Overview

The image edit function extends the generation workflow by:
1. Accepting input images
2. Uploading them to ComfyUI server
3. Mapping image filenames to workflow nodes
4. Processing image-to-image transformations

### Image Upload Process

#### Frontend → Backend

Located in: `backend/open_webui/routers/images.py` (line 780-1057)

```python
@router.post("/edit")
async def image_edits(
    request: Request,
    form_data: EditImageForm,
    user=Depends(get_verified_user),
):
    # Load image(s) from URL(s) or base64
    async def load_url_image(data):
        if data.startswith("http://") or data.startswith("https://"):
            # Download from URL
            r = await asyncio.to_thread(requests.get, data)
            r.raise_for_status()
            image_data = base64.b64encode(r.content).decode("utf-8")
            return f"data:{r.headers['content-type']};base64,{image_data}"
            
        elif data.startswith("/api/v1/files"):
            # Load from Open WebUI file storage
            file_id = data.split("/api/v1/files/")[1].split("/content")[0]
            file_response = await get_file_content_by_id(file_id, user)
            # ... load file bytes and convert to base64
            return f"data:{mime_type};base64,{image_data}"
        
        return data  # Already base64
    
    # Process single or multiple images
    if isinstance(form_data.image, str):
        form_data.image = await load_url_image(form_data.image)
    elif isinstance(form_data.image, list):
        form_data.image = [
            await load_url_image(img) for img in form_data.image
        ]
```

#### Backend → ComfyUI

Located in: `backend/open_webui/utils/images/comfyui.py` (line 96-113)

```python
async def comfyui_upload_image(image_file_item, base_url, api_key):
    """Upload image to ComfyUI server"""
    url = f"{base_url}/api/upload/image"
    headers = {}
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    # Extract filename, bytes, and MIME type
    _, (filename, file_bytes, mime_type) = image_file_item
    
    # Create multipart form data
    form = aiohttp.FormData()
    form.add_field("image", file_bytes, 
                   filename=filename, 
                   content_type=mime_type)
    form.add_field("type", "input")  # Required by ComfyUI
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()  # Returns {"name": "uploaded_filename.png"}
```

### Image Node Mapping

#### Single Image Mapping

```python
async def comfyui_edit_image(
    model: str, 
    payload: ComfyUIEditImageForm, 
    client_id, 
    base_url, 
    api_key
):
    workflow = json.loads(payload.workflow.workflow)
    
    for node in payload.workflow.nodes:
        if node.type == "image":
            if isinstance(payload.image, list):
                # Multiple images: distribute to node_ids
                for idx, node_id in enumerate(node.node_ids):
                    if idx < len(payload.image):
                        workflow[node_id]["inputs"][node.key] = payload.image[idx]
            else:
                # Single image: apply to all node_ids
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][node.key] = payload.image
```

**Example**: Image inpainting workflow
```json
{
  "10": {
    "inputs": {
      "image": "uploaded_image.png",  // ← Mapped from payload.image
      "mask": ["11", 0]
    },
    "class_type": "LoadImage"
  },
  "11": {
    "inputs": {
      "image": "uploaded_mask.png",  // ← Mapped from payload.image[1]
      "channel": "alpha"
    },
    "class_type": "LoadImageMask"
  }
}
```

Node mapping configuration:
```javascript
{
  type: 'image',
  key: 'image',
  node_ids: '10,11'  // First image → node 10, second → node 11
}
```

### Edit Workflow Execution

```python
# Upload images first
comfyui_images = []
for file_item in files:
    res = await comfyui_upload_image(
        file_item,
        request.app.state.config.IMAGES_EDIT_COMFYUI_BASE_URL,
        request.app.state.config.IMAGES_EDIT_COMFYUI_API_KEY,
    )
    # Store uploaded filename
    comfyui_images.append(res.get("name", file_item[1][0]))

# Map images to workflow
data = {
    "image": comfyui_images,  # Can be single string or list
    "prompt": form_data.prompt,
    "width": width if width is not None else {},
    "height": height if height is not None else {},
    "n": form_data.n if form_data.n else {},
}

# Execute workflow
form_data = ComfyUIEditImageForm(
    workflow=ComfyUIWorkflow(
        workflow=request.app.state.config.IMAGES_EDIT_COMFYUI_WORKFLOW,
        nodes=request.app.state.config.IMAGES_EDIT_COMFYUI_WORKFLOW_NODES,
    ),
    **data,
)

res = await comfyui_edit_image(
    model,
    form_data,
    user.id,
    request.app.state.config.IMAGES_EDIT_COMFYUI_BASE_URL,
    request.app.state.config.IMAGES_EDIT_COMFYUI_API_KEY,
)

# Filter results for output images
image_urls = set()
for image in res["data"]:
    image_urls.add(image["url"])
image_urls = list(image_urls)

# Prioritize output-type URLs
output_type_urls = [url for url in image_urls if "type=output" in url]
if output_type_urls:
    image_urls = output_type_urls
```

### Result Retrieval

Located in: `backend/open_webui/utils/images/comfyui.py` (line 69-93)

```python
def get_images(ws, prompt, client_id, base_url, api_key):
    """Execute workflow and retrieve generated images"""
    # Queue prompt
    prompt_id = queue_prompt(prompt, client_id, base_url, api_key)["prompt_id"]
    output_images = []
    
    # Listen on WebSocket for completion
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message["type"] == "executing":
                data = message["data"]
                if data["node"] is None and data["prompt_id"] == prompt_id:
                    break  # Execution is done
        else:
            continue  # Previews are binary data
    
    # Fetch results from history
    history = get_history(prompt_id, base_url, api_key)[prompt_id]
    
    # Extract image URLs from all output nodes
    for node_id in history["outputs"]:
        node_output = history["outputs"][node_id]
        if "images" in node_output:
            for image in node_output["images"]:
                url = get_image_url(
                    image["filename"], 
                    image["subfolder"], 
                    image["type"], 
                    base_url
                )
                output_images.append({"url": url})
    
    return {"data": output_images}
```

---

## Technical Implementation Guide

### Configuration Setup

#### 1. ComfyUI Server Configuration

**Environment Variables** (`.env` file):
```bash
# ComfyUI Base URL
COMFYUI_BASE_URL=http://localhost:8188

# Optional: API Key for secured ComfyUI
COMFYUI_API_KEY=your_api_key_here

# Optional: Custom workflow JSON
COMFYUI_WORKFLOW='{"3": {...}, "4": {...}}'
```

#### 2. Admin UI Configuration

Navigate to: **Admin Panel → Settings → Images → ComfyUI**

**Step 1**: Enable ComfyUI Engine
- Set `IMAGE_GENERATION_ENGINE` to `comfyui`

**Step 2**: Configure Base URL
- Enter ComfyUI server URL (e.g., `http://localhost:8188`)

**Step 3**: Configure Workflow
- Paste ComfyUI workflow JSON (exported from ComfyUI UI)
- Click "Edit Workflow" to open code editor

**Step 4**: Map Workflow Nodes
```
Prompt Node IDs:          6           (CLIPTextEncode node)
Negative Prompt Node IDs: 7           (CLIPTextEncode negative)
Model Node IDs:           4           (CheckpointLoaderSimple)
Width Node IDs:           5           (EmptyLatentImage)
Height Node IDs:          5           (EmptyLatentImage)
Steps Node IDs:           3           (KSampler)
Seed Node IDs:            3           (KSampler)
```

**Step 5**: Save Configuration

#### 3. Edit Workflow Configuration

Navigate to: **Admin Panel → Settings → Images → Image Edit**

- Set `IMAGE_EDIT_ENGINE` to `comfyui`
- Configure edit workflow JSON
- Map edit workflow nodes (image, prompt, model, etc.)

### Custom Workflow Integration

#### Exporting Workflow from ComfyUI

1. Design workflow in ComfyUI web UI
2. Click "Save (API Format)" button
3. Copy JSON output
4. Paste into Open WebUI admin settings

#### Identifying Node IDs

Example workflow:
```json
{
  "6": {  // ← This is the node ID
    "inputs": {
      "text": "...",  // ← This is the key to map
      "clip": ["4", 1]
    },
    "class_type": "CLIPTextEncode"  // ← Node type
  }
}
```

To find node IDs:
1. Look at the JSON keys at the top level (e.g., "6", "7", "8")
2. Check the `class_type` to identify node purpose
3. Note the `inputs` keys for mapping

#### Advanced Workflow Example

**Complex workflow with ControlNet**:
```json
{
  "3": { "class_type": "KSampler", ... },
  "4": { "class_type": "CheckpointLoaderSimple", ... },
  "5": { "class_type": "EmptyLatentImage", ... },
  "6": { "class_type": "CLIPTextEncode", ... },
  "7": { "class_type": "CLIPTextEncode", ... },
  "12": { "class_type": "ControlNetLoader", ... },
  "13": { "class_type": "ControlNetApply", ... }
}
```

Node mappings:
```javascript
Prompt:           6
Negative Prompt:  7
Model:            4
Width:            5
Height:           5
Steps:            3
Seed:             3
ControlNet Model: 12    // Custom mapping
ControlNet Scale: 13    // Custom mapping
```

### Development Integration

#### Adding Custom Node Types

**Backend** (`backend/open_webui/utils/images/comfyui.py`):
```python
async def comfyui_create_image(...):
    workflow = json.loads(payload.workflow.workflow)
    
    for node in payload.workflow.nodes:
        if node.type:
            # ... existing mappings ...
            
            elif node.type == "controlnet_scale":  # ← New type
                for node_id in node.node_ids:
                    workflow[node_id]["inputs"][
                        node.key if node.key else "strength"
                    ] = payload.controlnet_scale  # ← New parameter
```

**Frontend** (`src/lib/components/admin/Settings/Images.svelte`):
```javascript
let REQUIRED_WORKFLOW_NODES = [
  // ... existing nodes ...
  {
    type: 'controlnet_scale',
    key: 'strength',
    node_ids: ''
  }
];
```

#### Error Handling

```python
try:
    images = await comfyui_create_image(...)
except Exception as e:
    log.exception(f"ComfyUI error: {e}")
    
    # Emit error to frontend via WebSocket
    await __event_emitter__({
        "type": "status",
        "data": {
            "description": f"Image generation failed: {str(e)}",
            "done": True
        }
    })
    
    # Return error response
    raise HTTPException(
        status_code=500,
        detail=f"ComfyUI generation failed: {str(e)}"
    )
```

### Testing

#### Manual Testing Steps

1. **Connection Test**:
   - Admin Panel → Images → ComfyUI
   - Click "Verify URL"
   - Should return `200 OK`

2. **Generation Test**:
   - Enable image generation in chat
   - Send prompt: "A cute cat"
   - Verify image appears in message

3. **Edit Test**:
   - Upload image to chat
   - Enable image edit
   - Send edit prompt: "Make it blue"
   - Verify edited image appears

#### Automated Testing

```python
# test_comfyui.py
import pytest
from unittest.mock import patch
from open_webui.utils.images.comfyui import (
    comfyui_create_image,
    ComfyUICreateImageForm,
    ComfyUIWorkflow
)

@pytest.mark.asyncio
async def test_workflow_mapping():
    workflow_json = '{"3": {"inputs": {"seed": 0}}, "6": {"inputs": {"text": ""}}}'
    nodes = [
        {"type": "prompt", "key": "text", "node_ids": "6"},
        {"type": "seed", "key": "seed", "node_ids": "3"}
    ]
    
    form = ComfyUICreateImageForm(
        workflow=ComfyUIWorkflow(
            workflow=workflow_json,
            nodes=nodes
        ),
        prompt="test prompt",
        width=512,
        height=512,
        n=1,
        seed=12345
    )
    
    # Mock ComfyUI server
    with patch('open_webui.utils.images.comfyui.queue_prompt') as mock_queue:
        mock_queue.return_value = {"prompt_id": "test-id"}
        
        # Should not raise exception
        result = await comfyui_create_image(
            "model.safetensors",
            form,
            "client-123",
            "http://localhost:8188",
            ""
        )
```

---

## AI Agent TODO List

### Phase 1: Analysis & Planning (2-3 hours)
- [ ] Clone and setup Open WebUI development environment
- [ ] Study ComfyUI API documentation
- [ ] Review existing workflow JSON examples
- [ ] Identify all node types used in default workflows
- [ ] Document current mapping limitations

### Phase 2: Core Implementation (8-10 hours)

#### Backend Tasks
- [ ] **Task 2.1**: Refactor workflow mapping to support custom node types
  - File: `backend/open_webui/utils/images/comfyui.py`
  - Add plugin system for custom mappings
  - Expected time: 2 hours

- [ ] **Task 2.2**: Implement workflow validation
  - Validate node IDs exist in workflow JSON
  - Validate input keys exist in node inputs
  - Return detailed error messages
  - Expected time: 1.5 hours

- [ ] **Task 2.3**: Add workflow debugging mode
  - Log mapped workflow before execution
  - Add `/api/images/debug/workflow` endpoint
  - Expected time: 1 hour

- [ ] **Task 2.4**: Enhance image upload error handling
  - Better error messages for upload failures
  - Retry logic for transient failures
  - Expected time: 1 hour

- [ ] **Task 2.5**: Implement workflow caching
  - Cache parsed workflow JSON
  - Invalidate on configuration change
  - Expected time: 1.5 hours

#### Frontend Tasks
- [ ] **Task 2.6**: Improve workflow editor UI
  - File: `src/lib/components/admin/Settings/Images.svelte`
  - Add syntax highlighting for workflow JSON
  - Add node ID autocomplete
  - Expected time: 2 hours

- [ ] **Task 2.7**: Add workflow node visualizer
  - Display workflow as visual graph
  - Highlight mapped nodes
  - Expected time: 2 hours

- [ ] **Task 2.8**: Implement workflow templates
  - Provide pre-configured workflows
  - Template selector in admin UI
  - Expected time: 1 hour

### Phase 3: Testing (4-5 hours)
- [ ] **Task 3.1**: Unit tests for workflow mapping
  - Test all node types
  - Test multi-node mapping
  - Test error cases
  - Expected time: 2 hours

- [ ] **Task 3.2**: Integration tests
  - Test with actual ComfyUI server
  - Test generation flow end-to-end
  - Test edit flow end-to-end
  - Expected time: 2 hours

- [ ] **Task 3.3**: Performance testing
  - Test with large workflows
  - Test concurrent requests
  - Measure latency
  - Expected time: 1 hour

### Phase 4: Documentation (3-4 hours)
- [ ] **Task 4.1**: Update API documentation
  - Document workflow format
  - Document node mapping configuration
  - Expected time: 1.5 hours

- [ ] **Task 4.2**: Create user guide
  - How to export workflow from ComfyUI
  - How to identify node IDs
  - Common workflow examples
  - Expected time: 1.5 hours

- [ ] **Task 4.3**: Create developer guide
  - How to add custom node types
  - How to extend mapping system
  - Expected time: 1 hour

### Phase 5: Advanced Features (Optional, 6-8 hours)
- [ ] **Task 5.1**: Workflow marketplace
  - Allow users to share workflows
  - Rating and review system
  - Expected time: 3 hours

- [ ] **Task 5.2**: Dynamic node discovery
  - Auto-detect available nodes from ComfyUI
  - Suggest mappings based on node types
  - Expected time: 2 hours

- [ ] **Task 5.3**: Workflow versioning
  - Track workflow changes
  - Allow rollback to previous versions
  - Expected time: 2 hours

- [ ] **Task 5.4**: Multi-engine workflow
  - Support fallback to different engines
  - Load balancing across multiple ComfyUI servers
  - Expected time: 2 hours

### Estimated Total Time
- **Minimum (Core + Testing)**: 14-18 hours
- **With Documentation**: 17-22 hours
- **With Advanced Features**: 23-30 hours

### Priority Levels
- **P0 (Critical)**: Tasks 2.1, 2.2, 3.1, 3.2
- **P1 (High)**: Tasks 2.3, 2.6, 4.1, 4.2
- **P2 (Medium)**: Tasks 2.4, 2.5, 2.7, 2.8, 3.3, 4.3
- **P3 (Low)**: All Phase 5 tasks

### Success Criteria
- [ ] All P0 and P1 tasks completed
- [ ] Test coverage > 80%
- [ ] No regression in existing functionality
- [ ] Documentation complete and accurate
- [ ] Performance benchmarks met

---

## Appendix

### Glossary

- **Node ID**: Unique identifier for a workflow node (e.g., "3", "6", "12")
- **Node Type**: Classification of node purpose (e.g., "prompt", "model", "width")
- **Class Type**: ComfyUI node class (e.g., "KSampler", "CLIPTextEncode")
- **Workflow**: JSON graph definition of ComfyUI processing pipeline
- **Mapping**: Configuration linking Open WebUI parameters to workflow nodes

### References

- ComfyUI GitHub Repository: https://github.com/comfyanonymous/ComfyUI
- ComfyUI API Examples: https://github.com/comfyanonymous/ComfyUI/tree/master/script_examples
- Open WebUI Documentation: https://docs.openwebui.com
- WebSocket Protocol: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

### Version History

- v1.0 (2025-12-14): Initial documentation
