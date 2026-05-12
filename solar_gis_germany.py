from pvlib.iotools import get_pvgis_tmy
import pvlib
import pandas as pd
import numpy as np
import os
import time

# =====================================================
# Project: Germany-wide PV potential assessment
# Data source: PVGIS TMY meteorological data
# Output: GIS-ready CSV for QGIS
# =====================================================

# Create output folders
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# PV system assumptions
system_capacity_kw = 10
performance_ratio = 0.80
surface_tilt = 30
surface_azimuth = 180
timezone = "Europe/Berlin"

# =====================================================
# Germany grid
# Coarse grid first to avoid too many PVGIS requests
# =====================================================

latitudes = np.arange(47.5, 55.1, 1.0)
longitudes = np.arange(6.0, 15.1, 1.0)

results = []

for lat in latitudes:
    for lon in longitudes:
        print(f"Processing location: lat={lat:.2f}, lon={lon:.2f}")

        try:
            # Get real meteorological data from PVGIS
            tmy, meta = get_pvgis_tmy(
                latitude=lat,
                longitude=lon,
                outputformat="json",
                map_variables=True
            )

            tmy.index = tmy.index.tz_convert(timezone)

            location = pvlib.location.Location(
                latitude=lat,
                longitude=lon,
                tz=timezone
            )

            solar_position = location.get_solarposition(tmy.index)

            poa = pvlib.irradiance.get_total_irradiance(
                surface_tilt=surface_tilt,
                surface_azimuth=surface_azimuth,
                dni=tmy["dni"],
                ghi=tmy["ghi"],
                dhi=tmy["dhi"],
                solar_zenith=solar_position["zenith"],
                solar_azimuth=solar_position["azimuth"]
            )

            power_kw = system_capacity_kw * (poa["poa_global"] / 1000) * performance_ratio
            power_kw = power_kw.clip(lower=0)

            annual_energy_kwh = power_kw.sum()
            specific_yield = annual_energy_kwh / system_capacity_kw

            results.append({
                "lat": lat,
                "lon": lon,
                "annual_energy_kwh": annual_energy_kwh,
                "specific_yield_kwh_per_kwp": specific_yield
            })

            print(f"  Annual yield: {annual_energy_kwh:.1f} kWh")

            # Be polite to PVGIS server
            time.sleep(0.5)

        except Exception as e:
            print(f"  Failed at lat={lat}, lon={lon}: {e}")

            results.append({
                "lat": lat,
                "lon": lon,
                "annual_energy_kwh": None,
                "specific_yield_kwh_per_kwp": None
            })

# =====================================================
# Export GIS-ready CSV
# =====================================================

df = pd.DataFrame(results)

output_path = "data/germany_pv_potential_pvgis.csv"
df.to_csv(output_path, index=False)

print("===================================")
print("Germany-wide PVGIS analysis finished")
print(f"File saved: {output_path}")
print("===================================")
print(df.head())