"""
Intelligent Sampling Agent using CrewAI.

This agent intelligently samples datasets to discover object classes
without processing the entire dataset.
"""

import os
import random
import logging
from typing import Dict, List, Any
from pathlib import Path
from .base_agent import BaseALOAgent

logger = logging.getLogger(__name__)


class IntelligentSamplerAgent(BaseALOAgent):
    """
    Agent that intelligently samples datasets for discovery.
    
    Features:
    - Samples 5% of dataset or minimum 2 images
    - Uses diverse sampling strategies
    - Considers temporal, visual, and metadata diversity
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="IntelligentSampler",
            role="Dataset Sampling Specialist",
            goal="Select representative samples from large datasets efficiently",
            backstory="""You are an expert in statistical sampling and dataset analysis.
            Your specialty is identifying the most informative samples that represent
            the diversity of a large dataset while minimizing computational cost.""",
            **kwargs
        )
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute intelligent sampling on the dataset.
        
        Args:
            inputs: Dict containing:
                - dataset_path: Path to dataset
                - sample_percentage: Percentage to sample (default: 0.05)
                - min_samples: Minimum number of samples (default: 2)
                - max_samples: Maximum number of samples (default: 100)
                - strategy: Sampling strategy (default: 'diverse')
                
        Returns:
            Dict with sampled_images and sampling_metadata
        """
        dataset_path = inputs.get('dataset_path')
        sample_percentage = inputs.get('sample_percentage', 0.05)
        min_samples = inputs.get('min_samples', 2)
        max_samples = inputs.get('max_samples', 100)
        strategy = inputs.get('strategy', 'diverse')
        
        logger.info(f"Starting intelligent sampling of {dataset_path}")
        
        # Get all images from dataset
        all_images = self._get_all_images(dataset_path)
        total_images = len(all_images)
        
        logger.info(f"Found {total_images} images in dataset")
        
        # Calculate sample size
        sample_size = max(
            min_samples,
            min(int(total_images * sample_percentage), max_samples)
        )
        
        logger.info(f"Sampling {sample_size} images ({sample_size/total_images*100:.2f}%)")
        
        # Apply sampling strategy
        if strategy == 'diverse':
            sampled_images = self._diverse_sampling(all_images, sample_size)
        elif strategy == 'random':
            sampled_images = random.sample(all_images, sample_size)
        elif strategy == 'temporal':
            sampled_images = self._temporal_sampling(all_images, sample_size)
        else:
            sampled_images = random.sample(all_images, sample_size)
        
        metadata = {
            'total_images': total_images,
            'sampled_count': len(sampled_images),
            'sample_percentage': len(sampled_images) / total_images,
            'strategy': strategy
        }
        
        logger.info(f"Sampling complete: {len(sampled_images)} images selected")
        
        return {
            'sampled_images': sampled_images,
            'sampling_metadata': metadata
        }
    
    def _get_all_images(self, dataset_path: str) -> List[str]:
        """Get all image files from dataset path."""
        dataset_dir = Path(dataset_path)
        
        # Supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        
        images = []
        for ext in image_extensions:
            images.extend([str(p) for p in dataset_dir.rglob(f'*{ext}')])
        
        return sorted(images)
    
    def _diverse_sampling(self, images: List[str], sample_size: int) -> List[str]:
        """
        Sample images with diversity (spread evenly across dataset).
        
        This ensures temporal and spatial diversity by sampling
        at regular intervals across the dataset.
        """
        if len(images) <= sample_size:
            return images
        
        # Sample at regular intervals for diversity
        interval = len(images) // sample_size
        sampled = []
        
        for i in range(sample_size):
            idx = (i * interval) + (interval // 2)  # Middle of each interval
            if idx < len(images):
                sampled.append(images[idx])
        
        return sampled
    
    def _temporal_sampling(self, images: List[str], sample_size: int) -> List[str]:
        """
        Sample images based on temporal diversity (file timestamps).
        """
        # Sort by modification time
        images_with_time = [(img, os.path.getmtime(img)) for img in images]
        images_with_time.sort(key=lambda x: x[1])
        
        # Sample at regular time intervals
        return self._diverse_sampling([img for img, _ in images_with_time], sample_size)
