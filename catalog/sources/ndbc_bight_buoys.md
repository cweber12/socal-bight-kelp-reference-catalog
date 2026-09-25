---
id: ndbc_bight_buoys
title: Standard Meteorological Data
steward: National Data Buoy Center
url: https://www.ndbc.noaa.gov/
doi: null
citations: []
status: VERIFIED
tier: FETCHED
access:
  - >-
    Open https://www.ndbc.noaa.gov/, which answers HTTP 200 and is headed "Station Map". It carries
    a link labelled "Station List" to https://www.ndbc.noaa.gov/to_station.shtml, titled "NDBC -
    Station List" and headed "Station List". The same link stands at the top of each of the 41 pages
    this record cites under station_page.php, station_history.php and faq/measdes.shtml - 20, 20 and
    1 - and neither of the two directory indexes under /data/ that this record cites carries it. The
    Station List page prints "Click on the station ID code to gain access to station data and
    information." over 174 second-level headings, each an operator's name followed by the word
    "Stations", with the station ids under it; its own meta description reads "The National Data
    Buoy Center list of buoy and coastal stations, grouped by the various network operators." It
    carries 1,885 station links naming 1,885 distinct stations, no id appearing twice. The copy
    taken 2026-09-24 was 128,025 bytes of Content-Type "text/html; charset=ISO-8859-1"; the page
    prints a notice naming the tropical storms current that day, so its byte count is a fact of the
    copy rather than of the page (2026-09-24)
  - >-
    https://www.ndbc.noaa.gov/data/stations/, headed "Index of /data/stations/", lists
    station_table.txt among five text files.
    https://www.ndbc.noaa.gov/data/stations/station_table.txt answered HTTP 200 with 364,319 bytes
    of Content-Type "text/plain; charset=ISO-8859-1", Last-Modified "Thu, 24 Sep 2026 15:55:04 GMT"
    and ETag "58f1f-65c3c9f8e5197". Its first line is "# STATION_ID | OWNER | TTYPE | HULL | NAME |
    PAYLOAD | LOCATION | TIMEZONE | FORECAST | NOTE" and its 1,940 data rows are pipe separated.
    Every byte of the file is ASCII: the degree sign in the LOCATION column is written as the HTML
    entity "&#176;", which occurs 3,880 times (2026-09-24)
  - >-
    A station's own page is https://www.ndbc.noaa.gov/station_page.php?station=<id> and its
    available files are listed at https://www.ndbc.noaa.gov/station_history.php?station=<id>; the
    station page and the history page of each of the twenty stations this record names answered HTTP
    200 on 2026-09-24. A station page prints "Station <id>" with the station's name, a line naming
    who runs it, the station type, the payload and the position, and for the five stations held also
    "Site elevation:", "Air temp height:", "Anemometer height:", "Barometer elevation:", "Sea temp
    depth:", "Water depth:" and "Watch circle radius:". The page of each of the five held stations
    states "Owned and maintained by National Data Buoy Center"; the page of station 46221, a station
    this record does not hold, states "Information submitted by Scripps Institution of Oceanography"
    instead. A history page prints "Available historical data for station <id> include:" and, under
    "Historical data", a label over the years offered for each product it holds. Eight such labels
    stand on all five held stations - "Standard meteorological data:", "Continuous winds data:",
    "Spectral wave density data:", the four reading "Spectral wave (alpha1) direction data:",
    "Spectral wave (alpha2) direction data:", "Spectral wave (r1) direction data:" and "Spectral
    wave (r2) direction data:", and "Supplemental measurements data:" - and three more stand on some
    of them: "Ocean current data:" on 46054, 46053, 46025 and 46086, "Ocean data:" on 46053, 46025
    and 46086, and "Solar radiation data:" on 46086. So the labels under that heading number 9, 10,
    10, 8 and 11 for 46054, 46053, 46025, 46069 and 46086. The form "Supplemental Measurements
    data:", with a capital M, is printed by the same page in the "Quality controlled data for 2026"
    list above that heading, not under "Historical data". This record holds the standard
    meteorological files and none of the other products (2026-09-24)
  - >-
    https://www.ndbc.noaa.gov/faq/measdes.shtml, headed "Measurement Descriptions and Units",
    answered HTTP 200. It states "Real Time files generally contain the last 45 days of \"Realtime\"
    data - data that went through automated quality checks and were distributed as soon as they were
    received. Historical files have gone through post-processing analysis and represent the data
    sent to the archive centers. The formats for both are generally the same, with the major
    difference being the treatment of missing data. Missing data in the Realtime files are denoted
    by \"MM\" while a variable number of 9's are used to denote missing data in the Historical
    files, depending on the data type (for example: 999.0  99.0)." Under the heading "Standard
    Meteorological Data" it prints a three-line example block and then a description of each column,
    the descriptions this record's variables carry (2026-09-24)
  - >-
    https://www.ndbc.noaa.gov/data/historical/stdmet/ is the directory the held files come from; it
    answered HTTP 200. Each file is
    https://www.ndbc.noaa.gov/data/historical/stdmet/<id>h<year>.txt.gz. Run
    src/fetch/ndbc_bight_buoys.py, which sends the User-Agent "kelpcatalog/ndbc_bight_buoys" and
    requests these five URLs; no account, key or referrer is required, and each answered HTTP 200
    with Content-Type "application/x-gzip". The gzip the server sends is what is kept, never
    decompressed on the way in
  - https://www.ndbc.noaa.gov/data/historical/stdmet/46054h2025.txt.gz (625,149 bytes, 2026-09-24)
  - https://www.ndbc.noaa.gov/data/historical/stdmet/46053h2025.txt.gz (745,359 bytes, 2026-09-24)
  - https://www.ndbc.noaa.gov/data/historical/stdmet/46025h2025.txt.gz (766,270 bytes, 2026-09-24)
  - https://www.ndbc.noaa.gov/data/historical/stdmet/46069h2025.txt.gz (640,559 bytes, 2026-09-24)
  - https://www.ndbc.noaa.gov/data/historical/stdmet/46086h2025.txt.gz (724,241 bytes, 2026-09-24)
  - >-
    Each of the five answered with Last-Modified in "Wed, 11 Feb 2026 14:29:08 GMT" to "Wed, 11 Feb
    2026 14:29:10 GMT" and an ETag, and each carried the sha256 the fetch manifest beside it
    records. The rolling alternative this record does not hold is
    https://www.ndbc.noaa.gov/data/realtime2/<id>.txt, which for station 46221 answered HTTP 200
    with 203,134 bytes on 2026-09-24. Its header lines carry a PTDY column the held historical files
    do not, and give VIS the unit nmi where the held files give mi, the column name VIS being
    spelled the same in both; the 2,161 lines it held that day ran from 2026-08-11 to 2026-09-25
    (2026-09-24)
format: >-
  measdes states of the historical files that they "have gone through post-processing analysis and
  represent the data sent to the archive centers", that in the data files "the measurements are
  generally in metric units", and that "Both Realtime and Historical files show times in UTC only".
  Five gzip files, one per station, each the 2025 calendar-year standard meteorological file for
  that station, served as Content-Type "application/x-gzip" and kept as served. Decompressed, each
  is a space-aligned text file whose first two lines are a column-name line and a unit line and
  whose remaining lines are data rows of 18 whitespace-separated fields. The first token of the name
  line is "#YY" and of the unit line "#yr", and no page or file this record cites prints either
  without the "#". measdes states "Note that in the Realtime files, non-data lines begin with \"#\".
  Such lines should be treated as comment lines.", of the Realtime files and not of the historical
  files held here. This record reads that "#" as a marker on the line rather than part of the first
  column, and so enters that column as YY with unit yr; a reading that kept it would give the unit
  as "#yr". The two header lines are byte-identical across all five held files; their 18 name tokens
  are YY, MM, DD, hh, mm, WDIR, WSPD, GST, WVHT, DPD, APD, MWD, PRES, ATMP, WTMP, DEWP, VIS and
  TIDE, and their 18 unit tokens, in the same order, yr, mo, dy, hr, mn, degT, m/s, m/s, m, sec,
  sec, degT, hPa, degC, degC, degC, mi and ft. In the copies retrieved 2026-09-24 every byte of
  every decompressed file is ASCII, every line ending is LF with no CR, no data row is ragged, and
  the data rows number 52,247 (46054), 52,550 (46053), 52,547 (46025), 52,549 (46069) and 52,203
  (46086). Three columns are stated differently in different places. measdes states of PTDY, a
  column the Realtime header carries, "(not in Historical files)", and the held files carry no PTDY
  column. measdes states of PRES "( labeled BAR in Historical files)", and the held files spell that
  column PRES. And measdes and the realtime file both give VIS the unit nmi - each prints "nmi" in a
  unit line, of measdes's Standard Meteorological example block and of the realtime file's own
  header - where the five held files print mi; this record takes each unit from the held files,
  whose columns it holds, and each description from measdes, so the description entered for VIS
  reads "(nautical miles)" beside the unit mi. Of the products the held stations' history pages
  offer under "Historical data", which number 9, 10, 10, 8 and 11 for 46054, 46053, 46025, 46069 and
  46086 and which the third access step lists, this record holds only the standard meteorological
  files, and of the years each station offers only 2025
license: >-
  "The information on National Weather Service (NWS) Web pages are in the public domain, unless
  specifically noted otherwise, and may be used without charge for any lawful purpose so long as you
  do not: 1) claim it is your own (e.g., by claiming copyright for NWS information -- see below), 2)
  use it in a manner that implies an endorsement or affiliation with NOAA/NWS, or 3) modify its
  content and then present it as official government material. You also cannot present information
  of your own in a way that makes it appear to be official government information."
license_stated_at: >-
  https://www.weather.gov/disclaimer, the page each NDBC page links as "Disclaimer" from its own
  footer, under the heading "Use of NOAA/NWS Data and Products" - the heading writes the space
  before "Data" as the entity "&nbsp;" - where the quoted paragraph is the first of the five that
  section contains (retrieved 2026-09-24). Nothing nearer states terms: the five held files contain
  none of "licen", "copyright", "creative", "terms", "cite", "citation", "disclaim" or "public
  domain" in any letter case, and the five station pages contain none of those but "disclaim", which
  on them is the footer link and a caption over the station map. The same disclaimer page carries a
  later section headed "Use of Third-Party Data and Products" stating "Third-party information and
  imagery are used under license by the individual third-party provider." and "Please contact the
  third-party provider for information on your rights to further use these data/products."; the page
  of each of the five stations held states the station is "Owned and maintained by National Data
  Buoy Center"
variables:
  - name: YY
    description: null
    unit: yr
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: MM
    description: null
    unit: mo
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: DD
    description: null
    unit: dy
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: hh
    description: null
    unit: hr
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: mm
    description: null
    unit: mn
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: WDIR
    description: >-
      Wind direction (the direction the wind is coming from in degrees clockwise from true N) during
      the same period used for WSPD. See Wind Averaging Methods
    unit: degT
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: WSPD
    description: >-
      Wind speed (m/s) averaged over an eight-minute period for buoys and a two-minute period for
      land stations. Reported Hourly. See Wind Averaging Methods.
    unit: m/s
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: GST
    description: >-
      Peak 5 or 8 second gust speed (m/s) measured during the eight-minute or two-minute period. The
      5 or 8 second period can be determined by payload, See the Sensor Reporting, Sampling, and
      Accuracy section.
    unit: m/s
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: WVHT
    description: >-
      Significant wave height (meters) is calculated as the average of the highest one-third of all
      of the wave heights during the 20-minute sampling period. See the Wave Measurements section.
    unit: m
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: DPD
    description: >-
      Dominant wave period (seconds) is the period with the maximum wave energy. See the Wave
      Measurements section.
    unit: sec
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: APD
    description: >-
      Average wave period (seconds) of all waves during the 20-minute period. See the Wave
      Measurements section.
    unit: sec
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: MWD
    description: >-
      The direction from which the waves at the dominant period (DPD) are coming. The units are
      degrees from true North, increasing clockwise, with North as 0 (zero) degrees and East as 90
      degrees. See the Wave Measurements section.
    unit: degT
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: PRES
    description: >-
      Sea level pressure (hPa). For C-MAN sites and Great Lakes buoys, the recorded pressure is
      reduced to sea level using the method described in NWS Technical Procedures Bulletin 291
      (11/14/80). ( labeled BAR in Historical files)
    unit: hPa
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: ATMP
    description: >-
      Air temperature (Celsius). For sensor heights on buoys, see Hull Descriptions. For sensor
      heights at C-MAN stations, see C-MAN Sensor Locations
    unit: degC
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: WTMP
    description: >-
      Sea surface temperature (Celsius). For buoys the depth is referenced to the hull's waterline.
      For fixed platforms it varies with tide, but is referenced to, or near Mean Lower Low Water
      (MLLW).
    unit: degC
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: DEWP
    description: Dew point temperature taken at the same height as the air temperature measurement.
    unit: degC
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: VIS
    description: >-
      Station visibility (nautical miles). Note that buoy stations are limited to reports from 0 to
      1.6 nmi.
    unit: mi
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
  - name: TIDE
    description: The water level in feet above or below Mean Lower Low Water (MLLW).
    unit: ft
    file:
      - 46054h2025.txt.gz
      - 46053h2025.txt.gz
      - 46025h2025.txt.gz
      - 46069h2025.txt.gz
      - 46086h2025.txt.gz
coverage: >-
  This record holds one 2025 standard meteorological file for each of five NDBC buoys in the Bight,
  with the name and the position station_table.txt and each station's own page state for it: 46054
  "WEST SANTA BARBARA  38 NM West of Santa Barbara, CA", 34.274 N 120.468 W; 46053 "EAST SANTA
  BARBARA  - 12NM Southwest of Santa Barbara, CA", 34.246 N 119.842 W; 46025 "Santa Monica Basin -
  33NM WSW of Santa Monica, CA", 33.765 N 119.077 W; 46069 "SOUTH SANTA ROSA - 14 NM SW of Santa
  Rosa Island, CA", 33.657 N 120.227 W; and 46086 "SAN CLEMENTE BASIN - 27NM SE Of San Clemente Is,
  CA", 32.504 N 118.029 W. Each of the five states its position a second time in degrees, minutes
  and seconds, the degree sign written "&#176;": 34&#176;16'26" N 120&#176;28'5" W, 34&#176;14'46" N
  119&#176;50'31" W, 33&#176;45'54" N 119&#176;4'36" W, 33&#176;39'24" N 120&#176;13'36" W and
  32&#176;30'15" N 118&#176;1'44" W. Their pages state water depths of 454 m, 417 m, 868 m, 985 m
  and 1862 m, and sea temp depths of 2 m, 1.5 m, 2 m, 1.5 m and 1.1 m "below water line". Each held
  station's history page offers standard meteorological years beyond the one held: 46054 32 years,
  1994 to 2025; 46053 31 years, 1994 to 2025, 1997 absent; 46025 44 years, 1982 to 2025; 46069 23
  years, 2003 to 2025; and 46086 23 years, 2003 to 2025. In the five copies retrieved 2026-09-24 the
  first data row of every file is dated 2025 01 01 00 00 and the last 2025 12 31 23 50. The five
  were selected from NDBC's station list by three things NDBC states of each station and one bound
  on where it lies. The three: station_table.txt gives its OWNER as N and its own page states it is
  "Owned and maintained by National Data Buoy Center"; station_table.txt gives its TTYPE as a buoy;
  and its history page offers a standard meteorological file for 2025. Nineteen of the 1,940 rows of
  station_table.txt give OWNER as N and a TTYPE naming a buoy within 30-36 N, 114-124 W, and the
  page of every one of the nineteen states the ownership line quoted above; widening that window
  from 31.8-35.0 N, 116-122 W added two of the nineteen, 46028 and 46062, which NDBC names 55 NM and
  18 NM from Morro Bay. Eight of the nineteen also satisfy the third. The bound is the Bight as
  sccwrp_tr1289 states it, and this record applies it through the landmark NDBC's own name gives
  each station. It settles two of the three stations this record leaves out. NDBC names 46011 "SANTA
  MARIA - 21NM NW of Point Arguello, CA", 34.937 N 120.999 W, and CONTEXT.md, "The region tree",
  level 2, places Pt. Arguello north of level 1's Point Conception bound; 46028 "CAPE SAN MARTIN -
  55NM West NW of Morro Bay, CA" states 35.763 N, north again of that 34.937 N. It does not settle
  the third. NDBC names 46047 "TANNER BANK - 121 NM West of San Diego, CA" and states 32.418 N
  119.535 W: San Diego lies inside the Bight, and no source this record cites gives a coordinate for
  the seaward limb of the bound, "from the mainland coastal embayments west to the Channel Islands",
  so nothing NDBC prints settles whether a position 121 NM west of San Diego falls inside it. This
  record reads that limb as excluding 46047 and leaves it out on that reading; a reading that placed
  the limb further west would hold it. The eleven of the nineteen whose history page offers no 2025
  standard meteorological file are 46062 (offering 8 years, last 2004), 46023 (32, last 2016), 46051
  (5, last 1996), 46063 (12, last 2009), 46045 (9, last 1999), 46024 (9, last 2016), 46048 (3, last
  1993) and 46090, 46290, 46490 and 46412, which offer none; the pages of 46045, 46051 and 46063
  state "Station was disestablished in November, 1997", "Station was disestablished in April, 1994"
  and "This station has been disestablished on May 22, 2009." and that of 46290 "Station 46290
  stopped transmitting 10/16/08, and has gone adrift. Station disestablished." The page of 46063,
  "Pt.Conception, CA - 50NM West of Santa Barbara, CA", adds that "the NOAA-NDBC directs the user to
  station 46054 (Santa Barbara, CA) which is currently located eleven (11) nautical miles from the
  disestablished station", a station this record holds
coverage_stated_at: >-
  https://www.ndbc.noaa.gov/data/stations/station_table.txt states each station's OWNER, TTYPE, NAME
  and LOCATION, in the pipe-separated columns its first line names, and is the file the nineteen and
  the eight were counted from; https://www.ndbc.noaa.gov/station_page.php?station=<id> states, for
  each station named above, the "Owned and maintained by" line, the name, the position in both
  forms, and for the five held the "Sea temp depth:" and "Water depth:" values and, for 46045,
  46051, 46063 and 46290, the disestablishment sentence quoted;
  https://www.ndbc.noaa.gov/station_history.php?station=<id> states the years each station offers,
  as the list under the label "Standard meteorological data:" below its "Historical data" heading;
  the first and last data rows are read off the five held files, a fact of the copies retrieved
  2026-09-24; and the Bight's bound is sccwrp_tr1289, whose own coverage quotes it as "from Point
  Conception, CA in the north to the US-Mexico border in the south and from the mainland coastal
  embayments west to the Channel Islands", with CONTEXT.md, "The region tree", level 2, placing Pt.
  Arguello north of that northern bound
retrieved: 2026-09-24
fetch_script: src/fetch/ndbc_bight_buoys.py
file: null
transcribed_from: null
derived_from: null
topics:
  - waves-storms-sediment/swell-climate
  - waves-storms-sediment/storms
regions:
  - scb
beds: []
sites: []
site_key:
  - file: 46054h2025.txt.gz
  - file: 46053h2025.txt.gz
  - file: 46025h2025.txt.gz
  - file: 46069h2025.txt.gz
  - file: 46086h2025.txt.gz
references: []
human_task: null
---
