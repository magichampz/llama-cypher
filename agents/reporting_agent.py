from typing import Any, Dict
from .base_agent import BaseAgent

class ReportingAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name="llama3.1:8b")  # Will be replaced with your fine-tuned model
    
    def _get_system_prompt(self) -> str:
        return """You are a security reporting agent specialized in healthcare device security.
        Your role is to create comprehensive security reports that summarize findings,
        recommendations, and potential risks in a clear and actionable format."""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Combine all previous agent outputs
        recon_data = input_data.get("recon_data", {})
        planning_data = input_data.get("planning_data", {})
        exploit_data = input_data.get("exploit_data", {})
        
        # Generate executive summary
        summary_prompt = f"""Create an executive summary of the security assessment:
        Reconnaissance: {recon_data}
        Planning: {planning_data}
        Exploitation Research: {exploit_data}"""
        executive_summary = self._call_llm(summary_prompt)
        
        # Generate detailed report
        report = self._generate_detailed_report(
            recon_data,
            planning_data,
            exploit_data,
            executive_summary
        )
        
        return {
            "executive_summary": executive_summary,
            "detailed_report": report,
            "recommendations": self._extract_recommendations(report)
        }
    
    def _generate_detailed_report(
        self,
        recon_data: Dict[str, Any],
        planning_data: Dict[str, Any],
        exploit_data: Dict[str, Any],
        executive_summary: str
    ) -> Dict[str, Any]:
        """Generate a detailed security report."""
        return {
            "executive_summary": executive_summary,
            "findings": {
                "device_inventory": recon_data.get("identified_devices", []),
                "vulnerabilities": planning_data.get("cve_results", []),
                "exploitation_research": exploit_data.get("exploit_research", {})
            },
            "risk_assessment": self._assess_risks(planning_data, exploit_data),
            "recommendations": planning_data.get("security_plan", {}).get("recommendations", [])
        }
    
    def _assess_risks(
        self,
        planning_data: Dict[str, Any],
        exploit_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess the overall risk level of the findings."""
        return {
            "risk_level": "High",
            "impact_areas": ["Patient Safety", "Data Security", "System Availability"],
            "mitigation_priority": "Immediate"
        }
    
    def _extract_recommendations(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and prioritize recommendations from the report."""
        return {
            "immediate_actions": ["Action 1", "Action 2"],
            "short_term": ["Action 3", "Action 4"],
            "long_term": ["Action 5", "Action 6"]
        } 