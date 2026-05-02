import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# --- 1. SECURE KEY LOADING ---
# Ensure you add TAVILY_API_KEY and GOOGLE_API_KEY to your Streamlit Secrets!
try:
    TAVILY_KEY = st.secrets["tvly-dev-3HS3ax-WTnZLeRqRfPeQboEgJLF21FGd3INARKWJprY9FhtE5TAVILY_API_KEY"]
    GOOGLE_KEY = st.secrets["AIzaSyDP_VsCgFF5orvyMHtROEaStJwjlen2asE"]
except KeyError:
    st.error("Missing API Keys! Go to Settings > Secrets and add TAVILY_API_KEY and GOOGLE_API_KEY.")
    st.stop()

# Initialize the Free Tools
tavily = TavilyClient(api_key=TAVILY_KEY)
genai.configure(api_key=GOOGLE_KEY)

# Using Gemini 1.5 Flash (It's fast and has a great free tier)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. THE RESEARCH ENGINE ---
def get_ai_lore(show_name):
    # Search the web for free (Tavily has a free tier for 1,000 searches/mo)
    search_query = f"{show_name} animated series deep lore and plot secrets"
    search_results = tavily.search(query=search_query, search_depth="advanced")
    
    # Combine the search findings
    context = ""
    for result in search_results['results']:
        context += f"\nSource: {result['url']}\nContent: {result['content']}\n"

    # Use the Gemini API to write the lore report
    prompt = f"You are a lore expert. Based on these search results, explain the deep lore of {show_name}. Focus on secrets a casual fan wouldn't know:\n{context}"
    
    response = model.generate_content(prompt)
    return response.text

# --- 3. THE USER INTERFACE ---
st.set_page_config(page_title="Free AI Lore Agent", page_icon="🌐")

st.title("🌐 Free AI Lore Researcher")
st.write("Using Gemini API")

show_input = st.text_input("Enter Show Name:", placeholder="e.g., Adventure Time")

if st.button("Research Lore"):
    if show_input:
        with st.spinner(f"Searching the internet for {show_input}..."):
            try:
                lore_report = get_ai_lore(show_input)
                st.markdown("---")
                st.markdown(lore_report)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a show name first!")
