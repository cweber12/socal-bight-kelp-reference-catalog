---
id: sio_shore_stations
title: >-
  Shore Stations Program Data Archive: Current and historical coastal ocean temperature and
  salinity measurements from California stations
steward: Scripps Institution of Oceanography, UC San Diego
url: https://shorestations.ucsd.edu/
doi: 10.6075/J0S75GHD
status: VERIFIED
tier: FETCHED
access:
  - Open https://shorestations.ucsd.edu/
  - Follow "Data Access" in the site navigation to https://shorestations.ucsd.edu/publications/data/
  - That page states "Please fill out the form below before accessing the data. This helps us
    keep track of data usage." and links an "Access Form" at
    https://docs.google.com/forms/d/e/1FAIpQLSfq-ufEwjviE5GW5ulOyHj5IJPBe3E7iXaieZjJi9E9EXR4Fg/viewform
  - The same page states the data "are available in excel and csv spreadsheet formats through the
    UC San Diego Library Digital Collections. https://doi.org/10.6075/J0S75GHD", which resolves to
    https://library.ucsd.edu/dc/collection/bb4719748r
  - That collection page lists ten station objects, each with its own DOI. Each object page lists
    its archive components in a numbered order, _1_1, _2_1, ... in the order listed, each with a
    "Download file" link. On 2026-09-08 the first-listed component of every one of the ten was
    the most recent on that object, carrying the archive date 2026-06-30
  - Download the ten files over HTTPS; each returned HTTP 200 on 2026-09-08 with no account, key,
    referrer or form submission. Each URL below is the first-listed component of its station
    object on 2026-09-08
  - https://library.ucsd.edu/dc/object/bb4003017c/_1_1.zip/download (La Jolla, Scripps Pier)
  - https://library.ucsd.edu/dc/object/bb8849478k/_1_1.zip/download (San Clemente)
  - https://library.ucsd.edu/dc/object/bb1067837x/_1_1.zip/download (Newport Beach / Balboa Pier)
  - https://library.ucsd.edu/dc/object/bb5914297b/_1_1.zip/download (Point Dume / Zuma Beach)
  - https://library.ucsd.edu/dc/object/bb07606686/_1_1.zip/download (Santa Barbara)
  - https://library.ucsd.edu/dc/object/bb2979118z/_1_1.zip/download (Granite Canyon)
  - https://library.ucsd.edu/dc/object/bb02145898/_1_1.zip/download (Pacific Grove)
  - https://library.ucsd.edu/dc/object/bb3934759t/_1_1.zip/download (Farallon Islands)
  - https://library.ucsd.edu/dc/object/bb6187339c/_1_1.zip/download (Trinidad Beach)
  - https://library.ucsd.edu/dc/object/bb5880168m/_1_1.zip/download (Trinidad Bay)
format: >-
  ten ZIP archives, one per station; each object page states File Format "ZIP Format" and Scope
  And Content "This resource includes files in the following formats: .xls and .csv."; served as
  Content-Type application/zip
license: >-
  "Creative Commons Attribution 4.0 International Public License" (the License field on each of
  the ten station object pages under https://library.ucsd.edu/dc/object/, e.g.
  https://library.ucsd.edu/dc/object/bb4003017c, linking http://creativecommons.org/licenses/by/4.0/,
  retrieved 2026-09-08). The Copyright field on the same pages states "Under copyright (US)" and
  "Constraint(s) on Use: This work is protected by the U.S. Copyright Law (Title 17, U.S.C.). Use
  of this work beyond that allowed by "fair use" or any license applied to this work requires
  written permission of the copyright holder(s). Responsibility for obtaining permissions and any
  use and distribution of this work rests exclusively with the user and not the UC San Diego
  Library. Inquiries can be made to the UC San Diego Library program having custody of the work."
variables:
  - YEAR
  - MONTH
  - DAY
  - TIME_PST
  - TIME_FLAG
  - SURF_SAL_PSU
  - SURF_FLAG
  - BOT_SAL_PSU
  - BOT_FLAG
  - SURF_TEMP_C
  - BOT_TEMP_C
  - SALINITY_PSU
  - SALT_FLAG
  - TEMP_FLAG
  - TIME
  - DAY_TIME_FLAG
  - SURF_SALT_PSU
  - DATE_TIME_FLAG
  - FLAG_TIME_DAY
  - TRINIDAD_BEACH_SURF_TEMP_C
  - BEACH_FLAG
  - TRINIDAD_BAY_SURF_TEMP_C
  - BAY_FLAG
coverage: >-
  "current and historical daily sea surface temperature (SST) and salinity (SSS) measurements
  observed at shoreline locations along the west coast of the United States"; "Historically,
  stations ranged from the southernmost point at La Jolla, CA, to the northernmost point on the
  west coast, Neah Bay, WA, located at the entrance to the Straits of Juan de Fuca." and
  "Currently, all 10 active stations are located in California."; Date Collected "1916 to
  present"; Extent "10 digital objects." In the copy retrieved 2026-09-08 the first-listed
  component of each of the ten station objects carries the archive date 2026-06-30 in its title,
  and the last data row of every CSV inside those archives is dated 2026, 3, 31
coverage_stated_at: >-
  https://library.ucsd.edu/dc/collection/bb4719748r states the Description, Date Collected and
  Extent quoted above; the component titles on the ten station object pages linked from that
  collection page state the archive date, and the last data row of each CSV inside the archives
  retrieved 2026-09-08 states the end of the data
retrieved: 2026-09-08
fetch_script: src/fetch/sio_shore_stations.py
file: null
transcribed_from: null
topics:
  - ocean-climate/temperature
  - ocean-climate/heatwaves
regions:
  - scb
beds: []
sites: []
references: []
human_task: null
---
