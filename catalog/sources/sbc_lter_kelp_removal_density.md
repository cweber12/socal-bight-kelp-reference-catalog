---
id: sbc_lter_kelp_removal_density
title: >-
  SBC LTER: Reef: Long-term experiment: Kelp removal: Invertebrate and algal density
steward: Santa Barbara Coastal LTER
url: https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.34.22
doi: 10.6073/pasta/0c6c40d38f5143c7d56f61c455f7fe9b
status: VERIFIED
tier: FETCHED
access:
  - >-
    Open https://sbclter.msi.ucsb.edu/data/catalog/, the Santa Barbara Coastal LTER data catalog.
    Under the collection "SBC LTER: 15-year (2008-2023) long-term experiment of kelp removal (LTE
    KR)" it lists "LTE KR - Abundance of algae and invertebrates", linking to
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.34. The page's HTML
    carries a second link under the same label, to
    https://portal.edirepository.org/nis/mapbrowse?scope=knb-lter-sbc&identifier=34&revision=newest,
    inside an HTML comment (HTTP 200, 2026-09-20)
  - >-
    The steward's own package page,
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.34, is served as an
    application shell. The HTML answers HTTP 200 in 17,652 bytes and contains neither "removal" nor
    "density"; https://sbclter.msi.ucsb.edu/assets/js/package/main.js builds the page from
    `https://pasta.lternet.edu/package/metadata/eml/${ package.replace(/\./g, "/") }/newest`
    (2026-09-20)
  - >-
    This record's landing page is
    https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.34.22, where
    https://doi.org/10.6073/pasta/0c6c40d38f5143c7d56f61c455f7fe9b sends a request: the DOI answers
    HTTP 302 with that URL as its Location. A request to the landing page under the User-Agent
    "kelpcatalog/knb-lter-sbc.34" timed out on connect from this address, and the page's content was
    not read (2026-09-20)
  - >-
    The PASTA service methods answer HTTP 403 with a text/plain body that begins "User
    'EDI-078e6e3cee4f7f2812f150701da9351acb51e089 (Public Access)' is not authorized to execute
    service method '<method>'.": readMetadata at
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/34/22, readDataEntity at
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/34/22/aed8b4a5569f6a82577d6fb7327452b9,
    listDataPackageRevisions at https://pasta.lternet.edu/package/eml/knb-lter-sbc/34, and
    listDataPackageScopes at https://pasta.lternet.edu/package/eml, each asked under the User-Agent
    "kelpcatalog/knb-lter-sbc.34" (2026-09-20)
  - >-
    The package's EML was read from the DataONE copy of the same object. GET
    https://cn.dataone.org/cn/v2/object/ followed by the percent-encoded identifier
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/34/22 answered HTTP 200 with 46,223
    bytes whose root element declares packageId "knb-lter-sbc.34.22" and system
    "https://pasta.edirepository.org". The system metadata for that identifier,
    https://cn.dataone.org/cn/v2/meta/ plus the same percent-encoded identifier, states checksum
    algorithm "SHA-1" and value b2204c5a952bb6374f6f46414036c383043d9b9d, formatId
    "https://eml.ecoinformatics.org/eml-2.2.0" and originMemberNode "urn:node:LTER"; the SHA-1 of
    the 46,223 bytes served equals that value. That system metadata states an accessPolicy in which
    an allow block gives subject "public" the permission "read", and an obsoletes element naming
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/34/21; it carries no obsoletedBy
    element (2026-09-20)
  - >-
    Revision 22 is the revision this record enters.
    https://cite.edirepository.org/cite/knb-lter-sbc.34.22?style=RAW answers HTTP 200 and states
    'version': '22', 'pubdate': '2024-11-18', 'doi':
    'doi:10.6073/pasta/0c6c40d38f5143c7d56f61c455f7fe9b', 'publisher': 'Environmental Data
    Initiative' and authors Reed, Daniel C; Miller, Robert J. Asked for each of knb-lter-sbc.34.23
    through knb-lter-sbc.34.32 in turn, the same service answers HTTP 400, and
    https://cn.dataone.org/cn/v2/meta/ answers HTTP 404 for the percent-encoded identifiers
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/34/23 and
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/34/24. Asked for knb-lter-sbc.34.19,
    the cite service answers HTTP 200 and states 'version': '19', 'pubdate': '2022-05-22' and 'doi':
    'doi:10.6073/pasta/decb1dcc7b35d2ef401b2dd7d79ea257';
    https://doi.org/10.6073/pasta/decb1dcc7b35d2ef401b2dd7d79ea257 answers HTTP 302 with
    https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.34.19 as its Location, and
    the DataONE system metadata for
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/34/19 carries an obsoletedBy element
    naming https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/34/20, and that for revision
    20 one naming revision 21. The system metadata for revision 21 carries no obsoletedBy element,
    and that for revision 22 names revision 21 in its obsoletes element, as the step above states
    (2026-09-20)
  - >-
    The data entity is served by the DataONE member node EDI replicates to, at
    https://gmn.lternet.edu/mn/v2/object/ followed by the entity's PASTA identifier percent-encoded
    whole:
    https://gmn.lternet.edu/mn/v2/object/https%3A%2F%2Fpasta.lternet.edu%2Fpackage%2Fdata%2Feml%2Fknb-lter-sbc%2F34%2F22%2Faed8b4a5569f6a82577d6fb7327452b9.
    An anonymous GET under the User-Agent "kelpcatalog/knb-lter-sbc.34" answers HTTP 200 with
    Content-Length 79623824, Content-Disposition attachment;
    filename="LTE_Quad_Swath_All_Years_20241115.csv", Content-Type application/octet-stream,
    Last-Modified Tue, 19 Nov 2024 00:45:44 GMT, DataONE-Checksum
    "SHA-1,bc3a658f924d25b7ce921cf375a2bafd79b46bdb", DataONE-Proxy
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/34/22/aed8b4a5569f6a82577d6fb7327452b9
    and no ETag. A GET on https://cn.dataone.org/cn/v2/resolve/ followed by the same identifier is
    served from gmn.lternet.edu with the same Content-Length, Content-Disposition, DataONE-Checksum
    and DataONE-Proxy (2026-09-20)
  - >-
    Run src/fetch/sbc_lter_kelp_removal_density.py, which sends the User-Agent
    "kelpcatalog/knb-lter-sbc.34", stores the body under the Content-Disposition filename, and keeps
    it only when its SHA-1 and its length equal the checksum and size the DataONE system metadata
    states for the entity's identifier, given under format; no account, key or referrer is required.
    The 79623824 bytes held also have the MD5 the EML states for the entity, and 422932 lines after
    the header line, the EML's numberOfRecords (HTTP 200, 2026-09-20)
format: >-
  The EML lists one dataTable, entityName "LTE Benthic inverts and understory algae, all years" and
  entityDescription "Abundance and size of selected species of benthic invertebrates and understory
  algae in fixed plots along permanent transects in kelp removal experiment", whose physical states
  objectName "LTE_Quad_Swath_All_Years_20241115.csv", size 79623824 with unit "byte", an
  authentication of method "MD5" whose value is 0f2d0ea37d0e4c0cc842f683d592d33c, and a textFormat
  of numHeaderLines 1, recordDelimiter "\r\n", attributeOrientation "column", fieldDelimiter ",",
  collapseDelimiters "no" and quoteCharacter '"', distributed at
  https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/34/22/aed8b4a5569f6a82577d6fb7327452b9;
  the dataTable states numberOfRecords 422932. The attributes SP_CODE, SIZE, COUNT and AREA each
  state the missingValueCode -99999, "no measurement collected at this point, or not available", and
  SCIENTIFIC_NAME states -99999, "value not recorded or not available". The DataONE system metadata
  for the entity's identifier states size 79623824, checksum algorithm "SHA-1" with value
  bc3a658f924d25b7ce921cf375a2bafd79b46bdb, and formatId "text/csv"; the member node serves it as
  Content-Type application/octet-stream (2026-09-20)
license: >-
  "This data package is released under the Creative Commons License Attribution 4.0 International
  (CC BY 4.0, see https://creativecommons.org/licenses/by/4.0/). This license states that consumers
  ("Data Users" herein) may distribute, adapt, reuse, remix, and build upon this work, as long as
  they give appropriate credit, provide a link to the license, and indicate if changes were made. If
  redistributed, a Data User may not apply additional restrictions or technological measures that
  prevent access. The Data User has an ethical obligation to cite the data source appropriately in
  any publication or product that results from its use, and notify the data contact or creator.
  Communication, collaboration, or co-authorship (as appropriate) with the creators of this data
  package is encouraged to prevent duplicate research or publication. The Data User is urged to
  contact the authors of these data if any questions about methodology or results occur. The Data
  User should realize that these data may be actively used by others for ongoing research and that
  coordination may be necessary to prevent duplication or inappropriate use. The Data User should
  realize that misinterpretation may occur if data are used outside of the context of the original
  study. The Data User should be aware that data are updated periodically and it is the
  responsibility of the Data User to check for new versions of the data. While substantial efforts
  are made to ensure the accuracy of data and associated documentation, complete accuracy of data
  sets cannot be guaranteed. This data package (with its components) is made available “as is” and
  with no warranty of accuracy or fitness for use. The creators of this data package and the
  repository where these data were obtained shall not be liable for any damages resulting from
  misinterpretation, use or misuse of the data package or its components.", the dataset's
  intellectualRights element in the EML named in access (2026-09-20)
variables:
  - YEAR
  - MONTH
  - DATE
  - SITE
  - TRANSECT
  - TREATMENT
  - QUAD
  - SIDE
  - SP_CODE
  - SIZE
  - COUNT
  - AREA
  - SCIENTIFIC_NAME
  - COMMON_NAME
  - TAXON_KINGDOM
  - TAXON_PHYLUM
  - TAXON_CLASS
  - TAXON_ORDER
  - TAXON_FAMILY
  - TAXON_GENUS
  - GROUP
  - SURVEY
  - MOBILITY
  - GROWTH_MORPH
coverage: >-
  The abstract states "These data describe the abundance of common reef associated species of macro
  invertebrates and macroalgae within permanent plots of a long-term experiment designed to examine
  trajectories of change in the structure and productivity of kelp forest communities in response to
  changes in the frequency and severity of disturbance to giant kelp. The number of individuals of
  approximately 50 taxa were recorded by divers along 40 m transects within each plot. Small species
  of macroalgae and macinvertebrates were counted within six permanent 1 m2 quadrats positioned
  uniformly along the 40 m transect, while larger species were counted within four contiguous 20 m2
  sub-sections of each 40 m x 2 m transect. Also included at the quadrat scale are estimates of an
  average size-related measurement of each species, which was developed specifically for each
  species for the purpose of estimating its biomass. The experiment was initiated in 2008 at five
  reef sites along the mainland coast of the Santa Barbara Channel and included an annual kelp
  removal treatment designed to simulate increases in the frequency and severity of winter wave
  disturbance and a continual kelp removal treatment that allowed the effects of giant kelp on the
  community to be evaluated. The last experimental removals of giant kelp occurred in winter 2016 or
  winter 2017, depending on the site. Data collection continued in all plots until spring 2023 to
  document the recovery trajectory of the reef fish community following the cessation of
  experimental kelp removal." The methods state "The kelp removal was terminated in 2016 and 2017.
  The vegetation survey is still ongoing to monitor the kelp recovery in the post-treatment
  condition." The dataset's coverage holds five geographicCoverage elements, each giving one point
  as its boundingCoordinates, west equal to east and north equal to south: "AQUE: Arroyo Quemado
  Reef: Arroyo Quemado Reef depth range from 5.4 m to 10.7 m. Reference on Land is close to
  US101/Arroyo Quemada Ln." at -120.11905, 34.46774988; "CARP: Carpinteria Reef is located on the
  Santa Barbara Channel offshore of the Carpinteria Salt Marsh. Depth range is from -2.2 to -8.8
  meters" at -119.5416933, 34.3916319; "MOHK: Mohawk Reef: Mohawk Reef depth ranges from 4.5m to 6.0
  m. Reference on land is Mohawk Rd / Edgewater Way." at -119.72957, 34.3940708; "NAPL: Naples Reef
  is located on the Santa Barbara Channel near the community of Naples and Dos Pueblos Canyon, Santa
  Barbara County, CA. Depth ranges from -5.9 to -13.4 meters." at -119.95154, 34.4221216; and "IVEE:
  Isla Vista (IV) Reef is located on the Santa Barbara Channel near the University of California
  Santa Barbara, CA. Depth range is from -8.2 to -8.8 meters." at -119.85755, 34.402783. Its
  temporalCoverage runs from 2008-01-10 to 2023-05-23; the DATE values of the file run from
  2008-01-10 to 2023-05-23 in the copy retrieved 2026-09-20
coverage_stated_at: >-
  The EML named in access, https://cn.dataone.org/cn/v2/object/ plus the percent-encoded identifier
  https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/34/22, and the held file: the
  dataset's abstract element states the paragraph quoted; the dataset's methods element states the
  two sentences quoted; the dataset's coverage element states the five geographicDescriptions with
  their boundingCoordinates, and the temporalCoverage; and the data rows of
  LTE_Quad_Swath_All_Years_20241115.csv state the span of the copy (retrieved 2026-09-20)
retrieved: 2026-09-20
fetch_script: src/fetch/sbc_lter_kelp_removal_density.py
file: null
transcribed_from: null
topics:
  - bed-state/community
regions:
  - scb.mainland.santa-barbara
beds: []
sites: []
references: []
human_task: null
---
