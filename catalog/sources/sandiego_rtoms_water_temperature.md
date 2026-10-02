---
id: sandiego_rtoms_water_temperature
title: RTOMS Water Temperature - Ocean Monitoring Program
steward: Public Utilities, City of San Diego
url: https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-water-temperature/
doi: null
citations: []
status: VERIFIED
tier: FETCHED
access:
  - >-
    https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-water-temperature/, this record's
    landing page, answers HTTP 200 with 33,871 bytes of Content-Type text/html, no redirect,
    Last-Modified "Tue, 04 Aug 2026 15:05:11 GMT" and ETag "a7f17407295fc20ec7d6048f16c9aac8", the
    bytes served having SHA-256 cda9cf7e381876b2c5e1202ed7056158aaf395b1ff150c053f5c55158d21e1cd.
    Its <title> is "City of San Diego Open Data Portal" and its <h1> is this record's title; under
    the heading it prints "Public Utilities", linking /departments/public-utilities/, "Updated Aug
    20, 2024" and "As needed". Under "About this dataset" it states "Water temperature
    measurements collected by Real-time Oceanographic Mooring System (RTOMS)." and then a paragraph
    of six sentences, shown after its "Show More" button, of which coverage quotes the third and
    the others read "The Ocean Monitoring Program maintains two RTOMS in partnership with Scripps
    Institute of Oceanography.", "RTOMS are anchored buoys suspended in the water column configured
    with a range of instruments at multiple depths, collecting near continuous physical, chemical,
    and biological data and providing near real-time information of changing conditions.", "These
    high temporal resolution data are intended to enhance the assessment of environmental
    conditions and the potential impacts of oceanographic and anthropogenic events in coastal
    waters.", "These datasets have undergone quality control review." and "To access charts of
    provisional real-time data, see the Scripps website.", the words "Scripps website" linking
    https://mooring.ucsd.edu//, which answers HTTP 200 with 26,938 bytes whose <title> is "Ocean
    Time-Series Group at SIO". A paragraph headed "Disclaimer" follows: "RTOMS data undergo several
    checks, including preliminary automated checks and further manual review by Marine Biology and
    Ocean Operations staff. Inaccuracies in the data may persist due to subtle instrument problems
    or the lack of appropriate validation data, and subsequent review may result in future
    revisions to the data. For example, when water sample data for spectrophotometric pH and total
    alkalinity become available, these may be used to qualify or correct pH data. For
    nitrate/nitrite data, when available, water samples have been used to drift correct sensor
    data, and corrected data are provided when available. In addition, data downloaded directly
    from controllers and instruments may be used to fill in some data gaps in the future." Its
    "Dataset Details" panel prints "Publisher" over "Public Utilities", "Last Updated" over "Aug
    20, 2024", "Update Frequency" over "As needed", "Date Issued" over "Aug 14, 2023", "Available
    Formats" over ".CSV" and "License" over a link whose text is "View License"; "Tags" over
    "Water quality" and "Ocean water"; "References" over the links "Parameter Data Dictionary" and
    "Qualifier Data Dictionary"; and "Contact" over "Data & Analytics" and data@sandiego.gov. The
    HTML carries no JSON-LD and contains "doi", "cite" and "kelp" 0 times each in any letter case
    (2026-10-02)
  - >-
    The footer links "DCAT Dataset Catalog (JSON)" to
    https://raw.githubusercontent.com/COSD-PANDA/data-inventory/refs/heads/master/data.json, which
    answers HTTP 200 with 360,997 bytes and lists 122 datasets. The one whose identifier is
    "monitoring_ocean_rtoms_water_temperature" states title "RTOMS Water Temperature - Ocean
    Monitoring Program", description "Water temperature measurements collected by Real-time
    Oceanographic Mooring System (RTOMS).", publisher name "Public Utilities" with subOrganizationOf
    name "City of San Diego", contactPoint fn "Data & Analytics" and hasEmail "data@sandiego.gov",
    issued "2023-08-14", modified "2024-08-20", accrualPeriodicity "irregular", accessLevel
    "public", keyword "Water quality" and "Ocean water", license
    "https://opendefinition.org/licenses/odc-pddl/", rights, spatial and temporal each null,
    describedBy "https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_dictionary_datasd.csv"
    with describedByType "text/csv", references the two dictionary URLs the next step names, and
    eight distribution entries, each with mediaType "text/csv" and format "csv", whose title and
    downloadURL are the eight file names and "Download" links the landing page prints under "Get
    the data", in the same order. The same catalog lists three more identifiers beginning
    monitoring_ocean_rtoms_, namely monitoring_ocean_rtoms_salinity,
    monitoring_ocean_rtoms_ocean_chemistry and monitoring_ocean_rtoms_water_quality, none of
    which this record holds (2026-10-02)
  - >-
    Under "Understand the data" the landing page links "Download dictionary" to
    https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_dictionary_datasd.csv and renders its
    rows as a table headed "Field", "Data_type", "Description" and "Possible_values". That file
    answers HTTP 200 with 691 bytes of Content-Type text/csv: a header line
    "field,data_type,description,possible_values" and nine rows, one per column of the held files
    in the order their header line names them, data_type empty in every row; the variables below
    take each description from it. The two "References" links each answer HTTP 200 with
    Content-Type text/csv and a body that opens with a UTF-8 byte order mark:
    https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_parameter_dictionary_datasd.csv, 764
    bytes, a header line "Parameter,Instrument,Units" and twelve rows, among them "Water
    temperature,Sea-Bird MicroCAT,degrees Celcius", the one whose Parameter is the value every held
    row's parameter column carries; and
    https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_qualifier_dictionary_datasd.csv, 843
    bytes, a header line "Qual (QC flag),Designation,Use" and six rows, for the flags 1, 2, 3, 4,
    5 and 9, whose Designation reads "Pass/good", "Provisional/unreviewed",
    "Suspect/questionable", "Bad", "Value changed/drift-corrected" and "Missing" respectively
    (2026-10-02)
  - >-
    The footer links "Terms of Use" to https://data.sandiego.gov/help/guides/terms/, which answers
    HTTP 200 with 19,868 bytes, is headed "Terms of Use" and states under "III. Definitions"
    "“Data” means any of the data that is available for download through DataSD.org or
    data.sandiego.gov and includes any updates to that data."; the eight files the next step
    fetches are served from seshat.datasd.org. The footer of the landing page also prints "©
    2002–2026 City of San Diego. All rights reserved." (2026-10-02)
  - >-
    Under "Get the data" the landing page prints a table headed "File name", "Download actions",
    "File Format" and "File size" with eight rows, each a file name coverage quotes, a "Download"
    link, "CSV" and a size format quotes. Run src/fetch/sandiego_rtoms_water_temperature.py, which
    sends the User-Agent "kelpcatalog/sandiego_rtoms_water_temperature", requests the eight
    "Download" links in the table's order, and keeps a body only when its Content-Type begins
    text/csv and its first line is the nine fields of the data dictionary in that file's order; no
    account, key or referrer is required. Each answered HTTP 200 with Content-Type text/csv, no
    redirect, no Content-Disposition, a Last-Modified and an ETag, and the bytes held are
  - https://seshat.datasd.org/monitoring_ocean_rtoms_water_temperature/PLOO_water_temperature_2023_datasd.csv (27,830,949 bytes, 2026-10-02)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_water_temperature/SBOO_water_temperature_2023_datasd.csv (9,756,643 bytes, 2026-10-02)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_water_temperature/PLOO_water_temperature_2022_datasd.csv (36,087,956 bytes, 2026-10-02)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_water_temperature/SBOO_water_temperature_2022_datasd.csv (16,141,767 bytes, 2026-10-02)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_water_temperature/PLOO_water_temperature_2021_datasd.csv (6,166,181 bytes, 2026-10-02)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_water_temperature/SBOO_water_temperature_2021_datasd.csv (3,027,399 bytes, 2026-10-02)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_water_temperature/PLOO_water_temperature_2020_datasd.csv (27,926,195 bytes, 2026-10-02)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_water_temperature/SBOO_water_temperature_2020_datasd.csv (17,207,852 bytes, 2026-10-02)
format: >-
  The landing page prints "CSV" in the "File Format" column of each of the eight rows under "Get
  the data", ".CSV" after "Available Formats", and in the "File size" column "26.54 MB", "9.30
  MB", "34.42 MB", "15.39 MB", "5.88 MB", "2.89 MB", "26.63 MB" and "16.41 MB" for the PLOO 2023,
  SBOO 2023, PLOO 2022, SBOO 2022, PLOO 2021, SBOO 2021, PLOO 2020 and SBOO 2020 files; the DCAT
  entry states mediaType "text/csv" and format "csv" for each. The files held on 2026-10-02 are
  27,830,949, 9,756,643, 36,087,956, 16,141,767, 6,166,181, 3,027,399, 27,926,195 and 17,207,852
  bytes in that order, each served as Content-Type text/csv. Every byte of each is ASCII, every
  line ending is LF with no CR, and each first line is
  "project,Deployment#,unixtime_1000_gmt,datetime_pst,depth_m,parameter,units,value,qualifier_flag";
  the comma separated data rows that follow number 300,525, 106,772, 390,736, 174,684, 66,632,
  32,712, 303,752 and 189,440 in the same order, none of them ragged. The empty cells are in the
  value column alone and number 6,512, 22,918, 16,991, 6,950, 1,128, 533, 41,300 and 58,045 in the
  same order. parameter reads "Water temperature" and units "degrees Celsius" in every row of
  every file, where the parameter dictionary spells the unit "degrees Celcius"; qualifier_flag
  takes 1 and 9 in every file, and 3 in 1, 73 and 2 rows of the PLOO 2022, PLOO 2020 and SBOO
  2020 files
license: >-
  "View License", the text of the link the landing page prints after the label "License", to
  https://opendefinition.org/licenses/odc-pddl/. That page is headed "Open Data Commons Public
  Domain Dedication and Licence (ODC PDDL)" and states "Domain of Application: Data", under
  "Comments" "“Public Domain for data/databases”", and under "Full Text" the link
  http://opendatacommons.org/licenses/pddl/1.0/. The document that link reaches is headed "Open
  Data Commons Public Domain Dedication and License (PDDL) v1.0" and "Public Domain Dedication and
  License (PDDL)", and states under "Preamble" "The Open Data Commons – Public Domain Dedication
  and Licence is a document intended to allow you to freely share, modify, and use this work for
  any purpose and without any restrictions. This licence is intended for use on databases or their
  contents (“data”), either together or individually." and under "Part II: Dedication to the
  public domain" "3.1 Dedication of Copyright and Database Rights to the public domain. The
  Rightsholder by using this Document, dedicates the Work to the public domain for the benefit of
  the public and relinquishes all rights in Copyright and Database Rights over the Work."
license_stated_at: >-
  "License" and the "View License" link stand in the "Dataset Details" panel of
  https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-water-temperature/, and the DCAT
  entry the second access step names states the same URL as its license.
  https://opendefinition.org/licenses/odc-pddl/ answers HTTP 200 with 27,671 bytes of Content-Type
  text/html; charset=utf-8; the heading, the domain line and the comment quoted are its <h2>, the
  one <li> under it and its "Comments" section. Its "Full Text" link
  http://opendatacommons.org/licenses/pddl/1.0/ answers HTTP 301 with Location
  https://opendatacommons.org/licenses/pddl/1-0, which answers HTTP 301 with Location
  https://opendatacommons.org/licenses/pddl/1-0/, which answers HTTP 200 with 41,513 bytes; the
  two headings quoted are its <h2> elements, and the sentences quoted are the first paragraph
  under its "Preamble" heading and the paragraph beginning "3.1" under its heading "Part II:
  Dedication to the public domain", a section of sixteen paragraphs that the headings "4.0
  Relationship to other rights", "Part III: General provisions", "5.0 Warranties, disclaimer, and
  limitation of liability" and "6.0 General" follow. The same page's "Overview" link
  http://opendatacommons.org/licenses/pddl/summary/
  answers HTTP 301 with Location https://opendatacommons.org/licenses/pddl/summary/, which answers
  HTTP 200 with 25,686 bytes and states under "Disclaimer" "This is not a license. It is simply a
  handy reference for understanding the PDDL 1.0 — it is a human-readable expression of some of
  its key terms." The portal's Terms of Use, which the fourth access step names, state under "IV.
  City’s Intellectual Property Rights Not Affected" "If the City claims or seeks to protect any
  patent, copyright, or other intellectual property rights in any Data, the website will so
  indicate in the file containing such Data or on the page from which such Data is accessed." and
  under "VII. Acceptance of Other Conditions" "For certain of the Data, there may be additional
  terms and conditions that are stated in the file containing such Data or on the page from which
  such Data is accessed." Nothing nearer states terms: the eight held files and the three
  dictionary files contain none of "licen", "copyright", "terms", "public domain", "creative" or
  "disclaim" in any letter case (2026-10-02)
variables:
  - name: project
    description: "The Ocean Outfall project for this measurement "
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
  - name: "Deployment#"
    description: Unique identifier assigned to the monitoring equipment deployment.
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
  - name: unixtime_1000_gmt
    description: "Posixtime or number of seconds since 1-Jan-1970 0:00:00 UTC x 1000 "
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
  - name: datetime_pst
    description: Date and time of measurement in Pacific Standard Time (PST)
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
  - name: depth_m
    description: Actual depth for measurement
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
  - name: parameter
    description: Parameter being measured
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
  - name: units
    description: Unites of measured value of parameter
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
  - name: value
    description: Measured value of parameter
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
  - name: qualifier_flag
    description: Qualifier QC flag for associated parameter and depth
    unit: null
    file:
      - PLOO_water_temperature_2023_datasd.csv
      - SBOO_water_temperature_2023_datasd.csv
      - PLOO_water_temperature_2022_datasd.csv
      - SBOO_water_temperature_2022_datasd.csv
      - PLOO_water_temperature_2021_datasd.csv
      - SBOO_water_temperature_2021_datasd.csv
      - PLOO_water_temperature_2020_datasd.csv
      - SBOO_water_temperature_2020_datasd.csv
measures: []
coverage: >-
  The paragraph under "About this dataset" states "The RTOMS are located near the terminal ends of
  the Point Loma (PLOO) and South Bay (SBOO) ocean outfalls and are typically deployed for
  one-year intervals." The page lists eight files under "Get the data", named "Point
  Loma Ocean Outfall (PLOO) 2023 RTOMS water temperature measurements", "South Bay Ocean Outfall
  (SBOO) 2023 RTOMS water temperature measurements", "Point Loma Ocean Outfall (PLOO) 2022 RTOMS
  water temperature measurements", "South Bay Ocean Outfall (SBOO) 2022 RTOMS water temperature
  measurements", "PLOO 2021 RTOMS water temperature measurements", "SBOO 2021 RTOMS water
  temperature measurements", "PLOO 2020 RTOMS water temperature measurements" and "SBOO 2020 RTOMS
  water temperature measurements", and this record holds all eight. The data dictionary states
  for project the possible values "PLOO - Point Loma Ocean Outfall; SBOO - South Bay Ocean
  Outfall". In the files held on 2026-10-02, project reads PLOO_RTOMS in every row of the four
  PLOO files and SBOO_RTOMS in every row of the four SBOO files; Deployment# takes 4 and 5 (PLOO
  2023), 5 (SBOO 2023), 3 and 4 (PLOO 2022), 4 (SBOO 2022), 3 (PLOO 2021), 4 (SBOO 2021), 2 (PLOO
  2020) and 3 (SBOO 2020); depth_m takes 1, 10, 20, 30, 45, 60, 75 and 89 in the PLOO 2023 and
  PLOO 2020 files, 1, 9, 10, 20, 30, 45, 60, 74, 75, 87 and 89 in PLOO 2022, 1, 9, 20, 30, 45,
  60, 74 and 87 in PLOO 2021, and 1, 10, 18 and 26 in each SBOO file; and datetime_pst runs from
  2023-01-01 00:00:00 to 2023-12-31 23:50:00 (PLOO 2023), 2023-06-29 11:30:00 to 2023-12-31
  23:50:00 (SBOO 2023), 2022-01-01 00:00:00 to 2022-12-31 23:50:00 (PLOO 2022), 2022-01-01
  00:00:00 to 2022-11-03 03:00:00 (SBOO 2022), 2021-11-03 10:00:00 to 2021-12-31 23:50:00 (PLOO
  2021), 2021-11-03 14:00:00 to 2021-12-31 23:50:00 (SBOO 2021), 2020-01-01 00:00:00 to
  2020-09-29 18:00:00 (PLOO 2020) and 2020-01-01 00:00:00 to 2020-12-17 13:00:00 (SBOO 2020)
coverage_stated_at: >-
  The sentence quoted first is the third sentence of the six-sentence paragraph under "About this
  dataset" on
  https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-water-temperature/, which the page
  shows after its "Show More" button and whose HTML wraps "(PLOO)" and "(SBOO)" in <strong>
  elements; the eight file names are the "File name" column of the table under "Get the data" on
  the same page, top to bottom, and the title of the eight distribution entries of the DCAT entry
  the second access step names, in the same order; the possible values are the possible_values
  cell of the project row of
  https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_dictionary_datasd.csv, which the page
  renders under "Understand the data"; and the values last quoted are read off the eight held
  files, a fact of the copies retrieved 2026-10-02 into data/raw/sandiego_rtoms_water_temperature/
  by src/fetch/sandiego_rtoms_water_temperature.py
retrieved: 2026-10-02
fetch_script: src/fetch/sandiego_rtoms_water_temperature.py
file: null
transcribed_from: null
derived_from: null
topics:
  - ocean-climate/temperature
regions:
  - scb.mainland.san-diego
beds: []
sites: []
site_key:
  - file: PLOO_water_temperature_2023_datasd.csv
    column: project
  - file: SBOO_water_temperature_2023_datasd.csv
    column: project
  - file: PLOO_water_temperature_2022_datasd.csv
    column: project
  - file: SBOO_water_temperature_2022_datasd.csv
    column: project
  - file: PLOO_water_temperature_2021_datasd.csv
    column: project
  - file: SBOO_water_temperature_2021_datasd.csv
    column: project
  - file: PLOO_water_temperature_2020_datasd.csv
    column: project
  - file: SBOO_water_temperature_2020_datasd.csv
    column: project
references: []
human_task: null
---
