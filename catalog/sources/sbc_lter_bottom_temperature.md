---
id: sbc_lter_bottom_temperature
title: >-
  SBC LTER: Reef: Bottom Temperature: Continuous water temperature, ongoing since 2000
steward: Santa Barbara Coastal LTER
url: https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.13.33
doi: 10.6073/pasta/e565d409b63f20c768133c653ccdb2d7
status: VERIFIED
tier: FETCHED
access:
  - >-
    Open https://sbclter.msi.ucsb.edu/data/catalog/, the Santa Barbara Coastal LTER data catalog.
    Under the collection "SBC LTER: Ongoing time-series of abiotic variables in kelp forests" it
    lists "Reef bottom water temperature", linking to
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.13. The page's HTML
    carries a second link under the same label, to
    https://portal.edirepository.org/nis/mapbrowse?scope=knb-lter-sbc&identifier=13&revision=newest,
    inside an HTML comment (HTTP 200, 2026-09-19)
  - >-
    The steward's own package page,
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.13, is served as an
    application shell. The HTML answers HTTP 200 in 17,652 bytes and contains neither
    "Temperature" nor "temperature"; https://sbclter.msi.ucsb.edu/assets/js/package/main.js builds
    the page from
    `https://pasta.lternet.edu/package/metadata/eml/${ package.replace(/\./g, "/") }/newest`
    (2026-09-19)
  - >-
    This record's landing page is
    https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.13.33, where
    https://doi.org/10.6073/pasta/e565d409b63f20c768133c653ccdb2d7 sends a request: the DOI answers
    HTTP 302 with that URL as its Location. The landing page answered HTTP 403 with a 162-byte
    text/html body titled "403 Forbidden" and signed "nginx/1.18.0 (Ubuntu)" to a request whose
    User-Agent was "kelpcatalog/sbc_lter_bottom_temperature". Later requests to it that day timed
    out on connect, and the page's content was not read (2026-09-19)
  - >-
    The PASTA service methods answer HTTP 403 with a text/plain body that begins "User
    'EDI-078e6e3cee4f7f2812f150701da9351acb51e089 (Public Access)' is not authorized to execute
    service method '<method>'.": readMetadata at
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/13/33, readDataEntity at
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/13/33/d707a45a2cd6eee1d016d99844d537da,
    listDataPackageRevisions at https://pasta.lternet.edu/package/eml/knb-lter-sbc/13, and
    listDataPackageScopes at https://pasta.lternet.edu/package/eml, each asked under the
    User-Agent "kelpcatalog/knb-lter-sbc.13". Asked under the User-Agent
    "kelpcatalog/sbc_lter_bottom_temperature", each of the four instead answers HTTP 403 with the
    162-byte "403 Forbidden" page signed "nginx/1.18.0 (Ubuntu)" (2026-09-19)
  - >-
    The package's EML was read from the DataONE copy of the same object. GET
    https://cn.dataone.org/cn/v2/object/ followed by the percent-encoded identifier
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/13/33 answered HTTP 200 with
    36,250 bytes whose root element declares packageId "knb-lter-sbc.13.33" and system
    "https://pasta.edirepository.org". The system metadata for that identifier,
    https://cn.dataone.org/cn/v2/meta/ plus the same percent-encoded identifier, states checksum
    algorithm "SHA-1" and value 2c06b509a7d150f8be85d99948618cb8c6079f9d, formatId
    "https://eml.ecoinformatics.org/eml-2.2.0" and originMemberNode "urn:node:LTER"; the SHA-1 of
    the 36,250 bytes served equals that value. That system metadata states an accessPolicy in
    which an allow block gives subject "public" the permission "read", and an obsoletes element
    naming https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/13/32; it carries no
    obsoletedBy element (2026-09-19)
  - >-
    Revision 33 is the revision this record enters.
    https://cite.edirepository.org/cite/knb-lter-sbc.13.33?style=RAW answers HTTP 200 and states
    'version': '33', 'pubdate': '2026-02-20', 'doi':
    'doi:10.6073/pasta/e565d409b63f20c768133c653ccdb2d7', 'publisher': 'Environmental Data
    Initiative' and authors Reed, Daniel C; Miller, Robert J. Asked for each of knb-lter-sbc.13.25
    through knb-lter-sbc.13.44 in turn, the same service answers HTTP 200 for .25 through .33,
    each stating its own 'version', 'pubdate' and 'doi', and HTTP 400 for .34 through .44
    (2026-09-19)
  - >-
    The data entity is served by the DataONE member node EDI replicates to, at
    https://gmn.lternet.edu/mn/v2/object/ followed by the entity's PASTA identifier
    percent-encoded whole:
    https://gmn.lternet.edu/mn/v2/object/https%3A%2F%2Fpasta.lternet.edu%2Fpackage%2Fdata%2Feml%2Fknb-lter-sbc%2F13%2F33%2Fd707a45a2cd6eee1d016d99844d537da.
    An anonymous GET under the User-Agent "kelpcatalog/knb-lter-sbc.13" answers HTTP 200 with
    Content-Length 582980514, Content-Disposition attachment;
    filename="Bottom_temp_all_years_20260129.csv", Content-Type application/octet-stream,
    DataONE-Checksum "SHA-1,2c71847a7670e928800133c564aad85754c18bc6", DataONE-Proxy
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/13/33/d707a45a2cd6eee1d016d99844d537da
    and no ETag. A GET on https://cn.dataone.org/cn/v2/resolve/ followed by the same identifier
    is served from gmn.lternet.edu with the same Content-Length, Content-Disposition,
    DataONE-Checksum and DataONE-Proxy (2026-09-19)
  - >-
    The same GET under the User-Agent "kelpcatalog/sbc_lter_bottom_temperature" answers HTTP 200
    with those same headers, Content-Length 582980514 among them, over a body that is the
    162-byte "403 Forbidden" page signed "nginx/1.18.0 (Ubuntu)" (2026-09-19)
  - >-
    Run src/fetch/sbc_lter_bottom_temperature.py, which sends the User-Agent
    "kelpcatalog/knb-lter-sbc.13", stores the body under the Content-Disposition filename, and
    keeps it only when its SHA-1 and its length equal the checksum and size the DataONE system
    metadata states for the entity's identifier, given under format; no account, key or referrer
    is required. The 582980514 bytes held also have
    the MD5 the EML states for the entity, and 15469803 lines after the header line, the EML's
    numberOfRecords (HTTP 200, 2026-09-19)
format: >-
  The EML lists one dataTable, entityName "Bottom water temperature, all years" and
  entityDescription "Continous temperature at permanent reef sites", whose physical states
  objectName "Bottom_temp_all_years_20260129.csv", size 582980514 with unit "byte", an
  authentication of method "MD5" whose value is ecfa2dc0e1989a44a5e9a4e1d6311b6e, and a textFormat
  of numHeaderLines 1, recordDelimiter "\r\n", attributeOrientation "column", fieldDelimiter ","
  and quoteCharacter '"', distributed at
  https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/13/33/d707a45a2cd6eee1d016d99844d537da;
  the dataTable states numberOfRecords 15469803. Each of the five attributes states the
  missingValueCode -99999, "value not recorded or not available". The DataONE system metadata for
  the entity's identifier states size 582980514, checksum algorithm "SHA-1" with value
  2c71847a7670e928800133c564aad85754c18bc6, and formatId "text/csv"; the member node serves it as
  Content-Type application/octet-stream (2026-09-19)
license: >-
  "This data package is released under the Creative Commons License Attribution 4.0 International
  (CC BY 4.0, see https://creativecommons.org/licenses/by/4.0/). This license states that consumers
  ("Data Users" herein) may distribute, adapt, reuse, remix, and build upon this work, as long as
  they give appropriate credit, provide a link to the license, and indicate if changes were made.
  If redistributed, a Data User may not apply additional restrictions or technological measures
  that prevent access. The Data User has an ethical obligation to cite the data source
  appropriately in any publication or product that results from its use, and notify the data
  contact or creator. Communication, collaboration, or co-authorship (as appropriate) with the
  creators of this data package is encouraged to prevent duplicate research or publication. The
  Data User is urged to contact the authors of these data if any questions about methodology or
  results occur. The Data User should realize that these data may be actively used by others for
  ongoing research and that coordination may be necessary to prevent duplication or inappropriate
  use. The Data User should realize that misinterpretation may occur if data are used outside of
  the context of the original study. The Data User should be aware that data are updated
  periodically and it is the responsibility of the Data User to check for new versions of the data.
  While substantial efforts are made to ensure the accuracy of data and associated documentation,
  complete accuracy of data sets cannot be guaranteed. This data package (with its components) is
  made available “as is” and with no warranty of accuracy or fitness for use. The creators of this
  data package and the repository where these data were obtained shall not be liable for any
  damages resulting from misinterpretation, use or misuse of the data package or its components.",
  the dataset's intellectualRights element in the EML named in access (2026-09-19)
variables:
  - SITE
  - SERIAL
  - DATE_LOCAL
  - TIME_LOCAL
  - TEMP_C
coverage: >-
  The abstract states "To examine temporal and spatial patterns of temperature in giant kelp
  forests, SBC has measured ambient water temperature at nine reef sites located along the mainland
  coast of the Santa Barbara Channel and at two sites on the north side Santa Cruz Island beginning
  in 2000." The dataset's coverage holds eleven geographicCoverage elements, each giving one point
  as its boundingCoordinates, west equal to east and north equal to south: "ABUR: Arroyo Burro Reef
  is located on the Santa Barbara Channel near the mouth of Arroyo Burro Creek and Beach. Depth
  ranges from 5.4 to 7 meters." at -119.7445915, 34.400275; "AHND: Arroyo Hondo Reef is located on
  the Santa Barbara Channel near the east end of Gaviota State Park, CA. Depth ranges from -4.3m to
  -6.6 meters." at -120.1426165, 34.471817; "AQUE: Arroyo Quemada Reef: Arroyo Quemada Reef depth
  range from 5.4 m to 10.7 m. Reference on Land is close to US101/Arroyo Quemada Ln." at
  -120.11905, 34.46774988; "BULL: Builto: Bulito has three permanent transect: Transect I, III, VI.
  Depth Range from -5.5 to -7.3. Reference on land is close to Ranch Real road and Hollister Ranch
  road crossing section." at -120.33349, 34.45850533; "CARP: Carpinteria Reef is located on the
  Santa Barbara Channel offshore of the Carpinteria Salt Marsh. Depth range is from -2.2 to -8.8
  meters" at -119.5416933, 34.3916319; "GOLB: Goleta Bay is located on the Santa Barbara Channel
  east of Goleta Pier. Depth range is -4.2 to -5 meters." at -119.8221, 34.4137165; "IVEE: Isla
  Vista (IV) Reef is located on the Santa Barbara Channel near the University of California Santa
  Barbara, CA. Depth range is from -8.2 to -8.8 meters." at -119.85755, 34.402783; "MOHK: Mohawk
  Reef: Mohawk Reef depth ranges from 4.5m to 6.0 m. Reference on land is Mohawk Rd / Edgewater
  Way." at -119.72957, 34.3940708; "NAPL: Naples Reef is located on the Santa Barbara Channel near
  the community of Naples and Dos Pueblos Canyon, Santa Barbara County, CA. Depth ranges from -5.9
  to -13.4 meters." at -119.95154, 34.4221216; "SCDI: Santa Cruz Island, Diablo; Depth ranges from
  -5.2 to -11.9 meters" at -119.75763, 34.05865; and "SCTW: Santa Cruz Island, Twin Harbor West;
  Depth ranges from -2.7 to -7.8 meters" at -119.71513, 34.0444335. Its temporalCoverage runs from
  2002-08-14 to 2026-01-20; the DATE_LOCAL values of the file run from 2002-08-14 to 2026-01-27 in
  the copy retrieved 2026-09-19. The abstract states the cadence as "Two submersible temperature
  loggers, sampling every 30 minutes and offset from each other by 15 minutes, are deployed so that
  data is recorded every 15 minutes at each site." The SITE attribute's definition states "Depth of
  temperature logger at each site varies from 4.95 to 8.15 meters.", and the methods state "Two
  temperature loggers were deployed at each site at a depth of approximately 7 m (MLLW), and
  fastened to permanent rebar stakes on the seafloor with two cable ties." The dataset's place
  keywords name "Arroyo Burro", "Arroyo Hondo", "Arroyo Quemada", "Bullito", "Carpinteria", "Goleta
  Bay", "Isla Vista", "Mohawk", "Naples", "Santa Cruz Island, Diablo" and "Santa Cruz Island, Twin
  Harbor West"
coverage_stated_at: >-
  The span of the held copy apart, it is stated in the EML named in access,
  https://cn.dataone.org/cn/v2/object/ plus the
  percent-encoded identifier
  https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/13/33: the dataset's abstract element
  states the nine-and-two sentence; the dataset's coverage element states the eleven
  geographicDescriptions with their boundingCoordinates, and the temporalCoverage; the data rows of
  Bottom_temp_all_years_20260129.csv state the span of the copy; the abstract
  states the cadence sentence; the dataTable's attributeList states the SITE definition and the
  dataset's methods element the deployment sentence; and the dataset's keywordSet whose
  keywordThesaurus is "Santa Barbara Coastal LTER Places", in which every keyword carries
  keywordType "place", states the place keywords (retrieved 2026-09-19)
retrieved: 2026-09-19
fetch_script: src/fetch/sbc_lter_bottom_temperature.py
file: null
transcribed_from: null
topics:
  - ocean-climate/temperature
  - ocean-climate/heatwaves
regions:
  - scb
  - scb.islands.santa-cruz
beds: []
sites: []
references: []
human_task: null
---
