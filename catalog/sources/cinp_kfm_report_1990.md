---
id: cinp_kfm_report_1990
title: KELP FOREST MONITORING CHANNEL ISLANDS NATIONAL PARK 1990 Annual Report
steward: Channel Islands National Park
url: https://irma.nps.gov/DataStore/Reference/Profile/68419
doi: null
citations:
  - as_printed: >-
      Richards DV and Others. 1993. Kelp Forest Monitoring, Channel Islands National Park: 1990
      Annual Report. Technical report (Cooperative National Park Resources Studies Unit) no. 52..
      NPS/WRUC/NRTR 93-05. Cooperative National Park Resource Studies Unit, Univ. of California,
      Institute of Ecology. Davis, CA
    stated_at: >-
      The "DisplayCitation" value of the JSON literal passed to
      NPSDataStoreReferenceCoreModel.modelSerialize(...) in the HTML of
      https://irma.nps.gov/DataStore/Reference/Profile/68419, read by parsing that literal as JSON;
      and the "DisplayCitation" of the Result with "Id":68419 in the JSON answer to POST
      https://irma.nps.gov/DataStore/SavedSearch/GetSavedSearchReferences with
      savedSearchId=1508, the same string (both retrieved 2026-10-10)
  - as_printed: >-
      Richards DV, Avery W, Kushner D, National Park Service. Western Regional office. 1993. Kelp
      Forest Monitoring, Channel Islands National Park: 1990 Annual Report. Technical report
      (Cooperative National Park Resources Studies Unit) no. 52.. NPS/WRUC/NRTR 93-05. Cooperative
      National Park Resource Studies Unit, Univ. of California, Institute of Ecology. Davis, CA
    stated_at: >-
      The "AllContactsDisplayCitation" value of the same JSON literal in the HTML of
      https://irma.nps.gov/DataStore/Reference/Profile/68419, read by parsing that literal as JSON
      (retrieved 2026-10-10)
status: VERIFIED
tier: FETCHED
access:
  - >-
    Open https://www.nps.gov/im/medn/kelp-forest-communities.htm, which answers HTTP 200 with
    Content-Type text/html;charset=UTF-8. Its <title> is "Kelp Forest Community Monitoring (U.S.
    National Park Service)" and its <h1> "Kelp Forest Community Monitoring". It states "The Kelp
    Forest Monitoring Program was established by Channel Islands National Park in 1982 to collect
    baseline information about the kelp forest ecosystem in the Park." Under the <h2> "For More
    Information", the accordion panel whose button reads "Monitoring Reports" prints "Source:"
    and links https://irma.nps.gov/DataStore/SavedSearch/Profile/1508 with the link text "NPS
    DataStore Saved Search  1508", two spaces before "1508". The page prints "Last updated:
    December 1, 2023" (2026-10-10)
  - >-
    https://irma.nps.gov/DataStore/SavedSearch/Profile/1508 answers HTTP 200 with an application
    shell: its HTML carries the saved search as {"Id":1508,"Title":"Kelp Forest
    Monitor","Description":"Kelp Forest Monitor",...} and contains the string "1990 Annual
    Report" 0 times, and its script loads the list by POST
    https://irma.nps.gov/DataStore/SavedSearch/GetSavedSearchReferences with savedSearchId=1508.
    That POST answers JSON with "TotalCount":26 and 26 Results, whose Titles name each year from
    1990 to 2015 once. The Result with "Id":68419 has the Title "Kelp Forest Monitoring, Channel
    Islands National Park: 1990 Annual Report", Type "PublishedReport", Downloadability "Public",
    Visibility "Public", Lifecycle "Active", FileCount 1, the ReferenceUrl "
    https://irma.nps.gov/DataStore/Reference/Profile/68419" with a leading space as served,
    Contacts "Daniel Richards, William Avery, David Kushner,  National Park Service. Western
    Regional office", two spaces before "National" as served, and the DisplayCitation entered in
    citations (2026-10-10)
  - >-
    https://irma.nps.gov/DataStore/Reference/Profile/68419, this record's url, answers HTTP 200
    with Content-Type text/html; charset=utf-8 and is served as an application shell: its Core
    Info values are a JSON literal passed to NPSDataStoreReferenceCoreModel.modelSerialize(...)
    inside a script element. That literal carries "ReferenceId":68419, the Title above,
    "TypeName":"Published Report", "Downloadability":"Public", "HasCUI":false,
    "CanDownloadFiles":false, "LicenseTypeID":null, "LicenseTypeName":null and
    "LicenseTypeURL":null, the DisplayCitation and the AllContactsDisplayCitation entered in
    citations, and the Description quoted in coverage, and it defines the field "Contacts1" with
    the DisplayName "Author(s)" and the field "AgencyOriginated" with the DisplayName "Created by
    or for the NPS". POST https://irma.nps.gov/DataStore/Reference/GetProfileCoreModel with
    referenceId=68419&id=68419 answers "Contacts1":"Daniel V Richards; William Avery; David
    Kushner; National Park Service. Western Regional office", "Publisher":"Cooperative National
    Park Resource Studies Unit, Univ. of California, Institute of Ecology", "Location":"Davis,
    CA", "DateOfIssue":"June 1993", "MiscCode":"NPS/WRUC/NRTR 93-05", "Size1":"112 Pages",
    "PpTitle":"Technical report (Cooperative National Park Resources Studies Unit) no. 52.",
    "IsAgencyOriginated":0, "IntellectualRights":null, "ContentBeginDate":null and
    "ContentEndDate":null. With the same parameters, POST
    /DataStore/Reference/ProfileLinkedUnitsModel answers
    [{"Code":"CHIS","FullName":"Channel Islands National Park"},{"Code":"MEDN","FullName":"Mediterranean
    Coast Network"}], /DataStore/Reference/ProfileContentProducerUnitsModel answers [],
    /DataStore/Reference/GetCUIBanner answers
    {"LegalAuthorities":[],"ProducingUnit":null,"ContactEmail":null} and
    /DataStore/Reference/GetAllReferenceMethods answers [] (2026-10-10)
  - >-
    POST https://irma.nps.gov/DataStore/Reference/GetHoldings with referenceId=68419&id=68419
    lists one holding, with "Id":485218,
    "Url":"https://irma.nps.gov/DataStore/DownloadFile/485218",
    "FileDescription":"chis_kelp90.pdf", "Description":"1990 Annual Report for Kelp Forest
    Monitoring at Channel Islands National Park", "FileSize":306257,
    "MimeType":"application/pdf", "CanDownload":true, "MD5Hash":null and "Is508Compliant":false,
    and POST /DataStore/Reference/CanUserDownloadFiles with the same parameters answers true
    without an account. Download https://irma.nps.gov/DataStore/DownloadFile/485218, which
    answers HTTP 200 with 306,257 bytes of Content-Type application/pdf, Content-Disposition
    inline; filename="chis_kelp90.pdf", no Last-Modified and no ETag, no redirect, the bytes
    served having SHA-256 e04939d1671d7276d84bea44a311a123742e8dd0c378f405cf465b633cf67bfb and
    beginning %PDF-1.3; no account, key or referrer is required. Run
    src/fetch/cinp_kfm_report_1990.py, which sends the User-Agent
    "kelpcatalog/cinp_kfm_report_1990", requests that URL, and stores the body under the
    Content-Disposition file name only when the body begins with the bytes %PDF-, that name is
    chis_kelp90.pdf and the body is 306,257 bytes, the FileDescription and FileSize the holding
    states (2026-10-10)
  - >-
    https://www.nps.gov/chis/learn/management/index.htm answers HTTP 200 with Content-Type
    text/html;charset=UTF-8. Its <title> is "Management - Channel Islands National Park (U.S.
    National Park Service)" and its <h1> "Management", and it states "The park operates under
    Federal, Department of the Interior, and National Park Service policies and guidelines, in
    accordance with a General Management Plan (GMP) which was first published in 1980." The page
    prints "Last updated: January 23, 2024" (retrieved 2026-10-10). The footer the DataStore
    profile renders, defined in
    https://irmafiles.nps.gov/WebContent/Irma/Common/v3_0_2/Scripts/ext_7_7_0/Modern/nps-custom-components.js,
    links "National Park Service", https://www.nps.gov/index.htm, and "US Department of the
    Interior", https://www.doi.gov/ (2026-10-10)
  - >-
    The file has 224 PDF pages, where the profile's Size1 above states "112 Pages". Its first
    page prints, on separate lines in this order, "KELP FOREST MONITORING", "CHANNEL ISLANDS
    NATIONAL PARK" and "1990 Annual Report" (one printing of the title across three lines, which
    title joins with one space), "by", "DANIEL RICHARDS", "WILLIAM AVERY", "DAVID KUSHNER",
    "CHANNEL ISLANDS NATIONAL PARK", "1901 SPINNAKER DRIVE" and "VENTURA, CA 93001". The string
    "National Park Service" occurs twice in its text: under EXECUTIVE SUMMARY, PDF page 5, "In
    1990, 44 National Park Service and volunteer divers made 759 dives during a series of seven
    five-day and three shorter cruises to conduct the monitoring.", and under ACKNOWLEDGEMENTS,
    PDF page 75, "This program was supported by the U.S. National Park Service in cooperation
    with the California Department of Fish and Game and the Department of Commerce, National
    Oceanographic and Atmospheric Administration, Marine Sanctuary Program." The strings
    "Cooperative", "Davis, CA" and "Western Regional" occur in its text 0 times each
    (2026-10-10)
  - >-
    The sections are headed ABSTRACT (PDF page 4), EXECUTIVE SUMMARY (5), INTRODUCTION (8),
    METHODS (10), STATION RESULTS AND DISCUSSION (21), GENERAL DISCUSSION (66), ACKNOWLEDGEMENTS
    (75), LITERATURE CITED (76), "Appendix A.  1990 Station Data - All Sampling Methods" (78) and
    "Appendix B." (223). The printed page numbers run from 1 on PDF page 4 and begin again at 1
    on PDF page 78; locators in this record are PDF pages. The contents, PDF pages 2 and 3, list
    "FIGURE 1 Kelp Forest Monitoring Locations in Channel Islands" at page 64 and
    "APPENDIX B.  Species List - All stations". The file's pages carry no image XObject, and
    "FIGURE 1" occurs in its text once, in those contents. PDF page 223 prints the heading "Appendix B." over "1990
    Species List for all Channel Islands National Park Kelp Forest Monitoring Stations.", an
    "Introduction", "Abundance Ratings" and "Notes"; PDF page 224, the last, prints "Station
    names are listed in Table 3 of the text." (2026-10-10)
  - >-
    The PDF's document information dictionary states Creator "Microsoft Word - 90kfmtxt.doc",
    Title "KELP90", Producer "Acrobat PDFWriter 4.0 for Windows", CreationDate
    "D:19990924112138" and ModDate "D:19990924120230-06'00'", and the file's bytes contain
    "xmpmeta" 0 times. Its text is literal strings shown with Tj in its page content streams.
    pypdf 6.19.0's extract_text returns 388,425 characters for the 224 pages, and
    .claude/skills/review-source/pdftext_literal.py prints "PAGES 76 CHARS 83919". Quotations
    from the file in this record are those strings as the content streams show them: where a
    quotation runs across one of the file's line breaks, the line's trailing spaces and the break
    are joined as one space, and the file's other spacing is kept. In the Appendix A headings
    quoted in measures, the "2" after "M" is a string of its own set in 7.5-point type and raised
    above the 12-point line, and is written "M2" here (2026-10-10)
format: >-
  PDF; served as Content-Type application/pdf, 306,257 bytes beginning %PDF-1.3, 224 pages; the
  holding states "MimeType":"application/pdf" and "FileSize":306257
license: not stated
license_stated_at: >-
  Looked for first in the held PDF, whose text contains none of "copyright", "licen", "rights",
  "terms", "disclaim", "permission", "public domain" or "©" in any letter case; then on the
  landing page, https://irma.nps.gov/DataStore/Reference/Profile/68419, whose JSON carries
  "LicenseTypeID":null, "LicenseTypeName":null and "LicenseTypeURL":null and whose delivered
  HTML contains "copyright", "terms of use", "disclaim", "public domain" and "rights reserved" 0
  times each and "licen" 5 times, in those three field names, the field name "LicenseType" and
  its DisplayName "License Type"; POST /DataStore/Reference/GetProfileCoreModel on the same
  reference answers "IntellectualRights":null. The profile's footer is instantiated by its
  scripts rather than delivered as markup: the HTML carries xtype: 'footerComponent', which
  https://irmafiles.nps.gov/WebContent/Irma/Common/v3_0_2/Scripts/ext_7_7_0/Modern/nps-custom-components.js
  renders as the links ACCESSIBILITY, PRIVACY POLICY, FOIA, NOTICES, CONTACT, NO FEAR ACT,
  DISCLAIMER and USA.GOV. DISCLAIMER, https://www.doi.gov/disclaimer, headed by the <title>
  "Disclaimer of Liability and Endorsement | U.S. Department of the Interior", and NOTICES,
  https://www.nps.gov/aboutus/notices.htm, headed by the <title> "Notices (U.S. National Park
  Service)", both answer HTTP 200 and contain "licen", "terms of use" and "public domain" 0 times
  each. "copyright" occurs in any letter case in the first 4 times, in the href and the text of
  each of its two links "Copyright, Restrictions and Permissions Notice" and "Copyright", both to
  /copyright, a page the profile's footer does not link; and in the second 8 times: in the HTML
  comments "Content Copyright National Park Service" and "JavaScript & DHTML Code Copyright
  &copy; 1998-2025, PaperThin, Inc. All Rights Reserved.", in the <h2> "Digital Rights,
  Copyright, Trademark, and Patent Laws" and the sentence under it "All Department of the
  Interior (DOI) and bureau Internet websites comply with existing laws and directives that
  address the digital, copyright, trademark, and patent rights of the public.", in the link texts
  "Digital Millennium Copyright Act" and "Copyright Law", and twice in the URL
  http://www.copyright.gov/, the href and the id of the second of those links (all retrieved
  2026-10-10)
variables: []
measures:
  - "densities and distribution of discrete benthic organisms"
  - "percent cover of encrusting invertebrates, algae, and substrate composition"
  - "fish abundance"
  - "age structure, population recruitment, and growth rates"
  - "Kelp forest monitoring site status"
  - "QUADRAT DATA: MEAN NUMBER PER M2"
  - "BAND TRANSECT DATA: MEAN NUMBER PER M2"
  - "BAND TRANSECT: MEAN NUMBER PER M2"
  - "RANDOM POINT CONTACT DATA: MEAN PERCENT COVER"
  - "FISH TRANSECT DATA: MEAN NUMBER PER TRANSECT"
  - "SIZE FREQUENCY DISTRIBUTIONS"
  - "SIZE FREQUENCIES"
findings: []
coverage: >-
  "As part of the long-term ecological monitoring program, Channel Islands National Park has been
  conducting monitoring of the kelp forests around Santa Barbara, Anacapa, Santa Cruz, Santa
  Rosa, and San Miguel Islands since 1982."; "Population dynamics of 68 taxa or "target species"
  (Table 2) were measured at 16 fixed sites around the five park islands (Fig.  1)."; "Sites were
  monitored between June and October of 1990."; Table 2, captioned "Station information.", lists
  under LOCATION Wyckoff Ledge, Hare Rock, Johnson's Lee North, Johnson's Lee South, Rodes Reef,
  Gull Island South, Fry's Harbor, Pelican Bay, Scorpion Anchorage, Yellowbanks, Admiral's Reef,
  Cathedral Cove, Landing Cove, SE Sea Lion Rookery, Arch Point and Cat Canyon, under ISLAND San
  Miguel, San Miguel, Santa Rosa, Santa Rosa, Santa Rosa, Santa Cruz, Santa Cruz, Santa Cruz,
  Santa Cruz, Santa Cruz, Anacapa, Anacapa, Anacapa, Santa Barbara, Santa Barbara and Santa
  Barbara, and under DEPTH (FEET) 43-49, 20-30, 31-36, 46-52, 43-49, 45-54, 39-42, 21-27, 15-20,
  48-51, 42-49, 20-35, 15-40, 40-46, 22-27 and 22-30. The DataStore's Description of the
  reference: "Quadrants, band transects, random point contacts, size frequencies, fish and video
  transects, photogrammetric plots and species list surveys were used to monitor 68 species of
  algae, fish and invertebrates in the kelp forests of Channel Islands National Park." The
  reference's two linked geographic areas: "CHIS Default Bounding Rectangle", POLYGON
  ((-120.472664 33.4483757, -119.00782 33.4483757, -119.00782 34.23479, -120.472664 34.23479,
  -120.472664 33.4483757)), and "Mediterranean Coast Network  (MEDN). Default Bounding
  Rectangle", POLYGON ((-120.8993 32.53409, -116.5599 32.53409, -116.5599 36.86889, -120.8993
  36.86889, -120.8993 32.53409)); its ContentBeginDate and ContentEndDate are null. Saved search
  1508 lists 26 references, one for each year from 1990 to 2015; this record holds the one file
  the 1990 reference lists, chis_kelp90.pdf, and no file of the other 25
coverage_stated_at: >-
  The first quotation is the first sentence under EXECUTIVE SUMMARY, PDF page 5; the second and
  third are the first and third sentences under METHODS, PDF page 10; Table 2 and its caption are
  on PDF pages 18 and 19, its header printing "DEPTH" over "(FEET)", quoted here with the break
  joined by one space, all of the held PDF, retrieved 2026-10-10; the Description is the
  "Description" of the JSON literal in the HTML of
  https://irma.nps.gov/DataStore/Reference/Profile/68419; the linked geographic areas are the
  answer to POST /DataStore/Reference/ProfileLinkedGeographicAreasModel with
  referenceId=68419&id=68419, and the two dates the answer to POST
  /DataStore/Reference/GetProfileCoreModel with the same parameters; the count of references is
  the answer to POST /DataStore/SavedSearch/GetSavedSearchReferences with savedSearchId=1508
  (all retrieved 2026-10-10)
retrieved: 2026-10-10
fetch_script: src/fetch/cinp_kfm_report_1990.py
file: null
transcribed_from: null
derived_from: null
topics:
  - bed-state/diver-surveys
  - bed-state/community
  - bed-state/mpas
  - grazers-predators-competitors/urchins
  - grazers-predators-competitors/predators
  - ocean-climate/temperature
  - recruitment-connectivity/settlement
regions:
  - scb.islands.anacapa
  - scb.islands.san-miguel
  - scb.islands.santa-barbara
  - scb.islands.santa-cruz
  - scb.islands.santa-rosa
beds: []
sites: []
site_key: []
references: []
human_task: null
---
