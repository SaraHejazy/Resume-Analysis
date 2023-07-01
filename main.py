import streamlit as st
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_trf")
# nlp = spacy.load("en_core_web_sm")


def analyze_resume(resume_text,keywords):
    doc = nlp(resume_text)

    # Perform NLP analysis on the resume text
    named_entities = set()
    keyword_occurrences = {keyword: 0 for keyword in keywords}  # Initialize keyword occurrences counter

    for ent in doc.ents:
        # Count occurrences of keywords in the resume text
        for keyword in keywords:
            if keyword.lower() in ent.text.lower():
                keyword_occurrences[keyword] += 1
        # Filter out entities that are duplicates or locations
        if ent.label_ not in ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']:
            if ent.text.lower() not in named_entities and ent.label_ != 'GPE':
                named_entities.add(ent.text.lower())

    # Example: Extract noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]

    # Return the analysis results
    analysis_results = {
        "Keyword Occurrences:": keyword_occurrences,
        "Named Entities": named_entities,
        "Noun Phrases": noun_phrases
    }

    return analysis_results


# Streamlit app code
def main():
    # Set the app title
    st.title("Job Application NLP Analysis")

    # Create a textarea for the resume text input
    resume_text = st.text_area("Enter your resume text", height=300)

    # Create a text input for the keywords
    keywords_input = st.text_input("Enter the keywords (comma-separated)", "")

    # Split the input keywords into a list
    keywords = [keyword.strip() for keyword in keywords_input.split(",") if keyword.strip()]

    # Add a button to trigger the NLP analysis
    if st.button("Analyze"):
        # Call the analyze_resume function and display the results
        analysis_results = analyze_resume(resume_text,keywords)

        st.write("NLP analysis results:")
        for key, values in analysis_results.items():
            st.subheader(key)
            st.write(values)


# Run the app
if __name__ == "__main__":
    main()
