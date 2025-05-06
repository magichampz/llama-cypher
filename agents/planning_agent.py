import requests
from typing import Any, Dict, List
from .base_agent import BaseAgent

class PlanningAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name="llama3.1:8b")  # Will be replaced with your fine-tuned model
    
    def _get_system_prompt(self) -> str:
        return """You are a security planning agent specialized in healthcare device vulnerabilities.
        Your role is to research CVEs, analyze their impact, and create security plans for medical devices."""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        print("\n[PlanningAgent] Starting vulnerability analysis...")
        device_info = input_data.get("device_info", {})
        print(f"[PlanningAgent] Analyzing device: {device_info}")
        
        cve_results = self._search_cves(device_info)
        print(f"[PlanningAgent] Found CVEs: {cve_results}")
        
        # Analyze CVEs using LLM
        analysis_prompt = f"""Analyze these CVEs and provide security recommendations for the following device:
        Device Type: {device_info.get('type', 'Unknown')}
        IP Address: {device_info.get('ip', 'Unknown')}
        Risk Level: {device_info.get('risk_level', 'Unknown')}
        
        CVEs to analyze: {cve_results}"""
        
        print("[PlanningAgent] Sending CVEs to LLM for analysis...")
        analysis = self._call_llm(analysis_prompt)
        print(f"[PlanningAgent] LLM Analysis:\n{analysis}")
        
        security_plan = self._create_security_plan(analysis)
        print(f"[PlanningAgent] Generated security plan: {security_plan}")
        
        return {
            "cve_results": cve_results,
            "analysis": analysis,
            "security_plan": security_plan
        }
    
    def _search_cves(self, device_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for CVEs related to the device."""
        # This is a placeholder - in reality, you'd want to:
        # 1. Query the NVD API
        # 2. Search other vulnerability databases
        # 3. Cross-reference with device information
        device_type = device_info.get('type', '').lower()
        
        if 'mri' in device_type:
            return [{
                "cve_id": "CVE-2023-1234",
                "description": "Remote code execution vulnerability in MRI scanner control software",
                "severity": "Critical",
                "affected_versions": "v2.1.0 - v2.3.0"
            }]
        elif 'monitor' in device_type:
            return [{
                "cve_id": "CVE-2023-1235",
                "description": "Unauthorized access to patient monitoring data",
                "severity": "High",
                "affected_versions": "v1.5.0 - v1.8.0"
            }]
        elif 'pump' in device_type:
            return [{
                "cve_id": "CVE-2023-1236",
                "description": "Buffer overflow in infusion pump control interface",
                "severity": "Critical",
                "affected_versions": "v3.0.0 - v3.2.0"
            }]
        else:
            return [{
                "cve_id": "CVE-2023-1237",
                "description": "Generic medical device vulnerability",
                "severity": "Medium",
                "affected_versions": "Unknown"
            }]
    
    def _create_security_plan(self, analysis: str) -> Dict[str, Any]:
        """Create a security plan based on the analysis."""
        # This is a placeholder - in reality, you'd want to structure the plan
        # with specific recommendations and mitigation steps
        return {
            "recommendations": [
                "Update device firmware to latest version",
                "Implement network segmentation",
                "Enable device authentication",
                "Monitor device logs for suspicious activity"
            ],
            "mitigation_steps": [
                "Step 1: Isolate device from general network",
                "Step 2: Apply security patches",
                "Step 3: Configure access controls",
                "Step 4: Implement monitoring solution"
            ],
            "priority": "High",
            "estimated_effort": "4 hours",
            "required_resources": ["Network access", "Device credentials", "Backup system"]
        } 