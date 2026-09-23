---
id: bed_region
title: Bed to county index (derived)
steward: this repository
url: null
status: VERIFIED
tier: DERIVED
access: ["Run src/derive/bed_region.py; it wrote catalog/tables/bed_region.csv, 1 row, 2026-09-22"]
license: "as the inputs' records state"
variables: [bed, region]
retrieved: null
file: catalog/tables/bed_region.csv
derived_from:
  inputs: [noaa_oni, catalog/sites/]
  script: src/derive/bed_region.py
  parameters: {predicate: intersects, crs: "EPSG:3310", tolerance: 0}
topics: []
regions: [scb.mainland]
---
