"""
Validation Agent using CrewAI and LLMs.

This agent validates predictions for quality, consistency, and correctness.
"""

import logging
from typing import Dict, List, Any
from .base_agent import BaseALOAgent
from crewai import Task

logger = logging.getLogger(__name__)


class LLMValidatorAgent(BaseALOAgent):
    """
    Agent that validates predictions using LLMs.
    
    Features:
    - Checks prediction quality and consistency
    - Validates against expected classes
    - Flags low-confidence predictions
    - Identifies potential errors
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="LLMValidator",
            role="Quality Assurance and Validation Specialist",
            goal="Ensure high-quality, consistent, and accurate predictions",
            backstory="""You are an expert in data quality assurance with deep
            understanding of machine learning predictions, annotation standards,
            and consistency validation. You excel at identifying errors, 
            inconsistencies, and quality issues in automated predictions.""",
            **kwargs
        )
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate predictions for quality and consistency.
        
        Args:
            inputs: Dict containing:
                - predictions: List of predictions to validate
                - expected_classes: List of valid class names
                - min_confidence: Minimum confidence threshold
                - consistency_check: Enable consistency validation
                
        Returns:
            Dict with validation_results, flagged_predictions, quality_score
        """
        predictions = inputs.get('predictions', [])
        expected_classes = inputs.get('expected_classes', [])
        min_confidence = inputs.get('min_confidence', 0.6)
        consistency_check = inputs.get('consistency_check', True)
        
        logger.info(f"Validating {len(predictions)} predictions")
        
        validation_results = {
            'total_predictions': len(predictions),
            'valid_predictions': 0,
            'flagged_predictions': [],
            'validation_issues': []
        }
        
        for i, pred in enumerate(predictions):
            issues = []
            
            # Check confidence
            confidence = pred.get('confidence', 1.0)
            if confidence < min_confidence:
                issues.append(f"Low confidence: {confidence:.2f}")
            
            # Check if class is in expected classes
            pred_class = pred.get('class', '')
            if expected_classes and pred_class not in expected_classes:
                issues.append(f"Unexpected class: {pred_class}")
            
            # Consistency checks
            if consistency_check:
                consistency_issues = self._check_consistency(pred, predictions)
                issues.extend(consistency_issues)
            
            if issues:
                validation_results['flagged_predictions'].append({
                    'prediction_index': i,
                    'prediction': pred,
                    'issues': issues
                })
            else:
                validation_results['valid_predictions'] += 1
        
        # Calculate quality score
        quality_score = (
            validation_results['valid_predictions'] / 
            validation_results['total_predictions']
        ) if predictions else 0.0
        
        validation_results['quality_score'] = quality_score
        
        logger.info(f"Validation complete: Quality score = {quality_score:.2%}")
        logger.info(f"Flagged {len(validation_results['flagged_predictions'])} predictions")
        
        return validation_results
    
    def _check_consistency(
        self, 
        pred: Dict[str, Any], 
        all_predictions: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Check for consistency issues in predictions.
        
        Examples:
        - Multiple conflicting classes for same region
        - Overlapping bounding boxes with different classes
        - Unusual class combinations
        """
        issues = []
        
        # Check for overlapping predictions
        if 'bbox' in pred:
            overlaps = self._find_overlapping_boxes(pred, all_predictions)
            if overlaps:
                issues.append(f"Overlaps with {len(overlaps)} other predictions")
        
        return issues
    
    def _find_overlapping_boxes(
        self, 
        pred: Dict[str, Any], 
        all_predictions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Find predictions with overlapping bounding boxes."""
        overlaps = []
        pred_bbox = pred.get('bbox')
        
        if not pred_bbox:
            return overlaps
        
        for other_pred in all_predictions:
            if other_pred == pred:
                continue
            
            other_bbox = other_pred.get('bbox')
            if other_bbox and self._boxes_overlap(pred_bbox, other_bbox):
                overlaps.append(other_pred)
        
        return overlaps
    
    def _boxes_overlap(self, bbox1: List[float], bbox2: List[float]) -> bool:
        """Check if two bounding boxes overlap."""
        # bbox format: [x, y, width, height]
        x1, y1, w1, h1 = bbox1
        x2, y2, w2, h2 = bbox2
        
        # Check if boxes overlap
        return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)


class EnsembleValidatorAgent(BaseALOAgent):
    """
    Agent that validates using ensemble of multiple strategies.
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="EnsembleValidator",
            role="Multi-Strategy Validation Expert",
            goal="Validate predictions using multiple validation strategies",
            backstory="""You are an expert in ensemble validation techniques,
            combining multiple validation approaches to achieve robust quality
            assurance. You understand statistical validation, rule-based checks,
            and ML-based validation.""",
            **kwargs
        )
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate using ensemble of strategies.
        
        Args:
            inputs: Dict containing:
                - predictions: Predictions to validate
                - strategies: List of strategies to use
                
        Returns:
            Dict with ensemble validation results
        """
        predictions = inputs.get('predictions', [])
        strategies = inputs.get('strategies', ['confidence', 'consistency', 'statistical'])
        
        logger.info(f"Running ensemble validation with strategies: {strategies}")
        
        results = {
            'total_predictions': len(predictions),
            'strategy_results': {},
            'consensus_valid': 0,
            'consensus_invalid': 0
        }
        
        # Run each validation strategy
        for strategy in strategies:
            strategy_result = self._run_strategy(strategy, predictions)
            results['strategy_results'][strategy] = strategy_result
        
        # Calculate consensus
        # (Prediction is valid only if all strategies agree)
        for i in range(len(predictions)):
            all_valid = all(
                results['strategy_results'][s].get('valid_indices', set()) 
                and i in results['strategy_results'][s]['valid_indices']
                for s in strategies
            )
            
            if all_valid:
                results['consensus_valid'] += 1
            else:
                results['consensus_invalid'] += 1
        
        results['consensus_score'] = (
            results['consensus_valid'] / len(predictions)
        ) if predictions else 0.0
        
        logger.info(f"Ensemble validation complete: {results['consensus_score']:.2%} valid")
        
        return results
    
    def _run_strategy(self, strategy: str, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run a specific validation strategy."""
        if strategy == 'confidence':
            return self._confidence_validation(predictions)
        elif strategy == 'consistency':
            return self._consistency_validation(predictions)
        elif strategy == 'statistical':
            return self._statistical_validation(predictions)
        else:
            return {'valid_indices': set()}
    
    def _confidence_validation(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate based on confidence scores."""
        threshold = 0.7
        valid_indices = {
            i for i, pred in enumerate(predictions)
            if pred.get('confidence', 0) >= threshold
        }
        return {'valid_indices': valid_indices, 'threshold': threshold}
    
    def _consistency_validation(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate based on consistency checks."""
        # Implementation of consistency validation
        valid_indices = set(range(len(predictions)))  # Placeholder
        return {'valid_indices': valid_indices}
    
    def _statistical_validation(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate based on statistical analysis."""
        # Implementation of statistical validation
        valid_indices = set(range(len(predictions)))  # Placeholder
        return {'valid_indices': valid_indices}
