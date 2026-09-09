---
id: sio_shore_stations
title: >-
  Shore Stations Program Data Archive: Current and historical coastal ocean temperature and
  salinity measurements from California stations
steward: Scripps Institution of Oceanography, UC San Diego
url: https://library.ucsd.edu/dc/collection/bb4719748r
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
  - A component reference is positional, not a stable identifier. One DOI covers every component
    of a station object (https://doi.org/10.6075/J06T0K0M is cited by all fourteen La Jolla
    components), the component's file id is its position ("1.zip" for the first), and the dated
    archive name carried in the object metadata (LaJolla_Archive_20260630.zip) is not
    addressable - requesting it under the object path returned HTTP 404 on 2026-09-08. When a
    further quarterly archive is deposited it becomes _1_1, and the URLs below return that newer
    file; the archive date and data end recorded here are those of the copy retrieved 2026-09-08
  - Download the five files over HTTPS; each returned HTTP 200 on 2026-09-08 with no account, key,
    referrer or form submission. Each URL below is the first-listed component of its station
    object on 2026-09-08
  - https://library.ucsd.edu/dc/object/bb07606686/_1_1.zip/download (Santa Barbara)
  - https://library.ucsd.edu/dc/object/bb5914297b/_1_1.zip/download (Point Dume / Zuma Beach)
  - https://library.ucsd.edu/dc/object/bb1067837x/_1_1.zip/download (Newport Beach / Balboa Pier)
  - https://library.ucsd.edu/dc/object/bb8849478k/_1_1.zip/download (San Clemente)
  - https://library.ucsd.edu/dc/object/bb4003017c/_1_1.zip/download (La Jolla, Scripps Pier)
format: >-
  five ZIP archives, one per station; each object page states File Format "ZIP Format" and Scope
  And Content "This resource includes files in the following formats: .xls and .csv."; served as
  Content-Type application/zip. The variables below are the column-header rows of the archives'
  .csv members. No single file carries all of them: the Santa Barbara and Point Dume archives hold
  temperature only, and the bottom-depth columns appear only in the La Jolla archive
license: >-
  The archives themselves state no licence. Each .csv member carries a block headed "***PLEASE
  CITE & REFERENCE THIS PROGRAM AS FOLLOWS***" giving the preferred citation for that station's
  archive. The licence is stated on the station object pages: "Creative Commons Attribution 4.0
  International Public License" (the License field on each of the five object pages under
  https://library.ucsd.edu/dc/object/, e.g. https://library.ucsd.edu/dc/object/bb4003017c, linking
  http://creativecommons.org/licenses/by/4.0/, retrieved 2026-09-08). The Copyright field on the
  same pages states "Under copyright (US)" and "Constraint(s) on Use: This work is protected by
  the U.S. Copyright Law (Title 17, U.S.C.). Use of this work beyond that allowed by "fair use" or
  any license applied to this work requires written permission of the copyright holder(s).
  Responsibility for obtaining permissions and any use and distribution of this work rests
  exclusively with the user and not the UC San Diego Library. Inquiries can be made to the UC San
  Diego Library program having custody of the work."
variables:
  - YEAR
  - MONTH
  - DAY
  - TIME_PST
  - TIME_FLAG
  - SURF_TEMP_C
  - SURF_FLAG
  - TIME
  - DAY_TIME_FLAG
  - TEMP_FLAG
  - SALINITY_PSU
  - SALT_FLAG
  - SURF_SAL_PSU
  - BOT_SAL_PSU
  - BOT_FLAG
  - BOT_TEMP_C
coverage: >-
  The program as the collection states it: "current and historical daily sea surface temperature
  (SST) and salinity (SSS) measurements observed at shoreline locations along the west coast of
  the United States"; "Historically, stations ranged from the southernmost point at La Jolla, CA,
  to the northernmost point on the west coast, Neah Bay, WA, located at the entrance to the
  Straits of Juan de Fuca." and "Currently, all 10 active stations are located in California.";
  Date Collected "1916 to present"; Extent "10 digital objects." This record holds the five of
  those ten stations whose stated coordinates fall between Point Conception and the US-Mexico
  border: Santa Barbara Harbor 34°24'13.9"N, Point Dume 34°01'04.5"N, Newport Beach
  33°36'24.1"N, San Clemente 33°25'08.6"N and La Jolla 32°52'01.0"N. Each station's span as
  its object page states it: Santa Barbara "Temperature data: January 1, 1955 to March 31, 2026";
  Point Dume "Temperature data: December 5, 1956 to March 31, 2026"; Newport Beach "Temperature
  data: November 12, 1924 to March 31, 2026" and "Salinity data: November 12, 1924 to March 31,
  2026"; San Clemente "Temperature data: July 1, 1965 to March 31, 2026" and "Salinity data:
  July 1, 1965 to March 31, 2026"; La Jolla "Surface temperature and salinity data: August 22,
  1916 to March 31, 2026" and "Bottom (~5m) temperature and salinity data: July 21, 1926 to
  March 31, 2026". In the copy retrieved 2026-09-08 the first-listed component of each of those
  five objects carries the archive date 2026-06-30, and the last data row of every .csv inside
  them is dated 2026, 3, 31
coverage_stated_at: >-
  https://library.ucsd.edu/dc/collection/bb4719748r states the Description, Date Collected and
  Extent quoted above; each station's coordinates are printed in the header block of the .csv
  members of its own archive; the Description field of the first-listed component on each of the
  five station object pages linked from that collection page states that station's span
  (https://library.ucsd.edu/dc/object/ bb07606686, bb5914297b, bb1067837x, bb8849478k and
  bb4003017c, retrieved 2026-09-08); the component titles on those same pages state the archive
  date, and the last data row of each .csv inside the archives retrieved 2026-09-08 states the
  end of the data
retrieved: 2026-09-08
fetch_script: src/fetch/sio_shore_stations.py
file: null
transcribed_from: null
topics:
  - ocean-climate/temperature
  - ocean-climate/salinity
  - ocean-climate/heatwaves
regions:
  - scb
beds: []
sites: []
references: []
human_task: null
---
