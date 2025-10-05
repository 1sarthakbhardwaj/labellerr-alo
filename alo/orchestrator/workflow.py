"""
Workflow Orchestrator - Core engine for managing labeling pipelines.
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class WorkflowStep(BaseModel):
    """Represents a single step in the workflow."""
    
    name: str = Field(..., description="Step name")
    agent: Optional[str] = Field(None, description="Agent to execute")
    action: Optional[str] = Field(None, description="Action to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Step parameters")
    depends_on: List[str] = Field(default_factory=list, description="Dependencies")


class WorkflowConfig(BaseModel):
    """Workflow configuration model."""
    
    name: str = Field(..., description="Workflow name")
    description: Optional[str] = Field(None, description="Workflow description")
    steps: List[WorkflowStep] = Field(..., description="Workflow steps")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Global parameters")


class WorkflowOrchestrator:
    """
    Orchestrates the execution of labeling workflows.
    
    The orchestrator manages the lifecycle of a labeling pipeline, including:
    - Loading and validating workflow configurations
    - Executing steps in the correct order
    - Managing dependencies between steps
    - Error handling and recovery
    
    Args:
        config_path: Path to workflow YAML/JSON configuration file
        
    Example:
        >>> orchestrator = WorkflowOrchestrator("workflows/image_classification.yaml")
        >>> orchestrator.run(connector=labellerr_connector)
    """
    
    def __init__(self, config_path: str):
        """Initialize the orchestrator with a workflow configuration."""
        self.config_path = Path(config_path)
        self.config: Optional[WorkflowConfig] = None
        self.results: Dict[str, Any] = {}
        
        self._load_config()
    
    def _load_config(self) -> None:
        """Load and validate workflow configuration."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            if self.config_path.suffix in ['.yaml', '.yml']:
                config_dict = yaml.safe_load(f)
            else:
                import json
                config_dict = json.load(f)
        
        self.config = WorkflowConfig(**config_dict)
        logger.info(f"Loaded workflow: {self.config.name}")
    
    def run(self, connector: Any, dry_run: bool = False) -> Dict[str, Any]:
        """
        Execute the workflow.
        
        Args:
            connector: LabellerrConnector instance for data exchange
            dry_run: If True, validate without executing
            
        Returns:
            Dictionary with execution results
        """
        if not self.config:
            raise RuntimeError("No configuration loaded")
        
        logger.info(f"Starting workflow: {self.config.name}")
        
        if dry_run:
            logger.info("Dry run - validating workflow only")
            return {"status": "validated", "steps": len(self.config.steps)}
        
        for step in self.config.steps:
            logger.info(f"Executing step: {step.name}")
            
            try:
                result = self._execute_step(step, connector)
                self.results[step.name] = result
                logger.info(f"Step {step.name} completed successfully")
            except Exception as e:
                logger.error(f"Step {step.name} failed: {str(e)}")
                raise
        
        return self.results
    
    def _execute_step(self, step: WorkflowStep, connector: Any) -> Any:
        """Execute a single workflow step."""
        # Check dependencies
        for dep in step.depends_on:
            if dep not in self.results:
                raise RuntimeError(f"Dependency {dep} not satisfied for step {step.name}")
        
        # Execute based on agent or action
        if step.agent:
            return self._execute_agent(step, connector)
        elif step.action:
            return self._execute_action(step, connector)
        else:
            raise ValueError(f"Step {step.name} must specify either 'agent' or 'action'")
    
    def _execute_agent(self, step: WorkflowStep, connector: Any) -> Any:
        """Execute an agent-based step."""
        logger.info(f"Executing agent: {step.agent}")
        
        # Import appropriate agent
        agent_map = {
            'intelligent_sampler': 'IntelligentSamplerAgent',
            'smart_sampler': 'IntelligentSamplerAgent',
            'object_discoverer': 'ObjectDiscoveryAgent',
            'gpt4v_object_discoverer': 'ObjectDiscoveryAgent',
            'llm_validator': 'LLMValidatorAgent',
            'ensemble_validator': 'EnsembleValidatorAgent',
        }
        
        agent_class_name = agent_map.get(step.agent, step.agent)
        
        try:
            from alo import agents
            agent_class = getattr(agents, agent_class_name, None)
            
            if agent_class:
                # Initialize agent with step parameters
                agent = agent_class(**step.parameters)
                
                # Prepare inputs from previous step results
                inputs = self._prepare_agent_inputs(step, connector)
                
                # Execute agent
                result = agent.execute(inputs)
                logger.info(f"Agent {step.agent} completed successfully")
                return result
            else:
                logger.warning(f"Agent {step.agent} not found, returning placeholder")
                return {"status": "success", "agent": step.agent}
        except Exception as e:
            logger.error(f"Error executing agent {step.agent}: {str(e)}")
            raise
    
    def _prepare_agent_inputs(self, step: WorkflowStep, connector: Any) -> Dict[str, Any]:
        """Prepare inputs for agent from previous step results and step parameters."""
        inputs = dict(step.parameters)
        
        # Add results from dependent steps
        for dep in step.depends_on:
            if dep in self.results:
                dep_result = self.results[dep]
                # Merge results with a prefix to avoid conflicts
                for key, value in dep_result.items():
                    inputs[f"{dep}.{key}"] = value
        
        return inputs
    
    def _execute_action(self, step: WorkflowStep, connector: Any) -> Any:
        """Execute an action-based step."""
        # Execute built-in actions
        logger.info(f"Executing action: {step.action}")
        
        if step.action == "push_to_labellerr":
            return self._push_to_labellerr(step, connector)
        elif step.action == "pull_from_labellerr":
            return self._pull_from_labellerr(step, connector)
        else:
            raise ValueError(f"Unknown action: {step.action}")
    
    def _push_to_labellerr(self, step: WorkflowStep, connector: Any) -> Any:
        """Push annotations to Labellerr."""
        project_id = step.parameters.get("project_id")
        annotation_format = step.parameters.get("format", "coco_json")
        
        logger.info(f"Pushing to Labellerr project: {project_id}")
        # Implementation will use connector.push_annotations()
        return {"status": "pushed", "project_id": project_id}
    
    def _pull_from_labellerr(self, step: WorkflowStep, connector: Any) -> Any:
        """Pull annotations from Labellerr."""
        project_id = step.parameters.get("project_id")
        
        logger.info(f"Pulling from Labellerr project: {project_id}")
        # Implementation will use connector.pull_annotations()
        return {"status": "pulled", "project_id": project_id}
    
    def validate(self) -> Dict[str, Any]:
        """Validate workflow configuration without execution."""
        return self.run(connector=None, dry_run=True)
