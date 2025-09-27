from typing import Dict, Any
from Citizen_Input import CitizenProfile

def check_financial_eligibility(citizen_data: CitizenProfile) -> Dict[str, Any]:
    """
    Check financial eligibility for banking services and financial aid.
    Returns eligibility status and available programs.
    """
    eligibility_results = {
        "eligible": False,
        "programs": [],
        "requirements": [],
        "next_steps": []
    }
    
    # Income-based eligibility thresholds
    low_income_threshold = 50000  # Rs. 50,000 per month
    medium_income_threshold = 150000  # Rs. 150,000 per month
    
    # Check low-income programs
    if citizen_data.income <= low_income_threshold:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Low-Income Financial Aid")
        eligibility_results["programs"].append("Interest-Free Loan Program")
        eligibility_results["requirements"].append("Income below Rs. 50,000/month")
    
    # Check medium-income programs
    elif citizen_data.income <= medium_income_threshold:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Small Business Loan Program")
        eligibility_results["programs"].append("Education Loan Program")
        eligibility_results["requirements"].append("Income below Rs. 150,000/month")
    
    # Family size considerations
    if citizen_data.family_size >= 3:
        eligibility_results["programs"].append("Family Support Program")
        eligibility_results["requirements"].append("Family size of 3 or more")
    
    # Age-based programs
    if citizen_data.age >= 60:
        eligibility_results["programs"].append("Senior Citizen Financial Aid")
        eligibility_results["requirements"].append("Age 60 or above")
    elif citizen_data.age <= 30:
        eligibility_results["programs"].append("Youth Entrepreneurship Program")
        eligibility_results["requirements"].append("Age 30 or below")
    
    # Emergency financial assistance
    if citizen_data.emergency_status:
        eligibility_results["eligible"] = True
        eligibility_results["programs"].append("Emergency Financial Assistance")
        eligibility_results["requirements"].append("Emergency status verified")
    
    # Next steps
    if eligibility_results["eligible"]:
        eligibility_results["next_steps"] = [
            "Visit local bank branch",
            "Submit financial documents",
            "Complete application form",
            "Schedule interview with loan officer"
        ]
    else:
        eligibility_results["next_steps"] = [
            "Consider income improvement programs",
            "Explore alternative financial options",
            "Contact financial counselor for guidance"
        ]
    
    return eligibility_results

def calculate_zakat_eligibility(citizen_data: CitizenProfile) -> Dict[str, Any]:
    """
    Calculate Zakat eligibility and amount based on citizen profile.
    Returns Zakat calculation and distribution information.
    """
    zakat_results = {
        "eligible_for_zakat": False,
        "zakat_amount": 0,
        "nisab_threshold": 0,
        "calculation_details": {},
        "distribution_info": {}
    }
    
    # Nisab threshold (minimum wealth required to pay Zakat)
    # Using current gold price approximation
    nisab_threshold = 85000  # Rs. 85,000 (approximate value of 87.48 grams of gold)
    zakat_results["nisab_threshold"] = nisab_threshold
    
    # Calculate total wealth (simplified calculation)
    # Assuming monthly income * 12 as annual wealth
    annual_wealth = citizen_data.income * 12
    
    # Check if citizen meets Nisab threshold
    if annual_wealth >= nisab_threshold:
        zakat_results["eligible_for_zakat"] = True
        zakat_amount = annual_wealth * 0.025  # 2.5% Zakat rate
        zakat_results["zakat_amount"] = zakat_amount
        
        zakat_results["calculation_details"] = {
            "annual_wealth": annual_wealth,
            "zakat_rate": "2.5%",
            "calculated_amount": zakat_amount
        }
    
    # Zakat distribution information
    zakat_results["distribution_info"] = {
        "eligible_recipients": [
            "Poor and needy",
            "Zakat collectors",
            "New Muslims",
            "Debtors",
            "Travelers in need",
            "Those working for Zakat",
            "Those whose hearts are to be reconciled",
            "Slaves seeking freedom"
        ],
        "distribution_centers": [
            "Local Zakat Committee",
            "Mosque Zakat Fund",
            "Government Zakat Department",
            "Charitable Organizations"
        ],
        "contact_info": {
            "office": "Local Zakat Committee",
            "phone": "021-111-925-000",
            "email": "zakat@gov.pk",
            "hours": "9:00 AM - 4:00 PM (Monday to Friday)"
        }
    }
    
    return zakat_results
