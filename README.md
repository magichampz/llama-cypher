# Healthcare Cybersecurity Agentic System

This system provides an automated approach to healthcare device security assessment using multiple AI agents powered by Llama 2. Each agent specializes in a different aspect of security assessment:

1. **ReconAgent**: Performs network reconnaissance to identify medical devices
2. **PlanningAgent**: Researches CVEs and creates security plans
3. **ExploitingAgent**: Researches and develops proof-of-concept exploits
4. **ReportingAgent**: Generates comprehensive security reports

## Prerequisites

- Python 3.8+
- Ollama with Llama 2 model installed
- Kali Linux (recommended)
- Network access to target devices

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd healthcare-cybersecurity-agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is running with Llama 2:
```bash
ollama run llama2:8b
```

## Usage

1. Run the main assessment script:
```bash
python main.py
```

2. The system will:
   - Scan the target network for medical devices
   - Research vulnerabilities for identified devices
   - Generate security recommendations
   - Create a comprehensive report

## Configuration

- Modify the target network in `main.py` to match your environment
- Adjust agent parameters in their respective files
- Customize system prompts for each agent as needed

## Security Considerations

- This system is for authorized security testing only
- Always obtain proper authorization before testing
- Never run exploits on production systems
- Follow healthcare security best practices and regulations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
