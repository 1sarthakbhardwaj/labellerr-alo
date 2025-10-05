"""
Agentic Labeling Orchestrator (ALO)
====================================

An open-source framework for orchestrating end-to-end data labeling workflows
using autonomous AI agents.

Basic Usage:
    >>> from alo import WorkflowOrchestrator
    >>> from alo.connectors import LabellerrConnector
    >>> 
    >>> connector = LabellerrConnector(api_key="...", api_secret="...")
    >>> orchestrator = WorkflowOrchestrator("workflow.yaml")
    >>> orchestrator.run(connector=connector)

Main Components:
    - WorkflowOrchestrator: Manages pipeline execution
    - LabellerrConnector: Integration with Labellerr platform
    - Agents: Pre-labeling with foundation models
    - Validators: Quality assurance modules
    - ActiveLearning: Intelligent sample selection
"""

__version__ = "0.1.0"
__author__ = "Labellerr Team"
__license__ = "Apache-2.0"

from alo.orchestrator.workflow import WorkflowOrchestrator
from alo.connectors.labellerr_connector import LabellerrConnector

__all__ = [
    "WorkflowOrchestrator",
    "LabellerrConnector",
    "__version__",
]
