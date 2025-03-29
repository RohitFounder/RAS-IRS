import streamlit as st
import pandas as pd
import os

# File to store scores
SCORES_FILE = "scores.csv"

# Load scores file or create an empty one
if os.path.exists(SCORES_FILE):
    scores_df = pd.read_csv(SCORES_FILE)
else:
    scores_df = pd.DataFrame(columns=["Judge", "Category", "Presentation", "Score"])
    scores_df.to_csv(SCORES_FILE, index=False)

# Streamlit Page Setup
st.set_page_config(
    page_title="RAS~IRS RESEARCH PRESENTATIONS",
    page_icon="C:/Users/Lenovo/Downloads/CONSORTIUM (1).png",
    layout="wide"
)

# Header with Logo
col1, col2 = st.columns([1, 6])
with col1:
    st.image("C:/Users/Lenovo/Downloads/CONSORTIUM (1).png", width=100)
with col2:
    st.title("🔬 RAS~IRS RESEARCH PRESENTATIONS")

# Judge Selection
judges = {
    "Mentors": ["Dr. Indraneil Mukherjee", "Dr. Vamsi Chakradhar"],
    "Peers": ["Dr. Rohit Ganduboina", "Dr. Palak Dutta", "Dr. Keerthi Palagati"]
}
judge = st.selectbox("Select Your Name", sum(judges.values(), []))

# Password Protection for Dr. Rohit Ganduboina
admin_password = "Plasticsurg@2023"  # 🔒 Secure password

if judge == "Dr. Rohit Ganduboina":
    st.subheader("🛠 Admin Options")
    password_input = st.text_input("Enter Admin Password:", type="password")

    if password_input == admin_password:
        st.success("✅ Access Granted!")
        if st.button("🚨 Reset All Scores"):
            scores_df = pd.DataFrame(columns=["Judge", "Category", "Presentation", "Score"])
            scores_df.to_csv(SCORES_FILE, index=False)
            st.success("✅ All scores have been reset!")
    elif password_input:
        st.error("❌ Incorrect Password! Access Denied.")


# Select Presentation Type
category = st.radio("Select Presentation Type", ["Oral", "Poster"])
presentations = {
    "Oral": [
        "Diabetes mellitus (type 2) - Ibeojo, David Kitua",
        "Ablation Techniques for Atrial Fibrillation - Esther Amarachi Ojukwu",
        "Racial Disparities in Melanoma - Cankutay Muderrisoglu",
        "Leprosy Diagnosis in Coastal Karnataka - Dr Sindhuja",
        "Phage Therapy Innovations - Ojukwu, Esther Amarachi"
    ],
    "Poster": [
        "Microbiota & IVF Success - Taibia Rahman",
        "Healthcare Disparities in BIPOC - Ashling Teniola",
        "Ocular Microbiome Therapy - Sophia Marie",
        "Trigeminal Neuralgia Surgery - Esther Amarachi Ojukwu",
        "Anti-NMDAR Encephalitis Case - Joan Tumaini Mchunga",
        "Robotic Microsurgery - Symani Surgical System"
    ]
}
presentation = st.selectbox("Select Presentation", presentations[category])

# Scoring Criteria
mentor_criteria = {
    "Scientific Depth & Novelty": 10,
    "Presentation Clarity & Organization": 10,
    "Critical Thinking & Analysis": 10,
    "Engagement & Q&A Handling": 10,
    "Overall Impact & Contribution": 10
}
peer_criteria = {
    "Content & Relevance": 5,
    "Presentation & Communication": 5,
    "Visual Aids & Slide Quality": 5,
    "Q&A Performance": 5,
    "Overall Impact": 5
}

criteria = mentor_criteria if judge in judges["Mentors"] else peer_criteria

# Score Inputs
st.subheader("📊 Rate the Presentation")
scores = {crit: st.slider(crit, 1, max_score, max_score//2) for crit, max_score in criteria.items()}

if st.button("Submit Score"):
    total_score = sum(scores.values())
    
    if ((scores_df["Judge"] == judge) & (scores_df["Presentation"] == presentation)).any():
        st.warning("⚠️ You have already submitted a score for this presentation!")
    else:
        new_entry = pd.DataFrame([[judge, category, presentation, total_score]], columns=["Judge", "Category", "Presentation", "Score"])
        scores_df = pd.concat([scores_df, new_entry], ignore_index=True)
        scores_df.to_csv(SCORES_FILE, index=False)
        st.success(f"✅ Score Submitted: {total_score} points")

# Display Final Results After All Judges Submit
total_judges = len(sum(judges.values(), []))
submitted_judges = len(scores_df["Judge"].unique())

if submitted_judges >= total_judges:
    st.subheader("🏆 Final Results")

    # Aggregate Scores
    final_scores = scores_df.groupby(["Presentation", "Category"])["Score"].mean().reset_index()
    final_scores = final_scores.sort_values("Score", ascending=False)

    # Separate Results for Oral & Poster
    oral_winners = final_scores[final_scores["Category"] == "Oral"].head(2)
    poster_winners = final_scores[final_scores["Category"] == "Poster"].head(2)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🥇 Top 2 Oral Presentations")
        st.table(oral_winners)

    with col2:
        st.subheader("🥇 Top 2 Poster Presentations")
        st.table(poster_winners)

else:
    st.warning(f"Waiting for {total_judges - submitted_judges} more judges to submit scores...")