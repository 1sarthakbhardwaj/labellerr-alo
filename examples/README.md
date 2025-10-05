# ALO Workflow Examples

This directory contains example workflow configurations for common labeling scenarios.

## 📁 Available Examples

### 1. Image Classification (`image_classification_workflow.yaml`)
**Use Case**: Classify images into predefined categories

**Steps**:
- Pre-label with GPT-4V
- Validate classifications
- Select uncertain samples
- Push to Labellerr for review

**Best For**: Single-label or multi-label classification tasks

---

### 2. Object Detection (`object_detection_workflow.yaml`)
**Use Case**: Detect and localize objects in images

**Steps**:
- Detect objects with YOLO
- Refine masks with SAM
- Validate detections
- Export to Labellerr

**Best For**: Bounding box or instance segmentation tasks

---

### 3. Active Learning Loop (`active_learning_loop.yaml`)
**Use Case**: Continuous model improvement cycle

**Steps**:
- Pull labeled data from Labellerr
- Train model
- Predict on unlabeled pool
- Select most informative samples
- Push for labeling

**Best For**: Iterative dataset building and model improvement

---

## 🚀 How to Use

### 1. Configure Your Credentials

Create a `.env` file in the project root:

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 2. Customize Workflow Parameters

Edit the YAML file to match your project:

```yaml
parameters:
  project_id: "your_actual_project_id"
  confidence_threshold: 0.8
  # ... other parameters
```

### 3. Run the Workflow

```python
from alo import WorkflowOrchestrator
from alo.connectors import LabellerrConnector
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize connector
connector = LabellerrConnector(
    api_key=os.getenv("LABELLERR_API_KEY"),
    api_secret=os.getenv("LABELLERR_API_SECRET"),
    client_id=os.getenv("LABELLERR_CLIENT_ID")
)

# Load and run workflow
orchestrator = WorkflowOrchestrator("examples/image_classification_workflow.yaml")
results = orchestrator.run(connector=connector)

print(f"Workflow completed: {results}")
```

---

## 📝 Creating Custom Workflows

### Workflow Structure

```yaml
name: "your_workflow_name"
description: "Brief description of what this workflow does"

parameters:
  # Global parameters accessible in all steps
  project_id: "your_project_id"
  confidence_threshold: 0.8

steps:
  - name: "step_1"
    agent: "agent_name"  # or action: "action_name"
    parameters:
      # Step-specific parameters
      param1: value1
    depends_on:
      - "previous_step"  # Optional dependencies
```

### Available Actions

- `push_to_labellerr` - Push annotations to a project
- `pull_from_labellerr` - Pull annotations from a project

### Available Agents (Coming Soon)

- `gpt4v_classifier` - Image classification with GPT-4V
- `yolo_detector` - Object detection with YOLO
- `sam_segmenter` - Segmentation with SAM
- `llm_validator` - Validation with LLMs
- `uncertainty_sampler` - Active learning sample selection

---

## 💡 Tips

1. **Start Simple**: Begin with basic workflows and add complexity gradually
2. **Test First**: Use `dry_run=True` to validate without execution
3. **Monitor Progress**: Check logs for step-by-step execution details
4. **Iterate**: Adjust parameters based on results
5. **Share**: Contribute your workflows back to the community!

---

## 🤝 Contributing

Have a workflow that worked well for your use case? 

Please contribute it back:
1. Fork the repository
2. Add your workflow to this directory
3. Update this README
4. Submit a Pull Request

---

## 📚 More Information

- [Full Documentation](../docs/)
- [API Reference](../docs/api.md)
- [Contributing Guide](../CONTRIBUTING.md)
