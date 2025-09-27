from typing import Dict, Any
from Citizen_Input import CitizenProfile

def check_housing_eligibility(citizen_data: CitizenProfile) -> Dict[str, Any]:
    """
    Check housing eligibility based on citizen profile.
    Returns eligibility status and available programs.
    """
    eligibility_results = {
        "eligible": False,
        "programs": [],
        "requirements": [],
        "next_steps": []
    }
    
    # Basic eligibility criteria
    income_threshold = 100000  # Rs. 100,000 per month
    family_size_threshold = 2
    
    # Check income-based eligibility
    if citizen_data.income <= income_threshold:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Low-Income Housing Program")
        eligibility_results["requirements"].append("Income below Rs. 100,000/month")
    
    # Check family size eligibility
    if citizen_data.family_size >= family_size_threshold:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Family Housing Assistance")
        eligibility_results["requirements"].append("Family size of 2 or more")
    
    # Special programs based on location
    if citizen_data.location.lower() in ["karachi", "lahore", "islamabad"]:
        eligibility_results["programs"].append("Urban Housing Initiative")
        eligibility_results["requirements"].append("Residence in major city")
    
    # Emergency housing
    if citizen_data.emergency_status:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Emergency Housing Assistance")
        eligibility_results["requirements"].append("Emergency status verified")
    
    # Next steps
    if eligibility_results["eligible"]:
        eligibility_results["next_steps"] = [
            "Visit local LDA office",
            "Submit required documents",
            "Complete application form",
            "Schedule property inspection"
        ]
    else:
        eligibility_results["next_steps"] = [
            "Consider income improvement programs",
            "Explore alternative housing options",
            "Contact housing counselor for guidance"
        ]
    
    return eligibility_results

def generate_housing_forms(citizen_data: CitizenProfile) -> Dict[str, Any]:
    """
    Generate housing application forms based on citizen profile.
    Returns form data and instructions.
    """
    forms = {
        "application_form": {
            "personal_info": {
                "name": citizen_data.name,
                "age": citizen_data.age,
                "location": citizen_data.location
            },
            "financial_info": {
                "monthly_income": citizen_data.income,
                "family_size": citizen_data.family_size,
                "existing_benefits": citizen_data.existing_benefits
            },
            "housing_preferences": {
                "preferred_location": citizen_data.location,
                "property_type": "Apartment" if citizen_data.family_size <= 4 else "House",
                "urgency": "High" if citizen_data.emergency_status else "Normal"
            }
        },
        "required_documents": [
            "CNIC copy",
            "Income certificate",
            "Family registration certificate",
            "Property ownership documents (if applicable)",
            "Bank statements (last 3 months)",
            "Utility bills"
        ],
        "submission_instructions": [
            "Complete all sections of the application form",
            "Attach all required documents",
            "Submit to local LDA office",
            "Keep copies of all submitted documents",
            "Follow up within 15 business days"
        ],
        "contact_info": {
            "office": "Local LDA Office",
            "phone": "021-111-532-000",
            "email": "housing@lda.gov.pk",
            "hours": "9:00 AM - 5:00 PM (Monday to Friday)"
        }
    }
    
    return forms
