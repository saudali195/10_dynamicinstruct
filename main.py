from connection import model

# ------------------ Exercise 1 ------------------
def medical_agent(user_type, query):
    if user_type == "patient":
        instructions = "Use simple words, explain terms clearly, be empathetic and reassuring."
    elif user_type == "medical_student":
        instructions = "Use moderate medical terminology with explanations, add learning opportunities."
    elif user_type == "doctor":
        instructions = "Use full medical terminology, abbreviations, and clinical style, concise and professional."
    else:
        instructions = "Default to patient-friendly explanation."
    
    prompt = f"""
    You are a medical consultation assistant. 
    User type: {user_type}
    Instructions: {instructions}
    Question: {query}
    """
    
    response = model.generate_content(prompt)
    return response.text


# ------------------ Exercise 2 ------------------
def airline_agent(seat_preference, travel_experience):
    if seat_preference == "window" and travel_experience == "first_time":
        instructions = "Explain window benefits, scenic views, reassure about first flight."
    elif seat_preference == "middle" and travel_experience == "frequent":
        instructions = "Acknowledge middle seat compromise, suggest strategies, offer alternatives."
    elif seat_preference == "any" and travel_experience == "premium":
        instructions = "Highlight luxury options, upgrades, priority boarding."
    else:
        instructions = "Give balanced helpful advice."
    
    prompt = f"""
    You are an airline seat preference assistant.
    Seat: {seat_preference}
    Experience: {travel_experience}
    Instructions: {instructions}
    """
    
    response = model.generate_content(prompt)
    return response.text


# ------------------ Exercise 3 ------------------
def travel_agent(trip_type, traveler_profile):
    if trip_type == "adventure" and traveler_profile == "solo":
        instructions = "Suggest exciting activities, focus on safety, recommend hostels and group tours."
    elif trip_type == "cultural" and traveler_profile == "family":
        instructions = "Focus on educational attractions, kid-friendly museums, family accommodations."
    elif trip_type == "business" and traveler_profile == "executive":
        instructions = "Emphasize efficiency, airport proximity, business centers, reliable wifi, lounges."
    else:
        instructions = "Provide general travel advice."
    
    prompt = f"""
    You are a travel planning assistant.
    Trip type: {trip_type}
    Traveler profile: {traveler_profile}
    Instructions: {instructions}
    """
    
    response = model.generate_content(prompt)
    return response.text


# ------------------ Test Runs ------------------
if __name__ == "__main__":
    # Exercise 1 test
    print("Exercise 1:")
    print(medical_agent("patient", "What is hypertension?"))
    print("\n")

    # Exercise 2 test
    print("Exercise 2:")
    print(airline_agent("window", "first_time"))
    print("\n")

    # Exercise 3 test
    print("Exercise 3:")
    print(travel_agent("cultural", "family"))
