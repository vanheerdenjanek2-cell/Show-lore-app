import streamlit as st
from tavily import TavilyClient
import openai

# --- Setup Keys ---
# In a real app, use st.secrets for safety!
TAVILY_API_KEY = "your_tavily_key_here"
OPENAI_API_KEY = "your_openai_key_here"

client_tavily = TavilyClient(api_key=TAVILY_API_KEY)
openai.api_key = OPENAI_API_KEY

def research_lore(show_name):
    """Uses Tavily to find lore and OpenAI to summarize it."""
    query = f"{show_name} animated series deep lore, world building, and essential plot points"
    
    # 1. Search the internet for lore
    search_result = client_tavily.search(query=query, search_depth="advanced", max_results=5)
    
    # 2. Combine search results into one big text block
    context = "\n".join([f"Source {i+1}: {res['content']}" for i, res in enumerate(search_result['results'])])
    
    # 3. Use AI to turn that data into a cool lore guide
    prompt = f"""
    You are a Lore Expert. Based on the following search results about '{show_name}', 
    create a deep lore guide. Include:
    1. The World/Setting
    2. Major Lore Secrets
    3. Key Story Arcs to watch
    
    Search Data:
    {context}
    """
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# --- Streamlit UI ---
st.title("🌐 AI Lore Researcher")
st.write("Enter any show, and I'll scour the internet to find its deepest secrets.")

show_input = st.text_input("Enter Show Name:", placeholder="e.g., Adventure Time")

if st.button("Research Lore"):
    if show_input:
        with st.spinner(f"Agent is researching '{show_input}' across the web..."):
            try:
                lore_report = research_lore(show_input)
                st.markdown(lore_report)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a show name first!")