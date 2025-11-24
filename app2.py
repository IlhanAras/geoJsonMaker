import streamlit as st
import folium
from streamlit_folium import folium_static
import json

st.title("✈️ Dünya + Türkiye İller Haritası (Tamamen Çevrimdışı)")

# --- 1. Veri Yükleme ---
try:
    with open("world_plus_turkey_provinces.geojson", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("Hata: 'world_plus_turkey_provinces.geojson' dosyası bulunamadı.")
    st.stop()
except json.JSONDecodeError:
    st.error("Hata: GeoJSON dosyasının içeriği bozuk.")
    st.stop()


# --- 2. Harita Oluşturma ---
# tiles=None: İnternet ihtiyacını kesen kritik ayar.
# Harita merkezini Türkiye'ye daha yakın bir yere çektim (isteğe bağlı).
m = folium.Map(location=[38, 35], zoom_start=5, tiles=None)


# --- 3. Uçak İşaretleyicisini Ekleme (Çevrimdışı) ---
# İşaretleyici (Marker) ve İkon (Icon), Folium'un yerel kaynaklarını kullanır.

# Uçak 1: Türkiye Üzerinde
folium.Marker(
    location=[40.00, 32.50], # Ankara civarında bir nokta
    popup="**Uçuş No: TK2511**<br>Yükseklik: 35000 ft<br>Hız: 800 km/s",
    icon=folium.Icon(
        icon="plane",       # Uçak ikonu
        prefix="fa",        # Font Awesome (Yerel olarak gömülüdür)
        color="red",        # Marker rengi
        icon_color="white"
    )
).add_to(m)

# Uçak 2: Avrupa Üzerinde
folium.Marker(
    location=[45.00, 15.00], # Hırvatistan civarı
    popup="**Uçuş No: LH540**<br>Kalkış: Almanya, Varış: Yunanistan",
    icon=folium.Icon(
        icon="plane",
        prefix="fa",
        color="darkblue"
    )
).add_to(m)


# --- 4. GeoJSON Sınırlarını Ekleme ---
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
    # tooltip=None: Sizin de belirttiğiniz gibi, internet ihtiyacını keser.
    tooltip=None 
).add_to(m)


# --- 5. Haritayı Gösterme ---
folium_static(m)