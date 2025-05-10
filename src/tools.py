import nmap
import socket
import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from langchain.tools import tool

@dataclass
class DeviceInfo:
    ip: str
    hostname: Optional[str]
    services: List[Dict[str, str]]
    os_info: Optional[str]

@dataclass
class CVEInfo:
    id: str
    description: str
    references: List[str]
    # cwe_ids: List[str]

def get_local_network() -> str:
    """Get the local network address based on the current device's IP."""
    try:
        # Create a socket to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        # Extract network address (assuming /24 subnet)
        network_parts = local_ip.split('.')
        return f"{network_parts[0]}.{network_parts[1]}.{network_parts[2]}.0/24"
    except Exception as e:
        raise Exception(f"Failed to determine local network: {str(e)}")

@tool("scan_network")
def scan_network() -> List[DeviceInfo]:
    """
    Scans the local network for devices and their services. Use this when asked about devices on the network.
    
    Returns:
        List[DeviceInfo]: A list of DeviceInfo objects containing device details including IP, hostname, and services.
    """
    try:
        # Initialize nmap scanner
        nm = nmap.PortScanner()
        
        # Get local network
        network = get_local_network()
        
        # Run basic service scan without OS detection
        nm.scan(hosts=network, arguments='-sV')
        
        devices = []
        for host in nm.all_hosts():
            device_info = DeviceInfo(
                ip=host,
                hostname=None,
                services=[],
                os_info=None  # We'll keep this field but it will be None
            )
            
            # Get hostname if available
            try:
                device_info.hostname = socket.gethostbyaddr(host)[0]
            except:
                pass
            
            # Get services
            if 'tcp' in nm[host]:
                for port, service in nm[host]['tcp'].items():
                    device_info.services.append({
                        'port': str(port),
                        'name': service['name'],
                        'product': service.get('product', ''),
                        'version': service.get('version', '')
                    })
            
            devices.append(device_info)
        
        return devices
    
    except Exception as e:
        raise Exception(f"Network scan failed: {str(e)}")

@tool("web_search")
def web_search(device_name: str) -> List[Dict[str, str]]:
    """
    Searches for vulnerabilities associated with a device. Use this when asked about vulnerabilities of specific devices or software.
    
    Args:
        device_name (str): The name of the device or software to search for vulnerabilities.
            Example: "commvault command centre" or "apache 2.4.49"
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries containing CVE information including CVE ID, description, and severity.
    """
    try:
        # For demonstration, return some example CVEs
        # In a real implementation, this would call a search API
        return [
            {
                "cve_id": "CVE-2025-34028",
            }
        ]
    
    except Exception as e:
        raise Exception(f"Web search failed: {str(e)}")

@tool("cve_search")
def cve_search(cve_id: str) -> CVEInfo:
    """
    Searches for detailed information about a specific CVE. If you do not have any information about the specific CVE, use this function when asked about specific CVE IDs.
    
    Args:
        cve_id (str): The CVE identifier to search for (e.g., "CVE-2023-1234")
    
    Returns:
        CVEInfo: An object containing CVE information including ID, description, references, and CWE IDs.
    """
    try:
        # Make API request to CIRCL
        response = requests.get(f"https://cve.circl.lu/api/cve/{cve_id}")
        response.raise_for_status()
        cve_data = response.json()
        
        # Extract description from descriptions array
        description = "No description available"
        if 'descriptions' in cve_data and cve_data['descriptions']:
            for desc in cve_data['descriptions']:
                if desc.get('lang') == 'en':
                    description = desc.get('value', description)
                    break
        
        # # Extract CWE IDs from problemTypes
        # cwe_ids = []
        # if 'problemTypes' in cve_data and cve_data['problemTypes']:
        #     for problem_type in cve_data['problemTypes']:
        #         if 'descriptions' in problem_type:
        #             for desc in problem_type['descriptions']:
        #                 if desc.get('lang') == 'en' and desc.get('type') == 'CWE':
        #                     cwe_id = desc.get('cweId', '')
        #                     if cwe_id:
        #                         cwe_ids.append(cwe_id)
        
        # Extract references
        references = []
        if 'references' in cve_data and cve_data['references']:
            for ref in cve_data['references']:
                if 'url' in ref:
                    references.append(ref['url'])
                    
        references = [cve_data.get("containers", {}).get("cna", {}).get("references", {})[i].get("url") for i in range(len(cve_data.get("containers", {}).get("cna", {}).get("references", {})))]
        
        return CVEInfo(
            id=cve_id,
            description=cve_data.get("containers", {}).get("cna", {}).get("descriptions", {})[0].get("value", "No description available"),
            references=references,
            # cwe_ids=cwe_ids
        )
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch CVE information: {str(e)}")
    except Exception as e:
        raise Exception(f"CVE search failed: {str(e)}")

# testing
# output = cve_search("CVE-2025-34028")
# print(output)