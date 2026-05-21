import streamlit as st
from tavily import TavilyClient
from google import genai

# --- HARDCODED KEYS ---
t_key = "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"
g_key = "AIzaSyCb-amhqIl1UB-my8BgH-B0RgdniiwA6F0"

st.title("🕵️ Lore Researcher")

# Initialize the tools directly with your strings
try:
    tavily = TavilyClient(api_key=t_key)
    client = genai.Client(api_key=g_key)
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

show_query = st.text_input("Enter Show Name:", placeholder="e.g. Adventure Time")

if st.button("Research"):
    if not show_query:
        st.warning("Please enter a show name.")
    else:
        with st.spinner("Searching and Analyzing..."):
            try:
                # 1. Search the web using Tavily
                search = tavily.search(query=f"{show_query} lore secrets", search_depth="advanced")
                context = "\n".join([r['content'] for r in search['results']])
                
                # 2. Generate a deep summary using Gemini 2.0 Flash
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=f"Explain deep lore for {show_query} using this web data: {context}"
                )
                st.markdown(response.text)
            except Exception as e:
                # If Google hits you with a quota limit, it will tell you nicely here
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    st.error("⚠️ Google Free Tier limit reached! Your daily quota will reset tonight at midnight Pacific Time.")
                else:
                    st.error(f"Error running the research: {e}")
