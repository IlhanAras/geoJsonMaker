import streamlit as st
import folium
from streamlit_folium import folium_static
import json

st.title("Dünya + Türkiye İller Haritası (Offline)")

with open("world_plus_turkey_provinces.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

m = folium.Map(location=[20, 0], zoom_start=2, tiles=None)

folium.GeoJson(
    data,
    name="World + Turkey Provinces",
    style_function=lambda x: {
        "fillColor": (
            "orange" if x["properties"].get("adm0_a3") == "TUR"
            else "lightgray"
        ),
        "color": "white",
        "weight": 1,
        "fillOpacity": 0.6,
    },
    tooltip=None
).add_to(m)

folium_static(m)
