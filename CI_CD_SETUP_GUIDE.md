# 🚀 Guide Complet: Configuration CI/CD avec GitHub Actions

**Date**: 26 Août 2026  
**Projets**: bot-trading-deepseek + Sophiadeep-  
**Objectif**: Automatiser tests, builds, déploiements et qualité du code

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Configuration requise](#configuration-requise)
3. [Workflows à implémenter](#workflows-à-implémenter)
4. [Fichiers à créer](#fichiers-à-créer)
5. [Secrets GitHub](#secrets-github)
6. [Validation et tests](#validation-et-tests)

---

## 🎯 Vue d'ensemble

Pipeline CI/CD complète:

```
Push Code
    ↓
[Test] → Run tests, linting, type checking
    ↓
[Build] → Build Docker images
    ↓
[Quality] → Code quality scan
    ↓
[Deploy] → Deploy to Render.com
    ↓
[Release] → Create GitHub releases
```

---

## ⚙️ Configuration Requise

### Prérequis
- ✅ Repository GitHub accessible
- ✅ Compte Render.com (pour deployment)
- ✅ SonarCloud account (optionnel)
- ✅ GitHub Secrets configurés

---

## 📁 Workflows à Créer

### 1️⃣ Tests (.github/workflows/test.yml)

```yaml
name: Tests & Quality

on:
  push:
    branches: [ main, develop, feature/* ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Lint with flake8
      run: |
        flake8 bot_trading.py config.py --count --select=E9,F63,F7,F82

    - name: Type checking with mypy
      run: mypy bot_trading.py config.py --ignore-missing-imports
      continue-on-error: true

    - name: Format check with black
      run: black --check bot_trading.py config.py
      continue-on-error: true

    - name: Run pytest
      run: pytest tests/ -v --cov=. --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### 2️⃣ Docker Build (.github/workflows/docker.yml)

```yaml
name: Build & Push Docker

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v3
    - uses: docker/setup-buildx-action@v2
    
    - name: Log in to Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=semver,pattern={{version}}
          type=sha

    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### 3️⃣ Code Quality (.github/workflows/quality.yml)

```yaml
name: Code Quality & Security

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 0 * * 0'

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install tools
      run: |
        pip install black flake8 mypy pylint
        pip install -r requirements.txt

    - name: Black check
      run: black --check --diff .
      continue-on-error: true

    - name: Flake8
      run: flake8 . --max-line-length=127
      continue-on-error: true

    - name: MyPy
      run: mypy . --ignore-missing-imports
      continue-on-error: true
```

### 4️⃣ Deploy (.github/workflows/deploy.yml)

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - uses: actions/checkout@v3

    - name: Trigger Render deployment
      run: |
        curl --request POST \
          --url "https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }}" \
          --header 'content-type: application/json'
      continue-on-error: true
```

### 5️⃣ Release (.github/workflows/release.yml)

```yaml
name: Release

on:
  push:
    tags: [ 'v*' ]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Create Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref_name }}
        release_name: Release ${{ github.ref_name }}
        draft: false
        prerelease: false
```

---

## 📂 Fichiers à Créer

### Structure
```
.github/
├── workflows/
│   ├── test.yml
│   ├── docker.yml
│   ├── quality.yml
│   ├── deploy.yml
│   └── release.yml
```

### Étapes
1. Créer dossier `.github/workflows/`
2. Créer fichiers YAML (voir ci-dessus)
3. Commiter et pusher
4. Vérifier dans l'onglet Actions

---

## 🔐 Secrets GitHub à Ajouter

Settings → Secrets and variables → Actions

### Requis
```
DEEPSEEK_API_KEY              # API key Deepseek
RENDER_SERVICE_ID             # ID service Render
RENDER_API_KEY                # API key Render
```

### Optionnel
```
SONAR_TOKEN                   # SonarCloud token
GITHUB_TOKEN                  # Auto-généré
```

---

## ✅ Checklist

- [ ] Créer `.github/workflows/` folder
- [ ] Créer test.yml
- [ ] Créer docker.yml
- [ ] Créer quality.yml
- [ ] Créer deploy.yml
- [ ] Créer release.yml
- [ ] Ajouter les secrets GitHub
- [ ] Commiter et pusher
- [ ] Vérifier dans Actions tab
- [ ] Configurer branch protection (optionnel)

---

## 🎯 Résultats Attendus

### Après chaque push
✅ Tests pass  
✅ Linting passe  
✅ Type checking passe  
✅ Coverage généré  

### Après merge sur main
✅ Docker image buildée  
✅ Deploy sur Render.com  

### Après un tag (v2.0.0)
✅ Release GitHub créée  

---

*Guide créé par Voyageur 1.0 - 26 Août 2026*
