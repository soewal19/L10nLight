# 🚀 C4 Documentation Quick Start

## 🎯 5-Minute Setup

### 🐳 Fastest Way (Recommended)

```bash
# Navigate to C4 directory
cd docs/c4

# Run interactive viewer
docker run -p 8080:8080 -v $(pwd):/usr/local/structurizr structurizr/lite

# Open browser
open http://localhost:8080
```

**Result:** Interactive architecture diagrams at http://localhost:8080

---

## 📋 What You'll See

### 📍 Level 1: Context
- **User** → **L10nLight** → **PostgreSQL**
- System boundaries and external interactions

### 🏢 Level 2: Containers  
- **Nginx** (Reverse proxy)
- **Litestar API** (Python application)
- **PostgreSQL** (Database)

### ⚙️ Level 3: Components
- **Controllers**, **Services**, **Repositories**
- **Models**, **Schemas**, **Config**

### 🔄 Dynamic Views
- **Get OfferWall by Token** flow
- **Get Offer Names** flow

---

## 🎨 Viewing Options

### Option 1: Interactive (Docker)
```bash
docker run -p 8080:8080 -v $(pwd)/docs/c4:/usr/local/structurizr structurizr/lite
```
✅ **Pros**: Interactive, zoomable, exportable  
❌ **Cons**: Requires Docker

### Option 2: Static Images
```bash
# Generate PNG images
docker run --rm -v $(pwd):/workspace structurizr/cli \
  export -workspace /workspace/workspace.dsl -format png

# View images
open Context.png Containers.png Components.png
```
✅ **Pros**: No dependencies, fast  
❌ **Cons**: Not interactive

### Option 3: Online Tools
```bash
# Convert to PlantUML
docker run --rm -v $(pwd):/workspace structurizr/cli \
  export -workspace /workspace/workspace.dsl -format plantuml

# Copy to https://plantuml.com/online
cat structurizr-plantuml-context.puml
```
✅ **Pros**: Free, no installation  
❌ **Cons**: Manual copy-paste

---

## 📊 Quick Diagram Preview

### 🌍 System Context
```
┌─────────────┐    HTTP     ┌─────────────┐    SQL     ┌─────────────┐
│    User     │ ────────→   │  L10nLight  │ ────────→  │ PostgreSQL  │
└─────────────┘             └─────────────┘            └─────────────┘
```

### 🏢 Container Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    L10nLight System                         │
├─────────────────┬─────────────────┬─────────────────────────┤
│     Nginx       │   Litestar API  │      PostgreSQL         │
│                 │                 │                         │
│ • Reverse proxy │ • Python 3.12   │ • PostgreSQL 16+        │
│ • Port 80/443   │ • Port 8000     │ • Port 5432            │
└─────────────────┴─────────────────┴─────────────────────────┘
```

### ⚙️ Component Structure
```
┌─────────────────────────────────────────────────────────────┐
│                Litestar API Container                      │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Controllers   │     Services    │      Infrastructure     │
│                 │                 │                         │
│ • OfferWall     │ • OfferWall     │ • SQLAlchemy Models     │
│   Controller    │   Service       │ • DB Setup              │
│                 │                 │ • Config                │
│ • Error Handlers│                 │ • AsyncSession DI       │
└─────────────────┴─────────────────┴─────────────────────────┘
```

---

## 🔄 Common Workflows

### 📺 View Architecture (Daily)
```bash
# Start interactive viewer
cd docs/c4
docker run -p 8080:8080 -v $(pwd):/usr/local/structurizr structurizr/lite
open http://localhost:8080
```

### 📸 Export Images (Documentation)
```bash
# Generate all diagrams
cd docs/c4
docker run --rm -v $(pwd):/workspace structurizr/cli \
  export -workspace /workspace/workspace.dsl -format png

# Use in README
echo "![Architecture](docs/c4/Context.png)"
```

### ✅ Validate Changes (Development)
```bash
# Check DSL syntax
docker run --rm -v $(pwd):/workspace structurizr/cli \
  validate -workspace /workspace/workspace.dsl

# Should output: ✓ workspace.dsl is valid
```

### 🔄 Update Documentation (CI/CD)
```bash
# Automated update script
#!/bin/bash
cd docs/c4
docker run --rm -v $(pwd):/workspace structurizr/cli \
  export -workspace /workspace/workspace.dsl -format all
git add *.png *.svg
git commit -m "Update C4 diagrams"
```

---

## 🎯 Navigation Tips

### 🌐 Browser Interface
When you open http://localhost:8080:

1. **Load Workspace**: Click "Load Workspace" → select `workspace.dsl`
2. **Switch Views**: Use left sidebar
3. **Zoom**: Mouse wheel or pinch gesture
4. **Export**: Right-click → "Save as image"
5. **Fullscreen**: Press `F11`

### 📱 Mobile Viewing
- **Pinch to zoom** on touch devices
- **Swipe** to navigate between views
- **Tap** elements for details

### ⌨️ Keyboard Shortcuts
- `Space`: Pan mode
- `Ctrl + Scroll`: Zoom
- `Arrow keys`: Navigate
- `Esc`: Reset view

---

## 🔧 Troubleshooting

### ❌ "Port 8080 already in use"
```bash
# Use different port
docker run -p 8081:8080 -v $(pwd):/usr/local/structurizr structurizr/lite
open http://localhost:8081
```

### ❌ "Permission denied"
```bash
# Fix volume permissions
sudo chmod -R 755 docs/c4
docker run -p 8080:8080 -v $(pwd):/usr/local/structurizr structurizr/lite
```

### ❌ "Cannot load workspace.dsl"
```bash
# Check file exists and is readable
ls -la docs/c4/workspace.dsl
cat docs/c4/workspace.dsl | head -5

# Validate syntax
docker run --rm -v $(pwd):/workspace structurizr/cli \
  validate -workspace /workspace/workspace.dsl
```

### ❌ "Docker not running"
```bash
# Start Docker
# Windows: Start Docker Desktop
# Mac: Start Docker Desktop
# Linux: sudo systemctl start docker

# Test Docker
docker run hello-world
```

---

## 📚 Next Steps

### 🎓 Learn More
- 📖 **Full Guide**: [C4_ARCHITECTURE_GUIDE.md](C4_ARCHITECTURE_GUIDE.md)
- 🎨 **Visualization**: [VISUALIZATION_GUIDE.md](VISUALIZATION_GUIDE.md)
- 🌐 **C4 Model**: https://c4model.com/

### 🔄 Integrate with Team
1. **Add to README**: Include diagrams in project documentation
2. **CI/CD**: Auto-update diagrams on changes
3. **Code Reviews**: Validate C4 changes in pull requests
4. **Onboarding**: Use for new team member training

### 🎯 Advanced Usage
- **Custom styling**: Match company branding
- **Dynamic views**: Show request flows
- **Filtered views**: Focus on specific areas
- **Export automation**: Integrate with documentation pipeline

---

## 🎉 Success Criteria

You're successfully using C4 documentation when:

- ✅ **Team members** can understand system architecture quickly
- ✅ **New developers** onboard faster with clear diagrams
- ✅ **Architecture decisions** are documented and visible
- ✅ **Documentation** stays updated with code changes
- ✅ **Stakeholders** can review system design easily

---

## 📞 Need Help?

- 🐛 **Issues**: https://github.com/soewal19/L10nLight/issues
- 📖 **Documentation**: [Full Guide](C4_ARCHITECTURE_GUIDE.md)
- 🌐 **Live Demo**: http://localhost:8080 (when running)
- 💬 **Discussions**: https://github.com/soewal19/L10nLight/discussions

---

**🚀 Start visualizing your L10nLight architecture in just 5 minutes!** 🎯
