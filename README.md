# 🤖 Agentic Labeling Orchestrator (ALO)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/labellerr-alo.svg)](https://badge.fury.io/py/labellerr-alo)
[![CrewAI](https://img.shields.io/badge/Powered%20by-CrewAI-orange)](https://github.com/joaomdmoura/crewAI)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

**Intelligent, autonomous labeling pipelines powered by AI agents** 🚀

> **An Open Source Initiative** to democratize AI-powered data labeling

ALO is the first truly **agentic** data labeling framework that uses intelligent AI agents built on [CrewAI](https://github.com/joaomdmoura/crewAI) to automatically discover, label, and validate your data - with **zero manual class definition required**.

---

## 🎯 The Vision

### **Our Goal: Complete End-to-End Agentic Labeling**

ALO is designed to be a **comprehensive framework for autonomous labeling pipelines** that eliminates manual work at every step:

```yaml
# The Complete Vision
Dataset → Auto-Discovery → Pre-Label → AI Validation → Human Review Routing → Active Learning → Adaptive Retraining → Production
```

## 🌟 What Makes ALO Different?

### **❌ Traditional Approach**:
```python
# You manually define classes
classes = ["cat", "dog", "bird", "car", "person"]  # 😫 How do you know what's in your data?
model.predict(images, classes=classes)
```

### **✅ ALO Agentic Approach**:
```yaml
# ALO automatically discovers what's in your data!
steps:
  - name: "discover_objects"
    agent: "object_discoverer"
    parameters:
      sample_percentage: 0.05  # Analyze 5% of dataset
      min_samples: 2           # Minimum 2 images
      # Classes auto-discovered! 🎉
```

---

## Core Capabilities

### **1. Intelligent Object Discovery**
- **Automatic class detection** - Analyzes 5% of your dataset to discover all object classes
- **Smart sampling** - Uses diverse sampling strategies for representative samples
- **Cost-optimized** - Only uses expensive models (GPT-4V) on samples, not full dataset
- **Zero manual work** - No need to manually list classes!

### **2. Agentic Workflow to Avoid Hallucinations**
- **Modular architecture** - Each agent is a specialized agent
- **Multi-agent collaboration** - Agents work together seamlessly
- **Extensible** - Easy to add custom agents
- **Production-ready** - Built on battle-tested CrewAI framework

### **3. Multi-Model Support**
- **API-based models** - OpenAI GPT-4V, Anthropic Claude, etc.
- **Hosted models** - Roboflow, HuggingFace, Replicate
- **Custom endpoints** - Your own API endpoints
- **Local models** - PyTorch, TensorFlow models

### **4. AI-Powered Validation**
- **LLM validators** - Use Claude/GPT to validate predictions
- **Ensemble validation** - Multiple validation strategies
- **Consistency checks** - Detect conflicts and errors
- **Quality metrics** - Track annotation quality

### **5. Workflow Orchestration**
- **YAML-based configs** - Simple, declarative pipelines
- **Dependency management** - Auto-executes steps in correct order
- **Data flow** - Automatic data passing between agents
- **Error recovery** - Built-in retry and error handling

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install labellerr-alo (soon, try from source for now)

# Or from source
git clone https://github.com/1sarthakbhardawaj/labellerr-alo.git
cd labellerr-alo
pip install -e .
```

### Your First Intelligent Pipeline

**1. Create a workflow YAML** (`intelligent_pipeline.yaml`):

```yaml
name: "intelligent_discovery_pipeline"
description: "Auto-discover objects → Label full dataset → Validate → Export"

parameters:
  dataset_path: "/path/to/your/10000/images"
  project_id: "labellerr_project_id"

steps:
  # Step 1: Smart Sampling (5% of dataset)
  - name: "sample_dataset"
    agent: "intelligent_sampler"
    parameters:
      dataset_path: "${dataset_path}"
      sample_percentage: 0.05  # Only 500 images!
      min_samples: 2
      strategy: "diverse"

  # Step 2: Auto-Discover Classes
  - name: "discover_objects"
    agent: "object_discoverer"
    parameters:
      model_provider: "openai"
      api_key: "${OPENAI_API_KEY}"
      sampled_images: "${sample_dataset.sampled_images}"
      min_class_frequency: 0.05
      consolidate_similar: true
    depends_on: ["sample_dataset"]

  # Step 3: Label Full Dataset (uses discovered classes!)
  - name: "label_full_dataset"
    agent: "production_labeler"
    parameters:
      model_provider: "roboflow"
      api_key: "${ROBOFLOW_API_KEY}"
      classes: "${discover_objects.discovered_classes}"  # Auto-filled!
      dataset_path: "${dataset_path}"
    depends_on: ["discover_objects"]

  # Step 4: Validate with AI
  - name: "validate"
    agent: "llm_validator"
    parameters:
      model_provider: "anthropic"
      api_key: "${ANTHROPIC_API_KEY}"
      expected_classes: "${discover_objects.discovered_classes}"
    depends_on: ["label_full_dataset"]

  # Step 5: Export to Labellerr
  - name: "export"
    action: "push_to_labellerr"
    parameters:
      project_id: "${project_id}"
      format: "coco_json"
    depends_on: ["validate"]
```

**2. Run the pipeline**:

```python
from alo import WorkflowOrchestrator
from alo.connectors import LabellerrConnector

# Initialize Labellerr connection
connector = LabellerrConnector(
    api_key="your_api_key",
    api_secret="your_api_secret",
    client_id="your_client_id"
)

# Load and run workflow
orchestrator = WorkflowOrchestrator("intelligent_pipeline.yaml")
results = orchestrator.run(connector=connector)

# Check discovered classes
print(f"Discovered classes: {results['discover_objects']['discovered_classes']}")
print(f"Quality score: {results['validate']['quality_score']}")
```

**3. That's it!** 🎉

ALO automatically:
- Sampled 500 images (5%)
- Discovered all object classes in your dataset
- Labeled all 10,000 images with discovered classes
- Validated predictions for quality
- Exported to Labellerr for human review

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│            ALO Agentic Orchestration Engine                  │
│    (Powered by CrewAI Multi-Agent Framework)                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
       ┌──────────┼──────────┬──────────────┐
       │          │          │              │
┌──────▼────┐ ┌──▼─────┐ ┌─▼────────┐ ┌───▼──────┐
│  Sampling │ │Discovery│ │Validation│ │ Active   │
│   Agent   │ │ Agent   │ │  Agent   │ │ Learning │
│           │ │         │ │          │ │  Agent   │
│ • Diverse │ │• GPT-4V │ │• Claude  │ │• Uncer-  │
│ • Temporal│ │• Claude │ │• GPT-4   │ │  tainty  │
│ • Metadata│ │• LLaVA  │ │• Ensemble│ │• Diversity│
└───────────┘ └─────────┘ └──────────┘ └──────────┘
       │          │          │              │
       └──────────┼──────────┴──────────────┘
                  │
           ┌──────▼──────┐
           │  Labellerr  │
           │  Connector  │
           │  (SDK)      │
           └─────────────┘
```

---

## 🎯 Use Cases

### **1. Bootstrapping New Datasets**
```yaml
# Start with zero labels
# ALO discovers classes + labels everything
# Export to Labellerr for review
```

### **2. Unknown Dataset Analysis**
```yaml
# You have images, no idea what's in them
# ALO analyzes samples and tells you!
# Then labels the full dataset
```

### **3. Continuous Model Improvement**
```yaml
# Pull labeled data → Train → Predict → Select → Label
# Continuous active learning loop
```

### **4. Multi-Modal Labeling**
```yaml
# Combine GPT-4V + YOLO + SAM
# Vision-language-segmentation pipeline
```

---

## 📊 Agent Types

### **Sampling Agents**
- `IntelligentSamplerAgent` - Smart dataset sampling with diversity strategies

### **Discovery Agents**
- `ObjectDiscoveryAgent` - Auto-discover object classes using vision models

### **Validation Agents**
- `LLMValidatorAgent` - Validate with GPT-4/Claude
- `EnsembleValidatorAgent` - Multi-strategy validation

### **Active Learning Agents** (Coming Soon)
- `UncertaintySamplerAgent` - Uncertainty-based selection
- `DiversitySamplerAgent` - Maximize dataset diversity

---

## 🔧 Supported Model Providers

### **Vision Models**
| Provider | Models | Use Case |
|----------|--------|----------|
| OpenAI | GPT-4V, GPT-4-Turbo | Discovery, Classification |
| Anthropic | Claude 3.5 Sonnet | Validation, Analysis |
| Roboflow | YOLO, SAM | Production Labeling |
| HuggingFace | Open Source Models | Custom Pipelines |

### **Configuration Example**:
```yaml
# OpenAI GPT-4V
agent: "object_discoverer"
parameters:
  model_provider: "openai"
  api_key: "${OPENAI_API_KEY}"
  model: "gpt-4-vision-preview"

# Anthropic Claude
agent: "llm_validator"
parameters:
  model_provider: "anthropic"
  api_key: "${ANTHROPIC_API_KEY}"
  model: "claude-3-5-sonnet-20241022"

# Roboflow Hosted YOLO
agent: "production_labeler"
parameters:
  model_provider: "roboflow"
  api_key: "${ROBOFLOW_API_KEY}"
  model: "yolov8x-world"
```

---

## 🎪 Real-World Example

### **Scenario**: You have 50,000 wildlife images, no idea what animals are present

**Without ALO**:
```python
# 1. Manually review hundreds of images
# 2. Make a list of animal types
# 3. Set up labeling project
# 4. Configure detection model
# 5. Run predictions
# 6. Manual validation
# Time: ~2 days
```

**With ALO**:
```yaml
name: "wildlife_discovery"
steps:
  - name: "discover_animals"
    agent: "object_discoverer"
    parameters:
      sample_percentage: 0.05  # 2,500 images
      min_samples: 2
  
  - name: "label_all"
    agent: "yolo_detector"
    parameters:
      classes: "${discover_animals.discovered_classes}"
  
  - name: "export"
    action: "push_to_labellerr"
```

```python
orchestrator = WorkflowOrchestrator("wildlife_discovery.yaml")
results = orchestrator.run(connector)

# Discovered: ["elephant", "lion", "zebra", "giraffe", "buffalo", ...]
# Labeled: 50,000 images
# Time: ~2 hours
```

---

## 🆚 Comparison with Alternatives

| Feature | ALO | Roboflow Autodistill | Label Studio | Prodigy |
|---------|-----|---------------------|--------------|---------|
| **Auto Class Discovery** | ✅ | ❌ | ❌ | ❌ |
| **Agentic Architecture** | ✅ (CrewAI) | ❌ | ❌ | ❌ |
| **Smart Sampling** | ✅ (5% default) | ❌ | ❌ | Limited |
| **Multi-Model Orchestration** | ✅ | ✅ | Limited | Limited |
| **YAML Workflows** | ✅ | ❌ (Python) | ❌ | ❌ |
| **Active Learning** | ✅ | ❌ | Limited | ✅ |
| **Open Source** | ✅ | ✅ | ✅ | ❌ |
| **Labellerr Integration** | ✅ | ❌ | ❌ | ❌ |
| **Cost Optimization** | ✅ | ❌ | ❌ | ❌ |

---

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/1sarthakbhardawaj/labellerr-alo.git
cd labellerr-alo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black alo/
isort alo/
```

### Project Structure

```
labellerr-alo/
├── alo/
│   ├── agents/              # CrewAI-powered intelligent agents
│   │   ├── base_agent.py    # Base agent class
│   │   ├── sampler_agent.py # Intelligent sampling
│   │   ├── discovery_agent.py # Object discovery
│   │   └── validator_agent.py # Validation agents
│   ├── orchestrator/        # Workflow engine
│   ├── connectors/          # Labellerr SDK integration
│   ├── active_learning/     # Active learning strategies
│   └── utils/               # Utilities
├── examples/                # Example workflows
│   ├── intelligent_discovery_workflow.yaml
│   ├── image_classification_workflow.yaml
│   └── object_detection_workflow.yaml
└── tests/                   # Unit and integration tests
```

---

## 🗓️ Roadmap

### **✅ v0.1.0 - Foundation (Released)**
- [x] Core workflow orchestrator with YAML configs
- [x] Labellerr SDK integration (push/pull data)
- [x] Basic project structure and documentation
- [x] Example workflow templates

### **✅ v0.2.0 - Intelligent Discovery (Current Release)**
- [x] CrewAI agent framework integration
- [x] Intelligent sampling agent (5% dataset analysis)
- [x] **Object discovery agent** (auto-detect classes)
- [x] LLM validation agents (Claude, GPT-4)
- [x] Multi-model support (OpenAI, Anthropic, Roboflow, HuggingFace)
- [x] Comprehensive documentation (SDK vs ALO, PyPI guide)

### **🚧 v0.3.0 - Active Learning (In Progress) - Target: Feb 2026**
- [ ] **Active learning agents** (uncertainty, diversity, margin sampling)
- [ ] **Human review routing** (auto vs manual based on confidence)
- [ ] **Terminal monitoring dashboard** (progress tracking)
- [ ] Confidence threshold management
- [ ] Sample selection strategies
- [ ] Example notebooks and tutorials

### **🔮 v0.4.0 - Adaptive Retraining (Planned) - Target: Mar 2026**
- [ ] **Adaptive retraining workflows** (train → predict → select → retrain)
- [ ] Model training orchestration
- [ ] Performance tracking over iterations
- [ ] More pre-labeling agents (SAM, CLIP, LLaVA)
- [ ] Advanced validation strategies

### **🔮 v0.5.0 - Production Ready (Planned) - Target: Apr 2026**
- [ ] Web dashboard with real-time metrics
- [ ] Multi-user collaboration features
- [ ] Cloud deployment templates (AWS, GCP, Azure)
- [ ] API server mode
- [ ] Production deployment guides

### **🔮 v1.0.0 - Complete Vision (Planned) - Target: Q2 2026**
- [ ] Video labeling pipelines
- [ ] 3D point cloud support
- [ ] Multi-modal fusion (vision + language + audio)
- [ ] Automated hyperparameter tuning
- [ ] Enterprise features (SSO, audit logs)

---

### **🎯 Focus for Next Release (v0.3.0)**

The **critical missing piece** is active learning. This is what will complete the "agentic" nature:

```yaml
# Coming in v0.3.0
steps:
  - name: "select_uncertain_samples"
    agent: "uncertainty_sampler"
    parameters:
      strategy: "least_confident"
      batch_size: 100
  
  - name: "route_to_humans"
    action: "smart_routing"
    parameters:
      high_confidence: "auto_accept"
      low_confidence: "human_review"
      threshold: 0.85
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-agent`)
3. **Add your agent** (following CrewAI patterns)
4. **Write tests** (`pytest tests/`)
5. **Submit a Pull Request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built on [Labellerr SDK](https://github.com/tensormatics/SDKPython)
- Powered by [CrewAI](https://github.com/joaomdmoura/crewAI)
- Thanks to all contributors and the open-source community!

---

## 🌐 Open Source Initiative

ALO is more than just a tool - it's a **community-driven initiative** to make AI-powered labeling accessible to everyone:

### **Why Open Source?**

1. **Democratize AI Labeling**
   - Remove barriers to entry
   - Share best practices
   - Collaborative improvement

2. **Improve on SDK Experience**
   - SDK: 200+ lines of boilerplate
   - ALO: 3 lines + YAML config
   - [Read full comparison](docs/SDK_VS_ALO.md)

3. **Community Innovation**
   - Share custom agents
   - Contribute workflows
   - Build together

### **How to Contribute**

- **🌟 Star the repo** - Show your support
- **🐛 Report bugs** - Help us improve
- **💡 Suggest features** - Share your ideas
- **🔧 Submit PRs** - Add agents, fix bugs
- **📖 Improve docs** - Make it clearer
- **💬 Join discussions** - Help others

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📞 Support

- 📧 **Email**: support@labellerr.com
- 💬 **Discussions**: [GitHub Discussions](https://github.com/1sarthakbhardawaj/labellerr-alo/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/1sarthakbhardawaj/labellerr-alo/issues)
- 📖 **Docs**: [SDK vs ALO](docs/SDK_VS_ALO.md) | [PyPI Release Guide](docs/RELEASE_TO_PYPI.md)

---

<div align="center">

**⭐ Star us on GitHub — it motivates us a lot!**

**Made with ❤️ by the Labellerr team and open-source contributors**

[Website](https://labellerr.com) • [Documentation](https://docs.labellerr.com) • [Twitter](https://twitter.com/labellerr)

</div>

---

## 🎬 Demo

```bash
# Clone the repo
git clone https://github.com/1sarthakbhardawaj/labellerr-alo.git
cd labellerr-alo

# Install dependencies
pip install -e .

# Set up your API keys
export OPENAI_API_KEY="your-key"
export LABELLERR_API_KEY="your-key"
export LABELLERR_API_SECRET="your-secret"

# Run intelligent discovery on your dataset
python -m alo.cli run examples/intelligent_discovery_workflow.yaml

# Watch as ALO:
# 1. Samples 5% of your dataset (cost-effective!)
# 2. Discovers all object classes automatically
# 3. Labels your entire dataset
# 4. Validates with AI
# 5. Exports to Labellerr

# All in minutes! 🚀
```
