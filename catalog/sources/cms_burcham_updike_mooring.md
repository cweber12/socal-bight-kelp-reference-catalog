---
id: cms_burcham_updike_mooring
title: Dirk Burcham Scientific mooring and Jim Updike Seabed Station 2024 onward
steward: Catalina Marine Society
url: https://www.catalinamarinesociety.org/dirk-burchan-scientific-mooring-and-jim-updike-seabed-station.html
doi: null
citations: []
status: VERIFIED
tier: FETCHED
access:
- >-
  Open https://www.catalinamarinesociety.org/data-portal.html, which answered HTTP 200 with 179,424
  bytes of Content-Type "text/html". It states "This page is linked to others describing specific
  data collections." Its link labelled "Dirk Burcham Scientific mooring and Jim Updike Seabed Station
  2024 onward" is this record's url (2026-09-27)
- >-
  https://www.catalinamarinesociety.org/dirk-burchan-scientific-mooring-and-jim-updike-seabed-station.html
  answered HTTP 200 with 165,998 bytes of Content-Type "text/html". Its heading prints "Dirk Burcham",
  "SCIENTIFIC MOORING", "and", "Jim Updike" and "SEABED STATION" on five lines, and it states "CMS
  established the Jim Updike Seabed Station adjacent to the Dirk Burcham Scientific Mooring. We expect
  the platforms to be serviced simultaneously and their data linked to this page." Four headings follow,
  "February 2, 2025 - March 9, 2025", "Mixed-Layer Data January 5 2025 - January 30 2025", "April 27,
  2024 - May 26, 2024" and "Oct 13, 2024 - Jan 5, 2025", each over a list of data-file URLs that the
  page prints as text and not as links, each written without a scheme as www.catalinamarinesociety.org/files/<file
  name>. The page prints 26 such URLs, no two the same (2026-09-27)
- >-
  Run src/fetch/cms_burcham_updike_mooring.py, which sends the User-Agent "kelpcatalog/cms_burcham_updike_mooring
  (+https://github.com/cweber12/socal-bight-kelp-reference-catalog)" and requests each file over https://,
  as https://www.catalinamarinesociety.org/files/<file name>; no account, key or referrer is required.
  Of the 26 printed URLs, requested over https:// on 2026-09-27, 17 answered HTTP 200 and are held,
  and 9 answered HTTP 404 with a 1,251-byte body of Content-Type "text/html" and are not held: EXO2_02022025-03092025.txt,
  WIES_5ft_01052025-01302025-21292585..csv, WIES_30ft_01052025-01302025_22129128..csv, Thermograph_20ft_04272024-5262024_21894646.dat,
  Thermograph_80ft_04272024-05262024_21894635.dat, pH_95ft_04272024-05252025_21506840.dat, Current_95ft_04272024-05262024_2108000.dat,
  water-level_95ft_10132024-01052025_21511796.txt and pH_95ft_10132024-01052025_21506840.txt
- >-
  Each of the four headings is itself a link, and all four link the one file http://www.catalinamarinesociety.org/files/Merged_Sci_Mooring_12042014-10202014.txt.
  This record requests it over https://, where it answered HTTP 200, and holds it (2026-09-27)
- >-
  The script requests the 18 held files in this order, the 17 printed files in the order the page prints
  them and then the linked one:
- https://www.catalinamarinesociety.org/files/Temp_20ft_01302025-03092025_22169464.dat (62,723 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/Temp_40ft_01302025-03092025_22169467.dat (62,718 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/Temp_80ft_01302025-03092025_22169469.dat (62,718 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/JUSS_pH_02022025-03092025.txt (146,449 bytes, 2026-09-27)
- https://www.catalinamarinesociety.org/files/JUSS_depth_temp_95ft_02022025-03092025.dat (143,157 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/JUSS_current_02022025-03092025.txt (157,678 bytes, 2026-09-27)
- https://www.catalinamarinesociety.org/files/WIES_1ft_01052025-01302025_20894273.csv (42,009 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/WIES_10ft_01052025-01302025_20733049.csv (42,009 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/WIES_20ft_01052025-01302025_20894279.csv (42,009 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/WIES_40ft_01052025-01302025_22129129.csv (129,318 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/WIES_60ft_01052025-01302025_21292584.csv (42,009 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/Temp_40ft_04272024-05262024_20481390.csv (43,535 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/Pressure_95ft_04272024-05262024_21511799.txt (64,241 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/thermograph_20ft_10132024-01052025_21894636.txt (140,277
  bytes, 2026-09-27)
- https://www.catalinamarinesociety.org/files/thermograph_40ft_10132024-01052025_21894635.txt (140,276
  bytes, 2026-09-27)
- https://www.catalinamarinesociety.org/files/thermograph_60ft_10132024-01052025_20894280.txt (130,443
  bytes, 2026-09-27)
- https://www.catalinamarinesociety.org/files/current_95ft_10132024-01052025_2108000.txt (575,220 bytes,
  2026-09-27)
- https://www.catalinamarinesociety.org/files/Merged_Sci_Mooring_12042014-10202014.txt (1,940,926 bytes,
  2026-09-27)
format: >-
  The collection page states no format for any file. This record holds 18 files, 3,967,715 bytes as
  served, all from the steward's own host: 8 whose names end ".txt", served as Content-Type "text/plain";
  6 ending ".csv", served as "text/csv"; and 4 ending ".dat", served as "application/octet-stream".
  13 decode as UTF-8 behind a byte-order mark, 4 as UTF-8 without one, and JUSS_pH_02022025-03092025.txt
  as cp1252 and not as UTF-8, so the degree sign in a column label is the two bytes C2 B0 in the UTF-8
  files and the single byte B0 in that one; variables enters each label as its own file spells it.
  This record reads a file's column names from its first line, or from its second where the first begins
  "Plot Title", which one held file's does - Temp_40ft_04272024-05262024_20481390.csv, whose first line
  after its byte-order mark is "Plot Title: ,,,,,,"; it treats the line it lands on as a column line
  where that line's first field is "#" or carries a letter, and as a data row otherwise; and it splits
  the line on tab where the line holds one, else on comma, else on whitespace, a double-quoted field's
  own surrounding quotes delimiting that field and not being part of its name, and each field trimmed
  of surrounding whitespace. On that reading 17 files state column names - 3 splitting on tab, 2 on
  comma and 12 on whitespace, the five WIES_ files among those 12 although their names end ".csv" - and
  Merged_Sci_Mooring_12042014-10202014.txt states none, its first line being a data row that begins
  "8100.01" and a tab. Pressure_95ft_04272024-05262024_21511799.txt's first line reads "date and time          pressure,
  psi; temp F", with no tab and one comma, so it enters two names, "date and time          pressure" and
  "psi; temp F"; a reading that split that line on whitespace would enter seven, "date", "and", "time",
  "pressure,", "psi;", "temp" and "F". The two current files' first lines spell their first column "ISO
  8601  ime" and their fourth "Veloci y-N (cm/s)", and spell the fifth "Veloci y-E (cm/s)" in JUSS_current_02022025-03092025.txt
  and "Veloci y E (cm/s)" in current_95ft_10132024-01052025_2108000.txt, so that column is two entries.
  Across the 17 files there are 51 distinct column names over 88 name-and-file pairs. Where a label carries
  a unit it carries it inside the label, as "Speed (cm/s)" and "Temp, °F (LGR S/N: 20481390, SEN S/N:
  20481390)" do; the collection page states no unit or description for any column, and no held file
  states one apart from its labels, so every entry reads unit: null and description: null
license: not stated
license_stated_at: >-
  Looked for first in the held files themselves: none of the 18 contains any of "licen", "copyright",
  "creative", "terms", "cite", "citation", "disclaim", "public domain", "all rights reserved" or "attribut"
  in any letter case. Then on the collection page, https://www.catalinamarinesociety.org/dirk-burchan-scientific-mooring-and-jim-updike-seabed-station.html,
  on https://www.catalinamarinesociety.org/data-portal.html, and on the three pages the collection page's
  footer links by name - documents.html, archives.html and cms-magazine.html - all retrieved 2026-09-27.
  The footer carries twelve links: those three pages, the Conflict of Interest Policy, the IRS determination
  letter and the Bylaws as PDFs, a PayPal donation URL, Facebook, Twitter, Instagram and YouTube, and
  a mailto: whose address is "mail@domain.tld"; none is a terms, licence or disclaimer page. Searching
  the text of the five pages for "licen", "copyright", "creative commons", "terms of use", "public domain",
  "attribut", "all rights reserved", "cite", "citation" and "disclaim" in any letter case, one page matches,
  three times: cms-magazine.html, under a heading reading "COPYRIGHT", states "The CMS has copyright
  to the article and any publication wishing to reprint it must ask permission from the CMS.", the word
  "copyright" appearing twice there, and matches "cite" inside the word "unsolicited" in "We consider
  unsolicited articles for our magazine."; that page is about articles for the society's magazine and
  states nothing about these data. The portal page states "The Catalina Marine Society (CMS) assumes
  no responsibility for the accuracy of the data and we strongly suggest that you contact the CMS before
  using the data for any matter of significance.", which grants no permission and states no condition,
  so it is not entered as a licence
variables:
- name: '#'
  description: null
  unit: null
  file:
  - Temp_20ft_01302025-03092025_22169464.dat
  - Temp_40ft_01302025-03092025_22169467.dat
  - Temp_80ft_01302025-03092025_22169469.dat
  - JUSS_pH_02022025-03092025.txt
  - JUSS_depth_temp_95ft_02022025-03092025.dat
  - WIES_1ft_01052025-01302025_20894273.csv
  - WIES_10ft_01052025-01302025_20733049.csv
  - WIES_20ft_01052025-01302025_20894279.csv
  - WIES_40ft_01052025-01302025_22129129.csv
  - WIES_60ft_01052025-01302025_21292584.csv
  - Temp_40ft_04272024-05262024_20481390.csv
- name: 'Date Time  GMT-08 00'
  description: null
  unit: null
  file:
  - Temp_20ft_01302025-03092025_22169464.dat
  - Temp_40ft_01302025-03092025_22169467.dat
  - Temp_80ft_01302025-03092025_22169469.dat
  - JUSS_depth_temp_95ft_02022025-03092025.dat
- name: 'Temp  °F (LGR S N  22169464  SEN S N  22169464  LBL  temp)'
  description: null
  unit: null
  file:
  - Temp_20ft_01302025-03092025_22169464.dat
- name: 'Coupler Detached (LGR S N  22169464)'
  description: null
  unit: null
  file:
  - Temp_20ft_01302025-03092025_22169464.dat
- name: 'Temp  °F (LGR S N  22169467  SEN S N  22169467  LBL  temp)'
  description: null
  unit: null
  file:
  - Temp_40ft_01302025-03092025_22169467.dat
- name: 'End Of File (LGR S N  22169467)'
  description: null
  unit: null
  file:
  - Temp_40ft_01302025-03092025_22169467.dat
- name: 'Temp  °F (LGR S N  22169469  SEN S N  22169469  LBL  temp)'
  description: null
  unit: null
  file:
  - Temp_80ft_01302025-03092025_22169469.dat
- name: 'End Of File (LGR S N  22169469)'
  description: null
  unit: null
  file:
  - Temp_80ft_01302025-03092025_22169469.dat
- name: 'Date-Time (PST PDT)'
  description: null
  unit: null
  file:
  - JUSS_pH_02022025-03092025.txt
- name: 'Temperature , °F'
  description: null
  unit: null
  file:
  - JUSS_pH_02022025-03092025.txt
- name: 'Millivolts , mv'
  description: null
  unit: null
  file:
  - JUSS_pH_02022025-03092025.txt
- name: 'pH , pH'
  description: null
  unit: null
  file:
  - JUSS_pH_02022025-03092025.txt
- name: 'Abs Pres  psi (LGR S N  21137292  SEN S N  21137292)'
  description: null
  unit: null
  file:
  - JUSS_depth_temp_95ft_02022025-03092025.dat
- name: 'Temp  °F (LGR S N  21137292  SEN S N  21137292)'
  description: null
  unit: null
  file:
  - JUSS_depth_temp_95ft_02022025-03092025.dat
- name: 'End Of File (LGR S N  21137292)'
  description: null
  unit: null
  file:
  - JUSS_depth_temp_95ft_02022025-03092025.dat
- name: 'ISO 8601  ime'
  description: null
  unit: null
  file:
  - JUSS_current_02022025-03092025.txt
  - current_95ft_10132024-01052025_2108000.txt
- name: 'Speed (cm/s)'
  description: null
  unit: null
  file:
  - JUSS_current_02022025-03092025.txt
  - current_95ft_10132024-01052025_2108000.txt
- name: 'Heading (degrees)'
  description: null
  unit: null
  file:
  - JUSS_current_02022025-03092025.txt
  - current_95ft_10132024-01052025_2108000.txt
- name: 'Veloci y-N (cm/s)'
  description: null
  unit: null
  file:
  - JUSS_current_02022025-03092025.txt
  - current_95ft_10132024-01052025_2108000.txt
- name: 'Veloci y-E (cm/s)'
  description: null
  unit: null
  file:
  - JUSS_current_02022025-03092025.txt
- name: 'Date Time  GMT-06 00'
  description: null
  unit: null
  file:
  - WIES_1ft_01052025-01302025_20894273.csv
  - WIES_10ft_01052025-01302025_20733049.csv
  - WIES_20ft_01052025-01302025_20894279.csv
  - WIES_60ft_01052025-01302025_21292584.csv
- name: 'Temp  °F (LGR S N  20894273  SEN S N  20894273)'
  description: null
  unit: null
  file:
  - WIES_1ft_01052025-01302025_20894273.csv
- name: 'End Of File (LGR S N  20894273)'
  description: null
  unit: null
  file:
  - WIES_1ft_01052025-01302025_20894273.csv
- name: 'Temp  °F (LGR S N  20733049  SEN S N  20733049)'
  description: null
  unit: null
  file:
  - WIES_10ft_01052025-01302025_20733049.csv
- name: 'End Of File (LGR S N  20733049)'
  description: null
  unit: null
  file:
  - WIES_10ft_01052025-01302025_20733049.csv
- name: 'Temp  °F (LGR S N  20894279  SEN S N  20894279)'
  description: null
  unit: null
  file:
  - WIES_20ft_01052025-01302025_20894279.csv
- name: 'End Of File (LGR S N  20894279)'
  description: null
  unit: null
  file:
  - WIES_20ft_01052025-01302025_20894279.csv
- name: 'Date Time  GMT-07 00'
  description: null
  unit: null
  file:
  - WIES_40ft_01052025-01302025_22129129.csv
- name: 'Temp  °F (LGR S N  22129129  SEN S N  22129129)'
  description: null
  unit: null
  file:
  - WIES_40ft_01052025-01302025_22129129.csv
- name: 'End Of File (LGR S N  22129129)'
  description: null
  unit: null
  file:
  - WIES_40ft_01052025-01302025_22129129.csv
- name: 'Temp  °F (LGR S N  21292584  SEN S N  21292584)'
  description: null
  unit: null
  file:
  - WIES_60ft_01052025-01302025_21292584.csv
- name: 'End Of File (LGR S N  21292584)'
  description: null
  unit: null
  file:
  - WIES_60ft_01052025-01302025_21292584.csv
- name: 'Date Time, GMT-06:00'
  description: null
  unit: null
  file:
  - Temp_40ft_04272024-05262024_20481390.csv
- name: 'Temp, °F (LGR S/N: 20481390, SEN S/N: 20481390)'
  description: null
  unit: null
  file:
  - Temp_40ft_04272024-05262024_20481390.csv
- name: 'Coupler Detached (LGR S/N: 20481390)'
  description: null
  unit: null
  file:
  - Temp_40ft_04272024-05262024_20481390.csv
- name: 'Coupler Attached (LGR S/N: 20481390)'
  description: null
  unit: null
  file:
  - Temp_40ft_04272024-05262024_20481390.csv
- name: 'Host Connected (LGR S/N: 20481390)'
  description: null
  unit: null
  file:
  - Temp_40ft_04272024-05262024_20481390.csv
- name: 'End Of File (LGR S/N: 20481390)'
  description: null
  unit: null
  file:
  - Temp_40ft_04272024-05262024_20481390.csv
- name: 'date and time          pressure'
  description: null
  unit: null
  file:
  - Pressure_95ft_04272024-05262024_21511799.txt
- name: 'psi; temp F'
  description: null
  unit: null
  file:
  - Pressure_95ft_04272024-05262024_21511799.txt
- name: 'Se'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
- name: 'Mo'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'DoM'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'Y'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'hr'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'mi'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'se'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'A/P'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'TdegF'
  description: null
  unit: null
  file:
  - thermograph_20ft_10132024-01052025_21894636.txt
  - thermograph_40ft_10132024-01052025_21894635.txt
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'Seq'
  description: null
  unit: null
  file:
  - thermograph_60ft_10132024-01052025_20894280.txt
- name: 'Veloci y E (cm/s)'
  description: null
  unit: null
  file:
  - current_95ft_10132024-01052025_2108000.txt
coverage: >-
  The collection page's statement of the two platforms, "CMS established the Jim Updike Seabed Station
  adjacent to the Dirk Burcham Scientific Mooring. We expect the platforms to be serviced simultaneously
  and their data linked to this page.", and its four headings with the labels printed under each: under
  "February 2, 2025 - March 9, 2025", "thermographs at 20, 40 and 60 ft", "Sonde at 60 ft bad conductivity
  and pH data", "Jim Updike Seabed Station, 95 ft", "pH data", "depth and temperature" and "current";
  under "Mixed-Layer Data January 5 2025 - January 30 2025", "thermographs at 1, 5, 10, 20, 30, 40 and
  60 ft"; under "April 27, 2024 - May 26, 2024", "thermograph 20ft", "thermograph 40ft", "thermograph
  80 ft", "pH 95 ft", "water level 95 ft" and "current 95 ft"; and under "Oct 13, 2024 - Jan 5, 2025",
  "thermograph 20ft:", "thermograph 40 ft", "thermograph 60 ft", "water level 95ft", "pH 95 ft" and "current
  95 ft". This record holds 17 of the 26 files those headings list and the one file the headings link,
  as access states. The collection page states no place name, coordinate, island or county for either
  platform. The location this record is tagged with rests on three things the steward prints, none
  of them a statement on the collection page of where the platforms are: seven of the 26 URLs the collection
  page prints name files beginning "WIES_", five of them held; the steward's WIES mooring page, https://www.catalinamarinesociety.org/data-portal-wies-sci-moor-data.html,
  states "CMS occasionally deploys instrumentation on a mooring located at the Wrigley Institute of Environmental
  Studies (WIES)."; and the steward's home page, https://www.catalinamarinesociety.org/index.html, in
  the biography headed "mike doran" under "MEET THE CATALINA MARINE SOCIETY BOARD OF DIRECTORS", states
  "Mr. Doran has been a certified scuba diver since 1974, and is an active scientific research diver
  with Catalina Conservancy Divers through the USC Wrigley Institute of Environmental Studies at Catalina."
  The WIES mooring page does not name the Dirk Burcham Scientific Mooring or the Jim Updike Seabed Station,
  and neither the collection page's text nor the WIES mooring page's names an island. Each page's title
  carries the word "Catalina" once, in "Catalina Marine Society"; outside its title the WIES mooring page
  carries the word nowhere, and the collection page carries it 26 times, each inside the host name
  www.catalinamarinesociety.org of one of its 26 printed file URLs. This record states no span read
  off the files' own rows
coverage_stated_at: >-
  https://www.catalinamarinesociety.org/dirk-burchan-scientific-mooring-and-jim-updike-seabed-station.html
  states the platforms sentence, the four headings, the labels under them and the 26 file URLs, seven
  of them naming "WIES_" files; https://www.catalinamarinesociety.org/data-portal-wies-sci-moor-data.html
  states the WIES sentence; https://www.catalinamarinesociety.org/index.html states the Doran sentence,
  in the biography headed "mike doran" under "MEET THE CATALINA MARINE SOCIETY BOARD OF DIRECTORS";
  the byte counts are those of the copies retrieved 2026-09-27, each recorded in the fetch manifest beside
  its file in data/raw/cms_burcham_updike_mooring/ (all three pages retrieved 2026-09-27)
retrieved: '2026-09-27'
fetch_script: src/fetch/cms_burcham_updike_mooring.py
file: null
transcribed_from: null
derived_from: null
topics:
- ocean-climate/temperature
- ocean-climate/oxygen-ph
- recruitment-connectivity/larval-transport
regions:
- scb.islands.santa-catalina
beds: []
sites: []
site_key:
- file: JUSS_pH_02022025-03092025.txt
- file: JUSS_depth_temp_95ft_02022025-03092025.dat
- file: JUSS_current_02022025-03092025.txt
references: []
human_task: null
---
