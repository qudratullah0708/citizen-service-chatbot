# Citizen Service Navigator - Multi-Agent System Approach

## System Architecture Overview

This system follows the same successful pattern as the travel planner but adapted for citizen services in developing countries. The architecture uses specialized agents under a supervisor to handle complex, fragmented public service ecosystems.

## Core Components

### 1. Intent Classification
```python
async def classify_service_intent(user_query: str) -> str:
    # Classifies queries into: 'housing', 'banking', 'emergency', or 'general_info'
    # Uses the same Groq/Llama model approach
```

### 2. Specialized Agents

#### Housing Agent
- **Purpose**: Handles housing support, rent assistance, property registration, LDA services
- **Tools**: 
  - `check_housing_eligibility()` - Validates against housing criteria
  - `generate_housing_forms()` - Creates LDA application drafts
  - `research_housing_policies()` - Fetches current housing policies
- **Instructions**: Focus on eligibility checking, form generation, and policy explanation

#### Banking Agent  
- **Purpose**: Manages financial aid, loans, banking services, Zakat distribution
- **Tools**:
  - `check_financial_eligibility()` - Validates income/assets against criteria
  - `generate_banking_forms()` - Creates financial aid applications
  - `calculate_zakat_eligibility()` - Determines Zakat qualification
- **Instructions**: Handle financial assessments, aid applications, and banking services

#### Emergency Agent
- **Purpose**: Covers emergency services, disaster relief, urgent assistance
- **Tools**:
  - `check_emergency_eligibility()` - Validates emergency service access
  - `generate_emergency_forms()` - Creates emergency assistance applications
  - `research_emergency_services()` - Fetches available emergency resources
- **Instructions**: Prioritize urgent needs, provide immediate guidance, handle crisis situations

### 3. Supervisor Agent
- **Purpose**: Coordinates all specialized agents and combines results
- **Process**: Runs agents in parallel, synthesizes responses, provides comprehensive guidance
- **Output**: Unified response with eligibility, applications, and plain-language explanations

## API Structure

### Main Endpoint
```python
@app.post("/citizen-service")
async def citizen_service(request: CitizenQueryRequest):
    # Similar to plan_trip() but for citizen services
    # 1. Classify intent (housing/banking/emergency)
    # 2. Extract citizen data
    # 3. Run specialized agents in parallel
    # 4. Combine results with supervisor
    # 5. Return comprehensive response
```

### Request/Response Models
```python
class CitizenQueryRequest(BaseModel):
    query: str
    citizen_data: Optional[CitizenProfile] = None

class CitizenProfile(BaseModel):
    name: str
    age: int
    income: float
    family_size: int
    location: str
    existing_benefits: List[str]
    emergency_status: Optional[str] = None
```

## Implementation Flow

### 1. Intent Classification
- Uses same Groq/Llama model approach
- Classifies into service categories
- Handles general information queries

### 2. Data Extraction & Validation
- Extracts citizen information from queries
- Validates against service requirements
- Handles missing or incomplete data

### 3. Parallel Agent Execution
```python
async def supervisor():
    # Run specialized agents in parallel
    housing_task = Runner.run(housing_agent, citizen_data)
    banking_task = Runner.run(banking_agent, citizen_data)  
    emergency_task = Runner.run(emergency_agent, citizen_data)
    
    # Wait for all results
    results = await asyncio.gather(housing_task, banking_task, emergency_task)
    
    # Combine and optimize
    return combined_response
```

### 4. Response Format
```python
{
    "intent": "housing",
    "citizen_data": validated_profile,
    "housing_services": housing_result,
    "banking_services": banking_result, 
    "emergency_services": emergency_result,
    "recommended_actions": optimized_plan,
    "offline_mode": degraded_response
}
```

## Offline/Degraded Mode

### Strategy
- Cache eligibility rules locally
- Pre-computed service mappings
- Simplified responses without real-time lookups
- Progressive enhancement when online

### Implementation
```python
async def get_degraded_response(citizen_data: CitizenProfile) -> dict:
    # Use cached eligibility rules
    # Provide basic guidance without real-time data
    # Include offline form generation
    # Suggest next steps for online completion
```

## Mock Data Structure

### Citizen Profiles
```python
MOCK_CITIZENS = [
    {
        "name": "Ahmed Khan",
        "age": 35,
        "income": 25000,
        "family_size": 4,
        "location": "Lahore",
        "existing_benefits": ["electricity_subsidy"],
        "emergency_status": None
    },
    # More profiles...
]
```

### Service Eligibility Rules
```python
HOUSING_ELIGIBILITY = {
    "income_threshold": 30000,
    "family_size_min": 2,
    "location_restrictions": ["Lahore", "Karachi", "Islamabad"],
    "existing_benefits_exclusions": ["housing_support"]
}
```

## Tools Implementation

### Housing Tools
```python
async def check_housing_eligibility(citizen_data: CitizenProfile) -> dict:
    # Check against LDA criteria
    # Validate income, family size, location
    # Return eligibility status and requirements

async def generate_housing_forms(citizen_data: CitizenProfile) -> str:
    # Generate LDA application forms
    # Pre-fill with citizen data
    # Include required documents list
```

### Banking Tools
```python
async def check_financial_eligibility(citizen_data: CitizenProfile) -> dict:
    # Check against financial aid criteria
    # Validate income, assets, existing benefits
    # Return eligibility for different programs

async def calculate_zakat_eligibility(citizen_data: CitizenProfile) -> dict:
    # Calculate Zakat qualification
    # Check against Punjab Zakat criteria
    # Return eligibility and amount
```

### Emergency Tools
```python
async def check_emergency_eligibility(citizen_data: CitizenProfile) -> dict:
    # Check emergency service access
    # Validate crisis status
    # Return available emergency resources

async def generate_emergency_forms(citizen_data: CitizenProfile) -> str:
    # Generate emergency assistance applications
    # Prioritize urgent needs
    # Include emergency contact information
```

## Language Support

### Implementation
- Use same model for Urdu/Punjabi translation
- Provide responses in local languages
- Include English fallback
- Handle regional dialects

### Example
```python
async def translate_response(response: str, target_language: str) -> str:
    # Translate complex policy language to plain local language
    # Maintain accuracy while improving accessibility
    # Include cultural context
```

## Testing Strategy

### Test Cases
1. **Housing Query**: "Am I eligible for housing support in Lahore?"
2. **Banking Query**: "Can I get financial aid for my family?"
3. **Emergency Query**: "I need emergency assistance after flood damage"
4. **General Query**: "What services are available for low-income families?"

### Validation
- Test with different citizen profiles
- Verify eligibility calculations
- Check form generation accuracy
- Validate offline mode functionality

## Next Steps

1. **Setup**: Create project structure with agent_api.py as base
2. **Mock Data**: Implement citizen profiles and service rules
3. **Tools**: Build eligibility checking and form generation tools
4. **Agents**: Create specialized agents for each service area
5. **Supervisor**: Implement coordination logic
6. **Testing**: Test with various scenarios
7. **Offline Mode**: Implement degraded functionality
8. **Language**: Add local language support

## Success Metrics

- **Accuracy**: Correct eligibility determinations
- **Completeness**: Comprehensive service coverage
- **Accessibility**: Plain language explanations
- **Efficiency**: Fast response times
- **Reliability**: Consistent offline performance
- **Impact**: Real citizen benefit realization