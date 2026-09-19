---
id: sbc_lter_landsat_canopy
title: >-
  SBC LTER: Time series of quarterly NetCDF files of kelp biomass in the canopy from Landsat 5, 7
  and 8, since 1984 (ongoing)
steward: Santa Barbara Coastal LTER
url: https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.74.34
doi: 10.6073/pasta/8d67f78530eadd77aefd85e66f5643de
status: PATTERN
tier: NOT HELD
access:
  - >-
    Open https://sbclter.msi.ucsb.edu/data/catalog/, the Santa Barbara Coastal LTER data catalog.
    Under the collection "SBC LTER: Ongoing and long-term time-series of satellite and aerial
    estimates of giant kelp biomass" it lists "Kelp canopy area and biomass from Landsat", linking
    to https://portal.edirepository.org/nis/mapbrowse?scope=knb-lter-sbc&identifier=74&revision=newest
    and to https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.74 (HTTP 200,
    2026-09-18)
  - >-
    The steward's own package page,
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.74, is served as an
    application shell. The HTML answers HTTP 200 in 17,652 bytes and contains no occurrence of
    "Landsat"; https://sbclter.msi.ucsb.edu/assets/js/package/main.js builds the page from
    `https://pasta.lternet.edu/package/metadata/eml/${ package.replace(/\./g, "/") }/newest`
    (2026-09-18)
  - >-
    This record's landing page is
    https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.74.34. It answers HTTP
    200 in 16,554 bytes with the page titled "Data Portal - Login | Environmental Data Initiative
    (EDI)", which carries an h2 "Human Verification Check" over a form posting to ./turnstile with
    a div class "cf-turnstile" and data-sitekey "0x4AAAAAADdTzGlf2HJeMxoH", loading
    https://challenges.cloudflare.com/turnstile/v0/api.js. The delivered HTML contains no
    occurrence of "Landsat". The same 16,554 bytes are returned with a browser User-Agent and with
    a session cookie set by https://portal.edirepository.org/nis/home.jsp (2026-09-18)
  - >-
    The PASTA service methods answer HTTP 403 with a text/plain body of the form "User
    'EDI-078e6e3cee4f7f2812f150701da9351acb51e089 (Public Access)' is not authorized to execute
    service method '<method>'.": readMetadata at
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/74/34, readDataEntity at
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/74/34/c2bea785267fa434c40a22e2239bb337,
    listDataPackageRevisions at https://pasta.lternet.edu/package/eml/knb-lter-sbc/74, and
    listDataPackageScopes at https://pasta.lternet.edu/package/eml (2026-09-18)
  - >-
    The package's EML was read from the DataONE copy of the same object. GET
    https://cn.dataone.org/cn/v2/object/ followed by the percent-encoded identifier
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/74/34 answered HTTP 200 with
    25,932 bytes whose root element declares packageId "knb-lter-sbc.74.34" and system
    "https://pasta.edirepository.org". The system metadata for that identifier,
    https://cn.dataone.org/cn/v2/meta/ plus the same percent-encoded identifier, states checksum
    algorithm "SHA-1" and value 30850463aabbdd70d7dfd2affd6cb03ad11eec83, formatId
    "https://eml.ecoinformatics.org/eml-2.2.0" and originMemberNode "urn:node:LTER"; the SHA-1 of
    the 25,932 bytes served equals that value. That system metadata states an accessPolicy whose
    second allow block is subject "public" with permission "read" (2026-09-18)
  - >-
    https://cite.edirepository.org/cite/knb-lter-sbc.74.34?style=RAW answers HTTP 200 and states
    'version': '34', 'pubdate': '2026-08-04', 'doi':
    'doi:10.6073/pasta/8d67f78530eadd77aefd85e66f5643de', 'publisher': 'Environmental Data
    Initiative' and authors Bell, Tom W; Cavanaugh, Kyle C; Siegel, David A. Asked for each of
    knb-lter-sbc.74.1 through knb-lter-sbc.74.39 in turn, the same service answers HTTP 200 for
    .10 through .34, each stating its own 'version', 'pubdate' and 'doi', and HTTP 400 for .1
    through .9 and for .35 through .39 (2026-09-19)
  - >-
    The data entity is served by the DataONE member node EDI replicates to. A GET on
    https://gmn.lternet.edu/mn/v2/object/ followed by the percent-encoded identifier
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/74/34/c2bea785267fa434c40a22e2239bb337,
    and a GET on https://cn.dataone.org/cn/v2/resolve/ followed by the same percent-encoded
    identifier, each answered HTTP 200 over an anonymous request with Content-Length 2430814959,
    Content-Disposition attachment; filename="LandsatKelpBiomass_2026_Q2_withmetadata.nc",
    DataONE-Checksum "SHA-1,82c55e2ab5d1b1b8742ab6e546f81d1599f96fa6" and DataONE-Proxy
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/74/34/c2bea785267fa434c40a22e2239bb337.
    A Range request for the first 64 bytes of each returned a body beginning with the eight bytes
    89 48 44 46 0d 0a 1a 0a (2026-09-19)
  - >-
    No file was fetched and nothing of this source is held here. Only the 64-byte ranges named in
    the step above were read; the 2430814959-byte entity was not retrieved. See status and format
format: >-
  The EML lists one otherEntity, entityName "Satellite kelp biomass since 1984", whose physical
  states objectName "LandsatKelpBiomass_2026_Q2_withmetadata.nc", size 2430814959 with unit
  "byte", an authentication of method "MD5" whose value is 2be218c2ae22e8f4505ee8c3abe3a6ee, and
  formatName "NetCDF", distributed at
  https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/74/34/c2bea785267fa434c40a22e2239bb337.
  Its entityDescription reads "Canopy area (m2) of bull kelp (Nereocystis luetkeana) and giant kelp
  (Macrocystis pyrifera) and wet biomass (kg) of giant kelp from Landsat 5, 7 and 8 imagery, along
  coastal areas of California, Oregon USA and Baja California and Baja California Sur, Mexico." The
  abstract states "Data are organized into a single NetCDF file and contain the quarterly area and
  biomass means for each Landsat pixel across the three sensors." and "Relevant metadata such as
  number of Landsat estimates from which the mean was derived, the number of estimates from each
  sensor, standard error for each quarterly estimate, spatial coordinates, and date are all
  included in the file." The DataONE system metadata for the entity's identifier states size
  2430814959, checksum algorithm "SHA-1" with value
  82c55e2ab5d1b1b8742ab6e546f81d1599f96fa6, and formatId "application/octet-stream". The dataset's
  two distribution elements give https://sbclter.msi.ucsb.edu/ and
  https://doi.org/10.6073/pasta/8d67f78530eadd77aefd85e66f5643de (2026-09-18)
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
  the dataset's intellectualRights element in the EML named in access (2026-09-18)
variables: []
coverage: >-
  The dataset's geographicCoverage states the geographicDescription "West Coast: Coastal areas of
  Baja California, Mexico, California, Oregon, and the outer coast of Washington (including
  offshore islands)" and the boundingCoordinates west -124.77, east -114.04, north 48.40, south
  27.01. Its temporalCoverage runs from 1984-03-23 to 2026-06-30. The abstract states "Canopy area
  (m) data are given for individual 30 x 30 meter pixels for all coastal areas of Baja California,
  Mexico, California, Oregon, and the outer coast of Washington (including offshore islands)." and
  "Biomass data (wet weight, kg) are given for individual 30 x 30 meter pixels in the coastal areas
  extending from near Ano Nuevo, CA through the southern range limit in Baja California (including
  offshore islands), representing the range where giant kelp is the dominant canopy forming
  species." It states the cadence as "Observations are made on a 16 day repeat cycle, for each
  instrument, but the temporal coverage is irregular because of cloud cover, instrument failure,
  and the mission length of each sensor (TM: 1984 – 2011, ETM+: 1999 – present, OLI: 2013 –
  present)." and the sensors as "derived from Landsat 5 Thematic Mapper (TM), Landsat 7 Enhanced
  Thematic Mapper Plus (ETM+), Landsat 8 Operational Land Imager (OLI), and Landsat 9 Operational
  Land Imager 2 satellite imagery". The dataset's place keywords name "Anacapa Island", "San Clemente
  Island", "San Miguel Island", "San Nicolas Island", "Santa Barbara Channel Islands", "Santa
  Barbara County", "Santa Barbara Island", "Santa Catalina Island", "Santa Cruz Island" and "Santa
  Rosa Island"
coverage_stated_at: >-
  All of it is stated in the EML named in access, https://cn.dataone.org/cn/v2/object/ plus the
  percent-encoded identifier
  https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/74/34: the dataset's coverage element
  states the geographicDescription, the boundingCoordinates and the temporalCoverage; the dataset's
  abstract element states the two pixel-extent sentences, the repeat-cycle sentence and the sensor
  clause; and the dataset's keywordSet whose keywordThesaurus is "Santa Barbara Coastal LTER
  Places", in which every keyword carries keywordType "place", states the place keywords
  (retrieved 2026-09-18)
retrieved: null
fetch_script: null
file: null
transcribed_from: null
topics:
  - canopy/satellite
  - canopy/persistence
regions:
  - scb
beds: []
sites: []
references: []
human_task: null
---
