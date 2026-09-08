---
id: noaa_oni
title: Oceanic Niño Index
steward: NOAA Climate Prediction Center
url: https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
doi: null
status: VERIFIED
tier: FETCHED
access:
  - Open https://www.cpc.ncep.noaa.gov/data/indices/
  - Under the seasonal ERSSTv6 Niño 3.4 entry, follow the link labelled
    "Data (Oceanic Nino Index)" to https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
  - Download that file over HTTPS; no account, key or referrer is required
    (HTTP 200, 2026-09-08)
format: >-
  whitespace-delimited ASCII text, one header row and one row per season; served as
  Content-Type text/plain; charset=utf-8
license: >-
  "The information on National Weather Service (NWS) Web pages are in the public domain,
  unless specifically noted otherwise, and may be used without charge for any lawful
  purpose so long as you do not: 1) claim it is your own (e.g., by claiming copyright for
  NWS information -- see below), 2) use it in a manner that implies an endorsement or
  affiliation with NOAA/NWS, or 3) modify its content and then present it as official
  government material. You also cannot present information of your own in a way that makes
  it appear to be official government information." (NWS Disclaimer,
  https://www.weather.gov/disclaimer, linked as "Disclaimer" from the footer of
  https://www.cpc.ncep.noaa.gov/data/indices/, retrieved 2026-09-08)
variables:
  - SEAS
  - YR
  - TOTAL
  - ANOM
coverage: >-
  Seasonal ERSSTv6 (centered base periods) "Oceanic Niño Index" or the 3-month running
  average in Niño 3.4 (5oNorth-5oSouth) (170-120oWest); the data rows of the file run from
  SEAS DJF YR 1950 to SEAS JJA YR 2026 in the copy retrieved 2026-09-08
coverage_stated_at: >-
  https://www.cpc.ncep.noaa.gov/data/indices/ states the basis and region above the link to
  the file; the first and last data rows of
  https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt state the span
retrieved: 2026-09-08
fetch_script: src/fetch/noaa_oni.py
file: null
transcribed_from: null
topics:
  - ocean-climate/upwelling-enso
  - waves-storms-sediment
regions:
  - global
beds: []
sites: []
references: []
human_task: null
---
