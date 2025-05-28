import streamlit as st
import os
import streamlit as st

# Your API key setup here
openai.api_key = st.secrets["openai"]["api_key"]

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

st.title("📢 Marketing Copy Generator")

# ✅ Multiselect Goal Type
combined_goals = [
    "Travel", "Gadget", "Shopping", "Health Insurance", "Car Insurance",
    "Wealth Creation", "Retirement", "Parenting"
]
goal_type = st.multiselect("Select Goal Type(s)", combined_goals)

age_group = st.selectbox("Age Group", ["18-25", "26-35", "36+"])
user_type = st.selectbox("Target Audience", ["Returning User", "New User"])
channel = st.selectbox("Channel", ["WhatsApp", "Email", "SMS", "Web Banner"])
tone = st.selectbox("Tone", ["Friendly", "Urgent", "Persuasive", "Informative"])
# 🔁 Use-case templates
use_case_template = st.selectbox("Campaign Type", [
    "General", 
    "Festival campaign (e.g., Diwali sale)",
    "Offer launch (e.g., ₹500 off)",
    "Reminder for matured goal",
    "Tax-saving season push"
])
brand = st.text_input("Optional Brand or Offer (e.g. Samsung, Get ₹500 off)")
cta = st.text_input("Optional CTA (e.g. Start Saving Today)")
context = st.text_area("Optional Context (e.g. Monsoon offer, 5th anniversary, tax-saving season, etc.)")
creativity_level = st.slider("Creativity Level", min_value=0.2, max_value=1.2, value=0.7, step=0.1)

# Function to trim long lines
def polish_output(raw_text):
    lines = raw_text.strip().split("\n")
    final_lines = []
    for line in lines:
        if line.strip():
            if len(line) > 200:
                line = line[:197] + "..."
            final_lines.append(line)
    return "\n".join(final_lines)

output = None

if st.button("Generate Copy"):
    selected_goals = ", ".join(goal_type) if goal_type else "Not specified"
    prompt = f"""
    You are a fintech marketing expert working for an app that helps users invest in mutual funds for upcoming expenses like {selected_goals}.

    Your task is to write **3 short, high-converting marketing copies** tailored for:

    - Goal Type(s): {selected_goals}
    - Age Group: {age_group}
    - User Type: {user_type}
    - Channel: {channel}
    - Tone: {tone}
    - Campaign Type: {use_case_template}
    - Brand/Offer: {brand if brand else "None"}
    - CTA: {cta if cta else "None"}
    - Additional Context: {context if context else "None"}
    - Temperature : {creativity_level}

    📢 Instructions:
    - Each copy must be under 200 characters for WhatsApp/SMS and under 600 for Email/Web.
    - Adapt style and language to suit the user's age group and whether they're new or returning.
    - Emphasize how this goal-based investing benefits the user (e.g., smart savings, peace of mind, reward).
    - Avoid jargon, be clear, human, and impactful.
    - Use emotional hooks and strong CTA.

    Output format:
    1. [Copy 1]
    2. [Copy 2]
    3. [Copy 3]
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a fintech marketing expert for a mutual fund investment app."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    raw_output = response.choices[0].message.content
    output = polish_output(raw_output)

    # Save to history
    st.session_state.history.append({
        "goal": selected_goals,
        "age": age_group,
        "user_type": user_type,
        "channel": channel,
        "tone": tone,
        "use_case": use_case_template,
        "creativity_level": creativity_level,
        "brand": brand,
        "cta": cta,
        "context": context,
        "output": output
    })

# Output Section
if output:
    st.markdown("### 📝 Generated Copies:")
    st.text_area("Generated Output", output, height=200, label_visibility="collapsed")

# History Section
if st.session_state.history:
    with st.expander("📜 View Copy History"):
        for i, item in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.markdown(
                f"**{i}. {item['goal']} | {item['channel']} | {item['tone']} | Creativity: {item['creativity_level']}**"
            )
            st.text(item["output"])
            st.markdown("---")
