import streamlit as st
from tavily import TavilyClient
from google import genai

# --- SECURE KEY LOADING ---
# This code checks for the EXACT names in your Secrets dashboard
t_key = st.secrets.get"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"
g_key = st.secrets.get"AIzaSyDP_VsCgFF5orvyMHtROEaStJwjlen2asE"

# --- UI SETUP ---
st.title("🕵️ Lore Researcher")

# DIAGNOSTIC BOX: If this is red, the dashboard is the problem.
if not t_key or not g_key:
    st.error("🚨 KEY MISMATCH DETECTED")
    st.write(f"Tavily Key Found: {'✅' if t_key else '❌'}")
    st.write(f"Google Key Found: {'✅' if g_key else '❌'}")
    st.info("Check Settings > Secrets. Ensure they are ALL CAPS with underscores.")
    st.stop()

# Initialize with the new 2026 SDK
tavily = TavilyClient(api_key=t_key)
client = genai.Client(api_key=g_key)

show_query = st.text_input("Enter Show Name:", placeholder="e.g. Gravity Falls")

if st.button("Research"):
    with st.spinner("Searching and Analyzing..."):
        try:
            # 1. Search
            search = tavily.search(query=f"{show_query} lore secrets", search_depth="advanced")
            context = "\n".join([r['content'] for r in search['results']])
            
            # 2. Generate using Gemini 2.0 Flash (Modern API)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"Explain deep lore for {show_query} using this data: {context}"
            )
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
