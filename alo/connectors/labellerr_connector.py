"""
Labellerr Connector - Integration with Labellerr platform via SDK.
"""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

try:
    from labellerr.client import LabellerrClient
    from labellerr.exceptions import LabellerrError
except ImportError:
    raise ImportError(
        "Labellerr SDK is required. Install with: pip install labellerr-sdk"
    )

logger = logging.getLogger(__name__)


class LabellerrConnector:
    """
    Connector for seamless integration with Labellerr platform.
    
    This class wraps the Labellerr SDK and provides high-level methods
    for common labeling workflow operations.
    
    Args:
        api_key: Labellerr API key
        api_secret: Labellerr API secret
        client_id: Labellerr client ID
        
    Example:
        >>> connector = LabellerrConnector(
        ...     api_key="your_key",
        ...     api_secret="your_secret",
        ...     client_id="your_client_id"
        ... )
        >>> connector.push_preannotations(project_id, annotations)
    """
    
    def __init__(self, api_key: str, api_secret: str, client_id: Optional[str] = None):
        """Initialize the connector with Labellerr credentials."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.client_id = client_id
        
        self.client = LabellerrClient(
            api_key=api_key,
            api_secret=api_secret,
            enable_connection_pooling=True
        )
        
        logger.info("Labellerr connector initialized")
    
    def create_project(
        self,
        project_name: str,
        data_type: str,
        annotation_guide: List[Dict[str, Any]],
        dataset_config: Optional[Dict[str, Any]] = None,
        folder_to_upload: Optional[str] = None,
        files_to_upload: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new labeling project on Labellerr.
        
        Args:
            project_name: Name of the project
            data_type: Type of data ('image', 'video', 'audio', 'document', 'text')
            annotation_guide: List of annotation questions/guidelines
            dataset_config: Dataset configuration (optional)
            folder_to_upload: Path to folder with files (optional)
            files_to_upload: List of file paths (optional)
            
        Returns:
            Dictionary with project details including project_id
        """
        if not self.client_id:
            raise ValueError("client_id is required to create projects")
        
        payload = {
            "client_id": self.client_id,
            "project_name": project_name,
            "data_type": data_type,
            "annotation_guide": annotation_guide,
            "dataset_name": dataset_config.get("name", f"{project_name}_dataset") if dataset_config else f"{project_name}_dataset",
            "dataset_description": dataset_config.get("description", "") if dataset_config else "",
            "created_by": dataset_config.get("created_by", self.api_key) if dataset_config else self.api_key,
            "autolabel": False,
            "rotation_config": {
                "annotation_rotation_count": 1,
                "review_rotation_count": 1,
                "client_review_rotation_count": 0,
            }
        }
        
        if folder_to_upload:
            payload["folder_to_upload"] = folder_to_upload
        elif files_to_upload:
            payload["files_to_upload"] = files_to_upload
        else:
            raise ValueError("Either folder_to_upload or files_to_upload must be provided")
        
        try:
            result = self.client.initiate_create_project(payload)
            logger.info(f"Project created successfully: {result.get('project_id')}")
            return result
        except LabellerrError as e:
            logger.error(f"Failed to create project: {str(e)}")
            raise
    
    def push_preannotations(
        self,
        project_id: str,
        annotation_file: str,
        annotation_format: str = "coco_json",
        async_mode: bool = False,
    ) -> Dict[str, Any]:
        """
        Push pre-annotations to a Labellerr project.
        
        Args:
            project_id: ID of the target project
            annotation_file: Path to annotation file
            annotation_format: Format of annotations ('coco_json', 'json', etc.)
            async_mode: If True, use async upload (non-blocking)
            
        Returns:
            Dictionary with upload status
        """
        if not self.client_id:
            raise ValueError("client_id is required to push annotations")
        
        annotation_path = Path(annotation_file)
        if not annotation_path.exists():
            raise FileNotFoundError(f"Annotation file not found: {annotation_file}")
        
        try:
            if async_mode:
                logger.info(f"Starting async pre-annotation upload to project {project_id}")
                future = self.client.upload_preannotation_by_project_id_async(
                    project_id=project_id,
                    client_id=self.client_id,
                    annotation_format=annotation_format,
                    annotation_file=str(annotation_path),
                )
                result = future.result(timeout=600)  # 10 minutes timeout
            else:
                logger.info(f"Starting sync pre-annotation upload to project {project_id}")
                result = self.client.upload_preannotation_by_project_id(
                    project_id=project_id,
                    client_id=self.client_id,
                    annotation_format=annotation_format,
                    annotation_file=str(annotation_path),
                )
            
            logger.info("Pre-annotations uploaded successfully")
            return result
        except LabellerrError as e:
            logger.error(f"Failed to upload pre-annotations: {str(e)}")
            raise
    
    def pull_annotations(
        self,
        project_id: str,
        export_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Pull annotations from a Labellerr project.
        
        Args:
            project_id: ID of the project
            export_config: Export configuration (optional)
            
        Returns:
            Dictionary with export details
        """
        if not self.client_id:
            raise ValueError("client_id is required to pull annotations")
        
        if not export_config:
            export_config = {
                "export_name": f"ALO_Export_{project_id}",
                "export_description": "Export triggered by ALO",
                "export_format": "json",
                "statuses": ["accepted"]
            }
        
        try:
            logger.info(f"Creating export for project {project_id}")
            result = self.client.create_local_export(
                project_id=project_id,
                client_id=self.client_id,
                export_config=export_config,
            )
            logger.info("Export created successfully")
            return result
        except LabellerrError as e:
            logger.error(f"Failed to create export: {str(e)}")
            raise
    
    def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Get all projects for the client.
        
        Returns:
            List of project dictionaries
        """
        if not self.client_id:
            raise ValueError("client_id is required to get projects")
        
        try:
            result = self.client.get_all_project_per_client_id(self.client_id)
            projects = result.get("response", [])
            logger.info(f"Retrieved {len(projects)} projects")
            return projects
        except LabellerrError as e:
            logger.error(f"Failed to retrieve projects: {str(e)}")
            raise
    
    def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project dictionary or None if not found
        """
        projects = self.get_all_projects()
        for project in projects:
            if project.get("project_id") == project_id:
                return project
        return None
    
    def close(self):
        """Close the connector and cleanup resources."""
        self.client.close()
        logger.info("Labellerr connector closed")
