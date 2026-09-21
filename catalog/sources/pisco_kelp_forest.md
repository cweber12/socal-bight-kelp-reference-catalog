---
id: pisco_kelp_forest
title: PISCO Kelp Forest Community Surveys
steward: Partnership for Interdisciplinary Studies of Coastal Oceans (PISCO)
url: https://data.piscoweb.org/metacatui/view/doi:10.6085/AA/PISCO_kelpforest.1.11
doi: 10.6085/AA/PISCO_kelpforest.1.11
status: VERIFIED
tier: FETCHED
access:
  - >-
    The data paper at https://doi.org/10.1002/ecy.3630 states under "DATA AVAILABILITY STATEMENT":
    "Data are also available on the Metacat Data Catalog at
    https://doi.org/10.6085/AA/PISCO_kelpforest.1.6." That DOI answers HTTP 302 with
    https://data.piscoweb.org/metacatui/#view/doi:10.6085/AA/PISCO_kelpforest.1.6 as its Location.
    The paper's own DOI answers HTTP 302 with
    https://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecy.3630 as its Location, which answered
    HTTP 403 with a page titled "Just a moment..." under the User-Agent the fetch script sends; the
    statement was read in the copy of the article at
    https://repository.library.noaa.gov/view/noaa/53969/noaa_53969_DS1.pdf, which answered HTTP 200
    under the User-Agent "kelpcatalog/pisco_kelp_forest
    (+https://github.com/cweber12/socal-bight-kelp-reference-catalog)" and HTTP 403 under the one
    the fetch script sends (2026-09-20)
  - >-
    data.piscoweb.org is the PISCO member node of DataONE:
    https://cn.dataone.org/cn/v2/node/urn:node:PISCO states name "PISCO MN" and baseURL
    https://data.piscoweb.org/metacat/d1/mn, and restricts the create and update methods of its
    MNStorage service to the subject "CN=PISCO-data-managers,DC=dataone,DC=org". Its Solr index,
    https://data.piscoweb.org/metacat/d1/mn/v2/query/solr/?q=id:*PISCO_kelpforest*&fl=id,formatType,dateUploaded&rows=100&sort=dateUploaded+desc&wt=json,
    lists 55 objects whose identifier contains "PISCO_kelpforest", 11 of them of formatType
    METADATA: PISCO_kelpforest.metadata.1, then doi:10.6085/AA/PISCO_kelpforest.1.2 through
    doi:10.6085/AA/PISCO_kelpforest.1.11 (2026-09-20)
  - >-
    Revision 1.11 is the revision this record enters.
    https://data.piscoweb.org/metacat/d1/mn/v2/meta/ followed by the percent-encoded identifier
    doi:10.6085/AA/PISCO_kelpforest.1.11 states dateUploaded 2026-01-16T00:18:40.695+00:00, an
    obsoletes element naming doi:10.6085/AA/PISCO_kelpforest.1.10, no obsoletedBy element, and an
    accessPolicy in which an allow block gives subject "public" the permission "read"; the same
    request for doi:10.6085/AA/PISCO_kelpforest.1.12 answers HTTP 404, and that for
    doi:10.6085/AA/PISCO_kelpforest.1.6, the revision the paper names, states an obsoletedBy element
    naming doi:10.6085/AA/PISCO_kelpforest.1.7 (2026-09-20)
  - >-
    This record's landing page is
    https://data.piscoweb.org/metacatui/view/doi:10.6085/AA/PISCO_kelpforest.1.11, where
    https://doi.org/10.6085/AA/PISCO_kelpforest.1.11 sends a request: the DOI answers HTTP 302 with
    that URL as its Location. The page is served as an application shell: the HTML answers HTTP 200
    in 10,355 bytes and does not contain "kelp" in any letter case (2026-09-20)
  - >-
    The package's EML is served at
    https://data.piscoweb.org/metacat/d1/mn/v2/object/doi%3A10.6085%2FAA%2FPISCO_kelpforest.1.11,
    the member node's object endpoint followed by the identifier percent-encoded whole: HTTP 200
    with 174,063 bytes and Content-Disposition attachment; filename="PISCO_kelpforest.1.11.xml",
    whose root element declares packageId "doi:10.6085/AA/PISCO_kelpforest.1.11". The system
    metadata named above states size 174063 and checksum algorithm "SHA-256" with value
    a9ef07f2c09a6999e36fc375d50b5acf4a4b03a9a4d91feaa30dbd8cc91681b3, and the SHA-256 of the bytes
    served equals it (2026-09-20)
  - >-
    The EML lists eight entities, named under format, and distributes each at
    https://cn.dataone.org/cn/v2/resolve/ followed by its identifier,
    doi:10.6085/AA/PISCO_kelpforest_<name>.1.11 where <name> is swath, upc, sizefreq, fish, quad,
    taxon_table, site_table or methods.
    https://cn.dataone.org/cn/v2/resolve/doi:10.6085/AA/PISCO_kelpforest_methods.1.11 answers HTTP
    303 with
    https://data.piscoweb.org/metacat/d1/mn/v2/object/doi:10.6085%2FAA%2FPISCO_kelpforest_methods.1.11
    as its Location. This record holds all eight, each fetched from
    https://data.piscoweb.org/metacat/d1/mn/v2/object/ followed by the identifier percent-encoded
    whole, as in
    https://data.piscoweb.org/metacat/d1/mn/v2/object/doi%3A10.6085%2FAA%2FPISCO_kelpforest_methods.1.11.
    An anonymous GET answers HTTP 200 with Content-Disposition attachment;
    filename="PISCO_kelpforest_methods.1.11.pdf", Content-Type application/pdf, Transfer-Encoding
    chunked, and no Content-Length, Last-Modified or ETag; the seven CSV entities answer alike with
    Content-Type text/csv (2026-09-20)
  - >-
    Run src/fetch/pisco_kelp_forest.py, which sends the User-Agent "kelpcatalog/pisco_kelp_forest",
    stores each body under its Content-Disposition filename, and keeps it only when its SHA-256 and
    its length equal the checksum and size the member node's system metadata states for that
    identifier; no account, key or referrer is required. The eight files held are 130,791,944 bytes
    together. Each also has the MD5 the EML states for its entity, and each of the seven CSVs has
    the EML's attributeNames as its header line and the EML's numberOfRecords lines after it (HTTP
    200, 2026-09-20)
  - >-
    PISCO's own Data Access page, https://piscoweb.org/data-access, does not link data.piscoweb.org.
    It states "Partnerships with Oregon State University, Data Observation Network for Earth
    (DataONE), and the Pacific Rocky Intertidal Monitoring program at UC Santa Cruz help to provide
    access platforms." and "If you are interested in subtidal data please fill out the California
    Kelp Forest Data Request Form", linking
    https://docs.google.com/forms/d/e/1FAIpQLSct8vbkyM3l36GjQ0Uq6E50oeCQWlW7682DYecXnTfxpmzlUQ/viewform;
    the EML's abstract names the same form: "Please use this form as an initial method of contact:"
    followed by that URL (2026-09-20)
format: >-
  The EML lists seven dataTable entities and one otherEntity: "PISCO kelp  forest swath data",
  objectName PISCO_kelpforest_swath.1.11.csv, size 33316050, numberOfRecords 285808; "PISCO kelp
  forest upc data", objectName PISCO_kelpforest_upc.1.11.csv, size 20101670, numberOfRecords 198668;
  "PISCO kelp forest size frequency data", objectName PISCO_kelpforest_sizefreq.1.11.csv, size
  2616775, numberOfRecords 19140; "PISCO kelp forest fish data", objectName
  PISCO_kelpforest_fish.1.11.csv, size 68403795, numberOfRecords 446881; "PISCO kelp forest quadrat
  data", objectName PISCO_kelpforest_quad.1.11.csv, size 4954171, numberOfRecords 44561; "PISCO
  taxonomic lookup table", objectName PISCO_kelpforest_taxon_table.1.11.csv, size 201464,
  numberOfRecords 693; "PISCO kelp forest site lookup table", objectName
  PISCO_kelpforest_site_table.1.11.csv, size 1092929, numberOfRecords 10405; and the otherEntity
  "PISCO kelp forest methods description", objectName PISCO_kelpforest_methods.1.11.pdf, size
  105090, entityType "PDF" and formatName "Adobe Portable Document Format". Each physical states its
  size with unit "bytes" and an authentication of method "MD5". Each of the seven dataTables states
  a textFormat of numHeaderLines 1, recordDelimiter "\r\n", attributeOrientation "column",
  fieldDelimiter "," and quoteCharacter '"'. The variables below are the union of the seven tables'
  attributeNames, in the EML's order. No table carries all of them, and 17 of the 76 names occur in
  more than one table: size states the unit "number" in PISCO_kelpforest_swath.1.11.csv and
  "centimeter" in PISCO_kelpforest_sizefreq.1.11.csv. The one missingValueCode the EML states is
  "NA", "not available", on 49 of the 145 attributes of the seven tables. The member node's system
  metadata states formatId "text/csv" for the seven tables and "application/pdf" for the methods
  description, and for each of the eight a size equal to the EML's and a checksum of algorithm
  "SHA-256" (2026-09-20)
license: >-
  "This information is released under the Creative Commons license - Attribution - CC BY
  (https://creativecommons.org/licenses/by/4.0/). The consumer of these data ('Data User' herein) is
  required to cite it appropriately in any publication that results from its use. The Data User
  should realize that these data may be actively used by others for ongoing research and that
  coordination may be necessary to prevent duplicate publication. The Data User is urged to contact
  the authors of these data if any questions about methodology or results occur. Where appropriate,
  the Data User is encouraged to consider collaboration or co-authorship with the authors. The Data
  User should realize that misinterpretation of data may occur if used out of context of the
  original study. While substantial efforts are made to ensure the accuracy of data and associated
  documentation, complete accuracy of data sets cannot be guaranteed. All data are made available
  'as is'." and "The Data User should be aware, however, that data are updated periodically and it
  is the responsibility of the Data User to check for new versions of the data. The data authors and
  the repository where these data were obtained shall not be liable for damages resulting from any
  use or misinterpretation of the data. Thank you.", the two paragraphs of the dataset's
  intellectualRights element in the EML named in access (2026-09-20)
variables:
  - campus
  - method
  - survey_year
  - year
  - month
  - day
  - site
  - zone
  - transect
  - classcode
  - count
  - size
  - disease
  - observer
  - depth
  - notes
  - site_name_old
  - category
  - pct_cov
  - location
  - level
  - fish_tl
  - min_tl
  - max_tl
  - row_weight_g
  - sex
  - vis
  - temp
  - surge
  - pctcnpy
  - quad
  - sample_type
  - sample_subtype
  - Kingdom
  - Phylum
  - Class
  - Order
  - Family
  - Genus
  - Species
  - species_definition
  - taxonomic_source
  - taxonomic_id
  - common_name
  - size_cutoff
  - LOOKED1999
  - LOOKED2000
  - LOOKED2001
  - LOOKED2002
  - LOOKED2003
  - LOOKED2004
  - LOOKED2005
  - LOOKED2006
  - LOOKED2007
  - LOOKED2008
  - LOOKED2009
  - LOOKED2010
  - LOOKED2011
  - LOOKED2012
  - LOOKED2013
  - LOOKED2014
  - LOOKED2015
  - LOOKED2016
  - LOOKED2017
  - LOOKED2018
  - LOOKED2019
  - LOOKED2020
  - LOOKED2021
  - LOOKED2022
  - LOOKED2023
  - LOOKED2024
  - latitude
  - longitude
  - MPA_Name
  - mpa_type
  - site_status
coverage: >-
  The abstract states "In 1998, the Partnership for Interdisciplinary Studies of Coastal Oceans
  (PISCO) designed and initiated a large scale, long-term monitoring study of kelp forest ecosystems
  along portions of the southern, central and northern coast of California and southern Oregon,
  USA." The methods state "The geographic scope of the PISCO kelp forest monitoring program spans
  southern Oregon and north central, central, and southern California, encompassing three ecoregions
  distinguished by distinct oceanographic environments. The vast majority of surveys are conducted
  in central and southern California.", "Surveys are conducted annually, generally from June to late
  October." and "Quadrat surveys were done only at sites in southern California surveyed by UCSB.
  Quadrat sampling was discontinued after 2010." The dataset's coverage holds one
  geographicCoverage, geographicDescription "California and Oregon Coast" with boundingCoordinates
  west -125, east -118, north 45 and south 33. Its temporalCoverage runs from 1999-09-07 to
  2024-12-07; the year, month and day values of the five survey tables (swath, upc, sizefreq, fish,
  quad) run from 1999-09-07 to 2024-11-08 in the copy retrieved 2026-09-20
coverage_stated_at: >-
  The EML named in access,
  https://data.piscoweb.org/metacat/d1/mn/v2/object/doi%3A10.6085%2FAA%2FPISCO_kelpforest.1.11, and
  the held files: the dataset's abstract element states the sentence quoted; the description of its
  one methodStep states the five sentences quoted; the dataset's coverage element states the
  geographicDescription with its boundingCoordinates, and the temporalCoverage; and the data rows of
  PISCO_kelpforest_swath.1.11.csv, PISCO_kelpforest_upc.1.11.csv,
  PISCO_kelpforest_sizefreq.1.11.csv, PISCO_kelpforest_fish.1.11.csv and
  PISCO_kelpforest_quad.1.11.csv state the span of the copy (retrieved 2026-09-20)
retrieved: 2026-09-20
fetch_script: src/fetch/pisco_kelp_forest.py
file: null
transcribed_from: null
topics:
  - bed-state/diver-surveys
  - bed-state/community
  - grazers-predators-competitors/predators
regions:
  - scb
beds: []
sites: []
references: []
human_task: null
---
