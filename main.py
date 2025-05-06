from typing import Dict, Any
from agents.recon_agent import ReconAgent
from agents.planning_agent import PlanningAgent
from agents.exploiting_agent import ExploitingAgent
from agents.reporting_agent import ReportingAgent

class HealthcareSecurityOrchestrator:
    def __init__(self):
        print("\n[Orchestrator] Initializing healthcare security assessment system...")
        self.recon_agent = ReconAgent()
        self.planning_agent = PlanningAgent()
        self.exploiting_agent = ExploitingAgent()
        self.reporting_agent = ReportingAgent()
        print("[Orchestrator] All agents initialized successfully")
    
    def run_assessment(self, target_network: str) -> Dict[str, Any]:
        """
        Run a complete security assessment of the target network.
        
        Args:
            target_network: The network to assess (e.g., "192.168.1.0/24")
            
        Returns:
            Dict containing the complete assessment report
        """
        print(f"\n[Orchestrator] Starting security assessment for network: {target_network}")
        
        # Step 1: Reconnaissance
        print("\n[Orchestrator] Step 1: Starting network reconnaissance...")
        recon_results = self.recon_agent.process({
            "target_network": target_network
        })
        print("[Orchestrator] Reconnaissance completed")
        
        # Step 2: Planning for each identified device
        print("\n[Orchestrator] Step 2: Starting vulnerability planning...")
        planning_results = {}
        for device in recon_results["identified_devices"]:
            print(f"\n[Orchestrator] Planning for device: {device['type']} ({device['ip']})")
            planning_results[device["ip"]] = self.planning_agent.process({
                "device_info": device
            })
        print("[Orchestrator] Vulnerability planning completed")
        
        # Step 3: Exploitation research for each vulnerability
        print("\n[Orchestrator] Step 3: Starting exploitation research...")
        exploit_results = {}
        for device_ip, plan in planning_results.items():
            for cve in plan["cve_results"]:
                print(f"\n[Orchestrator] Researching exploit for {device_ip} - {cve['cve_id']}")
                exploit_results[f"{device_ip}_{cve['cve_id']}"] = self.exploiting_agent.process({
                    "cve_info": cve
                })
        print("[Orchestrator] Exploitation research completed")
        
        # Step 4: Generate final report
        print("\n[Orchestrator] Step 4: Generating final report...")
        final_report = self.reporting_agent.process({
            "recon_data": recon_results,
            "planning_data": planning_results,
            "exploit_data": exploit_results
        })
        print("[Orchestrator] Final report generated")
        
        return final_report

def main():
    # Example usage
    print("\n=== Healthcare Security Assessment System ===")
    orchestrator = HealthcareSecurityOrchestrator()
    target_network = "192.168.1.0/24"  # Example network
    
    try:
        print(f"\nStarting assessment for network: {target_network}")
        report = orchestrator.run_assessment(target_network)
        print("\n=== Assessment Completed Successfully! ===")
        print("\nExecutive Summary:")
        print(report["executive_summary"])
        print("\nDetailed Report:")
        print(report["detailed_report"])
        print("\nRecommendations:")
        print(report["recommendations"])
    except Exception as e:
        print(f"\nError during assessment: {str(e)}")

if __name__ == "__main__":
    main() 