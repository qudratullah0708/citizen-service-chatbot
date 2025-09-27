import re
from typing import Dict, Any, Optional
from pydantic import BaseModel, ValidationError

class CitizenProfile(BaseModel):
    name: str
    age: int
    income: float
    family_size: int
    location: str
    existing_benefits: list = []
    emergency_status: Optional[str] = None

def extract_citizen_data(user_query: str, provided_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Extract citizen data from user query and provided data.
    Falls back to default values if extraction fails.
    """
    extracted = {}
    
    # Extract name
    name_patterns = [
        r"my name is (\w+)",
        r"i'm (\w+)",
        r"i am (\w+)",
        r"name: (\w+)",
        r"call me (\w+)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, user_query.lower())
        if match:
            extracted["name"] = match.group(1).title()
            break
    
    if "name" not in extracted:
        extracted["name"] = provided_data.get("name", "Citizen")
    
    # Extract age
    age_patterns = [
        r"i'm (\d+) years old",
        r"i am (\d+) years old",
        r"age: (\d+)",
        r"(\d+) years old"
    ]
    
    for pattern in age_patterns:
        match = re.search(pattern, user_query.lower())
        if match:
            extracted["age"] = int(match.group(1))
            break
    
    if "age" not in extracted:
        extracted["age"] = provided_data.get("age", 25)
    
    # Extract income
    income_patterns = [
        r"income: (\d+(?:,\d+)*(?:\.\d+)?)",
        r"earn (\d+(?:,\d+)*(?:\.\d+)?)",
        r"salary: (\d+(?:,\d+)*(?:\.\d+)?)",
        r"(\d+(?:,\d+)*(?:\.\d+)?) per month"
    ]
    
    for pattern in income_patterns:
        match = re.search(pattern, user_query.lower())
        if match:
            income_str = match.group(1).replace(",", "")
            extracted["income"] = float(income_str)
            break
    
    if "income" not in extracted:
        extracted["income"] = provided_data.get("income", 50000.0)
    
    # Extract family size
    family_patterns = [
        r"family size: (\d+)",
        r"(\d+) family members",
        r"(\d+) people in family",
        r"(\d+) dependents"
    ]
    
    for pattern in family_patterns:
        match = re.search(pattern, user_query.lower())
        if match:
            extracted["family_size"] = int(match.group(1))
            break
    
    if "family_size" not in extracted:
        extracted["family_size"] = provided_data.get("family_size", 1)
    
    # Extract location
    location_patterns = [
        r"location: (\w+)",
        r"from (\w+)",
        r"live in (\w+)",
        r"city: (\w+)"
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, user_query.lower())
        if match:
            extracted["location"] = match.group(1).title()
            break
    
    if "location" not in extracted:
        extracted["location"] = provided_data.get("location", "Karachi")
    
    # Extract existing benefits
    benefits_patterns = [
        r"already receiving (\w+)",
        r"have (\w+) benefit",
        r"existing benefit: (\w+)"
    ]
    
    existing_benefits = []
    for pattern in benefits_patterns:
        match = re.search(pattern, user_query.lower())
        if match:
            existing_benefits.append(match.group(1))
    
    extracted["existing_benefits"] = provided_data.get("existing_benefits", existing_benefits)
    
    # Extract emergency status
    emergency_patterns = [
        r"emergency: (\w+)",
        r"urgent: (\w+)",
        r"crisis: (\w+)"
    ]
    
    for pattern in emergency_patterns:
        match = re.search(pattern, user_query.lower())
        if match:
            extracted["emergency_status"] = match.group(1)
            break
    
    if "emergency_status" not in extracted:
        extracted["emergency_status"] = provided_data.get("emergency_status")
    
    return extracted
