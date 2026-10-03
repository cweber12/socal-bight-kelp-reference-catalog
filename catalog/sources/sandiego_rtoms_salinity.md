---
id: sandiego_rtoms_salinity
title: RTOMS Salinity - Ocean Monitoring Program
steward: Public Utilities, City of San Diego
url: https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-salinity/
doi: null
citations: []
status: VERIFIED
tier: FETCHED
access:
  - >-
    https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-salinity/, this record's landing
    page, answers HTTP 200 with 33,462 bytes of Content-Type text/html, no redirect, Last-Modified
    "Tue, 04 Aug 2026 15:05:11 GMT" and ETag "48feea4f84d2310478971baf7bb0c030", the bytes served
    having SHA-256 d8b5266693b818c22a1ec02d81e4cd8b65a9b2268011026549b743c3d5f8a134. Its <title> is
    "City of San Diego Open Data Portal" and its <h1> is this record's title; under the heading it
    prints "Public Utilities", linking /departments/public-utilities/, "Updated Aug 20, 2024" and
    "As needed". Under "About this dataset" it states "Salinity measurements collected by
    Real-time Oceanographic Mooring System (RTOMS)." and then a paragraph of six sentences, shown
    after its "Show More" button, of which coverage quotes the third and the others read "The
    Ocean Monitoring Program maintains two RTOMS in partnership with Scripps Institute of
    Oceanography.", "RTOMS are anchored buoys suspended in the water column configured
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
    (2026-10-03)
  - >-
    The footer links "DCAT Dataset Catalog (JSON)" to
    https://raw.githubusercontent.com/COSD-PANDA/data-inventory/refs/heads/master/data.json, which
    answers HTTP 200 with 360,997 bytes and lists 122 datasets. The one whose identifier is
    "monitoring_ocean_rtoms_salinity" states title "RTOMS Salinity - Ocean Monitoring Program",
    description "Salinity measurements collected by Real-time Oceanographic Mooring System
    (RTOMS).", publisher name "Public Utilities" with subOrganizationOf
    name "City of San Diego", contactPoint fn "Data & Analytics" and hasEmail "data@sandiego.gov",
    issued "2023-08-14", modified "2024-08-20", accrualPeriodicity "irregular", accessLevel
    "public", keyword "Water quality" and "Ocean water", license
    "https://opendefinition.org/licenses/odc-pddl/", rights, spatial and temporal each null,
    describedBy "https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_dictionary_datasd.csv"
    with describedByType "text/csv", references the two dictionary URLs the next step names, and
    eight distribution entries, each with mediaType "text/csv" and format "csv", whose title and
    downloadURL are the eight file names and "Download" links the landing page prints under "Get
    the data", in the same order. The same catalog lists three more identifiers beginning
    monitoring_ocean_rtoms_, namely monitoring_ocean_rtoms_ocean_chemistry,
    monitoring_ocean_rtoms_water_quality and monitoring_ocean_rtoms_water_temperature, none of
    which this record holds (2026-10-03)
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
    bytes, a header line "Parameter,Instrument,Units" and twelve rows, among them
    "Salinity,Sea-Bird MicroCAT,PSU", the one whose Parameter is the value every held row's
    parameter column carries; and
    https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_qualifier_dictionary_datasd.csv, 843
    bytes, a header line "Qual (QC flag),Designation,Use" and six rows, for the flags 1, 2, 3, 4,
    5 and 9, whose Designation reads "Pass/good", "Provisional/unreviewed",
    "Suspect/questionable", "Bad", "Value changed/drift-corrected" and "Missing" respectively
    (2026-10-03)
  - >-
    The footer links "Terms of Use" to https://data.sandiego.gov/help/guides/terms/, which answers
    HTTP 200 with 19,868 bytes, is headed "Terms of Use" and states under "I. Introduction" "As a
    convenience to potential users, the City of San Diego (“City”) makes a variety of datasets
    (“Data”) available for download through this website." and under "III. Definitions"
    "“Data” means any of the data that is available for download through DataSD.org or
    data.sandiego.gov and includes any updates to that data."; the eight files the sixth access
    step fetches are the "Download" links the landing page prints, on seshat.datasd.org. The
    footer of the landing page also prints "© 2002–2026 City of San Diego. All rights reserved."
    (2026-10-03)
  - >-
    The steward states the moorings' positions in its biennial receiving waters reports.
    https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/annual-report-archives,
    whose <h1> is "Annual Receiving Waters Monitoring Reports", answers HTTP 200 with 149,160 bytes
    of Content-Type text/html; charset=UTF-8 and links "2020-2021 Report" to
    http://www.sandiego.gov/sites/default/files/compressed_2020-2021_biennial_receiving_waters_monitoring_report.pdf,
    which answers HTTP 301 with Location
    https://www.sandiego.gov/sites/default/files/compressed_2020-2021_biennial_receiving_waters_monitoring_report.pdf,
    which answers HTTP 200 with 38,157,298 bytes of Content-Type application/pdf, SHA-256
    683939f2d019d5efc8d79e0ed44c2f5f66352e36d713521eff712bbfbb777a13; and links "2022-2023
    Biennial Report" to
    https://www.sandiego.gov/sites/default/files/2024-12/compressed_2022-2023-biennial-receiving-waters-monitoring-and-assessment-report-for-ploo-and-sboo.pdf,
    which answers HTTP 200 with 48,069,765 bytes of Content-Type application/pdf, SHA-256
    ac4949335f06871e507d232884551f2f1f0202e8084304f0392561b88e00aae3. In each report Appendix C.2,
    on the page printed C2 (PDF page 432 of the 2020-2021 report and 472 of the 2022-2023 report),
    is a table captioned "Location, depth, and dates for each year-long deployment of the PLOO and
    SBOO RTOMS. Dates are displayed by deployment, recovery, and period of real-time (RT) data
    availability. All times are Pacific Standard Time; DD = decimal degrees." and headed "Site",
    "Deployment #", "Lat (DD)", "Long (DD)", "Total Depth (m)", "Deployment", "RTdata Start",
    "RTdata End" and "Recovery", as the 2022-2023 report's text layer reads them. The 2020-2021
    table prints, as Lat (DD), Long (DD), Total Depth (m), Deployment date and Recovery: PLOO 2,
    "32.66959", "-117.32298", "95", "10/7/2019", "9/29/2020"; PLOO 3, "32.66963", "-117.32272",
    "95", "11/3/2021", "--"; SBOO 3, "32.53185", "-117.18644", "31", "12/18/2019", "12/17/2020";
    and SBOO 4, "32.53177", "-117.18628", "31", "11/3/2021", "--". The 2022-2023 table prints
    PLOO 4, "32.66953", "-117.32404", "95", "12/8/2022", "10/26/2023"; PLOO 5, "32.67012",
    "-117.32463", "96", "12/20/2023", "--"; and SBOO 5, "32.53185", "-117.18651", "31",
    "6/29/2023", "--"; it also lists PLOO 3 and SBOO 4 with the positions above and Recovery
    "11/22/2022" and "Lost to Sea". Those are the Deployment# values the held files carry: 2, 3,
    4 and 5 for PLOO and 3, 4 and 5 for SBOO (2026-10-03)
  - >-
    Under "Get the data" the landing page prints a table headed "File name", "Download actions",
    "File Format" and "File size" with eight rows, each a file name coverage quotes, a "Download"
    link, "CSV" and a size format quotes. Run src/fetch/sandiego_rtoms_salinity.py, which
    sends the User-Agent "kelpcatalog/sandiego_rtoms_salinity", requests the eight
    "Download" links in the table's order, and keeps a body only when its Content-Type begins
    text/csv and its first line is the nine fields of the data dictionary in that file's order; no
    account, key or referrer is required. Each answered HTTP 200 with Content-Type text/csv, no
    redirect, no Content-Disposition, a Last-Modified and an ETag, and the bytes held are
  - https://seshat.datasd.org/monitoring_ocean_rtoms_salinity/PLOO_salinity_2023_datasd.csv (21,225,976 bytes, 2026-10-03)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_salinity/SBOO_salinity_2023_datasd.csv (7,433,217 bytes, 2026-10-03)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_salinity/PLOO_salinity_2022_datasd.csv (27,342,647 bytes, 2026-10-03)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_salinity/SBOO_salinity_2022_datasd.csv (12,156,296 bytes, 2026-10-03)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_salinity/PLOO_salinity_2021_datasd.csv (4,702,266 bytes, 2026-10-03)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_salinity/SBOO_salinity_2021_datasd.csv (2,308,911 bytes, 2026-10-03)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_salinity/PLOO_salinity_2020_datasd.csv (21,194,008 bytes, 2026-10-03)
  - https://seshat.datasd.org/monitoring_ocean_rtoms_salinity/SBOO_salinity_2020_datasd.csv (12,959,991 bytes, 2026-10-03)
format: >-
  The landing page prints "CSV" in the "File Format" column of each of the eight rows under "Get
  the data", ".CSV" after "Available Formats", and in the "File size" column "20.24 MB", "7.09
  MB", "26.08 MB", "11.59 MB", "4.48 MB", "2.20 MB", "20.21 MB" and "12.36 MB" for the PLOO 2023,
  SBOO 2023, PLOO 2022, SBOO 2022, PLOO 2021, SBOO 2021, PLOO 2020 and SBOO 2020 files; the DCAT
  entry states mediaType "text/csv" and format "csv" for each. The files held on 2026-10-03 are
  21,225,976, 7,433,217, 27,342,647, 12,156,296, 4,702,266, 2,308,911, 21,194,008 and 12,959,991
  bytes in that order, each served as Content-Type text/csv. Every byte of each is ASCII, every
  line ending is LF with no CR, and each first line is
  "project,Deployment#,unixtime_1000_gmt,datetime_pst,depth_m,parameter,units,value,qualifier_flag";
  the comma separated data rows that follow number 300,525, 106,772, 390,736, 174,684, 66,632,
  32,712, 303,752 and 189,440 in the same order, none of them ragged. The empty cells are in the
  value column alone and number 57,072, 22,941, 59,510, 38,010, 1,144, 537, 62,300 and 86,876 in
  the same order. parameter reads "Salinity" and units "PSU" in every row of every file;
  qualifier_flag takes 1, 3 and 9 in every file, 4 in the PLOO 2023, PLOO 2022 and PLOO 2020
  files, and 5 in the PLOO 2023 file
license: >-
  "View License", the text of the link the landing page prints after the label "License", to
  https://opendefinition.org/licenses/odc-pddl/, a page headed "Open Data Commons Public Domain
  Dedication and Licence (ODC PDDL)" that states "Domain of Application: Data" and, under
  "Comments", "“Public Domain for data/databases”". The portal's Terms of Use state "Your use of
  the Data is subject to these terms of use, which constitute a legal agreement between You and
  the City of San Diego (“City”).", "In order to use any of the Data, You must agree to these
  Terms of Use. You agree to the Terms of Use by either: (1) Clicking to accept the Terms of Use; or
  (2) Downloading or using any of the Data or any Derivative Work, in which case you understand
  and agree that the City will treat your download or use of the Data or a Derivative Work as an
  acceptance of the Terms of Use from that point forward.", "“Data” means any of the data that
  is available for download through DataSD.org or data.sandiego.gov and includes any updates to
  that data.", "If the City claims or seeks to protect any patent, copyright, or other intellectual
  property rights in any Data, the website will so indicate in the file containing such Data or on
  the page from which such Data is accessed. These Terms of Use do not grant You any title or right
  to any patent, copyright, or other such intellectual property rights that the City or others may
  have in the Data." and "For certain of the Data, there may be additional terms and conditions
  that are stated in the file containing such Data or on the page from which such Data is accessed.
  You understand and agree that You are bound by such additional terms and conditions."
license_stated_at: >-
  "License" and the "View License" link stand in the "Dataset Details" panel of
  https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-salinity/, and the DCAT
  entry the second access step names states the same URL as its license.
  https://opendefinition.org/licenses/odc-pddl/ answers HTTP 200 with Content-Type text/html;
  charset=utf-8: the heading quoted is its one <h2>, the domain line the one <li> under it, and the
  comment its "Comments" section; under its <h3> heading "Overview" it links
  http://opendatacommons.org/licenses/pddl/summary/, and under its <h3> heading "Full Text"
  http://opendatacommons.org/licenses/pddl/1.0/, each link's text being its own URL. The link
  under "Full Text" answers HTTP 301 with
  Location https://opendatacommons.org/licenses/pddl/1-0, which answers HTTP 301 with Location
  https://opendatacommons.org/licenses/pddl/1-0/, which answers HTTP 200 with a document whose two
  <h2> headings read "Open Data Commons Public Domain Dedication and License (PDDL) v1.0" and
  "Public Domain Dedication and License (PDDL)"; the link under "Overview" answers HTTP 301 with
  Location
  https://opendatacommons.org/licenses/pddl/summary/, which answers HTTP 200. The byte counts of
  those three pages depend on the client: curl 8.15.0 was served 27,671, 41,513 and 25,686 bytes
  and Python's urllib sending the User-Agent "kelpcatalog/sandiego_rtoms_salinity" 28,038,
  41,880 and 26,053, 367 more each, while urllib sending its default User-Agent was answered HTTP
  403 by each; every other byte count this record states was the same under curl 8.15.0 and under
  urllib sending that User-Agent. The Terms of Use sentences quoted are on
  https://data.sandiego.gov/help/guides/terms/, which the landing page's footer links as "Terms of
  Use" and the fourth access step describes: the first is the second sentence of the one paragraph
  under "I. Introduction"; the second is the whole paragraph under "II. Accepting the Terms of Use"
  and its subheading "A. Means of Acceptance."; the third is the first of the three paragraphs under
  "III. Definitions"; the fourth is the whole paragraph under "IV. City’s Intellectual Property
  Rights Not Affected"; and the fifth is the whole paragraph under "VII. Acceptance of Other
  Conditions". The same document carries the further headings "V. Exclusion of Warranties", "VI.
  Limitation of Liability and Indemnity" and "VIII. General Provisions". Nothing nearer states
  terms: the eight held files and the three dictionary files contain none of "licen", "copyright",
  "terms", "public domain", "creative" or "disclaim" in any letter case (2026-10-03)
variables:
  - name: project
    description: "The Ocean Outfall project for this measurement "
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
  - name: "Deployment#"
    description: Unique identifier assigned to the monitoring equipment deployment.
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
  - name: unixtime_1000_gmt
    description: "Posixtime or number of seconds since 1-Jan-1970 0:00:00 UTC x 1000 "
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
  - name: datetime_pst
    description: Date and time of measurement in Pacific Standard Time (PST)
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
  - name: depth_m
    description: Actual depth for measurement
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
  - name: parameter
    description: Parameter being measured
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
  - name: units
    description: Unites of measured value of parameter
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
  - name: value
    description: Measured value of parameter
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
  - name: qualifier_flag
    description: Qualifier QC flag for associated parameter and depth
    unit: null
    file:
      - PLOO_salinity_2023_datasd.csv
      - SBOO_salinity_2023_datasd.csv
      - PLOO_salinity_2022_datasd.csv
      - SBOO_salinity_2022_datasd.csv
      - PLOO_salinity_2021_datasd.csv
      - SBOO_salinity_2021_datasd.csv
      - PLOO_salinity_2020_datasd.csv
      - SBOO_salinity_2020_datasd.csv
measures: []
coverage: >-
  The paragraph under "About this dataset" states "The RTOMS are located near the terminal ends of
  the Point Loma (PLOO) and South Bay (SBOO) ocean outfalls and are typically deployed for
  one-year intervals." The page lists eight files under "Get the data", named "Point Loma Ocean
  Outfall (PLOO) 2023 RTOMS salinity measurements", "South Bay Ocean Outfall (SBOO) 2023 RTOMS
  salinity measurements", "Point Loma Ocean Outfall (PLOO) 2022 RTOMS salinity measurements",
  "South Bay Ocean Outfall (SBOO) 2022 RTOMS salinity measurements", "PLOO 2021 RTOMS salinity
  measurements", "SBOO 2021 RTOMS salinity measurements", "PLOO 2020 RTOMS salinity measurements"
  and "SBOO 2020 RTOMS salinity measurements", and this record holds all eight. The data
  dictionary states for project the possible values "PLOO - Point Loma Ocean Outfall; SBOO - South
  Bay Ocean Outfall". In the files held on 2026-10-03, project reads PLOO_RTOMS in every row of
  the four PLOO files and SBOO_RTOMS in every row of the four SBOO files; Deployment# takes 4 and 5 (PLOO
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
  dataset" on https://data.sandiego.gov/datasets/monitoring-ocean-rtoms-salinity/, which the page
  shows after its "Show More" button and whose HTML wraps "(PLOO)" and "(SBOO)" in <strong>
  elements; the eight file names are the "File name" column of the table under "Get the data" on
  the same page, top to bottom, and the title of the eight distribution entries of the DCAT entry
  the second access step names, in the same order; the possible values are the possible_values
  cell of the project row of
  https://seshat.datasd.org/monitoring_ocean_rtoms/rtoms_dictionary_datasd.csv, which the page
  renders under "Understand the data"; and the values last quoted are read off the eight held
  files, a fact of the copies retrieved 2026-10-03 into data/raw/sandiego_rtoms_salinity/
  by src/fetch/sandiego_rtoms_salinity.py
retrieved: 2026-10-03
fetch_script: src/fetch/sandiego_rtoms_salinity.py
file: null
transcribed_from: null
derived_from: null
topics:
  - ocean-climate/salinity
regions:
  - scb
beds: []
sites: []
site_key:
  - file: PLOO_salinity_2023_datasd.csv
    column: project
  - file: SBOO_salinity_2023_datasd.csv
    column: project
  - file: PLOO_salinity_2022_datasd.csv
    column: project
  - file: SBOO_salinity_2022_datasd.csv
    column: project
  - file: PLOO_salinity_2021_datasd.csv
    column: project
  - file: SBOO_salinity_2021_datasd.csv
    column: project
  - file: PLOO_salinity_2020_datasd.csv
    column: project
  - file: SBOO_salinity_2020_datasd.csv
    column: project
references: []
human_task: null
---
