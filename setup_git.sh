#!/bin/bash

# HouseIQ Git Setup Script
# Initializes git repository, creates .gitignore, and makes initial commit

set -e

echo "🚀 HouseIQ Git Setup"
echo "===================="

# Check if git repo exists
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Create .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
.venv
venv
env
ENV
__pycache__
*.py[cod]
*$py.class
*.so
.Python
build
develop-eggs
dist
downloads
eggs
.eggs
lib
lib64
parts
sdist
var
wheels
*.egg-info
.installed.cfg
*.egg
MANIFEST
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis
.pytest_cache
*.pot

# IDE
.vscode
.idea
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
.env.production
.env.*.local

# ML Artifacts
ml/artifacts/*.pkl
ml/artifacts/*.joblib

# Frontend
node_modules
.next
out
dist
.vercel

# Notebooks
.ipynb_checkpoints
notebooks
*.ipynb

# Logs
*.log
logs

# OS
.DS_Store
.AppleDouble
.LSOverride
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Misc
.cache
.parcel-cache
.venv
venv
*.code-workspace
EOF
echo "✓ .gitignore created"

# Stage all files
echo "📌 Staging files..."
git add .
echo "✓ Files staged"

# Make initial commit
echo "💾 Making initial commit..."
git commit -m "HouseIQ: production-ready ML web app" -q
echo "✓ Initial commit created"

echo ""
echo "✅ Git setup complete!"
echo ""
echo "📚 Next steps:"
echo ""
echo "1. Create a new repository on GitHub (https://github.com/new)"
echo "   - Repository name: houseiq"
echo "   - Description: California House Price Predictor (ML Web App)"
echo "   - Do NOT initialize with README, .gitignore, or license"
echo ""
echo "2. Add remote and push code:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/houseiq.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Enable GitHub Actions:"
echo "   - Go to repository Settings → Actions"
echo "   - Enable GitHub Actions"
echo "   - CI will run on next push"
echo ""
echo "4. Deploy to production:"
echo "   - Read DEPLOYMENT.md for Railway (backend) and Vercel (frontend) setup"
echo ""
