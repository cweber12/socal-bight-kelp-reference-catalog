---
id: sbc_lter_kelp_biomass
title: >-
  SBC LTER: Reef: Annual time series of biomass for kelp forest species, ongoing since 2000
steward: Santa Barbara Coastal LTER
url: https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.50.18
doi: 10.6073/pasta/cb45bf15430ba570828444b13dd8521f
status: VERIFIED
tier: FETCHED
access:
  - >-
    Open https://sbclter.msi.ucsb.edu/data/catalog/, the Santa Barbara Coastal LTER data catalog.
    Under the collection "SBC LTER: Ongoing time-series of giant kelp forest community dynamics
    (KFCD)" it lists "KFCD Biomass of algae, invertebrates and fish", linking to
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.50. The page's HTML
    carries a second link under the same label, to
    https://portal.edirepository.org/nis/mapbrowse?scope=knb-lter-sbc&identifier=50&revision=newest,
    inside an HTML comment (HTTP 200, 2026-09-19)
  - >-
    The steward's own package page,
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.50, is served as an
    application shell. The HTML answers HTTP 200 in 17,652 bytes and contains neither "Biomass"
    nor "biomass"; https://sbclter.msi.ucsb.edu/assets/js/package/main.js builds the page from
    `https://pasta.lternet.edu/package/metadata/eml/${ package.replace(/\./g, "/") }/newest`
    (2026-09-19)
  - >-
    This record's landing page is
    https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.50.18, where
    https://doi.org/10.6073/pasta/cb45bf15430ba570828444b13dd8521f sends a request: the DOI answers
    HTTP 302 with that URL as its Location. A request to the landing page under the User-Agent
    "kelpcatalog/knb-lter-sbc.50" timed out on connect from this address, and the page's content
    was not read (2026-09-19)
  - >-
    The PASTA service methods answer HTTP 403 with a text/plain body that begins "User
    'EDI-078e6e3cee4f7f2812f150701da9351acb51e089 (Public Access)' is not authorized to execute
    service method '<method>'.": readMetadata at
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/50/18, readDataEntity at
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/50/18/24d18d9ebe4f6e8b94e222840096963c,
    listDataPackageRevisions at https://pasta.lternet.edu/package/eml/knb-lter-sbc/50, and
    listDataPackageScopes at https://pasta.lternet.edu/package/eml, each asked under the
    User-Agent "kelpcatalog/knb-lter-sbc.50" (2026-09-19)
  - >-
    The package's EML was read from the DataONE copy of the same object. GET
    https://cn.dataone.org/cn/v2/object/ followed by the percent-encoded identifier
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/50/18 answered HTTP 200 with
    73,315 bytes whose root element declares packageId "knb-lter-sbc.50.18" and system
    "https://pasta.edirepository.org". The system metadata for that identifier,
    https://cn.dataone.org/cn/v2/meta/ plus the same percent-encoded identifier, states checksum
    algorithm "SHA-1" and value d43c6a413e63057c3c636ae155ee9c2736991ffa, formatId
    "https://eml.ecoinformatics.org/eml-2.2.0" and originMemberNode "urn:node:LTER"; the SHA-1 of
    the 73,315 bytes served equals that value. That system metadata states an accessPolicy in
    which an allow block gives subject "public" the permission "read", and an obsoletes element
    naming https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/50/17; it carries no
    obsoletedBy element (2026-09-19)
  - >-
    Revision 18 is the revision this record enters.
    https://cite.edirepository.org/cite/knb-lter-sbc.50.18?style=RAW answers HTTP 200 and states
    'version': '18', 'pubdate': '2025-10-15', 'doi':
    'doi:10.6073/pasta/cb45bf15430ba570828444b13dd8521f', 'publisher': 'Environmental Data
    Initiative' and authors Reed, Daniel C; Miller, Robert J. Asked for each of knb-lter-sbc.50.19
    through knb-lter-sbc.50.22 in turn, the same service answers HTTP 400 (2026-09-19)
  - >-
    The data entity is served by the DataONE member node EDI replicates to, at
    https://gmn.lternet.edu/mn/v2/object/ followed by the entity's PASTA identifier
    percent-encoded whole:
    https://gmn.lternet.edu/mn/v2/object/https%3A%2F%2Fpasta.lternet.edu%2Fpackage%2Fdata%2Feml%2Fknb-lter-sbc%2F50%2F18%2F24d18d9ebe4f6e8b94e222840096963c.
    An anonymous GET under the User-Agent "kelpcatalog/knb-lter-sbc.50" answers HTTP 200 with
    Content-Length 48203257, Content-Disposition attachment;
    filename="Annual_All_Species_Biomass_at_transect_20250903.csv", Content-Type
    application/octet-stream, DataONE-Checksum "SHA-1,a2a2ee412caa5a41af9d6d80f29b8a7fe09acd72",
    DataONE-Proxy
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/50/18/24d18d9ebe4f6e8b94e222840096963c
    and no ETag. A GET on https://cn.dataone.org/cn/v2/resolve/ followed by the same identifier
    is served from gmn.lternet.edu with the same Content-Length, Content-Disposition,
    DataONE-Checksum and DataONE-Proxy (2026-09-19)
  - >-
    Run src/fetch/sbc_lter_kelp_biomass.py, which sends the User-Agent
    "kelpcatalog/knb-lter-sbc.50", stores the body under the Content-Disposition filename, and
    keeps it only when its SHA-1 and its length equal the checksum and size the DataONE system
    metadata states for the entity's identifier, given under format; no account, key or referrer
    is required. The 48203257 bytes held also have the MD5 the EML states for the entity, and
    240588 lines after the header line, the EML's numberOfRecords (HTTP 200, 2026-09-19)
format: >-
  The EML lists one dataTable, entityName "SBC LTER Annual time series of biomass for kelp forest
  species" and entityDescription "The biomass of more than 200 kelp forest species at permanent
  sites", whose physical states objectName "Annual_All_Species_Biomass_at_transect_20250903.csv",
  size 48203257 with unit "byte", an authentication of method "MD5" whose value is
  5e73a13eff08d4b70ea01d1d5914eafb, and a textFormat of numHeaderLines 1, recordDelimiter "\r\n",
  attributeOrientation "column", fieldDelimiter ",", collapseDelimiters "no" and quoteCharacter
  '"', distributed at
  https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/50/18/24d18d9ebe4f6e8b94e222840096963c;
  the dataTable states numberOfRecords 240588. The attributes VIS, PERCENT_COVER, DENSITY, WM_GM2,
  DRY_GM2, SFDM, AFDM, SCIENTIFIC_NAME, TAXON_PHYLUM, TAXON_CLASS, TAXON_ORDER and TAXON_FAMILY
  each state the missingValueCode -99999, "value not recorded or not available". The DataONE
  system metadata for the entity's identifier states size 48203257, checksum algorithm "SHA-1"
  with value a2a2ee412caa5a41af9d6d80f29b8a7fe09acd72, and formatId "text/csv"; the member node
  serves it as Content-Type application/octet-stream (2026-09-19)
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
  - YEAR
  - MONTH
  - DATE
  - SITE
  - TRANSECT
  - VIS
  - SP_CODE
  - PERCENT_COVER
  - DENSITY
  - WM_GM2
  - DRY_GM2
  - SFDM
  - AFDM
  - SCIENTIFIC_NAME
  - COMMON_NAME
  - TAXON_KINGDOM
  - TAXON_PHYLUM
  - TAXON_CLASS
  - TAXON_ORDER
  - TAXON_FAMILY
  - TAXON_GENUS
  - GROUP
  - MOBILITY
  - GROWTH_MORPH
  - COARSE_GROUPING
coverage: >-
  The abstract's first paragraph states "These data are annual estimates of biomass of
  approximately 225 taxa of reef algae, invertebrates and fish in permanent transects at 11 kelp
  forest sites in the Santa Barbara Channel (2-8 transects per site). Abundance is measured
  annually (as percent cover or density, by size) and converted to biomass (i.e., wet mass, dry
  mass, decalcified dry mass, ash free dry mass) using published taxon-specific algorithms. Data
  collection began in summer 2000 and continues annually in summer to provide information on
  community structure, population dynamics and species change." and its second "The time period of
  data collection varied among the 11 kelp forest sites. Sampling at BULL, CARP, and NAPL began in
  2000, sampling at the other 6 mainland sites (AHND, AQUE, IVEE, GOLB, ABUR, MOHK) began in 2001
  (transects 3, 5, 6, 7, 8 at IVEE were added in 2011). Data collection at the two Santa Cruz
  Island sites (SCTW and SCDI) began in 2004." The dataset's coverage holds eleven
  geographicCoverage elements, each giving one point as its boundingCoordinates, west equal to
  east and north equal to south: "ABUR: Arroyo Burro Reef is located on the Santa Barbara Channel
  near the mouth of Arroyo Burro Creek and Beach. Depth ranges from 5.4 to 7 meters." at
  -119.7445915, 34.400275; "AHND: Arroyo Hondo Reef is located on the Santa Barbara Channel near
  the east end of Gaviota State Park, CA. Depth ranges from -4.3m to -6.6 meters." at
  -120.1426165, 34.471817; "AQUE: Arroyo Quemada Reef: Arroyo Quemada Reef depth range from 5.4 m
  to 10.7 m. Reference on Land is close to US101/Arroyo Quemada Ln." at -120.11905, 34.46774988;
  "BULL: Builto: Bulito has three permanent transect: Transect I, III, VI. Depth Range from -5.5
  to -7.3. Reference on land is close to Ranch Real road and Hollister Ranch road crossing
  section." at -120.33349, 34.45850533; "CARP: Carpinteria Reef is located on the Santa Barbara
  Channel offshore of the Carpinteria Salt Marsh. Depth range is from -2.2 to -8.8 meters" at
  -119.5416933, 34.3916319; "GOLB: Goleta Bay is located on the Santa Barbara Channel east of
  Goleta Pier. Depth range is -4.2 to -5 meters." at -119.8221, 34.4137165; "IVEE: Isla Vista
  (IV) Reef is located on the Santa Barbara Channel near the University of California Santa
  Barbara, CA. Depth range is from -8.2 to -8.8 meters." at -119.85755, 34.402783; "MOHK: Mohawk
  Reef: Mohawk Reef depth ranges from 4.5m to 6.0 m. Reference on land is Mohawk Rd / Edgewater
  Way." at -119.72957, 34.3940708; "NAPL: Naples Reef is located on the Santa Barbara Channel near
  the community of Naples and Dos Pueblos Canyon, Santa Barbara County, CA. Depth ranges from -5.9
  to -13.4 meters." at -119.95154, 34.4221216; "SCDI: Santa Cruz Island, Diablo; Depth ranges from
  -5.2 to -11.9 meters" at -119.75763, 34.05865; and "SCTW: Santa Cruz Island, Twin Harbor West;
  Depth ranges from -2.7 to -7.8 meters" at -119.71513, 34.0444335. Its temporalCoverage runs from
  2000-01-01 to 2025-07-30; the DATE values of the file run from 2000-09-08 to 2025-07-30 in the
  copy retrieved 2026-09-19
coverage_stated_at: >-
  The EML named in access, https://cn.dataone.org/cn/v2/object/ plus the percent-encoded
  identifier https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/50/18, and the held file:
  the dataset's abstract element states the two paragraphs quoted; the dataset's coverage element
  states the eleven geographicDescriptions with their boundingCoordinates, and the
  temporalCoverage; and the data rows of Annual_All_Species_Biomass_at_transect_20250903.csv state
  the span of the copy (retrieved 2026-09-19)
retrieved: 2026-09-19
fetch_script: src/fetch/sbc_lter_kelp_biomass.py
file: null
transcribed_from: null
topics:
  - bed-state/diver-surveys
  - bed-state/community
regions:
  - scb
  - scb.islands.santa-cruz
beds: []
sites: []
references: []
human_task: null
---
