# 📦 Releasing ALO to PyPI

This guide explains how to package and release Agentic Labeling Orchestrator (ALO) to PyPI so users can install it via `pip install labellerr-alo`.

---

## 📋 Prerequisites

### 1. **Install Build Tools**

```bash
pip install --upgrade pip
pip install --upgrade build twine
```

### 2. **Create PyPI Account**

- Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
- Create an account
- Verify your email
- Enable 2FA (required for uploads)

### 3. **Create API Token**

1. Go to [https://pypi.org/manage/account/#api-tokens](https://pypi.org/manage/account/#api-tokens)
2. Click "Add API token"
3. Name: `labellerr-alo-upload`
4. Scope: Entire account (or specific project after first upload)
5. Copy the token (starts with `pypi-...`)

### 4. **Configure PyPI Credentials**

Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-your-token-here

[testpypi]
username = __token__
password = pypi-your-testpypi-token-here
```

Or use environment variables:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-token-here
```

---

## 🚀 Release Process

### Step 1: Update Version Number

Update version in multiple places:

**1. `setup.py`:**
```python
setup(
    name="labellerr-alo",
    version="0.2.0",  # ← Update this
    ...
)
```

**2. `pyproject.toml`:**
```toml
[project]
name = "labellerr-alo"
version = "0.2.0"  # ← Update this
```

**3. `alo/__init__.py`:**
```python
__version__ = "0.2.0"  # ← Update this
```

**Semantic Versioning:**
- `0.1.0` → `0.2.0` for new features (minor)
- `0.2.0` → `0.2.1` for bug fixes (patch)
- `0.9.0` → `1.0.0` for stable release (major)

### Step 2: Update Changelog

Create/update `CHANGELOG.md`:

```markdown
# Changelog

## [0.2.0] - 2025-01-XX

### Added
- Intelligent object discovery with CrewAI agents
- Automatic class detection from 5% dataset sample
- Multi-model support (OpenAI, Anthropic, Roboflow)
- LLM-powered validation agents
- Smart sampling strategies

### Changed
- Redesigned README with open source messaging
- Enhanced workflow orchestrator with automatic data flow

### Fixed
- Agent initialization error handling
```

### Step 3: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Check code quality
black alo/
isort alo/
flake8 alo/

# Type checking
mypy alo/
```

### Step 4: Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info/
```

### Step 5: Build the Package

```bash
# Build source distribution and wheel
python -m build

# This creates:
# dist/labellerr_alo-0.2.0.tar.gz (source)
# dist/labellerr_alo-0.2.0-py3-none-any.whl (wheel)
```

### Step 6: Test Upload to TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ --no-deps labellerr-alo

# Test that it works
python -c "from alo import WorkflowOrchestrator; print('Success!')"

# Uninstall
pip uninstall labellerr-alo -y
```

### Step 7: Upload to PyPI (Production)

```bash
# Upload to PyPI
python -m twine upload dist/*

# You'll see:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading labellerr_alo-0.2.0-py3-none-any.whl
# Uploading labellerr_alo-0.2.0.tar.gz
```

### Step 8: Verify Installation

```bash
# Install from PyPI
pip install labellerr-alo

# Test it works
python -c "from alo import WorkflowOrchestrator; print('Installed!')"

# Check version
python -c "import alo; print(alo.__version__)"
```

### Step 9: Create GitHub Release

1. Go to [https://github.com/1sarthakbhardawaj/labellerr-alo/releases/new](https://github.com/1sarthakbhardawaj/labellerr-alo/releases/new)
2. Tag version: `v0.2.0`
3. Release title: `v0.2.0 - Intelligent Object Discovery`
4. Description: Copy from CHANGELOG.md
5. Attach dist files (optional)
6. Publish release

### Step 10: Update Documentation

```bash
# Update README badge
[![PyPI version](https://badge.fury.io/py/labellerr-alo.svg)](https://badge.fury.io/py/labellerr-alo)

# Update installation instructions
pip install labellerr-alo
```

---

## 📝 Quick Release Checklist

- [ ] Update version in `setup.py`, `pyproject.toml`, `alo/__init__.py`
- [ ] Update `CHANGELOG.md`
- [ ] Run tests (`pytest tests/`)
- [ ] Format code (`black`, `isort`, `flake8`)
- [ ] Clean old builds (`rm -rf build/ dist/ *.egg-info/`)
- [ ] Build package (`python -m build`)
- [ ] Test on TestPyPI (optional)
- [ ] Upload to PyPI (`twine upload dist/*`)
- [ ] Verify installation (`pip install labellerr-alo`)
- [ ] Create GitHub release
- [ ] Update README badges
- [ ] Announce on social media / forums

---

## 🔧 Troubleshooting

### **Issue: "Package already exists"**
```bash
# Solution: Increment version number
# 0.2.0 → 0.2.1
```

### **Issue: "Invalid API token"**
```bash
# Solution: Regenerate token on PyPI
# Update ~/.pypirc or environment variables
```

### **Issue: "Missing files in package"**
```bash
# Solution: Check MANIFEST.in includes all necessary files
# Rebuild: python -m build
```

### **Issue: "Import errors after install"**
```bash
# Solution: Check dependencies in setup.py
# Ensure all required packages are listed
```

---

## 📊 Post-Release

### Monitor Package

- **PyPI Stats**: [https://pypistats.org/packages/labellerr-alo](https://pypistats.org/packages/labellerr-alo)
- **GitHub Releases**: Track downloads from releases page
- **Issues**: Monitor for bug reports

### Promote Release

- **Twitter/X**: Announce new features
- **Reddit**: r/MachineLearning, r/Python
- **HackerNews**: Show HN post
- **LinkedIn**: Professional announcement
- **Discord/Slack**: ML communities

### Gather Feedback

- Monitor GitHub Issues
- Check PyPI comments/ratings
- Community discussions
- User testimonials

---

## 🎯 Version Strategy

### Pre-1.0 (Current)

- **0.1.x**: Initial MVP, basic features
- **0.2.x**: Intelligent discovery, CrewAI agents
- **0.3.x**: Active learning, more agents
- **0.4.x**: Dashboard, monitoring
- **0.9.x**: Release candidate

### Post-1.0

- **1.0.0**: Stable release
- **1.x.x**: Minor features, bug fixes
- **2.0.0**: Breaking changes (if needed)

---

## 📚 Additional Resources

- **PyPI Guide**: [https://packaging.python.org/tutorials/packaging-projects/](https://packaging.python.org/tutorials/packaging-projects/)
- **Semantic Versioning**: [https://semver.org/](https://semver.org/)
- **Twine Documentation**: [https://twine.readthedocs.io/](https://twine.readthedocs.io/)
- **setuptools**: [https://setuptools.pypa.io/](https://setuptools.pypa.io/)

---

## ✅ Ready to Release?

```bash
# One-liner for experienced users:
rm -rf build/ dist/ *.egg-info/ && python -m build && twine upload dist/*

# Don't forget to:
# 1. Update version numbers
# 2. Test the package
# 3. Create GitHub release
# 4. Celebrate! 🎉
```

---

**Questions?** Open an issue on GitHub or contact support@labellerr.com
