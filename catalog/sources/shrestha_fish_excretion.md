---
id: shrestha_fish_excretion
title: Marine Protection and Environmental Forcing Influence Fish-Derived Nutrient Cycling in Kelp Forests
steward: San Jose State University; University of California, Santa Barbara
url: https://datadryad.org/dataset/doi:10.5061/dryad.k6djh9wgj
doi: 10.5061/dryad.k6djh9wgj
citations:
  - as_printed: >-
      Shrestha, June; Peters, Joey; Caselle, Jennifer; Hamilton, Scott (2024). Marine Protection
      and Environmental Forcing Influence Fish-Derived Nutrient Cycling in Kelp Forests [Dataset].
      Dryad. https://doi.org/10.5061/dryad.k6djh9wgj
    stated_at: >-
      https://datadryad.org/dataset/doi:10.5061/dryad.k6djh9wgj, under the heading "Citation": in
      the HTML that page sends it is the content of the element <p id="dataset-citation" hidden>,
      which the heading's button shows, the DOI there being the text of a link to the same URL
      (2026-09-27)
status: VERIFIED
tier: FETCHED
access:
  - >-
    https://doi.org/10.5061/dryad.k6djh9wgj answers HTTP 302 with
    https://datadryad.org/dataset/doi:10.5061/dryad.k6djh9wgj as its Location, and that page, this
    record's landing page, answers HTTP 200 with 53,110 bytes of Content-Type "text/html;
    charset=utf-8". Its HTML loads a script from
    https://16077a4ae659.us-west-2.captcha-sdk.awswaf.com/16077a4ae659/jsapi.js and holds a <div
    id="captcha-div">, and the same response carries the text quoted here. It is headed with the
    title; names four authors, "Shrestha, June", "Peters, Joey", "Caselle, Jennifer" and "Hamilton,
    Scott", marked 1, 2, 2 and 1 against a list headed "Affiliations" under "Author information"
    that reads "San Jose State University" (1) and "University of California, Santa Barbara" (2);
    states "Research facility: Moss Landing Marine Laboratories" and "Published Nov 12, 2024 on
    Dryad"; and prints the citation entered under citations (2026-09-27)
  - >-
    README.md in the held zip, which the landing page also renders, is headed with the DOI
    https://doi.org/10.5061/dryad.k6djh9wgj, and under "## Access information" states "Other
    publicly accessible locations of the data:" followed directly by "Data was derived from the
    following sources:", naming no other location. The API's dataset response named below lists
    under relatedWorks, with relationship "primary_article", the identifier
    https://doi.org/10.1111/1365-2435.14708. That DOI answers HTTP 302 with
    https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2435.14708 as its Location, which
    answered HTTP 403 with a page titled "Just a moment..." under the User-Agent the fetch script
    sends. Crossref's record of the article, https://api.crossref.org/works/10.1111/1365-2435.14708,
    answers HTTP 200 and lists among its 74 references one whose unstructured text is "Shrestha J.
    Peters J. Caselle J. &Hamilton S.(2024).Marine protection and environmental forcing influence
    fish‐derived nutrient cycling in kelp forests [Dataset].Dryad.https://doi.org/10.5061/dryad.k6djh9wgj"
    (2026-09-27)
  - >-
    Dryad's API describes the deposit without an account.
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.k6djh9wgj answers HTTP 200 and
    states identifier "doi:10.5061/dryad.k6djh9wgj", storageSize 56236467, versionNumber 5,
    curationStatus "Published", publicationDate "2024-11-12", lastModificationDate "2024-11-13" and
    visibility "public". Its versions link,
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.k6djh9wgj/versions, states total 1
    and lists the version https://datadryad.org/api/v2/versions/328111, whose files link,
    https://datadryad.org/api/v2/versions/328111/files, states total 4 and lists the four files
    named under format (2026-09-27)
  - >-
    The landing page's "Data files" section, headed "Nov 12, 2024 version files", lists README.md,
    Shrestha_fish_excr_data_Channel_Islands_all.csv,
    Shrestha_fish_excr_data_Channel_Islands_longterm_sites.csv and
    Shrestha_Fish_length-weight_conversion_table.csv over the line "Click names to download
    individual files", and the JSON-LD in its HTML gives their contentUrl as
    http://datadryad.org/downloads/file_stream/ followed by 3627768, 3627769, 3627770 and 3627774.
    Requested over https://, each of the four answered HTTP 403 under the User-Agent the fetch
    script sends, and https://datadryad.org/robots.txt states "Disallow: /downloads" under
    "User-agent: *" (2026-09-27)
  - >-
    The API gives a download link to each file, to the dataset and to the version. Without a token
    https://datadryad.org/api/v2/files/3627768/download,
    https://datadryad.org/api/v2/files/3627770/download,
    https://datadryad.org/api/v2/files/3627774/download and
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.k6djh9wgj/download each answered
    HTTP 401 with the body {"error":"Unauthorized, must have current bearer token"}. The version's
    link, https://datadryad.org/api/v2/versions/328111/download, answered without one: HTTP 302 with
    a signed URL under lambda-url.us-west-2.on.aws as its Location, which answered HTTP 200 with
    Content-Type application/zip, Content-Disposition
    attachment;filename="doi_10_5061_dryad_k6djh9wgj__v20241112.zip", Transfer-Encoding chunked,
    and no Content-Length, Last-Modified or ETag (2026-09-27)
  - >-
    Run src/fetch/shrestha_fish_excretion.py, which sends the User-Agent
    "kelpcatalog/shrestha_fish_excretion", requests
    https://datadryad.org/api/v2/versions/328111/download, stores the body under its
    Content-Disposition filename, and keeps it only when the zip holds the four members the files
    listing names and no other, each with the size and the SHA-256 that listing states; no account,
    key or referrer is required. The zip held is 56,245,597 bytes. The zip is assembled on request:
    an earlier request that day was also served 56,245,597 bytes, with a different SHA-256, and in
    each of the two zips every member's modification time was the minute of its own request and
    every member had the size and the SHA-256 the listing states (HTTP 200, 2026-09-27)
format: >-
  The files listing named in access states four files, each with status "created" and digestType
  "sha-256": path "README.md", size 5724, mimeType "text/markdown", digest
  1a8b02349d7e896475403dbe88d4e0c481076857a1fb180a2e9d27e7e30fee93; path
  "Shrestha_fish_excr_data_Channel_Islands_all.csv", size 31436612, mimeType "text/csv", digest
  9f3d85a8b15e7180cdc62e82f3eb33a794b33b1f8b73871c0a9a5d2e6393295d; path
  "Shrestha_fish_excr_data_Channel_Islands_longterm_sites.csv", size 24786155, mimeType "text/csv",
  digest 79b06da4cd9b348cd72692bf9ecd51f12c9abc53f35fb84e7cb8534a7174cbb2; and path
  "Shrestha_Fish_length-weight_conversion_table.csv", size 7976, mimeType "text/csv", digest
  1431e380bbad779149a733920a43a2d97a852e5de47bacc5305bc661f4c4efcb. This record holds the zip the
  version's download link serves, doi_10_5061_dryad_k6djh9wgj__v20241112.zip, whose four members are
  those files. In the copy retrieved 2026-09-27 each of the three CSVs decodes as UTF-8 behind a
  byte-order mark, ends its lines with CR LF, and is a comma-separated header line over data rows,
  none of them ragged: 139,277 rows of 32 fields in Shrestha_fish_excr_data_Channel_Islands_all.csv,
  111,946 of 32 in Shrestha_fish_excr_data_Channel_Islands_longterm_sites.csv and 53 of 17 in
  Shrestha_Fish_length-weight_conversion_table.csv. The two excretion files' header lines are
  byte-identical. README.md states one list headed "##### Variables" after the description of
  Shrestha_fish_excr_data_Channel_Islands_longterm_sites.csv, and none after that of
  Shrestha_fish_excr_data_Channel_Islands_all.csv, and a second after that of
  Shrestha_Fish_length-weight_conversion_table.csv; each item is a line beginning with an asterisk
  and a space, then a name, a space, a hyphen, a space and a description, the space after the hyphen
  being U+00A0 in some items, and two items, "Notes" and "MLPA_region", carry a name alone. The
  second list's 17 names are the conversion table's header line, in its order. The first list names
  30 columns and the excretion header line 32, and 22 of the list's names are spelled otherwise than
  the header line spells any column: this record reads "Year", "Month", "Day", "Site", "Side",
  "Zone", "Transect", "Classcode", "fish_tl.cm", "estimated.wt.g", "Count", "Transect area",
  "density.indiv.m.2", "Family", "Genus", "Species", "Notes", "MPA_Status", "Reserve",
  "MLPA_region", "Region" and "Subregion" as the columns the header line spells "year", "month",
  "day", "SITE", "SIDE", "zone", "transect", "classcode", "fish_tl..cm.", "estimated.wt..g.",
  "count", "transect area (m2)", "density.indiv.m.2.", "family", "genus", "species", "notes",
  "MPA_STATUS", "RESERVE", "MLPA_REGN", "REGION" and "SUBREGION", and the other eight as spelled
  alike, and so enters each column under the header line's spelling with the description README.md
  states for it. The header line's "SITE_SIDE" and "level.in.the.water.column" are named in no list
  and are entered with description null. A reading that took the list's spellings as the names would
  enter 22 names no held file's header line spells. README.md states no unit apart from the words of
  a description, as "Fish total length in cm" does, so every entry reads unit: null; "genus" and
  "species" are each two entries, as the two lists describe them differently. The two excretion
  files key their rows by SITE, which README.md describes as "Location of the survey"; their
  LAT_WGS84 and LON_WGS84 values differ between rows of one SITE value in the copy retrieved
  2026-09-27, so site_key names no coordinate columns
license: >-
  "Public domain", under the heading "License:" and linked to
  https://creativecommons.org/publicdomain/zero/1.0/ with the label "CC0 (opens in new window)", in
  the licence panel the landing page loads from
  https://datadryad.org/stash_datacite/licenses/details.js?resource_id=328111, which answers HTTP
  200 to a request carrying the header X-Requested-With: XMLHttpRequest and HTTP 422 to one without
  it. The landing page's own HTML states in its JSON-LD a license of name "Creative Commons Zero
  v1.0 Universal" and license "https://spdx.org/licenses/CC0-1.0.html", and the API's dataset
  response named in access states license "https://spdx.org/licenses/CC0-1.0.html" (2026-09-27)
license_stated_at: >-
  Looked for first in the held zip: README.md, the one member that is not a data file, contains none
  of "licen", "copyright", "CC0", "public domain", "creative commons" or "terms" in any letter case.
  Then on the landing page, https://datadryad.org/dataset/doi:10.5061/dryad.k6djh9wgj, whose licence
  panel is filled from
  https://datadryad.org/stash_datacite/licenses/details.js?resource_id=328111, the script its HTML
  names; the JSON-LD in the same HTML, and
  https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.k6djh9wgj, state the SPDX identifier
  (retrieved 2026-09-27)
variables:
  - name: "year"
    description: "Year of the survey"
    unit: null
  - name: "month"
    description: "Month of the survey"
    unit: null
  - name: "day"
    description: "day of the survey"
    unit: null
  - name: "SITE"
    description: "Location of the survey"
    unit: null
  - name: "SIDE"
    description: "Sites can be split into two or three areas to stratify the sampling. W = west, Cen = central, E = East"
    unit: null
  - name: "SITE_SIDE"
    description: null
    unit: null
  - name: "zone"
    description: "Location of the visual transects from the outer (deep) to inner (shallow) areas of each kelp bed / site. Outer - deepest (20 m), Outmid - next deepest (15 m), Inmid - next deepest (10 m), Inner - shallowest (5 m)"
    unit: null
  - name: "level.in.the.water.column"
    description: null
    unit: null
  - name: "transect"
    description: "ID number of each transect in a particular zone per side of a site"
    unit: null
  - name: "classcode"
    description: "Fish species ID code (first letter of genus and first three letters of the species name)"
    unit: null
  - name: "fish_tl..cm."
    description: "Fish total length in cm"
    unit: null
  - name: "estimated.wt..g."
    description: "Fish weight estimated from published Length-Weight relationships for each species"
    unit: null
  - name: "EXCR_IND"
    description: "Estimated ammonium excretion per individual per hour, using species-specific relationships between body size and excretion"
    unit: null
  - name: "count"
    description: "The number of fish per species per size class counted on that transect"
    unit: null
  - name: "transect area (m2)"
    description: "area of each fish transect is 60 m2 (30 x 2 m)"
    unit: null
  - name: "EXCR_M2"
    description: "Estimated ammonium excretion per fish of that body size and species observed on the transect per unit area (m2)"
    unit: null
  - name: "density.indiv.m.2."
    description: "The density of fish per m2 of rocky reef habitat"
    unit: null
  - name: "family"
    description: "Taxonomic family for that fish species"
    unit: null
  - name: "genus"
    description: "Taxonomic grouping at genus level"
    unit: null
  - name: "species"
    description: "Taxonomic grouping at species level"
    unit: null
  - name: "notes"
    description: null
    unit: null
  - name: "MPAGroup"
    description: "Name of the Marine Protected Area (if any) associated with that site"
    unit: null
  - name: "MPA_STATUS"
    description: "Whether the site is a reference area (open to fishing), SMR (state marine reserve and fully no-take), or SMCA (state marine conservation area that may allow take of some species)"
    unit: null
  - name: "RESERVE"
    description: "whether a site is IN or OUT of an MPA of any kind"
    unit: null
  - name: "MLPA_REGN"
    description: null
    unit: null
  - name: "REGION"
    description: "location in the greater Southern California Bight"
    unit: null
  - name: "SUBREGION"
    description: "Island where the site is located. ANA - Anacapa Island, SCI - Santa Cruz Island, SRI - Santa Rosa Island, SMI - San Miguel Island"
    unit: null
  - name: "LAT_WGS84"
    description: "Latitude"
    unit: null
  - name: "LON_WGS84"
    description: "Longitude"
    unit: null
  - name: "YEAR_MPA_Est."
    description: "Year the MPA was established. Values of zero reflect a non-MPA site"
    unit: null
  - name: "MPAAreaNM2"
    description: "MPA area in nautical miles squared"
    unit: null
  - name: "MPA_Shore_length_NM"
    description: "Length of shoreline in the MPA in nautical miles"
    unit: null
  - name: "pisco_classcode"
    description: "Currently used PISCO classcode, usually first letter of genus, first three letters of species with exceptions for overlapping codes and species groupings"
    unit: null
  - name: "genus"
    description: "Currently accepted genus"
    unit: null
  - name: "species"
    description: "Currently accepted species"
    unit: null
  - name: "common_name"
    description: "Common name"
    unit: null
  - name: "ScientificName_accepted"
    description: "Full WoRMS accepted scientific name"
    unit: null
  - name: "Family"
    description: "Taxonomic Family"
    unit: null
  - name: "WL_a"
    description: "Length to weight parameter a (Weight = a*Length^b)"
    unit: null
  - name: "WL_b"
    description: "Length to weight parameter b (Weight = a*Length^b)"
    unit: null
  - name: "WL_W_units"
    description: "Output weight units (g, kg)"
    unit: null
  - name: "WL_L_units"
    description: "Input length units (mm, cm)"
    unit: null
  - name: "WL_input_length"
    description: "Input length type (SL=standard length, FL=fork length, TL=total length)"
    unit: null
  - name: "WL_Reference_Notes"
    description: "Primary source for length-weight parameters, and additional notes (e.g. when a similar species was used). RecFIN refers to the Recreational Fisheries Information Network, which is the source for some conversion parameters."
    unit: null
  - name: "LC.a._for_WL"
    description: "Length conversion parameter a (note only needed when input length type is not total length)"
    unit: null
  - name: "LC.b._for_WL"
    description: "Length conversion parameter b (note only needed when input length type is not total length)"
    unit: null
  - name: "LC_type_for_WL"
    description: "Length conversion type (typical, reverse) (note only needed when input length type is not total length)"
    unit: null
  - name: "LL_Reference_Notes_for_WL"
    description: "Source for length-length conversion parameters"
    unit: null
  - name: "LL_Equation_for_WL"
    description: "Equation for length-length conversion"
    unit: null
coverage: >-
  The landing page's Abstract states "we combined empirically-measured relationships between
  excretion rate and body mass with data on fish density and size structure from visual SCUBA
  surveys conducted from 2005-2018 in the northern Channel Islands, California, USA." Its Methods
  state "The northern Channel Islands, California, USA, are located in the middle of a dynamic
  oceanographic boundary formed by the cold California Current to the west and the warmer Southern
  California Countercurrent to the east.", "The convergence and mixing of the currents result in
  substantial variation in productivity and the formation of strong thermal gradients from west to
  east that influence benthic community structure across four islands, covering a scale of
  approximately 100 km.", "Visual surveys of kelp forest assemblages conducted by the Partnership
  for Interdisciplinary Studies of Coastal Oceans (PISCO) during summer/fall were used to quantify
  fish abundance and biomass, in order to estimate nutrient excretion by the fish community.",
  "Sampling effort has changed over time, but included n=46 sites in the northern Channel Islands at
  the peak of effort, with sites inside and outside MPAs.", "At each site, PISCO divers conducted
  n=8 to 12 fish transects (30 m long × 2 m wide × 2 m high) at multiple levels in the water column:
  benthic, midwater, and canopy in depths from 0-20 m.", "Although PISCO surveys started in 1999, we
  included only the year 2005 onwards in order to encompass when the survey effort expanded to
  include sufficient sites for analysis over time.", and "We first evaluated spatial differences in
  the supply of ammonium by fishes among islands due to MPA protection, using data from n=33 sites
  (15 MPA and 18 non-MPA) surveyed for at least 3 years (all sites). We also explored spatial and
  temporal patterns in excretion using data from a subset of n=19 sites (10 MPA and 9 non-MPA)
  surveyed concurrently from 2005-2018 (long-term sites)." README.md describes
  Shrestha_fish_excr_data_Channel_Islands_all.csv as "Fish ammonium excretion estimates for sites at
  the Channel Islands, USA from 2003-2018. Includes data from 33 sites surveys for at least 3 years
  between 2003-2018." and Shrestha_fish_excr_data_Channel_Islands_longterm_sites.csv as "Fish
  ammonium excretion estimates for sites at the Channel Islands, USA from 2003-2018. Includes data
  from 19 sites surveyed from 2005-2018.", describes the column Subregion as "Island where the site
  is located. ANA - Anacapa Island, SCI - Santa Cruz Island, SRI - Santa Rosa Island, SMI - San
  Miguel Island", and states "Data was derived from the following sources:" over two entries, the
  first linking https://doi.org/10.1002/ecy.3630 and the second
  https://doi.org/10.1016/j.jembe.2023.151956. The landing page's JSON-LD states "spatialCoverage":
  [] and a "temporalCoverage" of "2024-08-14 21:14:01 UTC", "2024-08-14 21:14:09 UTC", "2024-11-12
  00:00:00 UTC" and "2024-11-12 00:00:00 UTC". In the copy retrieved 2026-09-27 the year, month and
  day values run from 2005-07-18 to 2018-10-16 in Shrestha_fish_excr_data_Channel_Islands_all.csv
  and from 2005-09-08 to 2018-10-16 in Shrestha_fish_excr_data_Channel_Islands_longterm_sites.csv;
  SUBREGION holds ANA, SCI, SRI and SMI in both files and also SBI in the first, on rows whose
  REGION is "Southern CI" and whose SITE begins "SBI_"
coverage_stated_at: >-
  The Abstract and Methods of https://datadryad.org/dataset/doi:10.5061/dryad.k6djh9wgj state the
  sentences quoted first, the Methods under the headings "Study system", "Fish Community Survey
  Methodology" and "Testing spatial and temporal variability in fish community excretion";
  README.md in the held zip states the file descriptions, the Subregion description and the derived
  sources; the JSON-LD in the landing page's HTML states the spatialCoverage and the
  temporalCoverage; and the data rows of Shrestha_fish_excr_data_Channel_Islands_all.csv and
  Shrestha_fish_excr_data_Channel_Islands_longterm_sites.csv in the held zip state the span and the
  SUBREGION values of the copy (retrieved 2026-09-27)
retrieved: 2026-09-27
fetch_script: src/fetch/shrestha_fish_excretion.py
file: null
transcribed_from: null
derived_from: null
topics:
  - bed-state/community
  - bed-state/mpas
regions:
  - scb.islands.anacapa
  - scb.islands.san-miguel
  - scb.islands.santa-cruz
  - scb.islands.santa-rosa
beds: []
sites: []
site_key:
  - file: doi_10_5061_dryad_k6djh9wgj__v20241112.zip
    column: SITE
references: []
human_task: null
---
