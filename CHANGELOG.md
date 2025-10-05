# Changelog

All notable changes to the Agentic Labeling Orchestrator (ALO) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Active learning agents with uncertainty and diversity sampling
- Web dashboard for monitoring pipelines
- More foundation model integrations (LLaVA, Gemini, etc.)
- Video labeling workflows
- 3D point cloud support
- Cloud deployment options

---

## [0.2.0] - 2025-01-10

### 🚀 Major Release: Intelligent Object Discovery

### Added
- **CrewAI Agent Framework**
  - `BaseALOAgent`: Foundation class for all intelligent agents
  - `IntelligentSamplerAgent`: Smart dataset sampling with diverse strategies
  - `ObjectDiscoveryAgent`: Automatic class discovery using GPT-4V/Claude
  - `LLMValidatorAgent`: AI-powered prediction validation
  - `EnsembleValidatorAgent`: Multi-strategy validation

- **Intelligent Features**
  - Automatic object class discovery from 5% dataset sample
  - Zero manual class definition required
  - Smart sampling strategies (diverse, temporal, metadata-based)
  - Cost-optimized: expensive models only on samples

- **Multi-Model Support**
  - OpenAI GPT-4V integration
  - Anthropic Claude integration
  - Roboflow hosted models
  - HuggingFace models
  - Custom API endpoints
  - Local model support

- **Documentation**
  - [SDK vs ALO](docs/SDK_VS_ALO.md) - Comprehensive comparison
  - [PyPI Release Guide](docs/RELEASE_TO_PYPI.md) - Complete release process
  - [Documentation Index](docs/README.md) - Organized doc structure
  - Positioning as open source initiative

- **Packaging**
  - `setup.py` for PyPI distribution
  - `MANIFEST.in` for package files
  - PyPI-ready configuration

- **Example Workflows**
  - `intelligent_discovery_workflow.yaml` - Full smart pipeline
  - Updated `image_classification_workflow.yaml` with auto-discovery

### Changed
- **Workflow Orchestrator**
  - Enhanced agent execution with automatic data flow
  - Support for dependency-based input passing between steps
  - Agent mapping for easy extensibility
  - Improved error handling and logging

- **README**
  - Complete redesign with open source messaging
  - Clear comparison with traditional SDK approach
  - Real-world examples and use cases
  - Added PyPI badge and installation instructions
  - Open Source Initiative section

### Dependencies
- Added `crewai>=0.11.0`
- Added `crewai-tools>=0.2.0`
- Added `langchain>=0.1.0`
- Added `langchain-openai>=0.0.5`
- Added `langchain-anthropic>=0.1.0`

### Performance
- **50x faster** dataset discovery (minutes vs hours/days)
- **Cost-optimized**: 5% sample for discovery vs 100% dataset
- **Reduced complexity**: 3 lines vs 200+ lines of code

### Breaking Changes
None - Fully backwards compatible with v0.1.0

---

## [0.1.0] - 2025-01-08

### 🎉 Initial Release

### Added
- **Core Workflow Orchestrator**
  - YAML/JSON configuration support
  - Dependency management between steps
  - Error handling and recovery
  - Dry-run validation

- **Labellerr SDK Integration**
  - `LabellerrConnector` for seamless SDK access
  - Project creation
  - Pre-annotation upload (sync and async)
  - Annotation export
  - Project and dataset management

- **Project Structure**
  - Modular package architecture
  - Placeholder modules for agents, validators, active learning
  - Example workflow templates
  - Comprehensive README

- **Example Workflows**
  - Image classification pipeline
  - Object detection pipeline
  - Active learning loop

- **Documentation**
  - README with features and architecture
  - Contributing guidelines
  - Apache 2.0 license

- **Development Tools**
  - Modern Python packaging (pyproject.toml)
  - Black code formatting
  - pytest testing setup
  - Type hints with mypy

### Dependencies
- `labellerr-sdk>=1.0.0`
- `pyyaml>=6.0`
- `pydantic>=2.0.0`
- `requests>=2.28.0`
- Additional utilities (tqdm, numpy, pillow)

---

## Release Notes

### Version History

- **v0.2.0** (Current) - Intelligent discovery with CrewAI agents
- **v0.1.0** - Initial MVP release

### Upgrade Guide

#### From 0.1.0 to 0.2.0

No breaking changes! Simply update:

```bash
pip install --upgrade labellerr-alo
```

New features are opt-in. Existing workflows continue to work unchanged.

To use new intelligent discovery:

```yaml
# Add discovery step to your workflow
steps:
  - name: "discover_classes"
    agent: "object_discoverer"
    parameters:
      dataset_path: "/path/to/data"
      sample_percentage: 0.05
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting features  
- Submitting pull requests
- Code style and standards

---

## Links

- **GitHub**: [github.com/1sarthakbhardawaj/labellerr-alo](https://github.com/1sarthakbhardawaj/labellerr-alo)
- **PyPI**: [pypi.org/project/labellerr-alo](https://pypi.org/project/labellerr-alo)
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/1sarthakbhardawaj/labellerr-alo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/1sarthakbhardawaj/labellerr-alo/discussions)
