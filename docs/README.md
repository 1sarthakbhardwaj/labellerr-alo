# 📚 ALO Documentation

Welcome to the Agentic Labeling Orchestrator (ALO) documentation!

## 📖 Documentation Index

### **Getting Started**
- [Main README](../README.md) - Project overview, quick start, features
- [Installation Guide](../README.md#installation) - How to install ALO
- [Quick Start Tutorial](../README.md#quick-start) - Your first pipeline in 5 minutes

### **Understanding ALO**
- [SDK vs ALO](SDK_VS_ALO.md) - **Why ALO exists** and how it improves SDK experience
  - Problem with direct SDK usage (200+ lines of boilerplate)
  - ALO solution (3 lines + YAML)
  - Real-world comparisons
  - When to use what

### **Usage Guides**
- [Example Workflows](../examples/README.md) - Pre-built workflow templates
  - Image Classification
  - Object Detection
  - Intelligent Discovery
  - Active Learning

### **Agent Documentation**
- [Base Agent](../alo/agents/base_agent.py) - Foundation for all agents
- [Intelligent Sampler](../alo/agents/sampler_agent.py) - Smart dataset sampling
- [Object Discovery](../alo/agents/discovery_agent.py) - Auto-discover classes
- [Validators](../alo/agents/validator_agent.py) - Quality assurance agents

### **Workflow Configuration**
- [YAML Workflow Syntax](../examples/intelligent_discovery_workflow.yaml) - Complete example
- [Agent Parameters](#) - Configuration options for each agent
- [Actions Reference](#) - Built-in actions (push/pull to Labellerr)

### **Development**
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [PyPI Release Guide](RELEASE_TO_PYPI.md) - **How to release to PyPI**
  - Build and package
  - Upload to PyPI
  - Version management
  - Post-release checklist

### **API Reference**
- [WorkflowOrchestrator](../alo/orchestrator/workflow.py) - Main orchestration engine
- [LabellerrConnector](../alo/connectors/labellerr_connector.py) - SDK integration
- [Agent API](#) - Creating custom agents

---

## 🎯 Quick Links

### **For First-Time Users**
1. Read [SDK vs ALO](SDK_VS_ALO.md) to understand the value
2. Follow [Quick Start](../README.md#quick-start)
3. Try [Example Workflows](../examples/README.md)

### **For Contributors**
1. Read [Contributing Guide](../CONTRIBUTING.md)
2. Check [Development Setup](../README.md#development)
3. See [Agent Creation Guide](#) (coming soon)

### **For Maintainers**
1. Follow [PyPI Release Guide](RELEASE_TO_PYPI.md)
2. Update [Changelog](../CHANGELOG.md)
3. Create [GitHub Releases](#)

---

## 📝 Documentation Principles

Our documentation follows these principles:

1. **Clear Examples** - Every feature has a working example
2. **Real-World Use Cases** - Show practical applications
3. **Progressive Disclosure** - Start simple, add complexity gradually
4. **Comparison with Alternatives** - Show why ALO is better
5. **Community-Driven** - Improve based on user feedback

---

## 🤝 Improving Documentation

Found something unclear? Want to add examples?

- **Open an Issue**: [GitHub Issues](https://github.com/1sarthakbhardawaj/labellerr-alo/issues)
- **Submit a PR**: Improve docs directly
- **Ask in Discussions**: [GitHub Discussions](https://github.com/1sarthakbhardawaj/labellerr-alo/discussions)

---

## 🌟 Highlights

### **Most Important Docs**

1. **[SDK vs ALO](SDK_VS_ALO.md)** ⭐
   - Understand why ALO exists
   - See the dramatic difference (200 lines → 3 lines)
   - Real-world examples

2. **[PyPI Release Guide](RELEASE_TO_PYPI.md)** ⭐
   - Complete release process
   - Step-by-step checklist
   - Troubleshooting tips

3. **[Example Workflows](../examples/README.md)** ⭐
   - Ready-to-use templates
   - Common use cases
   - Customization guides

---

## 🔜 Coming Soon

- **Advanced Agent Guide** - Creating custom agents with CrewAI
- **Best Practices** - Production deployment tips
- **Performance Tuning** - Optimize your pipelines
- **Troubleshooting Guide** - Common issues and solutions
- **API Reference** - Complete API documentation
- **Video Tutorials** - Visual walkthroughs

---

## 📧 Questions?

- **Email**: support@labellerr.com
- **Discussions**: [GitHub Discussions](https://github.com/1sarthakbhardawaj/labellerr-alo/discussions)
- **Issues**: [GitHub Issues](https://github.com/1sarthakbhardawaj/labellerr-alo/issues)

---

<div align="center">

**Made with ❤️ by the Labellerr team and open-source contributors**

[Star on GitHub](https://github.com/1sarthakbhardawaj/labellerr-alo) • [Report Bug](https://github.com/1sarthakbhardawaj/labellerr-alo/issues) • [Request Feature](https://github.com/1sarthakbhardawaj/labellerr-alo/issues)

</div>
