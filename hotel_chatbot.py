import streamlit as st
import requests
import base64
import os
import urllib.parse
import gradio as gr
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Page configuration with travel theme
st.set_page_config(
    page_title="✈️ Travel Companion",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS with travel-themed gradients and animations
st.markdown("""
    <style>
            

        /* Footer styling */
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0F172A;
            color: #94A3B8;
            text-align: center;
            padding: 1rem;
            border-top: 1px solid #334155;
            z-index: 100;
        }
        
        .footer a {
            color: #06B6D4;
            text-decoration: none;
            margin: 0 10px;
            transition: all 0.3s ease;
        }
        
        .footer a:hover {
            color: #0EA5E9;
            text-decoration: underline;
        }
        
        .footer-content {
            display: flex;
            justify-content: center;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .footer-social {
            display: flex;
            gap: 15px;
        }
        
        @media (max-width: 768px) {
            .footer-content {
                flex-direction: column;
                gap: 10px;
            }
        }
            
        
        
        /* Main header container - matches dark navy theme */
        header.stAppHeader {
            background: #0F172A !important;
            
            
        }
        
        /* Decoration bar (if visible) */
        .stDecoration {
            background: #06B6D4 !important;  /* Teal accent color */
            height: 4px !important;
        }
        
        /* Toolbar buttons and menu */
        .stAppToolbar {
            background: transparent !important; 
        }
            
        /* Deploy button styling */
        button[data-testid="stBaseButton-header"] {
            background: #1E293B !important;
            color: #E2E8F0 !important;
            border-radius: 4px !important;
            border: 1px solid #334155 !important;
        }
        
        /* Hamburger menu icon */
        .stMainMenu button svg{
            color: #06B6D4 !important;  /* Your teal accent color */
            width: 24px !important;
            height: 24px !important;
        }
            
        .stMainMenu button:hover svg {
            color: #0EA5E9 !important;  /* Brighter teal on hover */
            transform: scale(1.1);
        }
            
        .stMainMenu button[aria-expanded="true"] svg {
            color: #FFFFFF !important;  /* Pure white when menu is open */
        }
        
        /* Hover effects */
        button[data-testid="stBaseButton-header"]:hover {
            background: #06B6D4 !important;
            color: #0F172A !important;
        }
            
        /* Target the arrow button specifically */
        button.st-emotion-cache-l1ktzw[data-testid="stBaseButton-headerNoPadding"] {
            background: transparent !important;
            padding: 8px !important;
            border-radius: 4px !important;
            transition: all 0.3s ease !important;

        }
        
        /* Arrow icon color */
        button.st-emotion-cache-l1ktzw svg {
            color: #06B6D4 !important;  /* Your teal accent color */
            width: 24px !important;
            height: 24px !important;
        }
        
        /* Hover states */
        button.st-emotion-cache-l1ktzw:hover {
            background: rgba(6, 182, 212, 0.1) !important;  /* Light teal overlay */
        }
        
        button.st-emotion-cache-l1ktzw:hover svg {
            color: #0EA5E9 !important;  /* Brighter teal on hover */
            transform: scale(1.1);
        }
        
        /* Active/click state */
        button.st-emotion-cache-l1ktzw:active svg {
            transform: scale(0.95);
        }

                
        @media screen and (max-width: 768px) {
            header.stAppHeader {
                padding: 0.5rem !important;
            }
        }

        
            
        /* Main background gradient */
        .stApp {
            background: #0F172A;
            color: #E2E8F0;
        }
        
        
        /* Header with travel gradient */
        .st-emotion-css-1kyxreq, h1, h2, h3 {
            color: #E2E8F0 !important;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
            padding: 1rem;
            border-radius: 0.5rem;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
            
        /* Change search bar placeholder text color */
        .stTextInput input::placeholder {
            color: #94A3B8 !important;  /* Your muted blue-gray color */
            opacity: 1 !important;     /* Ensure full visibility */
        }
            
        /* Change the search bar label text color */
        .stTextInput label {
            color: #E2E8F0 !important;  /* Your light text color */
            font-size: 1rem !important;
            font-weight: 500 !important;
        }
        
        /* Optional: Add subtle animation to label */
        .stTextInput label {
            transition: color 0.3s ease;
        }
        .stTextInput:hover label {
            color: #06B6D4 !important;  /* Teal accent on hover */
        }
        
        /* Search input with subtle animation */
        .stTextInput input {
            background: #1E293B;
            color: #E2E8F0 !important;
            border: 1px solid #334155;
            transition: all 0.3s ease;
            border: 2px solid #e0e0e0;
        }
        .stTextInput input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }
        
        /* Beautiful cards with hover effects */
        .card {
            background: #1E293B;
            border: 1px solid #334155;
            color: #E2E8F0;
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
            border: none;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
        }
        .hotel-card {
            background: white;
        }
        .hotel-card::before {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        }
        .attraction-card {
            background: white;
        }
        .attraction-card::before {
            background: linear-gradient(90deg, #f78ca0 0%, #f9748f 100%);
        }
        .activity-card {
            background: white;
        }
        .activity-card::before {
            background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
        }
        
        /* Rating stars */
        .rating {
            color: #FFD700;
            font-weight: bold;
        }
        
        /* Tabs with travel colors */
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            gap: 1;
            padding: 0;
        }

        .stTabs [data-baseweb="tab"] {
            flex: 1;
            text-align: center;
            padding: 0.75rem 0.5rem;
            margin: 0;
            border-radius: 0.5rem 0.5rem 0 0;
            transition: all 0.3s ease;
        }
        .stTabs [aria-selected="true"] {
            background: #06B6D4;
            color: #0F172A !important;
            border-radius: 0.5rem 0.5rem 0 0;
            flex: 1;
        }
        .stTabs [aria-selected="false"] {
            background: #1E293B;
            color: #94A3B8;
            flex: 1;
        }
        
        /* Button with travel gradient */
        .stButton>button {
            background: #06B6D4;
            color: #0F172A;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: #0EA5E9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Sidebar with subtle pattern */
        .sidebar .sidebar-content {
            background: #0F172A;
            border-right: 1px solid #334155;
            background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        }
        
        /* Map container */
        .stMap {
            border: 1px solid #334155;
            border-radius: 0.8rem;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Responsive adjustments */
        @media screen and (max-width: 768px) {
            .stTextInput input {
                font-size: 1rem;
            }
            .stTabs [data-baseweb="tab-list"] {
                flex-direction: row;
                flex-wrap: wrap;
            }
            .stTabs [data-baseweb="tab"] {
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Title with travel theme
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #E2E8F0; font-size: 2.5rem; margin-bottom: 0.5rem;">
            ✈️ Travel Companion
        </h1>
        <p style="color: #06B6D4; font-size: 1.1rem;">
            Discover the world's best hotels, attractions, and hidden gems
        </p>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "last_search" not in st.session_state:
    st.session_state.last_search = None
# Sidebar with travel inspiration
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h3 style="color: #E2E8F0;">🌎 Travel Inspiration</h3>
            <p style="color: #06B6D4;">Try searching for:</p>
        </div>
    """, unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        if st.button("Paris", use_container_width=True):
            st.session_state.search_input = "Hotels in Paris"
    with cols[1]:
        if st.button("Tokyo", use_container_width=True):
            st.session_state.search_input = "Things to do in Tokyo"
    cols = st.columns(2)
    with cols[0]:
        if st.button("New York", use_container_width=True):
            st.session_state.search_input = "Attractions in New York"
    with cols[1]:
        if st.button("Dubai", use_container_width=True):
            st.session_state.search_input = "Hotels in Dubai"
    st.markdown("---")
    st.markdown("""
        <div style="margin-top: 1.5rem;">
            <h4 style="color: #4a4a4a;">Recent Searches</h4>
    """, unsafe_allow_html=True)
    if st.session_state.history:
        for i, message in enumerate(reversed(st.session_state.history[-3:])):
            st.markdown(f"""
                <div style="background: white; padding: 0.5rem; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                    🔍 {message.title()}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="color: #667eea; font-style: italic;">
                No recent searches yet
            </div>
        """, unsafe_allow_html=True)
# Search section with travel vibe
with st.container():
    query = st.text_input(
        "Where would you like to travel?",
        placeholder="e.g. 'Beach resorts in Bali' or 'Historic sites in Rome'",
        key="search_input"
    )
    search_btn = st.button("Explore Now", type="primary", use_container_width=True)
# API functions (same as before)
def get_location(city):
    location_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(city)}&key={GOOGLE_API_KEY}"
    res = requests.get(location_url).json()
    if res["status"] == "OK":
        location = res["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        return None, None
def get_hotels(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=10000&type=lodging&key={GOOGLE_API_KEY}"
    res = requests.get(url).json()
    return res.get("results", []) if res["status"] == "OK" else []
def get_attractions(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=10000&type=tourist_attraction&key={GOOGLE_API_KEY}"
    res = requests.get(url).json()
    return res.get("results", []) if res["status"] == "OK" else []
def get_things_to_do(lat, lon):
    types = ["park", "museum", "shopping_mall", "art_gallery", "zoo", "aquarium"]
    all_places = []
    for place_type in types:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=10000&type={place_type}&key={GOOGLE_API_KEY}"
        res = requests.get(url).json()
        if res["status"] == "OK":
            all_places.extend(res.get("results", []))
    return list({p["place_id"]: p for p in all_places}.values())
def extract_city(query):
    lower = query.lower()
    if "in" in lower:
        city = query.split("in")[-1].strip()
        # return query.split("in")[-1].strip()
    else:
        city = query.strip()
    return city.title()
# Main search functionality
if (query and search_btn) or (query and st.session_state.last_search != query):
    st.session_state.last_search = query
    city = extract_city(query)
    with st.spinner(f"✈️ Discovering the best of {city}..."):
        lat, lon = get_location(city)
        if lat and lon:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.history.append(f"{timestamp}: {query}")
            hotels = get_hotels(lat, lon)
            attractions = get_attractions(lat, lon)
            things_to_do = get_things_to_do(lat, lon)
            st.success(f"✨ Found amazing places in **{city.capitalize()}**")
            # Create tabs with travel icons
            tab1, tab2, tab3, tab4 = st.tabs(["🏨 Hotels", "🗼 Attractions", "🎭 Activities", "🗺️ Map View"])
            with tab1:
                if hotels:
                    st.markdown(f'<h3 style="text-align: center; color: #E2E8F0; margin-bottom: 1rem;">Top Hotels in {city.title()}</h3>', unsafe_allow_html=True)
                    for hotel in hotels[:10]:
                        name = hotel["name"]
                        address = hotel.get("vicinity", "Address not available")
                        rating = hotel.get("rating", "N/A")
                        price_level = hotel.get("price_level", "N/A")
                        price_icons = "💲" * price_level if isinstance(price_level, int) else ""
                        st.markdown(f"""
                            <div class="card hotel-card">
                                <h4 style="color: #28282B;">{name}</h4>
                                <p style="color: #94A3B8;">📍 {address}</p>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <p style="color: #94A3B8;">⭐ <span class="rating">{rating}</span>/5</p>
                                    <p>{price_icons}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No hotels found in this area. Try expanding your search radius.")
            with tab2:
                if attractions:
                    st.markdown(f'<h3 style = "text-align: center; color: #E2E8F0; margin-bottom: 1rem;">Must-See Attractions in {city.title()}</h3>', unsafe_allow_html=True)
                    for place in attractions[:10]:
                        name = place["name"]
                        rating = place.get("rating", "N/A")
                        st.markdown(f"""
                            <div class="card attraction-card">
                                <h4 style="color: #28282B;">{name}</h4>
                                <p style="color: #94A3B8;">⭐ <span class="rating">{rating}</span>/5</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No attractions found. Try a different location or broader category.")
            with tab3:
                if things_to_do:
                    st.markdown(f'<h3 style="text-align: center; color: #E2E8F0; margin-bottom: 1rem;">Fun Activities in {city.title()}</h3>', unsafe_allow_html=True)
                    for place in things_to_do[:10]:
                        name = place["name"]
                        address = place.get("vicinity", "Address not available")
                        rating = place.get("rating", "N/A")
                        st.markdown(f"""
                            <div class="card activity-card">
                                <h4 style="color: #28282B;">{name}</h4>
                                <p style="color: #94A3B8;">📍 {address}</p>
                                <p style="color: #94A3B8;">⭐ <span class="rating">{rating}</span>/5</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No activities found. Try searching for specific activities.")
            with tab4:
                st.markdown(f'<h3 style="text-align: center; color: #E2E8F0; margin-bottom: 1rem;">{city.title()} on the Map</h3>', unsafe_allow_html=True)
                st.map(data={"lat": [lat], "lon": [lon]}, zoom=12)
        else:
            st.error("We couldn't find that location. Please try a different city or spelling.")
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <a href="#">Jhanvi (xxxxxxxx)</a>
            <a href="#">Aditya (xxxxxxxx)</a>
            <a href="#">Riya (xxxxxxxx)</a>
        </div>
    </div>
""", unsafe_allow_html=True)


