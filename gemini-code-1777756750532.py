import streamlit as st
from tavily import TavilyClient
from google import genai

# --- SECURE KEY LOADING ---
# These names inside the brackets MUST stay as TAVILY_API_KEY and GOOGLE_API_KEY
# Do NOT put the long 'tvly-' or 'AIza-' keys here. 
# Those keys stay in the "Secrets" dashboard only.
t_key = st.secrets.get("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")
g_key = st.secrets.get("AIzaSyCb-amhqIl1UB-my8BgH-B0RgdniiwA6F0")

st.title("🕵️ Lore Researcher")

# Diagnostic check to help us find issues
if not t_key or not g_key:
    st.error("🚨 Key Mismatch!")
    st.write(f"Tavily Key Found: {'✅' if t_key else '❌'}")
    st.write(f"Google Key Found: {'✅' if g_key else '❌'}")
    st.info("Ensure your Secrets dashboard has the keys named TAVILY_API_KEY and GOOGLE_API_KEY.")
    st.stop()

# Initialize tools
tavily = TavilyClient(api_key=t_key)
client = genai.Client(api_key=g_key)

show_query = st.text_input("Enter Show Name:", placeholder="e.g. Gravity Falls")

if st.button("Research"):
    with st.spinner("Searching and Analyzing..."):
        try:
            # 1. Search
            search = tavily.search(query=f"{show_query} lore secrets", search_depth="advanced")
            context = "\n".join([r['content'] for r in search['results']])
            
            # 2. Generate using Gemini
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"Explain deep lore for {show_query} using this data: {context}"
            )
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
