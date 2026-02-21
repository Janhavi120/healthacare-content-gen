from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from datetime import datetime
import streamlit as st

# Configure Gemini API directly
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]  
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a professional {doctor_type} AI assistant. Generate concise 1-page medical reports from {doctor_type}'s perspective using appropriate medical terminology and focusing on {doctor_type}'s specialty."""),
        
        ("user", """Generate a detailed 1-page medical report from {doctor_type}'s perspective using this information:

Patient: {age} years old, {gender}
Symptoms: {primary_symptoms}
Report Type: {report_type}
Date: {current_date}


## Patient Information
- **Date of Visit:** {current_date}
- **Patient Details:** {age} years old, {gender}
- **Specialist:** {doctor_type}
- **Visit Type:** {report_type}
- **Mode of Visit:** [In-person/Teleconsultation - based on context]
- **Referral Source:** [Self/Referred by physician]

## Chief Complaint
[Provide a detailed description of the main symptoms as reported by the patient, including:
- Onset and duration of symptoms
- Severity and frequency
- Any triggering or relieving factors
- Associated symptoms
- Impact on daily activities]

## Present Condition
[Comprehensive assessment of the current clinical status:
- Detailed examination findings relevant to {doctor_type}'s specialty
- Progression of symptoms since onset
- Current severity level (mild/moderate/severe)
- Any immediate concerns or red flags
- Correlation with patient's medical history
- Physical examination highlights relevant to the specialty]

## Medication Prescribed
[List all medications with complete details:
- **Medication Name:** [Generic/Brand name]
- **Dosage:** [Strength and frequency]
- **Duration:** [How long to take]
- **Timing:** [Before/after meals, specific times]
- **Purpose:** [Why each medication is prescribed]
- **Administration Route:** [Oral/Topical/Injection etc.]
- **Special Instructions:** [Any specific guidance for taking medication]

**Current Medications Review:**
[Assessment of any existing medications and their interactions]

## Lifestyle Modifications for Recovery
[Comprehensive lifestyle recommendations including:
- **Dietary Changes:** Specific foods to eat/avoid
- **Physical Activity:** Exercises, rest requirements, activity restrictions
- **Sleep Recommendations:** Optimal sleep position, duration
- **Work Modifications:** Time off work, ergonomic adjustments
- **Stress Management:** Relaxation techniques, mental health support
- **Daily Routine Modifications:** Changes to daily activities
- **Habit Modifications:** Smoking, alcohol, caffeine recommendations
- **Environmental Changes:** Home/work environment adjustments]

## Future Precautions
[Detailed precautionary measures:
- **Immediate Precautions:** What to avoid right now
- **Activity Restrictions:** Lifting, bending, driving, etc.
- **Warning Signs:** When to seek immediate medical attention
- **Prevention Strategies:** How to prevent recurrence
- **Monitoring Parameters:** What symptoms to track
- **Lifestyle Modifications:** Long-term changes needed
- **Environmental Precautions:** Specific situations to avoid
- **Seasonal Considerations:** Weather-related precautions if applicable]

## Required Tests/Investigations
[Complete list of recommended diagnostic tests:
- **Laboratory Tests:** [Blood work, urine tests, etc. with specific parameters]
- **Imaging Studies:** [X-rays, MRI, CT scan, Ultrasound - with specific views if needed]
- **Specialized Tests:** [ECG, EEG, Nerve conduction, etc.]
- **Follow-up Tests:** [When to repeat tests]
- **Preparation Instructions:** [Fasting requirements, medication adjustments before tests]
- **Priority Level:** [Urgent/Routine/Elective]
- **Expected Timeline:** [When to get tests done]
- **Special Instructions:** [Any specific preparations or considerations]

## Follow-up Plan
- **Next Visit:** [Specific date or timeframe]
- **Referral Needed:** [To other specialists if required]
- **Emergency Contact:** [When and how to reach the clinic]
- **Telemedicine Option:** [If follow-up can be done remotely]

**Additional Notes:**
[Any other relevant information, specific instructions, or general advice based on the patient's condition and {report_type} context]

**IMPORTANT GUIDELINES:**
- Use simple, clear language with minimal medical jargon
- Keep total report under 300 words while maintaining comprehensiveness
- Focus specifically on {doctor_type}'s specialty expertise
- Include only relevant and necessary details
- Maintain a professional yet empathetic tone
- Tailor the content specifically for a {report_type} visit
- Ensure all recommendations are practical and actionable
- Include patient education elements throughout the report
- Make the report actionable and easy for the patient to follow
""")
    ]
)

# Create the Chain
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Function to Generate Medical Report
def generate_medical_report(age, gender, primary_symptoms, report_type, doctor_type):
    try:
        current_date = datetime.now().strftime("%B %d, %Y")
        # Generate the medical report using the chain
        report = chain.invoke({
            "age": age,
            "gender": gender,
            "primary_symptoms": primary_symptoms,
            "doctor_type": doctor_type,
            "report_type": report_type,
            "current_date": current_date
        })
        return report
    except Exception as e:
        error_message = str(e)
        if "API_KEY_INVALID" in error_message or "429" in error_message:
            return f"API Error: Please check your Gemini API key configuration. Current error: {error_message[:200]}"
        elif "503" in error_message or "500" in error_message:
            return f"Service Error: Gemini API service is currently unavailable. Error: {error_message[:200]}"
        else:

            return f"An error occurred while generating the report: {error_message[:300]}"
