---
id: okun_inner_shelf_flow
title: "Data from: Semidiurnal inner shelf flow in the Southern California Bight"
steward: Scripps Institution of Oceanography
url: https://datadryad.org/dataset/doi:10.5061/dryad.x3ffbg7tk
doi: 10.5061/dryad.x3ffbg7tk
citations:
  - as_printed: >-
      Okun, Kevin; Desai, Ajinkya; Parnell, Ed et al. (2025). Data from: Semidiurnal inner shelf
      flow in the Southern California Bight [Dataset]. Dryad.
      https://doi.org/10.5061/dryad.x3ffbg7tk
    stated_at: >-
      https://datadryad.org/dataset/doi:10.5061/dryad.x3ffbg7tk, under the heading "Citation": in
      the HTML that page sends it is the content of the element <p id="dataset-citation" hidden>,
      which the heading's button shows, the DOI there being the text of a link to the same URL
      (2026-09-27)
status: VERIFIED
tier: FETCHED
access:
  - >-
    https://doi.org/10.5061/dryad.x3ffbg7tk answers HTTP 302 with
    https://datadryad.org/dataset/doi:10.5061/dryad.x3ffbg7tk as its Location, and that page, this
    record's landing page, answers HTTP 200 with 62,578 bytes of Content-Type "text/html;
    charset=utf-8". Its HTML loads a script from
    https://16077a4ae659.us-west-2.captcha-sdk.awswaf.com/16077a4ae659/jsapi.js and holds a <div
    id="captcha-div">, and the same response carries the text quoted here. It is headed with the
    title; names seven authors, "Okun, Kevin", "Desai, Ajinkya", "Parnell, Ed", "Masunaga, Eiji",
    "Lucas, Drew", "Lerczak, James" and "Pawlak, Geno", marked 1, 2, 1, 3, 1, 4 and 5 against a
    list headed "Affiliations" under "Author information" that reads "Scripps Institution of
    Oceanography" (1), "University of California, Irvine" (2), "Ibaraki University" (3), "Oregon
    State University" (4) and "University of California San Diego" (5); states "Published Dec 16,
    2024; Updated Apr 24, 2025 on Dryad"; names no research facility and no depositor; and prints
    the citation entered under citations (2026-09-27)
  - >-
    Dryad's API describes the deposit without an account.
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.x3ffbg7tk answers HTTP 200 and
    states identifier "doi:10.5061/dryad.x3ffbg7tk", storageSize 24186042, versionNumber 5,
    curationStatus "Published", publicationDate "2025-04-24", lastModificationDate "2025-04-24",
    visibility "public", the seven authors in the page's order, the first, Kevin Okun, with
    affiliation "Scripps Institution of Oceanography" and the one email address the response
    carries, and under relatedWorks, with relationship "primary_article", the identifier
    https://doi.org/10.1029/2024JC021591, which answers HTTP 302 with
    https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2024JC021591 as its Location. Its version
    link is https://datadryad.org/api/v2/versions/360631. Its versions link,
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.x3ffbg7tk/versions, states total 2
    and lists https://datadryad.org/api/v2/versions/334486 (versionNumber 3, publicationDate
    "2024-12-16") and https://datadryad.org/api/v2/versions/360631 (versionNumber 5,
    publicationDate "2025-04-24"). The files link of version 360631,
    https://datadryad.org/api/v2/versions/360631/files, states total 18 and lists the eighteen
    files named under format. The DataCite record of the DOI,
    https://api.datacite.org/dois/10.5061/dryad.x3ffbg7tk, answers HTTP 200 and states publisher
    "Dryad" and contributors [] (2026-09-27)
  - >-
    The landing page's "Data files" section lists two groups of files, headed "Dec 16, 2024 version
    files" and "Apr 24, 2025 version files", over the line "Click names to download individual
    files". The second group lists the eighteen files named under format; the first lists
    scatter_invisc_01_SoCal_2023_02_ih1_is3.mat, which the second does not, and does not list
    scatter_invisc_SoCal_February2025_Xsection_ih2_is1.mat. The JSON-LD in the page's HTML gives
    the eighteen files' contentUrl as http://datadryad.org/downloads/file_stream/ followed by
    4036458, 4036459, 4036460, 4036461, 4036462, 4036463, 4036464, 4036465, 4036467, 4036468,
    4036469, 4036470, 4036471, 4036472, 4036473, 4036475, 4036477 and 4036482. Requested over
    https://, each of the eighteen answered HTTP 403 under the User-Agent the fetch script sends,
    and https://datadryad.org/robots.txt states "Disallow: /downloads" under "User-agent: *"
    (2026-09-27)
  - >-
    The API gives a download link to each file, to the dataset and to each version. Without a token
    https://datadryad.org/api/v2/files/<n>/download answered HTTP 401 for each of the eighteen
    numbers listed in the previous step, https://datadryad.org/api/v2/files/4036482/download (the
    README.md) being one, and
    https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.x3ffbg7tk/download answered HTTP
    401, each with the body {"error":"Unauthorized, must have current bearer token"}. The link of
    version 360631, https://datadryad.org/api/v2/versions/360631/download, answered without one:
    HTTP 302 with a signed URL under lambda-url.us-west-2.on.aws as its Location, which answered
    HTTP 200 with Content-Type application/zip, Content-Disposition
    attachment;filename="doi_10_5061_dryad_x3ffbg7tk__v20250424.zip", Transfer-Encoding chunked,
    and no Content-Length, Last-Modified or ETag (2026-09-27)
  - >-
    Run src/fetch/okun_inner_shelf_flow.py, which sends the User-Agent
    "kelpcatalog/okun_inner_shelf_flow", requests
    https://datadryad.org/api/v2/versions/360631/download, stores the body under its
    Content-Disposition filename, and keeps it only when the file begins with the zip local file
    header signature, the bytes 50 4B 03 04, carries no bytes before its first member and no
    archive comment, and holds the eighteen members the files listing of version 360631 names and
    no other, each with the size and the SHA-256 that listing states; no account, key or referrer
    is required. The zip held is 24,192,581 bytes. The zip is assembled on request: an earlier
    request that day was served 24,192,611 bytes with a different SHA-256, and in both zips every
    member's modification time was the minute of its own request and every member had the size and
    the SHA-256 the listing states (HTTP 200, 2026-09-27)
format: >-
  The files listing of version 360631 named in access states eighteen files, each with digestType
  "sha-256": path "Bathymetry_Profiles.mat", size 25454, digest
  8891872a789244777521c2f368a592f5ef037c3c00e42142205cc81f8844b1e8; "Quasi_Barotropic.mat", 2378,
  92548e80fe50fee5fb7e158f6656e21ffe96bf8145fd6bb246d9d2bbd2023f4c; "README.md", 3861,
  748855d4b094fc4075364408c77a04d12ffd56ff97190087acb6449d68e034cd;
  "RunsForPub_bathy2_strat1.mat", 2021725,
  db02e5a04ca397ce339ead9172f5427ae914528acbcacb863dba6949fbd66f00;
  "scatter_invisc_01_SoCal_2023_02_ih1_is1.mat", 8009,
  ff6c55cbe39e78c5f34feb62399d5785105e3662a8f8a6c87e1272dc64a9170e;
  "scatter_invisc_01_SoCal_2023_02_ih1_is2.mat", 7992,
  a93e7651126af75d14a35b65daab0d93cb90b9ae4953ed0734c93671a14e9daa;
  "scatter_invisc_01_SoCal_2023_02_ih1_is4.mat", 8022,
  7626f0d40b791975ce8616ee5dc9f51f3c8549f764c263d3c355979085d0cd9f;
  "scatter_invisc_01_SoCal_2023_02_ih2_is1.mat", 7473,
  ad21c530fe8d2548417f9c5584eaf524c09cf3a817a2556ff2677aa20205ed0b;
  "scatter_invisc_01_SoCal_2023_02_ih2_is2.mat", 7806,
  b98579c25fa5a56c9d20b74efbb15c577f6f76e8882e2ec5e8920eb11bb71e4c;
  "scatter_invisc_01_SoCal_2023_02_ih2_is3.mat", 7914,
  9facf04fed6d5ee661ffbd88eaf8282e62e777a573fdccb272f8afba16be36d9;
  "scatter_invisc_01_SoCal_2023_02_ih2_is4.mat", 7696,
  924552cd2bb80d343545684d6b0961ab36035ad79e5e57031855a32ea8a084d9;
  "scatter_invisc_01_SoCal_2023_02_ih3_is1.mat", 7994,
  4e10a3377f248c9158080062825e93bcd4e1afd455cb699c9c27432f7561ff4d;
  "scatter_invisc_01_SoCal_2023_02_ih3_is2.mat", 8022,
  4d2b0ffcda249ca402b9eec1ecace60536ff750cccba4a577138cd849d8dcc1c;
  "scatter_invisc_01_SoCal_2023_02_ih3_is3.mat", 7997,
  ff65c69d11770c12c37889f281ed1463f3351708ab86d8bf5ef6cc1de5873284;
  "scatter_invisc_01_SoCal_2023_02_ih3_is4.mat", 8077,
  4b6a07630e0530cdd86c57c1383d1558092cd102b373bb27243b7fca8ce12abc;
  "scatter_invisc_SoCal_February2025_Xsection_ih2_is1.mat", 1768765,
  94b18bd073b40057092a21f38f528925ca0e77aabf7b0b89ba4e2f1705d6812c; "SD_IT_Current_Data.mat",
  20239579, e531d6e9cff208c7bcd1df746599a934455c7576a73e74d65c7f2c1c07cfbc6c; and
  "Seasonal_N_2.mat", 37278, fbfebe31862332c79aa8529b8cb31636ae8c002100e28577baccedf94212f619. It
  states mimeType "text/markdown" for README.md and an empty mimeType for the other seventeen. This
  record holds the zip the version's download link serves,
  doi_10_5061_dryad_x3ffbg7tk__v20250424.zip, whose eighteen members are those files. README.md
  describes SD_IT_Current_Data.mat under the heading "### Observational Data
  (SD\_IT\_Current\_Data.mat)" as "This MATLAB file contains the primary acoustic Doppler current
  profiler (ADCP) measurements, with variables stored in a structured array format.", listing
  "Velocity measurements (m/s):" ("Depth-averaged alongshore and cross-shore components",
  "Filtered within the semidiurnal band (11-14.5 hours)", "Positive values indicate
  northward/eastward flow", "Sampling interval: 5 minutes, derived from 50-point ensemble averages
  of 6-second measurements"), "Bottom measurements at 33m depth:" ("Pressure (decibars),
  referenced to surface", "Temperature (°C)", "Time series in UTC (MATLAB datenum format)") and
  "Quality control parameters:" ("Top 15% and bottom 3.1m of water column excluded from
  depth-averaging", "Periodic NaNs result from regular maintenance of the equipment"). It
  describes under "### Phase Analysis Data (Quasi-Barotropic.mat)", a name the zip spells
  Quasi_Barotropic.mat, "Contains processed data for quasi-barotropic current analysis:"
  ("Time-averaged phase calculations for depth-averaged alongshore current", "Time-averaged phase
  of bottom pressure"); under "### Environmental Data", Bathymetry_Profiles.mat as "Cross-shore
  bathymetric profiles between monitoring sites", "Referenced to 100m depth datum", "Average
  spacing approximately 140m N-S", "Derived from NOAA's San Diego 1/3 arc-second MHW Coastal
  Digital Elevation Model" and "Profiles span Point Loma to La Jolla, La Jolla to Cardiff, and
  Point Loma to Cardiff sections", with "Bathymetry has been corrected for an erroneous scale
  factor." under "**Update: 04/23/25**", and Seasonal_N_2.mat as "Seasonal buoyancy frequency (N²)
  profiles (rad²/s²)", "Temporal coverage: 2008-2018", "Vertical profiles to 609m depth", "Data
  from CalCOFI CTD casts (Line 93.3 Station 28)", "Seasonal groupings: December-February,
  March-May, June-August, September-November" and "Processing: 10m median filter applied to raw
  profiles"; and under "### Model Results", the scatter_invisc files as "Coastal trapped wave (CTW)
  model output", "Solutions for each bathymetry-stratification combination", "Includes resonant
  mode characteristics", "Wave properties: wavelength, phase speed" and "Vertical and cross-shore
  structure of pressure and velocity fields", with "Added
  scatter_invisc_SoCal_February2025_Xsection_ih2_is1.mat, which shows the above for the updated
  bathymetry." under "**Update: 04/23/25**", and RunsForPub_bathy2_strat1.mat as "Specific model
  results featured in manuscript Figure 9", "Demonstrates wavelength sensitivity to environmental
  parameters" and "Cross-shore pressure field structure". README.md names no variable or field of
  any file, so variables is empty
license: >-
  "Public domain", under the heading "License:" and linked to
  https://creativecommons.org/publicdomain/zero/1.0/ with the label "CC0 (opens in new window)", in
  the licence panel the landing page loads from
  https://datadryad.org/stash_datacite/licenses/details.js?resource_id=360631, which answers HTTP
  200 to a request carrying the header X-Requested-With: XMLHttpRequest. The landing page's own
  HTML states in its JSON-LD a license of name "Creative Commons Zero v1.0 Universal" and license
  "https://spdx.org/licenses/CC0-1.0.html", and the API's dataset response named in access states
  license "https://spdx.org/licenses/CC0-1.0.html" (2026-09-27)
license_stated_at: >-
  Looked for first in the held zip: README.md, the one member whose name does not end ".mat",
  contains none of "licen", "copyright", "CC0", "public domain", "creative commons" or "terms" in
  any letter case. Then on the landing page, https://datadryad.org/dataset/doi:10.5061/dryad.x3ffbg7tk, whose
  licence panel is filled from
  https://datadryad.org/stash_datacite/licenses/details.js?resource_id=360631, the script its HTML
  names; the JSON-LD in the same HTML, and
  https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.x3ffbg7tk, state the SPDX identifier
  (retrieved 2026-09-27)
variables: []
coverage: >-
  The landing page's Abstract states "Semidiurnal variability of alongshore currents on the inner
  shelf of the Southern California Bight is investigated using a 7 year velocity and pressure time
  series." README.md states "The observational data spans seven years (August 2011 to September
  2018), collected at three monitoring sites along the 33m isobath off Southern California.";
  describes Bathymetry_Profiles.mat as "Cross-shore bathymetric profiles between monitoring
  sites" whose "Profiles span Point Loma to La Jolla, La Jolla to Cardiff, and Point Loma to
  Cardiff sections"; and describes Seasonal_N_2.mat with "Temporal coverage: 2008-2018", "Vertical
  profiles to 609m depth" and "Data from CalCOFI CTD casts (Line 93.3 Station 28)". The landing
  page's JSON-LD states "spatialCoverage": [] and a "temporalCoverage" of "2024-07-15 21:42:23
  UTC", "2024-12-09 16:54:23 UTC", "2024-12-16 00:00:00 UTC", "2024-12-16 00:00:00 UTC" and
  "2025-04-24 00:00:00 UTC"
coverage_stated_at: >-
  The Abstract of https://datadryad.org/dataset/doi:10.5061/dryad.x3ffbg7tk states the sentence
  quoted first; README.md in the held zip, which the landing page also renders, states the
  observational span and sites, the Bathymetry_Profiles.mat description and the Seasonal_N_2.mat
  description, under its introduction and the headings "### Environmental Data",
  "Bathymetry_Profiles.mat:" and "Seasonal_N_2.mat:"; and the JSON-LD in the landing page's HTML
  states the spatialCoverage and the temporalCoverage (retrieved 2026-09-27)
retrieved: 2026-09-27
fetch_script: src/fetch/okun_inner_shelf_flow.py
file: null
transcribed_from: null
derived_from: null
topics:
  - recruitment-connectivity/larval-transport
regions:
  - scb.mainland.san-diego
beds: []
sites: []
site_key: []
references: []
human_task: null
---
