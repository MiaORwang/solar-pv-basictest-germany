# Germany-wide Solar PV Potential Assessment using PVGIS and QGIS

## Overview
This project assesses the spatial variability of solar PV potential across Germany using real meteorological data from PVGIS and visualises the results in QGIS.

The goal is to demonstrate a workflow combining:
- PVGIS meteorological data
- Python/PVlib-based energy yield estimation
- GIS-ready spatial data output
- QGIS-based cartographic visualisation

## Methodology

A coarse grid of locations across Germany was generated. For each grid point, typical meteorological year data were retrieved from PVGIS and used to estimate annual PV energy yield for a simplified 10 kWp PV system.
Main assumptions:
- System capacity: 10 kWp
- Performance ratio: 0.80
- Module tilt: 30°
- Module azimuth: 180° south-facing

## Outputs
- Germany-wide PV potential CSV
- QGIS project file
- Final map showing:
  - Annual energy yield [kWh]
  - Specific yield [kWh/kWp]

## Interpretation
The results show higher PV potential in southern Germany compared with northern Germany, reflecting spatial differences in solar irradiation.

## Limitations
This is a simplified screening-level analysis. It does not yet include:
- Detailed terrain effects
- Local shading
- Grid connection constraints
- Land-use restrictions
- Protected areas
- Project-specific engineering constraints

## Tools
- Python
- PVlib
- PVGIS
- Pandas
- QGIS

## Author
MiaORwang
