---
id: sbc_lter_kelp_removal_cover
title: >-
  SBC LTER: Reef: Long-term experiment: Kelp removal: Cover of sessile organisms, Uniform Point
  Contact
steward: Santa Barbara Coastal LTER
url: https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.28.33
doi: 10.6073/pasta/c30a92d17bf0f4245baea0a7bbe1036f
status: VERIFIED
tier: FETCHED
access:
  - >-
    Open https://sbclter.msi.ucsb.edu/data/catalog/, the Santa Barbara Coastal LTER data catalog.
    Under the collection "SBC LTER: 15-year (2008-2023) long-term experiment of kelp removal (LTE
    KR)" it lists "LTE KR - Percent cover of algae and invertebrates", linking to
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.28. The page's HTML
    carries a second link under the same label, to
    https://portal.edirepository.org/nis/mapbrowse?scope=knb-lter-sbc&identifier=28&revision=newest,
    inside an HTML comment (HTTP 200, 2026-09-20)
  - >-
    The steward's own package page,
    https://sbclter.msi.ucsb.edu/data/catalog/package/?package=knb-lter-sbc.28, is served as an
    application shell. The HTML answers HTTP 200 in 17,652 bytes and contains neither "removal" nor
    "sessile"; https://sbclter.msi.ucsb.edu/assets/js/package/main.js builds the page from
    `https://pasta.lternet.edu/package/metadata/eml/${ package.replace(/\./g, "/") }/newest`
    (2026-09-20)
  - >-
    This record's landing page is
    https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.28.33, where
    https://doi.org/10.6073/pasta/c30a92d17bf0f4245baea0a7bbe1036f sends a request: the DOI answers
    HTTP 302 with that URL as its Location. A request to the landing page under the User-Agent
    "kelpcatalog/knb-lter-sbc.28" timed out on connect from this address, and the page's content was
    not read (2026-09-20)
  - >-
    The PASTA service methods answer HTTP 403 with a text/plain body that begins "User
    'EDI-078e6e3cee4f7f2812f150701da9351acb51e089 (Public Access)' is not authorized to execute
    service method '<method>'.": readMetadata at
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/28/33, readDataEntity at
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/28/33/ef952a9e3e5a4006207eedc30367f224,
    listDataPackageRevisions at https://pasta.lternet.edu/package/eml/knb-lter-sbc/28, and
    listDataPackageScopes at https://pasta.lternet.edu/package/eml, each asked under the User-Agent
    "kelpcatalog/knb-lter-sbc.28" (2026-09-20)
  - >-
    The package's EML was read from the DataONE copy of the same object. GET
    https://cn.dataone.org/cn/v2/object/ followed by the percent-encoded identifier
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/28/33 answered HTTP 200 with 44,993
    bytes whose root element declares packageId "knb-lter-sbc.28.33" and system
    "https://pasta.edirepository.org". The system metadata for that identifier,
    https://cn.dataone.org/cn/v2/meta/ plus the same percent-encoded identifier, states checksum
    algorithm "SHA-1" and value 3f17081c57713a09794d49c0c393db60ec3353b1, formatId
    "https://eml.ecoinformatics.org/eml-2.2.0" and originMemberNode "urn:node:LTER"; the SHA-1 of
    the 44,993 bytes served equals that value. That system metadata states an accessPolicy in which
    an allow block gives subject "public" the permission "read", and an obsoletes element naming
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/28/32; it carries no obsoletedBy
    element (2026-09-20)
  - >-
    Revision 33 is the revision this record enters.
    https://cite.edirepository.org/cite/knb-lter-sbc.28.33?style=RAW answers HTTP 200 and states
    'version': '33', 'pubdate': '2024-05-07', 'doi':
    'doi:10.6073/pasta/c30a92d17bf0f4245baea0a7bbe1036f', 'publisher': 'Environmental Data
    Initiative' and authors Reed, Daniel C; Miller, Robert J. Asked for each of knb-lter-sbc.28.34
    through knb-lter-sbc.28.37 in turn, the same service answers HTTP 400. Asked for
    knb-lter-sbc.28.30, it answers HTTP 200 and states 'version': '30', 'pubdate': '2022-05-22' and
    'doi': 'doi:10.6073/pasta/1151c1dcf5110432b6d35f7dc00bb834';
    https://doi.org/10.6073/pasta/1151c1dcf5110432b6d35f7dc00bb834 answers HTTP 302 with
    https://portal.edirepository.org/nis/mapbrowse?packageid=knb-lter-sbc.28.30 as its Location, and
    the DataONE system metadata for
    https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/28/30 carries an obsoletedBy element
    naming https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/28/31, that for revision 31
    one naming revision 32, and that for revision 32 one naming revision 33 (2026-09-20)
  - >-
    The data entity is served by the DataONE member node EDI replicates to, at
    https://gmn.lternet.edu/mn/v2/object/ followed by the entity's PASTA identifier percent-encoded
    whole:
    https://gmn.lternet.edu/mn/v2/object/https%3A%2F%2Fpasta.lternet.edu%2Fpackage%2Fdata%2Feml%2Fknb-lter-sbc%2F28%2F33%2Fef952a9e3e5a4006207eedc30367f224.
    An anonymous GET under the User-Agent "kelpcatalog/knb-lter-sbc.28" answers HTTP 200 with
    Content-Length 107784745, Content-Disposition attachment;
    filename="LTE_Cover_All_Years_20240501.csv", Content-Type application/octet-stream,
    Last-Modified Tue, 07 May 2024 18:46:34 GMT, DataONE-Checksum
    "SHA-1,7d274b95564351726ae4707b230e8b46dd1f78cb", DataONE-Proxy
    https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/28/33/ef952a9e3e5a4006207eedc30367f224
    and no ETag. A GET on https://cn.dataone.org/cn/v2/resolve/ followed by the same identifier is
    served from gmn.lternet.edu with the same Content-Length, Content-Disposition, DataONE-Checksum
    and DataONE-Proxy (2026-09-20)
  - >-
    Run src/fetch/sbc_lter_kelp_removal_cover.py, which sends the User-Agent
    "kelpcatalog/knb-lter-sbc.28", stores the body under the Content-Disposition filename, and keeps
    it only when its SHA-1 and its length equal the checksum and size the DataONE system metadata
    states for the entity's identifier, given under format; no account, key or referrer is required.
    The 107784745 bytes held also have the MD5 the EML states for the entity, and 508518 lines after
    the header line, the EML's numberOfRecords (HTTP 200, 2026-09-20)
format: >-
  The EML lists one dataTable, entityName "LTE Benthic cover, all years" and entityDescription
  "cover of algae and sessile invertebrate in kelp removal experiment", whose physical states
  objectName "LTE_Cover_All_Years_20240501.csv", size 107784745 with unit "byte", an authentication
  of method "MD5" whose value is 8c0c55049f5d6fce8559832f242f147e, and a textFormat of
  numHeaderLines 1, recordDelimiter "\r\n", attributeOrientation "column", fieldDelimiter ",",
  collapseDelimiters "no" and quoteCharacter '"', distributed at
  https://pasta.lternet.edu/package/data/eml/knb-lter-sbc/28/33/ef952a9e3e5a4006207eedc30367f224;
  the dataTable states numberOfRecords 508518. The attributes SP_CODE and PERCENT_COVER each state
  the missingValueCode -99999, "no information available", and SCIENTIFIC_NAME states -99999, "value
  not recorded or not available". The DataONE system metadata for the entity's identifier states
  size 107784745, checksum algorithm "SHA-1" with value 7d274b95564351726ae4707b230e8b46dd1f78cb,
  and formatId "text/csv"; the member node serves it as Content-Type application/octet-stream
  (2026-09-20)
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
  - PERCENT_COVER
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
  The abstract states "These data describe the percent cover of sessile invertebrates and understory
  macroalgae within permanent plots of a long-term experiment designed to examine trajectories of
  change in the structure and productivity of kelp forest communities in response to changes in the
  frequency and severity of disturbance to giant kelp. Percent cover was determined using a uniform
  point contact method that consists of noting the identity and relative vertical position of all
  organisms under 80 uniformly placed points located within a 1 m wide band centered on permanent 40
  m transects in each sampling plot. Each species may only be recorded once per point. Using this
  method, the percent cover of all species combined may exceed 100%, however, the maximum percent
  cover possible for any single species cannot exceed 100%. The experiment was initiated in 2008 at
  five reef sites along the mainland coast of the Santa Barbara Channel and included an annual kelp
  removal treatment designed to simulate increases in the frequency and severity of winter wave
  disturbance and a continual kelp removal treatment that allowed the effects of giant kelp on the
  community to be evaluated. The last experimental removals of giant kelp occurred in winter 2016 or
  winter 2017, depending on the site. Data collection continued in all plots until spring 2023 to
  document the recovery trajectory of the reef fish community following the cessation of
  experimental kelp removal." The dataset's coverage holds five geographicCoverage elements, each
  giving one point as its boundingCoordinates, west equal to east and north equal to south: "AQUE:
  Arroyo Quemado Reef: Arroyo Quemado Reef depth range from 5.4 m to 10.7 m. Reference on Land is
  close to US101/Arroyo Quemada Ln." at -120.11905, 34.46774988; "CARP: Carpinteria Reef is located
  on the Santa Barbara Channel offshore of the Carpinteria Salt Marsh. Depth range is from -2.2 to
  -8.8 meters" at -119.5416933, 34.3916319; "MOHK: Mohawk Reef: Mohawk Reef depth ranges from 4.5m
  to 6.0 m. Reference on land is Mohawk Rd / Edgewater Way." at -119.72957, 34.3940708; "NAPL:
  Naples Reef is located on the Santa Barbara Channel near the community of Naples and Dos Pueblos
  Canyon, Santa Barbara County, CA. Depth ranges from -5.9 to -13.4 meters." at -119.95154,
  34.4221216; and "IVEE: Isla Vista (IV) Reef is located on the Santa Barbara Channel near the
  University of California Santa Barbara, CA. Depth range is from -8.2 to -8.8 meters." at
  -119.85755, 34.402783. Its temporalCoverage runs from 2008-01-01 to 2023-05-23; the DATE values of
  the file run from 2008-01-10 to 2023-05-23 in the copy retrieved 2026-09-20
coverage_stated_at: >-
  The EML named in access, https://cn.dataone.org/cn/v2/object/ plus the percent-encoded identifier
  https://pasta.lternet.edu/package/metadata/eml/knb-lter-sbc/28/33, and the held file: the
  dataset's abstract element states the paragraph quoted; the dataset's coverage element states the
  five geographicDescriptions with their boundingCoordinates, and the temporalCoverage; and the data
  rows of LTE_Cover_All_Years_20240501.csv state the span of the copy (retrieved 2026-09-20)
retrieved: 2026-09-20
fetch_script: src/fetch/sbc_lter_kelp_removal_cover.py
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
