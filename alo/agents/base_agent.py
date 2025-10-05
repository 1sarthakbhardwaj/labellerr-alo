"""
Base Agent class using CrewAI for modular, intelligent agents.
"""

import logging
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class BaseALOAgent(ABC):
    """
    Base class for all ALO agents using CrewAI framework.
    
    This provides a consistent interface for all intelligent agents
    while leveraging CrewAI's multi-agent orchestration capabilities.
    """
    
    def __init__(self, name: str, role: str, goal: str, backstory: str, **kwargs):
        """
        Initialize the base agent.
        
        Args:
            name: Agent identifier
            role: Agent's role in the system
            goal: What the agent aims to achieve
            backstory: Context about the agent's expertise
            **kwargs: Additional configuration
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.config = kwargs
        
        # Initialize LLM if needed
        self.llm = self._initialize_llm()
        
        # Create CrewAI agent
        self.crew_agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=kwargs.get('verbose', False),
            allow_delegation=kwargs.get('allow_delegation', False),
            llm=self.llm
        )
        
        logger.info(f"Initialized {self.name} agent with role: {role}")
    
    def _initialize_llm(self) -> Optional[Any]:
        """Initialize the language model for the agent."""
        model_provider = self.config.get('model_provider', 'openai')
        
        if model_provider == 'openai':
            return ChatOpenAI(
                model=self.config.get('model', 'gpt-4-turbo-preview'),
                temperature=self.config.get('temperature', 0.7),
                api_key=self.config.get('api_key')
            )
        elif model_provider == 'anthropic':
            # Add Anthropic support
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=self.config.get('model', 'claude-3-5-sonnet-20241022'),
                temperature=self.config.get('temperature', 0.7),
                api_key=self.config.get('api_key')
            )
        else:
            return None
    
    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task.
        
        Args:
            inputs: Input data for the agent
            
        Returns:
            Dictionary with agent's outputs
        """
        pass
    
    def create_task(self, description: str, expected_output: str) -> Task:
        """
        Create a CrewAI task for this agent.
        
        Args:
            description: Task description
            expected_output: What output is expected
            
        Returns:
            CrewAI Task object
        """
        return Task(
            description=description,
            expected_output=expected_output,
            agent=self.crew_agent
        )
    
    def run_crew(self, tasks: List[Task]) -> Dict[str, Any]:
        """
        Run a crew with this agent and given tasks.
        
        Args:
            tasks: List of tasks to execute
            
        Returns:
            Crew execution results
        """
        crew = Crew(
            agents=[self.crew_agent],
            tasks=tasks,
            verbose=self.config.get('verbose', False)
        )
        
        result = crew.kickoff()
        return {"status": "completed", "result": result}
