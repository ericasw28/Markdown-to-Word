"""
Template Manager for Header/Footer Templates
Handles loading, saving, and managing header/footer templates
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class TemplateManager:
    """Manages header/footer templates"""

    def __init__(self, template_path: Optional[str] = None):
        """
        Initialize template manager

        Args:
            template_path: Path to template JSON file. If None, uses default location.
        """
        if template_path is None:
            # Default to config/header_footer_template.json in project root
            project_root = Path(__file__).parent.parent
            template_path = project_root / "config" / "header_footer_template.json"

        self.template_path = Path(template_path)
        self.template_data = self._load_template()

    def _load_template(self) -> Dict[str, Any]:
        """Load template from JSON file"""
        try:
            if self.template_path.exists():
                with open(self.template_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Return default template if file doesn't exist
                return self._get_default_template()
        except Exception as e:
            print(f"Error loading template: {e}")
            return self._get_default_template()

    def _get_default_template(self) -> Dict[str, Any]:
        """Return default template structure"""
        return {
            "current_preset": "professional",
            "presets": {
                "professional": {
                    "name": "Professional",
                    "description": "Clean professional layout",
                    "enabled": True,
                    "header": {
                        "left": "{title}",
                        "center": "",
                        "right": "{date}"
                    },
                    "footer": {
                        "left": "Page {page} of {total}",
                        "center": "",
                        "right": "{author}"
                    },
                    "style": {
                        "font_size": "10pt",
                        "separator_line": True
                    }
                }
            },
            "default_variables": {
                "title": "Untitled Document",
                "author": "Anonymous",
                "company": "",
                "version": "1.0",
                "date": "{current_date}",
                "time": "{current_time}"
            }
        }

    def save_template(self) -> bool:
        """Save current template data to file"""
        try:
            # Ensure directory exists
            self.template_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.template_path, 'w', encoding='utf-8') as f:
                json.dump(self.template_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False

    def get_current_preset(self) -> str:
        """Get the name of the current preset"""
        return self.template_data.get("current_preset", "professional")

    def set_current_preset(self, preset_name: str) -> bool:
        """
        Set the current preset

        Args:
            preset_name: Name of the preset to activate

        Returns:
            True if successful, False if preset doesn't exist
        """
        if preset_name in self.template_data.get("presets", {}):
            self.template_data["current_preset"] = preset_name
            return True
        return False

    def get_preset(self, preset_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a specific preset or the current one

        Args:
            preset_name: Name of preset to get. If None, returns current preset.

        Returns:
            Preset dictionary
        """
        if preset_name is None:
            preset_name = self.get_current_preset()

        return self.template_data.get("presets", {}).get(preset_name, {})

    def get_all_presets(self) -> Dict[str, Dict[str, Any]]:
        """Get all available presets"""
        return self.template_data.get("presets", {})

    def update_preset(self, preset_name: str, preset_data: Dict[str, Any]) -> bool:
        """
        Update a preset's configuration

        Args:
            preset_name: Name of the preset to update
            preset_data: New preset data

        Returns:
            True if successful
        """
        if "presets" not in self.template_data:
            self.template_data["presets"] = {}

        self.template_data["presets"][preset_name] = preset_data
        return True

    def get_default_variables(self) -> Dict[str, str]:
        """Get default variable values"""
        return self.template_data.get("default_variables", {})

    def update_default_variables(self, variables: Dict[str, str]) -> bool:
        """
        Update default variable values

        Args:
            variables: Dictionary of variable names and values

        Returns:
            True if successful
        """
        if "default_variables" not in self.template_data:
            self.template_data["default_variables"] = {}

        self.template_data["default_variables"].update(variables)
        return True

    def get_preset_names(self) -> list:
        """Get list of all preset names"""
        return list(self.template_data.get("presets", {}).keys())

    def create_custom_preset(self, name: str, description: str,
                            header: Dict[str, str], footer: Dict[str, str],
                            style: Dict[str, Any]) -> bool:
        """
        Create a new custom preset

        Args:
            name: Preset name
            description: Preset description
            header: Header configuration (left, center, right)
            footer: Footer configuration (left, center, right)
            style: Style configuration (font_size, separator_line)

        Returns:
            True if successful
        """
        preset_data = {
            "name": name,
            "description": description,
            "enabled": True,
            "header": header,
            "footer": footer,
            "style": style
        }

        return self.update_preset(name, preset_data)

    def delete_preset(self, preset_name: str) -> bool:
        """
        Delete a preset

        Args:
            preset_name: Name of preset to delete

        Returns:
            True if successful, False if preset doesn't exist or is currently active
        """
        # Don't allow deleting the current preset
        if preset_name == self.get_current_preset():
            return False

        if preset_name in self.template_data.get("presets", {}):
            del self.template_data["presets"][preset_name]
            return True

        return False

    def export_preset(self, preset_name: str, output_path: str) -> bool:
        """
        Export a preset to a JSON file

        Args:
            preset_name: Name of preset to export
            output_path: Path to save exported preset

        Returns:
            True if successful
        """
        preset = self.get_preset(preset_name)
        if not preset:
            return False

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(preset, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting preset: {e}")
            return False

    def import_preset(self, preset_name: str, input_path: str) -> bool:
        """
        Import a preset from a JSON file

        Args:
            preset_name: Name to give the imported preset
            input_path: Path to preset JSON file

        Returns:
            True if successful
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                preset_data = json.load(f)

            return self.update_preset(preset_name, preset_data)
        except Exception as e:
            print(f"Error importing preset: {e}")
            return False
