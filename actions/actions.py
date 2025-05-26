# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Sample scholarship database (replace with actual database in production)
SCHOLARSHIP_DB = [
    {
        "name": "National Scholarship Portal",
        "eligibility": "All students with family income below 6 lakhs",
        "documents": ["Income certificate", "Caste certificate", "Mark sheets", "Aadhaar card"],
        "deadline": "October 31, 2025",
        "categories": ["SC", "ST", "OBC", "General"],
        "education_levels": ["10th", "12th", "undergraduate", "graduate"],
        "max_income": 600000
    },
    {
        "name": "INSPIRE Scholarship",
        "eligibility": "Top 1% in 12th standard or qualified in competitive exams",
        "documents": ["Mark sheets", "Competitive exam result", "Bank account details"],
        "deadline": "December 15, 2025",
        "categories": ["General", "OBC", "SC", "ST"],
        "education_levels": ["undergraduate"],
        "min_score": 90
    },
    {
        "name": "Post-Matric Scholarship",
        "eligibility": "Students belonging to SC/ST/OBC with family income below 2.5 lakhs",
        "documents": ["Income certificate", "Caste certificate", "Mark sheets", "Institution verification"],
        "deadline": "September 30, 2025",
        "categories": ["SC", "ST", "OBC"],
        "education_levels": ["12th", "undergraduate", "graduate"],
        "max_income": 250000
    }
]

class ActionSearchScholarships(Action):
    def name(self) -> Text:
        return "action_search_scholarships"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        education = tracker.get_slot("education_level")
        category = tracker.get_slot("category")
        income = tracker.get_slot("income_level")
        
        # Basic matching logic - enhance this with better filtering in production
        matching_scholarships = []
        
        for scholarship in SCHOLARSHIP_DB:
            # Simple matching logic - refine this based on your requirements
            if (not education or education.lower() in [e.lower() for e in scholarship["education_levels"]]) and \
               (not category or category.lower() in [c.lower() for c in scholarship["categories"]]):
                matching_scholarships.append(scholarship)
        
        if matching_scholarships:
            response = "Here are some scholarships you may be eligible for:\n\n"
            for scholarship in matching_scholarships:
                response += f"📚 **{scholarship['name']}**\n"
                response += f"- Eligibility: {scholarship['eligibility']}\n"
                response += f"- Deadline: {scholarship['deadline']}\n\n"
            
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="I couldn't find any scholarships matching your profile. Would you like to provide more details about your educational background?")
        
        return []

class ActionCheckEligibility(Action):
    def name(self) -> Text:
        return "action_check_eligibility"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        scheme_name = tracker.get_slot("scheme_name")
        
        if not scheme_name:
            dispatcher.utter_message(text="Which scholarship or scheme would you like to check eligibility for?")
            return []
            
        # Find the scheme in our database
        scheme = next((s for s in SCHOLARSHIP_DB if scheme_name.lower() in s["name"].lower()), None)
        
        if scheme:
            dispatcher.utter_message(text=f"Eligibility criteria for {scheme['name']}:\n{scheme['eligibility']}")
        else:
            dispatcher.utter_message(text=f"I don't have information about {scheme_name}. Please check if the name is correct or ask about another scholarship.")
            
        return []

class ActionGetDocuments(Action):
    def name(self) -> Text:
        return "action_get_documents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        scheme_name = tracker.get_slot("scheme_name")
        
        if not scheme_name:
            dispatcher.utter_message(text="For which scholarship would you like to know the required documents?")
            return []
            
        # Find the scheme in our database
        scheme = next((s for s in SCHOLARSHIP_DB if scheme_name.lower() in s["name"].lower()), None)
        
        if scheme:
            docs = "\n- ".join(scheme["documents"])
            dispatcher.utter_message(text=f"Documents required for {scheme['name']}:\n- {docs}")
        else:
            dispatcher.utter_message(text=f"I don't have information about {scheme_name}. Please check if the name is correct or ask about another scholarship.")
            
        return []

class ActionGetDeadline(Action):
    def name(self) -> Text:
        return "action_get_deadline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        scheme_name = tracker.get_slot("scheme_name")
        
        if not scheme_name:
            dispatcher.utter_message(text="For which scholarship would you like to know the deadline?")
            return []
            
        # Find the scheme in our database
        scheme = next((s for s in SCHOLARSHIP_DB if scheme_name.lower() in s["name"].lower()), None)
        
        if scheme:
            dispatcher.utter_message(text=f"The application deadline for {scheme['name']} is {scheme['deadline']}.")
        else:
            dispatcher.utter_message(text=f"I don't have information about {scheme_name}. Please check if the name is correct or ask about another scholarship.")
            
        return []

class ActionSetReminder(Action):
    def name(self) -> Text:
        return "action_set_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        scheme_name = tracker.get_slot("scheme_name")
        
        if not scheme_name:
            dispatcher.utter_message(text="For which scholarship would you like to set a reminder?")
            return []
            
        # Find the scheme in our database
        scheme = next((s for s in SCHOLARSHIP_DB if scheme_name.lower() in s["name"].lower()), None)
        
        if scheme:
            # In a production system, you would store this reminder in a database
            # and set up a notification system
            dispatcher.utter_message(text=f"I've set a reminder for the {scheme['name']} deadline on {scheme['deadline']}. I'll notify you 7 days before the deadline.")
        else:
            dispatcher.utter_message(text=f"I don't have information about {scheme_name}. Please check if the name is correct or ask about another scholarship.")
            
        return []

class ActionCollectUserInfo(Action):
    def name(self) -> Text:
        return "action_collect_user_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Check what information we already have
        education = tracker.get_slot("education_level")
        category = tracker.get_slot("category")
        income = tracker.get_slot("income_level")
        state = tracker.get_slot("state")
        field = tracker.get_slot("field")
        score = tracker.get_slot("score")
        
        events = []
        
        # Ask for missing information
        if not education:
            dispatcher.utter_message(template="utter_ask_education_level")
            return events
            
        if not category:
            dispatcher.utter_message(template="utter_ask_category")
            return events
            
        if not income:
            dispatcher.utter_message(template="utter_ask_income_level")
            return events
            
        if not state:
            dispatcher.utter_message(template="utter_ask_state")
            return events
            
        if not field:
            dispatcher.utter_message(template="utter_ask_field")
            return events
            
        if not score:
            dispatcher.utter_message(template="utter_ask_score")
            return events
        
        # If we have all the information, mark the profile as complete
        dispatcher.utter_message(template="utter_profile_complete")
        events.append(SlotSet("user_profile_complete", True))
        
        return events

class ActionRecommendSchemes(Action):
    def name(self) -> Text:
        return "action_recommend_schemes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Check if profile is complete
        if not tracker.get_slot("user_profile_complete"):
            return [ActionCollectUserInfo().run(dispatcher, tracker, domain)]
        
        # Get user profile data
        education = tracker.get_slot("education_level")
        category = tracker.get_slot("category")
        income = tracker.get_slot("income_level")
        state = tracker.get_slot("state")
        field = tracker.get_slot("field")
        score = tracker.get_slot("score")
        
        # Simple recommendation logic - enhance this in production
        dispatcher.utter_message(text=f"Based on your profile ({education}, {category}, {field}), here are personalized recommendations:")
        
        # Call the scholarship search action to show matches
        return [ActionSearchScholarships().run(dispatcher, tracker, domain)]
