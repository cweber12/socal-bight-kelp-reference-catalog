---
id: calcofi
title: California Cooperative Oceanic Fisheries Investigations
steward: >-
  California Cooperative Oceanic Fisheries Investigations, whose Data Policy lists its
  participating agencies as "NOAA Southwest Fisheries Science Center, National Marine Fisheries
  Service", "Scripps Institution of Oceanography, UC San Diego" and "California Department of
  Fish & Wildlife (Marine Region)"
url: https://calcofi.org/
doi: null
status: VERIFIED
tier: FETCHED
access:
  - Open https://calcofi.org/
  - >-
    Follow "Data" to https://calcofi.org/data/, then "Oceanographic Data" and "Bottle Database",
    to https://calcofi.org/data/oceanographic-data/bottle-database/. That page states "The
    database is available in four different formats and can be downloaded below." and links four
    whole-database archives under https://calcofi.org/downloads/database/, named
    CalCOFI_Database_194903-202105_csv_16October2023.zip and the same stem with mdb, sql and xml
  - >-
    The same two tables are served one station at a time as ERDDAP tabledap, on a host of the
    NOAA Southwest Fisheries Science Center, which the Data Policy above names among CalCOFI's
    participating agencies
  - >-
    Open https://coastwatch.pfeg.noaa.gov/erddap/search/index.html?searchFor=CalCOFI. The
    entries titled "CalCOFI SIO Hydrographic Cast Data" and "CalCOFI SIO Hydrographic Bottle
    Data" carry the dataset ids siocalcofiHydroCast and siocalcofiHydroBottle, institution
    "UCSD SIO", and an infoUrl of
    https://wp.calcofi.org/wp/data/oceanographic-data/bottle-database/
  - >-
    Requests under https://coastwatch.pfeg.noaa.gov/erddap/tabledap/ returned HTTP 302 on
    2026-09-08 with a Location under https://oceanview.pfeg.noaa.gov/erddap/tabledap/ carrying
    the same query. The two URLs below are the oceanview ones, which answer without a redirect
  - >-
    The pattern is <erddap>/tabledap/<dataset>.csv?&sta_id=%22<line>%20<station>%22 - one
    request per table; no variable list before the constraint, so every variable is returned;
    line and station zero-padded as sta_id spells them, quoted, and the quotes and the space
    percent-encoded. Every constraint must be preceded by "&", without which the server answers
    HTTP 400 and a message reading: Bad Request: Query error: All constraints (including
    "sta_id=...") must be preceded by '&'. Worked example, the cast table at station 93.3 28.0 -
    https://oceanview.pfeg.noaa.gov/erddap/tabledap/siocalcofiHydroCast.csv?&sta_id=%22093.3%20028.0%22
  - >-
    Download the two files over HTTPS. Both returned HTTP 200 on 2026-09-08 with no account, key
    or referrer, and both answered with a Content-Disposition file name
  - https://oceanview.pfeg.noaa.gov/erddap/tabledap/siocalcofiHydroCast.csv?&sta_id=%22093.3%20028.0%22
  - https://oceanview.pfeg.noaa.gov/erddap/tabledap/siocalcofiHydroBottle.csv?&sta_id=%22093.3%20028.0%22
format: >-
  two CSV files, one per table of the Bottle Database, served as Content-Type
  text/csv;charset=ISO-8859-1 with the file name in Content-Disposition; each file carries a row
  of column names, then a row of units, then one row per record, and holds no byte above 127 in
  the copy retrieved 2026-09-08. The variables below are those two column-name rows: 62 columns
  in the cast file and 65 in the bottle file, of which five - time, latitude, longitude, cst_cnt
  and sta_id - appear in both. No single file carries all of them; the measurements are in the
  bottle file and the cast metadata in the cast file
license: >-
  "CalCOFI oceanographic and biological data are licensed under the Creative Commons Attribution
  4.0 International License." and "Persons who utilize CalCOFI data are required to state so in
  their work. An acceptable acknowledgment is to state in the methods that the data were obtained
  from the California Cooperative Oceanic Fisheries Investigations and mention in the
  acknowledgments that the data are available at https://calcofi.org/." (Data Policy,
  https://calcofi.org/data/data-usage-policy/, reached as "Data Usage Policy" under Data in the
  navigation of https://calcofi.org/ and as the "data-use agreement" that
  https://calcofi.org/data/oceanographic-data/bottle-database/ states is accepted by downloading,
  retrieved 2026-09-08). The two ERDDAP dataset pages the files were fetched from state a
  different licence, seven <br>-separated lines beginning "The data may be used and redistributed
  for free but is not intended" and ending "completeness, or usefulness, of this information."
  (https://oceanview.pfeg.noaa.gov/erddap/info/siocalcofiHydroCast/index.html and
  https://oceanview.pfeg.noaa.gov/erddap/info/siocalcofiHydroBottle/index.html, retrieved
  2026-09-08)
variables:
  - time
  - latitude
  - longitude
  - cst_cnt
  - cruise_id
  - cruise
  - cruz_sta
  - dbsta_id
  - cast_id
  - sta_id
  - quarter
  - sta_code
  - distance
  - date
  - year
  - month
  - julian_date
  - julian_day
  - time_string
  - lat_deg
  - lat_min
  - lat_hem
  - lon_deg
  - lon_min
  - lon_hem
  - rpt_line
  - st_line
  - ac_line
  - rpt_sta
  - st_station
  - ac_sta
  - bottom_d
  - secchi
  - fore_iu
  - ship_name
  - ship_code
  - data_type
  - order_occ
  - event_num
  - cruz_leg
  - orig_sta_id
  - data_or
  - cruz_num
  - intchl
  - intc14
  - inc_str
  - inc_end
  - pst_lan
  - civil_t
  - timezone
  - wave_dir
  - wave_ht
  - wave_prd
  - wind_dir
  - wind_spd
  - barometer
  - dry_t
  - wet_t
  - wea
  - cloud_typ
  - cloud_amt
  - visibility
  - btl_cnt
  - depth_id
  - depthm
  - t_degc
  - salinity
  - o2ml_l
  - stheta
  - o2sat
  - oxy
  - btlnum
  - recind
  - t_prec
  - t_qual
  - s_prec
  - s_qual
  - p_qual
  - o_qual
  - sthtaq
  - o2satq
  - chlora
  - chlqua
  - phaeop
  - phaqua
  - po4um
  - po4q
  - sio3um
  - sio3qu
  - no2um
  - no2q
  - no3um
  - no3q
  - nh3um
  - nh3q
  - c14as1
  - c14a1p
  - c14a1q
  - c14as2
  - c14a2p
  - c14a2q
  - darkas
  - darkap
  - darkaq
  - meanas
  - meanap
  - meanaq
  - inctim
  - lightp
  - r_depth
  - r_temp
  - r_sal
  - r_dynht
  - r_nuts
  - r_oxy
  - dic1
  - dic2
  - ta1
  - ta2
  - ph1
  - ph2
  - dic_quality_comment
coverage: >-
  The database as its own page states it, "Oceanographic data collected from chemical analyses of
  seawater samples (1949 - present)", and "The Bottle Database spans the entire timeseries – from
  1949, when CalCOFI was initiated, to the present."; both ERDDAP datasets state
  time_coverage_start 1949-02-28T22:42:00Z and time_coverage_end 2021-05-13T20:37:00Z. This
  record holds one station of that database, CalCOFI line 93.3 station 28.0, which the CalCOFI
  Station Positions page lists as Line 93.3, Sta 28, Lat (dec) 32.91304, Lon (dec) -117.39438,
  Est Depth 609, Sta Type ROS - a position between Point Conception and the US-Mexico border. In
  the copy retrieved 2026-09-08 the cast file holds 220 rows and the bottle file 5910 rows; every
  row of both carries sta_id "093.3 028.0"; both run from 1959-02-06T23:48:00Z to
  2021-05-04T21:02:00Z; bottle depths (depthm, meters) run 0.0 to 639.0; and the positions
  recorded on the rows run 32.5 to 32.942 degrees_north and -117.417 to -117.35 degrees_east, the
  southernmost of them the single cast timed 1978-08-02T02:33:00Z, whose ac_line and ac_sta are
  95.1 and 30.9
coverage_stated_at: >-
  https://calcofi.org/data/oceanographic-data/bottle-database/ states the description and the
  span quoted above;
  https://oceanview.pfeg.noaa.gov/erddap/info/siocalcofiHydroCast/index.html and
  https://oceanview.pfeg.noaa.gov/erddap/info/siocalcofiHydroBottle/index.html state
  time_coverage_start and time_coverage_end;
  https://calcofi.org/sampling-info/station-positions/ states the station's line, station,
  latitude, longitude, estimated depth and station type; the row counts, sta_id, spans, depths
  and positions are those of the two files retrieved 2026-09-08 into data/raw/calcofi/ by
  src/fetch/calcofi.py
retrieved: 2026-09-08
fetch_script: src/fetch/calcofi.py
file: null
transcribed_from: null
topics:
  - ocean-climate/temperature
  - ocean-climate/nutrients
  - ocean-climate/oxygen-ph
regions:
  - scb
beds: []
sites: []
references: []
human_task: null
---
