---
id: sccwrp_kelp_aerial
title: Southern California Bight Regional Aerial Kelp Surveys
steward: Southern California Coastal Water Research Project
url: http://kelp.sccwrp.org/
doi: null
status: VERIFIED
tier: FETCHED
access:
  - >-
    Open http://kelp.sccwrp.org/, whose title is "Southern California Bight Regional Aerial Kelp
    Surveys". It serves the same 3,413 bytes, with the same ETag, as
    http://kelp.sccwrp.org/home.html, the page its "Home" menu link opens (HTTP 200, 2026-09-16)
  - >-
    Use http://, not https://. Over HTTPS the host presents a certificate for *.sccwrp.org, issued
    by Sectigo RSA Domain Validation Secure Server CA, valid until Mar 25 23:59:59 2026 GMT; curl
    8.15.0 (Schannel) and Python 3.13 urllib with its default SSL context each refused it as
    expired, while HTTP answered 200 with no redirect (2026-09-16)
  - >-
    Follow the menu link "Reports" to http://kelp.sccwrp.org/reports.html. It links each "Status of
    the Kelp Beds" report as a PDF at a path relative to the host. Some file names hold literal
    spaces, which a client sends as %20, as in the link to
    http://kelp.sccwrp.org/2013_Status_of_Kelp_Beds_Final%20Report_20140721.pdf;
    all fourteen PDF links on the page answered HTTP 200 with Content-Type application/pdf
    (2026-09-16). This record fetches http://kelp.sccwrp.org/home.html and
    http://kelp.sccwrp.org/reports.html, not the PDFs
  - No account, key or referrer is required
  - >-
    No page of the site names the organisation that publishes it. The host is a subdomain of
    sccwrp.org. The "Meetings" page, http://kelp.sccwrp.org/meeting.html, links two meeting
    videos, https://vimeo.com/sccwrp/review/177135739/739970ee1d and
    https://vimeo.com/229723053. Vimeo's oEmbed endpoint, as
    https://vimeo.com/api/oembed.json?url=https://vimeo.com/229723053, returns for each video id,
    https://vimeo.com/177135739 and https://vimeo.com/229723053, JSON whose author_name is
    "SCCWRP" and whose author_url, once its escaped slashes are read, is https://vimeo.com/sccwrp;
    for the review link as the page gives it, the endpoint answered 404 (2026-09-16). The "About
    Us" page, http://kelp.sccwrp.org/about.html, is in four parts, headed "Region Nine Kelp Survey
    Consortium", "Central Region Kelp Survey Consortium", "Regional Water Boards" and "Project
    Consultant"
format: >-
  HTML pages declared as XHTML 1.0 Transitional, charset UTF-8; served as Content-Type text/html.
  The Reports page links PDF files, served as Content-Type application/pdf
license: >-
  not stated: none of the site's four pages, http://kelp.sccwrp.org/home.html, about.html,
  reports.html and meeting.html, contains "copyright", "licen", "terms", "disclaimer" or "public
  domain", and none has a footer. Their links are the menu, "Home", "About Us", "Reports" and
  "Meetings", the report PDFs on reports.html, and meeting agenda PDFs and the two meeting videos
  named in access on meeting.html (all retrieved 2026-09-16)
variables: []
coverage: >-
  "The status of the giant kelp forests (Macrocystis pyrifera) that occur along most of the
  southern California coast are mapped annually as part of NPDES permit requirements for most
  ocean dischargers in the region. The program began about 30 years ago (1982-1983) when the Region
  Nine Kelp Survey Consortium (RNKSC) was formed to address regulations drafted by the San Diego
  Regional Water Quality Control Board for San Diego and southern Orange Counties. The extent of
  these surveys was extended to northern Orange County, Los Angeles County and Ventura County in
  2002 when the Central Region Kelp Survey Consortium (CRKSC) was formed to address similar
  requirements put forth by the Los Angeles Regional Water Control Board."; "With the RNKSC and
  CRKSC programs combined, all coastal kelp beds from the Ventura River to the USA/Mexico Border
  are now surveyed synoptically several times a year, a coverage representing approximately 81% of
  the southern California mainland coast. Although the results of these kelp surveys were reported
  separately for each region prior to 2012, these reports have since been combined into a single
  “Status of the Kelp Beds” report published in July of each year." The Reports page lists "Status
  of the Kelp Beds, 2016. Ventura, Los Angeles, Orange, and San Diego Counties" and that title with
  the year 2015, 2014, 2013 and 2012 in turn, then for each of 2011 and 2010 two reports, "San
  Diego and Orange Counties" and "Ventura, Los Angeles and Orange Counties", as in "Status of the
  Kelp Beds, 2011. San Diego and Orange Counties"
coverage_stated_at: >-
  The first quoted passage is the whole paragraph beginning "The status of the giant kelp forests",
  where Macrocystis pyrifera is set in an em element whose tags are removed here, and the second is
  the first two sentences of the paragraph beginning "With the RNKSC and CRKSC programs combined",
  both on http://kelp.sccwrp.org/home.html; the report titles are the link texts of
  http://kelp.sccwrp.org/reports.html. Both retrieved 2026-09-16
retrieved: 2026-09-16
fetch_script: src/fetch/sccwrp_kelp_aerial.py
file: null
transcribed_from: null
topics:
  - canopy/aerial-surveys
  - water-quality-harvest/discharges-outfalls
regions:
  - scb.mainland.ventura
  - scb.mainland.los-angeles
  - scb.mainland.orange
  - scb.mainland.san-diego
beds: []
sites: []
references: []
human_task: null
---
