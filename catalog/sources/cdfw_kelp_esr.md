---
id: cdfw_kelp_esr
title: Giant Kelp and Bull Kelp Enhanced Status Report
steward: California Department of Fish and Wildlife
url: https://marinespecies.wildlife.ca.gov/kelp/
doi: null
status: VERIFIED
tier: FETCHED
access:
  - Open https://wildlife.ca.gov/Conservation/Marine/Kelp, CDFW's "Kelp and Other Marine Algae"
    page
  - Follow a link labelled "Giant Kelp and Bull Kelp Enhanced Status Report". The page carries
    three of them, in the paragraph beginning "A detailed summary of CDFW kelp management" and in
    the giant kelp and bull kelp rows of its species table, and all three point to
    https://marinespecies.wildlife.ca.gov/kelp/true/
  - That host serves a React single-page application, the California Marine Species Portal, and
    needs JavaScript. Every path under it answers HTTP 200 with the same 2,960-byte shell, whose
    noscript element reads "You need to enable JavaScript to run this app." and which contains no
    occurrence of "Macrocystis" and none of the report text. /kelp/, /kelp/the-species/,
    /kelp/management/ and /kelp/true/ each returned that same shell on 2026-09-15
  - >-
    The report's own routes, and the page number each carries, are a constant in the application
    bundle https://marinespecies.wildlife.ca.gov/static/js/main.976995ce.chunk.js, which the shell
    loads. It prints them as
    STATUS_REPORT:{URL:"/",TITLE:"Species-at-a-Glance",VALUE:0},SPECIES:{URL:"/the-species/",TITLE:"The
    Species",VALUE:1},FISHERY:{URL:"/the-fishery/",TITLE:"The
    Fishery",VALUE:2},MANAGEMENT:{URL:"/management/",TITLE:"Management",VALUE:3},MONITORING:{URL:"/monitoring/",TITLE:"Monitoring
    & Essential Fishery Information",VALUE:4},FUTURE:{URL:"/future/",TITLE:"Future Management Needs
    & Directions",VALUE:5},APPENDIX:{URL:"/appendix/",TITLE:"Appendices",VALUE:6}
    — so the page number to fetch for a route is its VALUE. "true/", the path the three CDFW links
    use, is not among them (retrieved 2026-09-15)
  - The report text is served as JSON, one response per page, from the URL that same bundle builds
    as '"https://".concat(Q.API,"/api/reports/").concat(a,"/").concat(t)', where Q.API is
    "marinespecies-api.wildlife.ca.gov", a is the species path segment, "kelp", and t is the page
    number above. So https://marinespecies-api.wildlife.ca.gov/api/reports/kelp/0 for
    Species-at-a-Glance, through https://marinespecies-api.wildlife.ca.gov/api/reports/kelp/6 for
    Appendices; this record fetches all seven. Each answered HTTP 200 with Content-Type
    "application/json; charset=utf-8" and Cache-Control "public, max-age=3600", and sent no ETag
    and no Last-Modified (2026-09-15)
  - The seventh response, .../kelp/6, carries one section, sectionId "6." named "Appendices", whose
    content is the empty string; the payload's hasAppendix is false on all seven pages
    (2026-09-15)
  - No account, key or referrer is required for either host. Both HTTPS certificates verified
    without customisation on 2026-09-15, from curl and from Python 3.13 urllib using its default
    SSL context
  - In the payload the text quoted in this record sits in speciesESRPage.sections[].content as HTML
    markup, and the report's own line breaks are newline characters inside it that fall within
    phrases, as in "compass" newline "headings". The quotations here are that content with the
    tags removed and each run of whitespace as one space, which is the text the rendered page shows
format: >-
  JSON, one response per report page; served as Content-Type application/json; charset=utf-8. Each
  response is an object with the single key speciesESRPage, carrying commonName, scientificName,
  esrPage, hasAppendix, year, status, hasEnhancedStatusReport, profileImageUrl, mfdeSpeciesId, a
  sections list whose content holds the section text as HTML markup, and a footer holding the
  report's citation, contributors, acknowledgement, table of contents, list of acronyms, lists of
  figures, charts and tables, literature cited and related links
license: >-
  not stated: the report states no licence, copyright or terms. None of the seven JSON payloads
  contains "copyright", "terms of use", "conditions of use", "disclaimer" or "public domain", and
  every occurrence of "licen" in them is a permission to harvest or to trade rather than a
  statement of terms for the report — the "Commercial Kelp Harvesting License" throughout, a
  "sport-fishing license" in section 3.1 and a harvester's "business license" in section 3.2. The
  report's landing page, https://marinespecies.wildlife.ca.gov/kelp/, links no terms, licence or
  disclaimer page: its footer, built by the bundle above, holds a "Back to Top" link, links titled
  "Facebook Pages", "Twitter Feeds", "YouTube Channel", "Blog Sites", "Photos" and "Mobile Apps",
  and a copyright line the bundle composes from the three parts it
  prints as "Copyright \xa9 ", (new Date).getFullYear() and " State of California", so the year in
  that line is the reader's own (all retrieved 2026-09-15)
variables:
  - >-
    "abundance, distribution, and metrics of ecosystem function, such as community composition, as
    well as amount and location of kelp harvested", which section 4.1 states "EFI for kelp
    management primarily includes"
  - >-
    the monthly commercial harvest logs, which section 4.2.1 states "must include the weight of the
    harvest and the Administrative Kelp Bed number where kelp was harvested", while "Kelp harvested
    for edible seaweed is reported by commercial fishing block number and the nearest prominent
    landmark where the kelp was harvested"
  - >-
    "kelp canopy area", which section 4.2.2 states the Department collected "for most years using
    aerial surveys in 1989, 1999, and annually from 2002–2016"
  - >-
    "surface canopy cover", which section 4.2.2 states is available "from publications using
    satellite imagery"; Figure 1-5 presents "Quarterly kelp canopy area (grey) from 1984–2020 in
    three regions"
  - Table 3-1, "Current number of Administrative Kelp Beds in each status."
  - >-
    Table 3-4, "Revenues from Commercial Kelp Harvesting Licenses and royalties 2015–2020.
    Royalties includes lease pre-payments. (Calstars and Fi$cal, accessed 07-14-2021)"
coverage: >-
  The report cites itself as "California Department of Fish and Wildlife. 2021. Giant Kelp and Bull
  Kelp, Macrocystis pyrifera and Nereocystis luetkeana, Enhanced Status Report." and states "The
  Giant Kelp and Bull Kelp Enhanced Status Report was updated in 2021. As of January 1, 2024, note
  that regulations may change." Its top-level sections are Species-at-a-Glance (page 0), "1. The
  Species", "2. The Fishery", "3. Management", "4. Monitoring and Essential
  Fishery Information" and "5. Future Management Needs and Directions". Species range: "In the
  northern hemisphere, giant kelp ranges from Kodiak Island, Alaska to Punta San Hipolito in Baja
  California Sur, Mexico, but is rare north of San Francisco. Bull kelp ranges from Unimak Island,
  Alaska to Point Conception, California, but is most abundant north of San Francisco." Depth: "In
  California, giant kelp typically grows on rocky reefs from the low intertidal to depths of 25
  meters (82 feet) with maximum depths of 30 meters (98 feet). Bull kelp grows on similar substrate
  typically from the low intertidal to 17 meters (56 feet) with maximum depths of 40 meters (131
  feet)." Administrative Kelp Beds: "Commercial kelp harvest is managed through 87 officially
  delineated Administrative Kelp Beds that span the entire California coastline including the
  Channel Islands."; "The kelp fishery is managed spatially in Administrative Kelp Beds, charted by
  the Commission in 1931. Originally, the Administrative Kelp Beds covered only the central and
  Southern California coasts, but in 1995, the northern Beds were established (Collins et al.
  2001). These Beds have additional restrictions, including closures and harvest limits (§165.5,
  Title 14, CCR). Although not completely contiguous, Administrative Kelp Beds span the majority of
  California’s coastline including the Channel Islands (see Figure 3-1 for a map of the
  southernmost Administrative Kelp Beds as an example). Maps for all 87 Administrative Kelp Beds
  can be found at https://wildlife.ca.gov/Conservation/Marine/Kelp/Commercial-Harvest." Canopy
  surveys: "The Department collected fishery-independent data on kelp canopy area for most years
  using aerial surveys in 1989, 1999, and annually from 2002–2016, with most data collected by the
  Department and its contractors." and "Shapefiles of these surveys are available for download
  at filelib.wildlife.ca.gov - /Public/R7_MR/BIOLOGICAL/Kelp/ or using MarineBIOS, a Department
  marine and coastal data viewer at https://wildlife.ca.gov/Conservation/Marine/GIS/MarineBIOS."
  Satellite canopy: Figure 1-5 is captioned "Quarterly kelp canopy area (grey) from 1984–2020 in
  three regions: north coast (Oregon-California border to San Francisco Bay), central coast (San
  Francisco Bay to Point Conception), and south coast (Point Conception to USA-Mexico border
  including the Channel Islands) as estimated from satellite imagery (Santa Barbara Coastal LTER et
  al. 2021)."
coverage_stated_at: >-
  The citation and version are speciesESRPage.footer.citation and .footer.version, present on all
  seven pages; the top-level sections are .footer.tableOfContents, whose entries carry the page
  each falls on. Then, on https://marinespecies-api.wildlife.ca.gov/api/reports/kelp/0, sections
  "0.2." Range and "0.3." Habitat for the range and the depths, and section "0.15." Management for
  the 87 beds; then .../kelp/3, section "3.1." Past and Current Management for the charting, the
  1995 northern beds and the maps of all 87; then .../kelp/4, section "4.2.2."
  Fishery-independent Data Collection for the aerial surveys and the shapefiles; then .../kelp/1,
  the caption of Figure 1-5 in section "1.2.1." Abundance Estimates, for the satellite series. All
  retrieved 2026-09-15
retrieved: 2026-09-15
fetch_script: src/fetch/cdfw_kelp_esr.py
file: null
transcribed_from: null
topics:
  - canopy/aerial-surveys
  - canopy/satellite
  - bed-state/diver-surveys
  - bed-state/mpas
  - grazers-predators-competitors/urchins
  - ocean-climate/heatwaves
  - water-quality-harvest/kelp-harvest
  - water-quality-harvest/power-plants
  - restoration-mitigation
regions:
  - scb
beds: []
sites: []
references: []
human_task: null
---
