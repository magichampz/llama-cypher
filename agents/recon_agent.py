import subprocess
from typing import Any, Dict, List
from .base_agent import BaseAgent

class ReconAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """You are a network reconnaissance agent specialized in healthcare device discovery.
        Your role is to identify medical devices on the network and assess their potential security risks.
        You have access to various command-line tools and can analyze network traffic."""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        print("\n[ReconAgent] Starting network reconnaissance...")
        target_network = input_data.get("target_network", "192.168.1.0/24")
        
        # Placeholder scan results instead of actual nmap scan
        # scan_results = self._run_nmap_scan(target_network)
        scan_results = """
        Nmap scan report for 192.168.1.0/24
        Host: 192.168.1.100 (Medical Device - MRI Scanner)
        Host: 192.168.1.101 (Medical Device - Patient Monitor)
        Host: 192.168.1.102 (Medical Device - Infusion Pump)
        """
        print(f"[ReconAgent] Scan results:\n{scan_results}")
        
        # Analyze results using LLM
        analysis_prompt = f"Analyze these scan results and identify potential medical devices: {scan_results}"
        print("[ReconAgent] Sending results to LLM for analysis...")
        analysis = self._call_llm(analysis_prompt)
        print(f"[ReconAgent] LLM Analysis:\n{analysis}")
        
        identified_devices = self._extract_medical_devices(analysis)
        print(f"[ReconAgent] Identified devices: {identified_devices}")
        
        return {
            "scan_results": scan_results,
            "analysis": analysis,
            "identified_devices": identified_devices
        }
    
    def _run_nmap_scan(self, target: str) -> str:
        """Run an nmap scan on the target network."""
        try:
            result = subprocess.run(
                ["nmap", "-sn", target],
                capture_output=True,
                text=True
            )
            return result.stdout
        except Exception as e:
            return f"Error running nmap scan: {str(e)}"
    
    def _extract_medical_devices(self, analysis: str) -> List[Dict[str, Any]]:
        """Extract medical device information from the analysis."""
        # This is a placeholder - in reality, you'd want to parse the analysis
        # and extract structured information about medical devices
        return [
            {"type": "MRI Scanner", "ip": "192.168.1.100", "risk_level": "High"},
            {"type": "Patient Monitor", "ip": "192.168.1.101", "risk_level": "Medium"},
            {"type": "Infusion Pump", "ip": "192.168.1.102", "risk_level": "Critical"}
        ] 