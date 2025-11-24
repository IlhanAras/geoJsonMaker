import geopandas as gpd
import pandas as pd

# --- Shapefile yolları (kendi dizinine göre düzenle) ---
COUNTRIES_SHP = "ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp"
PROVINCES_SHP = "ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp"

OUTPUT_GEOJSON = "world_plus_turkey_provinces.geojson"

# --- 1. Dünya ülkelerini yükle ---
countries = gpd.read_file(COUNTRIES_SHP)

# --- 2. Tüm diğer ülkeler + Türkiye ülkesi (admin_0) ---
world_countries = countries.copy()

# --- 3. Türkiye illerini admin_1 dosyasından çek ---
provinces = gpd.read_file(PROVINCES_SHP)

turkey_provinces = provinces[provinces["adm0_a3"] == "TUR"]

if turkey_provinces.empty:
    raise ValueError("Türkiye illeri bulunamadı. 'adm0_a3' alanını kontrol edin.")

# --- 4. Türkiye illerinin attribute'larını standartlaştır ---
turkey_provinces["feature_type"] = "turkey_province"
world_countries["feature_type"] = "country"

# GeoDataFrame’lerin kolonlarını eşitle (farklı kolonlar varsa birleştirmeye izin vermez)
common_cols = set(world_countries.columns).intersection(set(turkey_provinces.columns))
world_countries = world_countries[list(common_cols)]
turkey_provinces = turkey_provinces[list(common_cols)]

# --- 5. Hepsini tek GeoDataFrame içinde birleştir ---
combined = pd.concat([world_countries, turkey_provinces], ignore_index=True)

# --- 6. GeoJSON olarak kaydet ---
combined.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

print(f"GeoJSON oluşturuldu: {OUTPUT_GEOJSON}")
print(f"Ülke sayısı: {len(world_countries)}")
print(f"Türkiye şehir sayısı: {len(turkey_provinces)}")
print(f"Toplam feature sayısı: {len(combined)}")
