# 🎨 C4 Visualization Guide for L10nLight

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Docker Visualization](#docker-visualization)
- [CLI Visualization](#cli-visualization)
- [Online Tools](#online-tools)
- [Custom Diagrams](#custom-diagrams)
- [Export Options](#export-options)
- [Integration Examples](#integration-examples)

---

## 🚀 Quick Start

### 🐳 Fastest Way (Docker)
```bash
# Navigate to C4 directory
cd docs/c4

# Run Structurizr Lite
docker run -p 8080:8080 -v $(pwd):/usr/local/structurizr structurizr/lite

# Open browser
open http://localhost:8080
```

**Result:** Interactive diagrams at http://localhost:8080

---

## 🐳 Docker Visualization

### 📋 Structurizr Lite Setup

```bash
# Full command with explanations
docker run \
  -p 8080:8080 \                    # Port mapping
  -v $(pwd):/usr/local/structurizr \  # Volume mount
  structurizr/lite                   # Image name
```

### 🔧 Docker Compose (Optional)

```yaml
# docker-compose.c4.yml
version: "3.9"
services:
  structurizr:
    image: structurizr/lite
    ports:
      - "8080:8080"
    volumes:
      - ./docs/c4:/usr/local/structurizr
    working_dir: /usr/local/structurizr
    command: ["serve"]
```

```bash
# Run with Docker Compose
docker-compose -f docker-compose.c4.yml up
```

### 🌐 Browser Interface

When you open http://localhost:8080:

1. **Load Workspace**: Click "Load Workspace" → select `workspace.dsl`
2. **View Diagrams**: Automatic generation of all views
3. **Navigate**: Use sidebar to switch between diagrams
4. **Export**: Download as PNG, SVG, or PlantUML

---

## 💻 CLI Visualization

### 📦 Installation

```bash
# Using npm
npm install -g structurizr-cli

# Using yarn
yarn global add structurizr-cli

# Using Docker
docker pull structurizr/cli
```

### 🔍 Validation

```bash
# Validate DSL syntax
structurizr-cli validate -workspace docs/c4/workspace.dsl

# Output:
# ✓ workspace.dsl is valid
# ✓ 3 views found
# ✓ 7 elements defined
```

### 📤 Export Commands

```bash
# Export to PlantUML
structurizr-cli export -workspace docs/c4/workspace.dsl -format plantuml

# Export to PNG
structurizr-cli export -workspace docs/c4/workspace.dsl -format png

# Export to SVG
structurizr-cli export -workspace docs/c4/workspace.dsl -format svg

# Export to Mermaid
structurizr-cli export -workspace docs/c4/workspace.dsl -format mermaid

# Export all formats
structurizr-cli export -workspace docs/c4/workspace.dsl -format all
```

### 📁 Output Structure

```
docs/c4/
├── workspace.dsl              # Original DSL
├── structurizr-*.json         # JSON representation
├── Context.png                # Level 1 diagram
├── Containers.png             # Level 2 diagram
├── Components.png             # Level 3 diagram
├── Get-OfferWall-by-Token.png # Dynamic diagram
└── Get-Offer-Names.png        # Dynamic diagram
```

---

## 🌐 Online Tools

### 🌿 PlantUML Online

1. **Go to**: https://plantuml.com/online
2. **Convert DSL to PlantUML**:
   ```bash
   structurizr-cli export -workspace docs/c4/workspace.dsl -format plantuml
   ```
3. **Copy PlantUML code** to online editor
4. **Generate diagram**

### 🌊 Mermaid Live Editor

1. **Go to**: https://mermaid.live/
2. **Convert to Mermaid**:
   ```bash
   structurizr-cli export -workspace docs/c4/workspace.dsl -format mermaid
   ```
3. **Paste Mermaid code**
4. **Preview diagram**

### 🎨 Draw.io Integration

1. **Go to**: https://app.diagrams.net/
2. **File → Import → XML**
3. **Upload**: `structurizr-diagrams.xml` (if exported)
4. **Edit and customize**

---

## 🎨 Custom Diagrams

### 📋 Adding New Views

```dsl
# Add to workspace.dsl

views {
  # Existing views...
  
  # New custom view
  deployment "Deployment View" {
    include *
    autoLayout
  }
  
  # Filtered view
  filtered "API Only" {
    include *
    exclude user
    exclude drf
    autoLayout
  }
}
```

### 🎯 Custom Styling

```dsl
styles {
  # Existing styles...
  
  # Custom element styles
  element "Database" { 
    background "#ff6b6b" 
    color "#ffffff" 
    shape "Database" 
  }
  
  element "External API" { 
    background "#4ecdc4" 
    color "#ffffff" 
  }
  
  # Custom relationship styles
  relationship "HTTPS" { 
    color "#2ecc71" 
    thickness 2 
  }
  
  relationship "SQL" { 
    color "#e74c3c" 
    style "dashed" 
  }
}
```

### 📊 Custom Dynamic Views

```dsl
# Add new dynamic view
dynamic "Create OfferWall" {
  user -> nginx "POST /api/offerwalls"
  nginx -> api "Proxy to ASGI"
  api -> controller "Route: POST /offerwalls"
  controller -> service "create_offerwall(data)"
  service -> repository "save(entity)"
  repository -> db "INSERT INTO offer_walls"
  controller -> user "201 Created"
}

dynamic "Error Handling" {
  user -> nginx "GET /api/offerwalls/invalid"
  nginx -> api "Proxy to ASGI"
  api -> controller "Route: /offerwalls/{token}"
  controller -> errors "404 Not Found"
  errors -> user "404 JSON response"
}
```

---

## 📤 Export Options

### 🖼️ Image Formats

| Format | Best For | Features |
|--------|----------|----------|
| **PNG** | Presentations, docs | High quality, transparent |
| **SVG** | Web, scaling | Vector, searchable |
| **PDF** | Documents, printing | Multi-page, high-res |
| **JPG** | Web, email | Small size, compatible |

### 📝 Text Formats

| Format | Use Case | Features |
|--------|----------|----------|
| **PlantUML** | Documentation, version control | Text-based, diffable |
| **Mermaid** | Markdown, GitHub | Native MD support |
| **JSON** | API integration, parsing | Machine-readable |
| **DOT** | Graphviz, custom tools | Graph description |

### 🔧 Export Scripts

```bash
#!/bin/bash
# export-all.sh - Export all diagrams

echo "Exporting C4 diagrams..."

# Create output directory
mkdir -p docs/c4/exports

# Export all formats
structurizr-cli export -workspace docs/c4/workspace.dsl -format all

# Move to exports folder
mv *.png *.svg *.plantuml *.json *.mermaid docs/c4/exports/

echo "Export complete! Files in docs/c4/exports/"
```

```bash
# Make executable and run
chmod +x export-all.sh
./export-all.sh
```

---

## 🔗 Integration Examples

### 📚 GitHub Pages Integration

```yaml
# .github/workflows/c4-docs.yml
name: Update C4 Documentation

on:
  push:
    paths:
      - 'docs/c4/**'
  workflow_dispatch:

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate diagrams
        run: |
          cd docs/c4
          docker run --rm \
            -v $(pwd):/workspace \
            structurizr/cli \
            export -workspace /workspace/workspace.dsl -format png
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/c4
          destination_dir: c4
```

### 📖 README Integration

```markdown
# L10nLight Architecture

## 📋 System Architecture

### 📍 Context View
![Context](docs/c4/exports/Context.png)

### 🏢 Container View  
![Containers](docs/c4/exports/Containers.png)

### ⚙️ Component View
![Components](docs/c4/exports/Components.png)

### 🔄 Request Flows
- **Get OfferWall**: ![Get OfferWall](docs/c4/exports/Get-OfferWall-by-Token.png)
- **Get Offer Names**: ![Get Offer Names](docs/c4/exports/Get-Offer-Names.png)

## 🎨 Interactive Diagrams

View interactive diagrams at: https://soewal19.github.io/L10nLight/c4/
```

### 🔄 Git Hooks Integration

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Validating C4 model..."

# Check if C4 files changed
if git diff --cached --name-only | grep -q "docs/c4/workspace.dsl"; then
    # Validate DSL
    docker run --rm \
        -v $(pwd)/docs/c4:/workspace \
        structurizr/cli \
        validate -workspace /workspace/workspace.dsl
    
    if [ $? -ne 0 ]; then
        echo "❌ C4 model validation failed!"
        echo "Please fix workspace.dsl before committing."
        exit 1
    fi
    
    echo "✅ C4 model validated successfully"
fi
```

### 📱 Mobile-Friendly Viewer

```html
<!-- docs/c4/viewer.html -->
<!DOCTYPE html>
<html>
<head>
    <title>L10nLight Architecture</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        .diagram-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
            padding: 20px;
        }
        .diagram {
            text-align: center;
        }
        .diagram img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .nav {
            position: sticky;
            top: 0;
            background: white;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="nav">
        <h2>L10nLight Architecture</h2>
        <a href="#context">Context</a> |
        <a href="#containers">Containers</a> |
        <a href="#components">Components</a> |
        <a href="#dynamics">Dynamics</a>
    </div>
    
    <div class="diagram-container">
        <div id="context" class="diagram">
            <h3>System Context</h3>
            <img src="exports/Context.png" alt="Context Diagram">
        </div>
        
        <div id="containers" class="diagram">
            <h3>Container Architecture</h3>
            <img src="exports/Containers.png" alt="Container Diagram">
        </div>
        
        <div id="components" class="diagram">
            <h3>Component Structure</h3>
            <img src="exports/Components.png" alt="Component Diagram">
        </div>
        
        <div id="dynamics" class="diagram">
            <h3>Request Flows</h3>
            <img src="exports/Get-OfferWall-by-Token.png" alt="Get OfferWall Flow">
            <img src="exports/Get-Offer-Names.png" alt="Get Offer Names Flow">
        </div>
    </div>
</body>
</html>
```

---

## 🎯 Best Practices

### 📋 Diagram Naming

- **Consistent**: Use same naming convention
- **Descriptive**: Clear what each diagram shows
- **Versioned**: Include version if needed

```
✅ Good names:
- Context-v1.2.png
- Container-Architecture.png
- Component-Structure.png
- Get-OfferWall-Flow.png

❌ Avoid:
- img1.png
- diagram.png
- new_diagram.png
```

### 🎨 Visual Consistency

```dsl
# Use consistent colors
styles {
  element "Database" { background "#e74c3c" color "#ffffff" }
  element "API" { background "#3498db" color "#ffffff" }
  element "Frontend" { background "#2ecc71" color "#ffffff" }
  
  # Consistent relationships
  relationship "HTTP" { color "#3498db" }
  relationship "SQL" { color "#e74c3c" }
  relationship "Async" { color "#9b59b6" style "dashed" }
}
```

### 📝 Documentation Integration

```markdown
## Architecture Documentation

### 📋 System Overview
![System Context](c4/exports/Context.png)

### 🏢 Technology Stack
![Container Architecture](c4/exports/Containers.png)

### ⚙️ Internal Structure
![Component Diagram](c4/exports/Components.png)

### 🔄 Request Processing
- **Get OfferWall**: See flow diagram below
- **Get Offer Names**: See flow diagram below

### 🎨 Interactive View
👉 [View interactive diagrams](c4/viewer.html)
```

---

## 🚀 Advanced Features

### 🔍 Automated Updates

```bash
#!/bin/bash
# update-c4.sh - Auto-update C4 docs

echo "🔄 Updating C4 documentation..."

# Update from code structure
python scripts/generate-c4-from-code.py

# Validate new model
docker run --rm \
    -v $(pwd)/docs/c4:/workspace \
    structurizr/cli \
    validate -workspace /workspace/workspace.dsl

# Generate new diagrams
docker run --rm \
    -v $(pwd)/docs/c4:/workspace \
    structurizr/cli \
    export -workspace /workspace/workspace.dsl -format all

# Update viewer
python scripts/update-viewer.py

echo "✅ C4 documentation updated!"
```

### 📊 Metrics Dashboard

```python
# scripts/c4-metrics.py
import json
import requests

def calculate_complexity(workspace_file):
    """Calculate architectural complexity metrics"""
    with open(workspace_file) as f:
        workspace = json.loads(f.read())
    
    metrics = {
        'elements': len(workspace['model']['elements']),
        'relationships': len(workspace['model']['relationships']),
        'views': len(workspace['views']),
        'complexity_score': 0
    }
    
    # Calculate complexity score
    metrics['complexity_score'] = (
        metrics['elements'] * 1 +
        metrics['relationships'] * 2 +
        metrics['views'] * 0.5
    )
    
    return metrics

if __name__ == "__main__":
    metrics = calculate_complexity('docs/c4/structurizr-workspace.json')
    print(f"📊 C4 Metrics: {metrics}")
```

### 🎯 Custom Templates

```dsl
# templates/microservice.dsl
workspace "{{systemName}}" "{{systemDescription}}" {
  model {
    user = person "User" "End user of the system"
    
    {{system}} = softwareSystem "{{systemName}}" "{{systemDescription}}" {
      nginx = container "Nginx" "Reverse proxy" "Nginx"
      api = container "{{apiName}}" "{{apiDescription}}" "{{apiTech}}"
      db = container "Database" "Data storage" "{{dbTech}}"
    }
    
    user -> nginx "HTTPS"
    nginx -> api "HTTP"
    api -> db "{{dbProtocol}}"
  }
  
  views {
    systemLandscape "Context" {
      include *
      autoLayout
    }
    
    container {{system}} "Containers" {
      include nginx api db
      autoLayout
    }
  }
}
```

---

## 🎉 Conclusion

This visualization guide provides **comprehensive options** for creating, maintaining, and sharing C4 architecture diagrams for L10nLight:

- 🚀 **Quick start** with Docker
- 💻 **CLI automation** for CI/CD
- 🌐 **Online tools** for collaboration
- 🎨 **Custom styling** for branding
- 📱 **Mobile-friendly** viewers
- 🔗 **GitHub integration** for documentation

**Choose the approach that best fits your workflow and team needs!** 🎯

---

## 📞 Support

- 📖 **Structurizr Docs**: https://docs.structurizr.com/
- 🌐 **C4 Model**: https://c4model.com/
- 🐳 **Docker Hub**: https://hub.docker.com/r/structurizr/lite
- 📧 **Issues**: https://github.com/soewal19/L10nLight/issues
