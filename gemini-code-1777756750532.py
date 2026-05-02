import streamlit as st
from tavily import TavilyClient
import google.generativeai as genai

# --- AUTO-CONFIG ---
st.set_page_config(page_title="Lore Agent", page_icon="🕵️")

# This part checks your dashboard for the "passwords" automatically
def initialize_agents():
    try:
        t_key = st.secrets["TAVILY_API_KEY"]
        g_key = st.secrets["GOOGLE_API_KEY"]
        
        # Connect to Tavily (Search)
        tavily_client = TavilyClient(api_key=t_key)
        
        # Connect to Gemini (Brain)
        genai.configure(api_key=g_key)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        return tavily_client, gemini_model
    except Exception:
        st.error("⚠️ Setup incomplete! You need to add your keys to the Streamlit Secrets dashboard.")
        st.info("Go to Settings > Secrets and paste your keys there.")
        st.stop()

tavily, model = initialize_agents()

# --- THE APP INTERFACE ---
st.title("🕵️ Lore Researcher")
st.write("I'll search the web and write a deep-dive report for you.")

show_query = st.text_input("Which show should I investigate?", placeholder="e.g. Adventure Time")

if st.button("Start Research"):
    if show_query:
        with st.spinner(f"Scouring the web for {show_query} lore..."):
            try:
                # 1. Automated Web Search
                search = tavily.search(query=f"{show_query} deep lore secrets and plot analysis", search_depth="advanced")
                context = "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in search['results']])
                
                # 2. AI Brain Processing
                prompt = f"Act as a lore expert. Using these search results, write a fascinating deep-dive report on {show_query}. Focus on hidden details:\n\n{context}"
                response = model.generate_content(prompt)
                
                # 3. Show Result
                st.markdown("### 📜 The Lore Report")
                st.markdown(response.text)
                st.success("Research complete!")
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a name first!")
