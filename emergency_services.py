from typing import Dict, Any
from Citizen_Input import CitizenProfile

def check_emergency_eligibility(citizen_data: CitizenProfile) -> Dict[str, Any]:
    """
    Check emergency eligibility for emergency services and disaster relief.
    Returns eligibility status and available programs.
    """
    eligibility_results = {
        "eligible": False,
        "programs": [],
        "requirements": [],
        "next_steps": [],
        "priority_level": "Low"
    }
    
    # Emergency status check
    if citizen_data.emergency_status:
        eligibility_results["eligible"] = True
        eligibility_results["priority_level"] = "High"
        eligibility_results["programs"].append("Emergency Relief Program")
        eligibility_results["programs"].append("Crisis Support Services")
        eligibility_results["requirements"].append("Emergency status verified")
    
    # Income-based emergency assistance
    emergency_income_threshold = 75000  # Rs. 75,000 per month
    if citizen_data.income <= emergency_income_threshold:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Low-Income Emergency Aid")
        eligibility_results["requirements"].append("Income below Rs. 75,000/month")
    
    # Family size considerations for emergency
    if citizen_data.family_size >= 4:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Large Family Emergency Support")
        eligibility_results["requirements"].append("Family size of 4 or more")
    
    # Age-based emergency programs
    if citizen_data.age >= 65 or citizen_data.age <= 18:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Vulnerable Population Emergency Aid")
        eligibility_results["requirements"].append("Age 65+ or 18 and below")
    
    # Location-based emergency programs
    high_risk_locations = ["karachi", "lahore", "islamabad", "peshawar", "quetta"]
    if citizen_data.location.lower() in high_risk_locations:
        eligibility_results["programs"].append("Urban Emergency Response")
        eligibility_results["requirements"].append("Residence in high-risk urban area")
    
    # Set priority level based on multiple factors
    priority_factors = 0
    if citizen_data.emergency_status:
        priority_factors += 3
    if citizen_data.income <= emergency_income_threshold:
        priority_factors += 2
    if citizen_data.family_size >= 4:
        priority_factors += 1
    if citizen_data.age >= 65 or citizen_data.age <= 18:
        priority_factors += 1
    
    if priority_factors >= 3:
        eligibility_results["priority_level"] = "High"
    elif priority_factors >= 2:
        eligibility_results["priority_level"] = "Medium"
    else:
        eligibility_results["priority_level"] = "Low"
    
    # Next steps based on priority
    if eligibility_results["priority_level"] == "High":
        eligibility_results["next_steps"] = [
            "Call emergency hotline immediately",
            "Visit nearest emergency service center",
            "Submit emergency application",
            "Follow up within 24 hours"
        ]
    elif eligibility_results["priority_level"] == "Medium":
        eligibility_results["next_steps"] = [
            "Contact emergency services",
            "Submit application within 48 hours",
            "Schedule emergency assessment",
            "Follow up within 72 hours"
        ]
    else:
        eligibility_results["next_steps"] = [
            "Submit standard emergency application",
            "Schedule assessment appointment",
            "Follow up within 1 week"
        ]
    
    return eligibility_results

def generate_emergency_forms(citizen_data: CitizenProfile) -> Dict[str, Any]:
    """
    Generate emergency assistance forms based on citizen profile.
    Returns form data and instructions.
    """
    forms = {
        "emergency_application_form": {
            "personal_info": {
                "name": citizen_data.name,
                "age": citizen_data.age,
                "location": citizen_data.location,
                "emergency_status": citizen_data.emergency_status
            },
            "financial_info": {
                "monthly_income": citizen_data.income,
                "family_size": citizen_data.family_size,
                "existing_benefits": citizen_data.existing_benefits
            },
            "emergency_details": {
                "nature_of_emergency": "To be specified",
                "urgency_level": "High" if citizen_data.emergency_status else "Normal",
                "affected_family_members": citizen_data.family_size,
                "estimated_damage": "To be assessed"
            }
        },
        "required_documents": [
            "CNIC copy",
            "Emergency incident report",
            "Income certificate",
            "Family registration certificate",
            "Medical certificates (if applicable)",
            "Property damage assessment (if applicable)",
            "Bank statements (last 3 months)"
        ],
        "submission_instructions": [
            "Complete emergency application form",
            "Attach all required documents",
            "Submit to emergency service center",
            "Keep copies of all submitted documents",
            "Follow up within 24 hours for high priority cases"
        ],
        "contact_info": {
            "emergency_hotline": "112",
            "office": "Emergency Services Center",
            "phone": "021-111-911-000",
            "email": "emergency@gov.pk",
            "hours": "24/7 Emergency Services"
        },
        "immediate_actions": [
            "Call emergency hotline if life-threatening",
            "Visit nearest emergency center",
            "Document all damages and losses",
            "Keep receipts for emergency expenses",
            "Contact family and support network"
        ]
    }
    
    return forms
