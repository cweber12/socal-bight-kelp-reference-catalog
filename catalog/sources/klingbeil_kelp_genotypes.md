---
id: klingbeil_kelp_genotypes
title: >-
  Macrocystis pyrifera before (2008) and after (2018-19) microsatellite data in Structure format
steward: University of Wisconsin System
url: https://datadryad.org/dataset/doi:10.5061/dryad.nzs7h44v9
doi: 10.5061/dryad.nzs7h44v9
status: VERIFIED
tier: FETCHED
access:
  - >-
    https://doi.org/10.5061/dryad.nzs7h44v9 answers HTTP 302 with
    https://datadryad.org/dataset/doi:10.5061/dryad.nzs7h44v9 as its Location, and that page, this
    record's landing page, answers HTTP 200. It is headed with the title; names one author,
    "Alberto, Filipe", with the affiliation "University of Wisconsin System" and the line "Research
    facility: University of Wisconsin–Milwaukee"; states "Published Aug 14, 2023 on Dryad"; and
    gives the citation "Alberto, Filipe (2023). Macrocystis pyrifera before (2008) and after
    (2018-19) microsatellite data in Structure format [Dataset]. Dryad.
    https://doi.org/10.5061/dryad.nzs7h44v9" (2026-09-21)
  - >-
    Under "Works referencing this dataset" the page lists "Klingbeil, William H.; Montecinos, G. J.;
    Alberto, Filipe (2022), Giant kelp genetic monitoring before and after disturbance reveals
    stable genetic diversity in Southern California, Frontiers in Marine Science, Journal-article,
    https://doi.org/10.3389/fmars.2022.947393". That article states under "Data availability
    statement": "The original contributions presented in the study are publicly available. This data
    can be found here: doi: 10.5061/dryad.nzs7h44v9. The data link:
    https://datadryad.org/stash/share/fHKFVylYh5L0t1M0RLyPBvqyTXfRs5wMlzN5OaXu0lw." That link was
    not requested: the robots.txt named below states "Disallow: /stash/share". The article's DOI
    answers HTTP 302 with
    https://www.frontiersin.org/articles/10.3389/fmars.2022.947393/full as its Location, and the
    article answered HTTP 200 at
    https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2022.947393/full
    under the User-Agent the fetch script sends. README.md in the held zip states under
    "Sharing/Access information": "This data is only available in this repository." (2026-09-21)
  - >-
    The page's "Data files" section, headed "Aug 14, 2023 version files", links README.md at
    https://datadryad.org/downloads/file_stream/2475844 and
    Structure_before_and_after.Klingbeil2022.txt at
    https://datadryad.org/downloads/file_stream/2475842, over the line "Click names to download
    individual files". Each of the two links answered HTTP 403 under the User-Agent the fetch script
    sends, and https://datadryad.org/robots.txt states "Disallow: /downloads" under "User-agent: *"
    (2026-09-21)
  - >-
    Dryad's API describes the deposit without an account.
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.nzs7h44v9 answers HTTP 200 and
    states identifier "doi:10.5061/dryad.nzs7h44v9", versionNumber 6, curationStatus "Published",
    publicationDate "2023-08-14" and visibility "public". Its versions link,
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.nzs7h44v9/versions, states total 1
    and lists the version https://datadryad.org/api/v2/versions/248755, whose files link,
    https://datadryad.org/api/v2/versions/248755/files, states total 2 and lists the two files named
    under format (2026-09-21)
  - >-
    The API gives a download link to each file, to the dataset and to the version. Without a token
    https://datadryad.org/api/v2/files/2475844/download,
    https://datadryad.org/api/v2/files/2475842/download and
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.nzs7h44v9/download each answered
    HTTP 401 with the body {"error":"Unauthorized, must have current bearer token"}, and Dryad's API
    accounts document,
    https://raw.githubusercontent.com/datadryad/dryad-app/main/documentation/apis/api_accounts.md,
    states "Some API calls, such as creating a new dataset and downloading files, require a token
    for any call." and, in its next paragraph, "Without a token, only published datasets will be
    available."; the landing page's JSON-LD states "isAccessibleForFree": true. The version's link,
    https://datadryad.org/api/v2/versions/248755/download, answered without one: HTTP 302 with a
    signed URL under lambda-url.us-west-2.on.aws as its Location, which answered HTTP 200 with
    Content-Type application/zip, Content-Disposition
    attachment;filename="doi_10_5061_dryad_nzs7h44v9__v20230814.zip", Transfer-Encoding chunked, and
    no Content-Length, Last-Modified or ETag (2026-09-21)
  - >-
    Run src/fetch/klingbeil_kelp_genotypes.py, which sends the User-Agent
    "kelpcatalog/klingbeil_kelp_genotypes", requests
    https://datadryad.org/api/v2/versions/248755/download, stores the body under its
    Content-Disposition filename, and keeps it only when the zip holds the two members the files
    listing names and no other, each with the size and the SHA-256 that listing states; no account,
    key or referrer is required. The zip held is 176,604 bytes. The zip is assembled on request:
    three further requests six seconds apart were each served 176,604 bytes, their three SHA-256s
    differing from one another and from the held zip's, with each member's modification time within
    a second of the response's Date header; two other requests that day were served 176,599 bytes;
    and in each of the five the two members had the size and the SHA-256 the listing states (HTTP
    200, 2026-09-21)
format: >-
  The files listing named in access states two files, each with digestType "sha-256": path
  "README.md", size 1438, mimeType "text/markdown", digest
  61c5826338ea7422ee172f2f95b42c0976ae9aec886b676771c0558c79f318bb; and path
  "Structure_before_and_after.Klingbeil2022.txt", size 174743, mimeType "text/plain", digest
  756933ec92efbd75632471c373c4755fd14e15c75b303756d5c9d2091cb1ec41. This record holds the zip the
  version's download link serves, doi_10_5061_dryad_nzs7h44v9__v20230814.zip, whose two members are
  those files. README.md states "The data format is that of STRUCTURE program
  (https://web.stanford.edu/group/pritchardlab/structure.html)" and "The data includes  the six loci
  analyzed in Klingbeil et al., (2022) Frontiers in Marine Sciences
  (https://doi.org/10.3389/fmars.2022.947393), the "after" data,  and all the data from the "before"
  study Johansson et al. (2015, https://doi.org/10.1111/mec.13371)." The first line of
  Structure_before_and_after.Klingbeil2022.txt is tab-separated and names the six loci listed under
  variables, in that order; the landing page's Methods name them "(Mpy-8, Mpy-14, BC-4, BC-18,
  BC-19, BC-25)" (2026-09-21)
license: >-
  "Public domain", under the heading "License:" and linked to
  https://creativecommons.org/publicdomain/zero/1.0/ with the label "CC0 (opens in new window)", in
  the licence panel the landing page loads from
  https://datadryad.org/stash_datacite/licenses/details.js?resource_id=248755, which answers HTTP
  200 to a request carrying the header X-Requested-With: XMLHttpRequest and HTTP 500 to one without
  it. README.md, the one member of the held zip that is not the data file, contains none of
  "licen", "copyright", "CC0", "public domain", "creative commons" or "terms" in any letter case.
  The landing page's own HTML states in its JSON-LD a license of name "Creative Commons Zero v1.0
  Universal" and license "https://spdx.org/licenses/CC0-1.0.html", and the API's dataset response
  named in access states license "https://spdx.org/licenses/CC0-1.0.html" (2026-09-21)
variables:
  - BC.18
  - BC.25
  - BC.19
  - BC.4
  - Mpy.8
  - Mpy.14
coverage: >-
  The landing page's Methods state "To conduct a temporal genetic analysis, we sampled giant kelp at
  five sites between 2018 and 2019 located in three regions differing in genetic coancestry in the
  Southern California Bight (SCB), hereafter referred to as 2018 samples.", "These regions had also
  been sampled before, in 2007 and 2008, and genotyped by Johansson et al. (2015) using
  microsatellite marker analysis, hereafter referred to as 2008 samples.", "Two of our locations are
  continental, Leo Carrillo, and Camp Pendleton, with one site sampled in each.", "Our third
  location was Catalina Island, where we sampled three sites" and "New sample collections occurred
  between January 2018 and June 2019." README.md states "The "after" disturbance sites, sampled in
  2018-19, have their individual names starting with the following characters." over "CIR-19
  (Catalina Island Backside 2-2019)", "CIQ-19 (Catalina Island Quarry-2019)" and "CSC-19 (Catalina
  Island Quarry-2018)", and "Additionally, the following sites CIA-18, CIH-19, and CIW-18 are
  "after" disturbance sites that did not have matching "before" data and thus were not included in
  the Klingbeil et al., (2022) paper. These were all sites sampled on Catalina Island. They
  correspond to Catalina Arrow Point, Catalina Indian Head Rock, and Catalina Wrigley." In the held
  data file "CSC" occurs nowhere, and the names in its first column that carry a hyphen begin with
  one of eight prefixes: LCA-18, CIB-19, CIR-19, CIA-18, CIH-19, CIW-18, CIQ-19 and CBD-18.
  README.md also states that the data includes "all the data from the "before" study Johansson et
  al. (2015, https://doi.org/10.1111/mec.13371)". Table 2 of the article named in access,
  "Population genetics summary statistics for Macrocystis pyrifera temporal genetic diversity for
  five sites in Southern California.", gives each population and sample year a Latitude and a
  Longitude: "Leo Carrillo
  (LCA-08)" and "Leo Carrillo (LCA-18)", "34°2’34.56”N" and "118°56’4.20”W"; "Catalina Island
  Backside 1 (CIB-08)" and "Catalina Island Backside 1 (CIB-19)", "33°20’2.76”N" and
  "118°29’16.68”W"; "Catalina Island Backside 2 (CIR-08)" and "Catalina Island Backside 2 (CIR-19)",
  "33°25’45.72”N" and "118°31’49.32”W"; "Catalina Island Quarry (CIQ-08)", "33°26’32.51”N" and
  "118°28’20.88”W"; "Catalina Island Quarry (CIQ-19)", "33°26’ 26.16”N" and "118°27’ 45.00”W";
  "Carlsbad (CBD-08)", "33°22’4.00”N" and "117°35’24.40”W"; and "Camp Pendleton (CBD-18)",
  "33°17’27.28”N" and "117°29’59.89”W". The landing page's JSON-LD states "spatialCoverage": []
coverage_stated_at: >-
  The Methods section of https://datadryad.org/dataset/doi:10.5061/dryad.nzs7h44v9 states the five
  sentences quoted first; README.md in the held zip states the sentences and the site names quoted
  next, and Structure_before_and_after.Klingbeil2022.txt beside it holds the prefixes; Table 2 of
  https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2022.947393/full states
  the populations and their coordinates; and the JSON-LD in the landing page's HTML states the
  spatialCoverage (retrieved 2026-09-21)
retrieved: 2026-09-21
fetch_script: src/fetch/klingbeil_kelp_genotypes.py
file: null
transcribed_from: null
topics:
  - recruitment-connectivity/genetics
regions:
  - scb
  - scb.islands.santa-catalina
beds: []
sites: []
references: []
human_task: null
---
