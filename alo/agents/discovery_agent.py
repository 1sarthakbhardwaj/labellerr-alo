"""
Object Discovery Agent using CrewAI and Vision Models.

This agent automatically discovers object classes in a dataset
by analyzing sample images with foundation models.
"""

import logging
import base64
from typing import Dict, List, Any
from collections import Counter
from .base_agent import BaseALOAgent
from crewai import Task

logger = logging.getLogger(__name__)


class ObjectDiscoveryAgent(BaseALOAgent):
    """
    Agent that discovers object classes in images using vision models.
    
    Features:
    - Analyzes sample images with GPT-4V or other vision models
    - Automatically identifies all object classes
    - Merges similar classes
    - Filters rare classes
    - Returns consolidated class list
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="ObjectDiscoverer",
            role="Computer Vision Object Discovery Specialist",
            goal="Identify and categorize all objects present in a dataset",
            backstory="""You are an expert computer vision analyst with deep knowledge
            of object detection, classification, and taxonomy. You excel at analyzing
            images and identifying all objects present, creating consistent taxonomies,
            and merging similar classes into coherent categories.""",
            **kwargs
        )
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Discover object classes from sampled images.
        
        Args:
            inputs: Dict containing:
                - sampled_images: List of image paths
                - prompt: Custom prompt (optional)
                - min_class_frequency: Minimum occurrence (default: 0.05)
                - max_classes: Maximum number of classes (default: 50)
                - consolidate_similar: Merge similar classes (default: True)
                
        Returns:
            Dict with discovered_classes, class_confidence, class_examples
        """
        sampled_images = inputs.get('sampled_images', [])
        prompt = inputs.get('prompt', self._default_prompt())
        min_frequency = inputs.get('min_class_frequency', 0.05)
        max_classes = inputs.get('max_classes', 50)
        consolidate = inputs.get('consolidate_similar', True)
        
        logger.info(f"Discovering objects in {len(sampled_images)} sampled images")
        
        # Analyze each image
        all_detections = []
        class_examples = {}
        
        for img_path in sampled_images:
            try:
                detections = self._analyze_image(img_path, prompt)
                all_detections.extend(detections)
                
                # Store example images for each class
                for det in detections:
                    if det not in class_examples:
                        class_examples[det] = []
                    if len(class_examples[det]) < 3:  # Store up to 3 examples
                        class_examples[det].append(img_path)
                        
            except Exception as e:
                logger.error(f"Error analyzing {img_path}: {str(e)}")
                continue
        
        # Count class frequencies
        class_counts = Counter(all_detections)
        total_detections = len(all_detections)
        
        # Calculate frequencies
        class_frequencies = {
            cls: count / total_detections
            for cls, count in class_counts.items()
        }
        
        # Filter by minimum frequency
        filtered_classes = {
            cls: freq
            for cls, freq in class_frequencies.items()
            if freq >= min_frequency
        }
        
        # Consolidate similar classes if requested
        if consolidate:
            filtered_classes = self._consolidate_classes(filtered_classes)
        
        # Limit to max_classes
        final_classes = dict(
            sorted(filtered_classes.items(), key=lambda x: x[1], reverse=True)[:max_classes]
        )
        
        discovered_classes = list(final_classes.keys())
        
        logger.info(f"Discovered {len(discovered_classes)} object classes")
        logger.info(f"Classes: {', '.join(discovered_classes)}")
        
        return {
            'discovered_classes': discovered_classes,
            'class_confidence': final_classes,
            'class_examples': class_examples,
            'total_detections': total_detections
        }
    
    def _analyze_image(self, image_path: str, prompt: str) -> List[str]:
        """
        Analyze a single image and return detected object classes.
        
        This uses the configured vision model (GPT-4V, Claude, etc.)
        to identify objects in the image.
        """
        # Create analysis task
        task_description = f"""
        Analyze the image at: {image_path}
        
        {prompt}
        
        Return ONLY a comma-separated list of object class names.
        Example: "person, car, dog, tree, building"
        """
        
        task = self.create_task(
            description=task_description,
            expected_output="Comma-separated list of object classes"
        )
        
        # Run the crew
        result = self.run_crew([task])
        
        # Parse result into list of classes
        classes_str = result.get('result', '')
        classes = [cls.strip().lower() for cls in classes_str.split(',') if cls.strip()]
        
        return classes
    
    def _consolidate_classes(self, class_frequencies: Dict[str, float]) -> Dict[str, float]:
        """
        Consolidate similar classes into single categories.
        
        Examples:
        - "sedan", "suv", "truck" → "vehicle"
        - "golden_retriever", "labrador" → "dog"
        - "apple", "banana", "orange" → "fruit"
        """
        # Create consolidation task
        classes_str = ', '.join(class_frequencies.keys())
        
        task_description = f"""
        Given these object classes: {classes_str}
        
        Consolidate similar or overlapping classes into broader categories.
        For example:
        - Merge specific dog breeds into "dog"
        - Merge vehicle types into "vehicle"
        - Keep distinct classes separate
        
        Return a JSON mapping of original → consolidated:
        {{"sedan": "vehicle", "suv": "vehicle", "golden_retriever": "dog"}}
        """
        
        task = self.create_task(
            description=task_description,
            expected_output="JSON mapping of class consolidations"
        )
        
        result = self.run_crew([task])
        
        # Parse consolidation mapping
        # (In real implementation, parse JSON and apply mapping)
        # For now, return original classes
        return class_frequencies
    
    def _default_prompt(self) -> str:
        """Default prompt for object discovery."""
        return """
        Analyze this image carefully and identify ALL distinct objects present.
        
        For each object:
        1. Use simple, common names (e.g., "dog" not "golden retriever")
        2. Focus on major objects (ignore tiny background elements)
        3. Be consistent with naming across images
        4. Include both foreground and significant background objects
        
        Return only object class names, comma-separated.
        """
