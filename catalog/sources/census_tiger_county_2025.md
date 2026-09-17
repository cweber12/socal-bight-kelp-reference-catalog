---
id: census_tiger_county_2025
title: TIGER/Line Shapefile, Current, Nation, U.S., County and Equivalent Entities
steward: U.S. Department of Commerce, U.S. Census Bureau, Geography Division
url: https://www2.census.gov/geo/tiger/TIGER2025/COUNTY/tl_2025_us_county.zip
doi: null
status: VERIFIED
tier: FETCHED
access:
  - Open https://www2.census.gov/geo/tiger/TIGER2025/COUNTY/
  - Follow the one file listed there, tl_2025_us_county.zip, to
    https://www2.census.gov/geo/tiger/TIGER2025/COUNTY/tl_2025_us_county.zip
  - Download that file over HTTPS; no account, key or referrer is required
    (HTTP 200, Content-Type application/zip, 83989800 bytes, 2026-09-17)
  - The archive holds seven members, tl_2025_us_county.shp, .shx, .dbf, .prj, .cpg,
    .shp.iso.xml and .shp.ea.iso.xml; the metadata quoted in this record is in .shp.iso.xml,
    the field definitions in .shp.ea.iso.xml, the projection in .prj and the code page in .cpg
  - The 2025 technical documentation is
    https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2025/TGRSHP2025_TechDoc.pdf;
    its Appendix I-2 is the record layout of this file
format: >-
  "ZIP" (tl_2025_us_county.shp.iso.xml,
  distributionInfo/MD_Distribution/distributionFormat/MD_Format/name); the archive's members
  are the shapefile tl_2025_us_county.shp with .shx, .dbf, .prj and .cpg ("UTF-8") and the two
  ISO metadata files tl_2025_us_county.shp.iso.xml and tl_2025_us_county.shp.ea.iso.xml;
  reference system "North American Datum of 1983" ("NAD83"), "urn:ogc:def:crs:EPSG::4269"
  (the same file, referenceSystemInfo/MD_ReferenceSystem/referenceSystemIdentifier/RS_Identifier,
  its authority title, alternateTitle and code), and the .prj reads GCS_North_American_1983;
  served as Content-Type application/zip
license: >-
  "Access constraints: None" and "Use Constraints: The TIGER/Line Shapefile products are not
  copyrighted however TIGER/Line and Census TIGER are registered trademarks of the U.S. Census
  Bureau. These products are free to use in a product or publication, however acknowledgement
  must be given to the U.S. Census Bureau as the source. The boundary information in the
  TIGER/Line Shapefiles are for statistical data collection and tabulation purposes only; their
  depiction and designation for statistical purposes does not constitute a determination of
  jurisdictional authority or rights of ownership or entitlement and they are not legal land
  descriptions. Coordinates in the TIGER/Line shapefiles have six implied decimal places, but
  the positional accuracy of these coordinates is not as great as the six decimal places
  suggest." (tl_2025_us_county.shp.iso.xml inside the archive,
  identificationInfo/MD_DataIdentification/resourceConstraints/MD_LegalConstraints/otherConstraints,
  two CharacterString values, retrieved 2026-09-17)
variables:
  - "STATEFP: Current state Federal Information Processing Series (FIPS) code"
  - "COUNTYFP: Current county Federal Information Processing Series (FIPS) code"
  - "COUNTYNS: Current county GNIS code"
  - >-
    "GEOID: County identifier; a concatenation of Current state FIPS code and county FIPS code";
    "The GEOID attribute is a concatenation of the state FIPS code followed by the county FIPS
    code. No spaces are allowed between the two codes. The State FIPS code is taken from
    "National Standard Codes (ANSI INCITS 38-2009), Federal Information Processing Series (FIPS)
    - States". The county FIPS code is taken from "National Standard Codes (ANSI INCITS 31-2009),
    Federal Information Processing Series (FIPS) - Counties/County Equivalents"."
  - >-
    "GEOIDFQ: Fully qualified county identifier; a concatenation of census survey summary level
    information with the county identifier. The GEOIDFQ attribute is calculated to facilitate
    joining census spatial data to census survey summary files."
  - "NAME: Current county name"
  - "NAMELSAD: Current name and the translated legal/statistical area description for county"
  - "LSAD: Current legal/statistical area description code for county"
  - "CLASSFP: Current Federal Information Processing Series (FIPS) class code"
  - "MTFCC: MAF/TIGER feature class code"
  - "CSAFP: Current combined statistical area code"
  - "CBSAFP: Current metropolitan statistical area/micropolitan statistical area code"
  - "METDIVFP: Current metropolitan division code"
  - "FUNCSTAT: Current functional status"
  - "ALAND: Current land area"
  - "AWATER: Current water area"
  - "INTPTLAT: Current latitude of the internal point"
  - "INTPTLON: Current longitude of the internal point"
coverage: >-
  "The entire area of the United States, Puerto Rico, and the Island Areas is covered by
  counties or equivalent entities." and "The boundaries for counties and equivalent entities
  are mostly as of January 1, 2025, as reported through the Census Bureau's Boundary and
  Annexation Survey (BAS)."; bounding box westBoundLongitude -178.443593, eastBoundLongitude 146.154418,
  southBoundLatitude -14.601813, northBoundLatitude 71.439786; citation date 2025
  (publication), 2025-10 (creation, lastUpdate). In the copy retrieved 2026-09-17 the header of
  tl_2025_us_county.dbf gives 3235 records, and its rows with STATEFP 06 and NAME Santa Barbara,
  Ventura, Los Angeles, Orange or San Diego carry GEOID 06083, 06111, 06037, 06059 and 06073
  and NAMELSAD "Santa Barbara County", "Ventura County", "Los Angeles County", "Orange County"
  and "San Diego County"
coverage_stated_at: >-
  tl_2025_us_county.shp.iso.xml inside the archive states the two abstract sentences quoted
  (identificationInfo/MD_DataIdentification/abstract), the bounding box
  (identificationInfo/MD_DataIdentification/extent/EX_Extent/geographicElement/EX_GeographicBoundingBox)
  and the citation dates (identificationInfo/MD_DataIdentification/citation/CI_Citation/date);
  the record count is in the header of tl_2025_us_county.dbf and the five rows are in that table
retrieved: 2026-09-17
fetch_script: src/fetch/census_tiger_county_2025.py
file: null
transcribed_from: null
topics:
  - canopy
regions:
  - scb
beds: []
sites: []
references: []
human_task: null
---
