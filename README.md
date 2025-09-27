# Citizen Service Navigator

A multi-agent AI system designed to help citizens in developing countries navigate complex public service ecosystems.

## Overview

The Citizen Service Navigator is an intelligent chatbot system that assists citizens in accessing housing support, banking services, emergency assistance, and general information about public services. The system uses specialized AI agents to provide personalized guidance, check eligibility, and generate application forms based on citizen profiles.

## Features

- **Intent Classification**: Automatically determines if a citizen query relates to housing, banking, emergency services, or general information
- **Specialized Service Agents**:
  - **Housing Agent**: Handles housing support, rent assistance, property registration, and LDA services
  - **Banking Agent**: Manages financial aid, loans, banking services, and Zakat distribution
  - **Emergency Agent**: Covers emergency services, disaster relief, and urgent assistance
- **Comprehensive Responses**: Provides eligibility information, application guidance, and plain-language explanations
- **Offline/Degraded Mode**: Functions with cached data when real-time services are unavailable
- **Multi-language Support**: Handles queries in multiple languages including English, Urdu, and Punjabi

## System Architecture

The system follows a multi-agent architecture:

1. **Intent Classification**: Determines the type of service the citizen is seeking
2. **Data Extraction**: Extracts citizen information from queries and validates against service requirements
3. **Specialized Agents**: Runs the appropriate agent based on the identified intent
4. **Supervisor**: Coordinates agent execution and combines results
5. **Response Generation**: Provides comprehensive guidance with eligibility, applications, and next steps

## Getting Started

### Prerequisites

- Python 3.8+
- Groq API key (for LLM access)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/citizen-service-chatbot.git
cd citizen-service-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
GROQ_API_KEY=your_groq_api_key
MODEL=meta-llama/llama-4-scout-17b-16e-instruct
```

### Running the Application

Start the FastAPI server:
```bash
uvicorn agent_api:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check
```
GET /health
```
Returns the status of the API.

### Citizen Service
```
POST /citizen-service
```
Processes a citizen query and returns appropriate service information.

Request body:
```json
{
  "query": "I need housing support in Lahore",
  "citizen_data": {
    "name": "Ahmed Khan",
    "age": 35,
    "income": 25000,
    "family_size": 4,
    "location": "Lahore",
    "existing_benefits": ["electricity_subsidy"],
    "emergency_status": null
  }
}
```

## Project Structure

- `agent_api.py`: Main API implementation with FastAPI
- `Citizen_Input.py`: Citizen profile model and data extraction
- `housing_services.py`: Housing-specific tools and services
- `banking_services.py`: Banking and financial services tools
- `emergency_services.py`: Emergency services tools
- `requirements.txt`: Project dependencies

## Testing

The system includes mock data for testing:
- Sample citizen profiles with various demographics
- Service eligibility rules for different programs
- Test cases for housing, banking, emergency, and general queries

## Future Enhancements

1. **Enhanced Language Support**: Improve handling of regional dialects
2. **Mobile Interface**: Develop a mobile app for better accessibility
3. **Document Processing**: Add capability to scan and process official documents
4. **Integration with Government Systems**: Connect with actual government service APIs
5. **Voice Interface**: Add voice input/output for citizens with limited literacy

## License

[MIT License](LICENSE)

## Acknowledgments

- Built using the OpenAI Agents framework
- Powered by Groq and Meta Llama models
