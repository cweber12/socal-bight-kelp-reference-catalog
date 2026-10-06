---
id: sandiego_mwqr_ploo
title: POINT LOMA OCEAN OUTFALL MONTHLY RECEIVING WATERS MONITORING REPORT
steward: Public Utilities, City of San Diego
url: https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/monthly-report-archives
doi: null
citations: []
status: VERIFIED
tier: FETCHED
access:
  - >-
    https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/monthly-report-archives,
    the City's monthly water quality reports page, answers HTTP 200 with Content-Type text/html;
    charset=UTF-8, no redirect. Its <title> is "Monthly Water Quality Reports | City of San Diego
    Official Website" and its <h1> "Monthly Water Quality Reports". Above the <h1> it prints <p
    class="h1 main__heading">Public Utilities</p> over a <nav aria-label="Department top menu">
    whose <ul id="department-top-menu"> begins with a link whose text is "Public Utilities Home"
    and whose href is /public-utilities, and the first item of the <ul
    id="department-top-menu-mobile"> under "Site Menu" is the same link with the same text, so the
    page prints that link twice. Under the <h1> it prints one paragraph of two sentences, "Monthly
    reports of water quality and ocean conditions for the San Diego coastal region surrounding the
    Point Loma Ocean Outfall (PLOO) and the South Bay Ocean Outfall (SBOO) are submitted to the San
    Diego Regional Water Quality Control Board and U.S. EPA Region 9 in accordance with National
    Pollutant Discharge Elimination System (NPDES) permit requirements." and "These reports include
    receiving waters monitoring data collected from all NPDES mandated shore, kelp and offshore
    stations.", then four <h2 class="h3"> headings in this order: "2026 Monthly Receiving Waters
    Monitoring Reports for the PLOO", "2026 Monthly Receiving Waters Monitoring Reports for the
    SBOO", "PLOO Monthly Receiving Waters Monitoring Report Archives" and "SBOO Monthly Receiving
    Waters Monitoring Report Archives", the first two with U+00A0 between "2026" and "Monthly".
    The strings "cite" and "citation" occur in its HTML 0 and 4 times in any letter case, the 4
    being the text and the href of the navigation link "Parking Citations", /parking/citations,
    which the page prints twice, once in each of two of its navigation menus (2026-10-05)
  - >-
    Under "2026 Monthly Receiving Waters Monitoring Reports for the PLOO" the page prints a list
    of eight links whose texts are "January", "February", "March", "April", "May", "June", "July"
    and "August" and whose hrefs are, in that order, /sites/default/files/2026-02/ploo_mwqr_jan_2026.pdf,
    /sites/default/files/2026-03/ploo_mwqr_feb_2026.pdf,
    /sites/default/files/2026-04/ploo_mwqr_mar_2026.pdf,
    /sites/default/files/2026-05/ploo_mwqr_apr_2026.pdf,
    /sites/default/files/2026-07/ploo_mwqr_may_2026.pdf,
    /sites/default/files/2026-07/ploo_mwqr_jun_2026.pdf,
    /sites/default/files/2026-08/ploo_mwqr_jul_2026.pdf and
    /sites/default/files/2026-09/ploo_mwqr_aug_2026.pdf; the eight files this record holds. Under
    "PLOO Monthly Receiving Waters Monitoring Report Archives" it prints eleven accordions, each
    headed by a link whose text is a year, "2025" down to "2015", each holding twelve links whose
    texts are the month names "January" to "December", 132 links in all, which this record does not
    hold: 117 of their hrefs end in a file name beginning ploo_mwqr_; 4 end in
    point_loma_mwqr_jan_2021.pdf, point_loma_monthly_sep_2020.pdf, ploo_monthly_oct_2020.pdf and
    point_loma_quarterly_nov_2020.pdf; and 11, the "2024" accordion's "January" and "March" to
    "December", end in file names beginning sbwrp_mwqr_, each of which the page also links under
    "SBOO Monthly Receiving Waters Monitoring Report Archives". Of the 140 hrefs under the two
    PLOO headings, 36 are relative paths under /sites/default/files/, 97 begin
    http://www.sandiego.gov/sites/default/files/ and 7 begin
    https://www.sandiego.gov/sites/default/files/; each of the 97 answers HTTP 301 with Location
    the same path under https://www.sandiego.gov; and to a HEAD request 139 of the 140 answered
    HTTP 200 with Content-Type application/pdf, while the "2020" accordion's "May",
    http://www.sandiego.gov/sites/default/files/ploo_mwqr_may_2020_revised.pdf, answered HTTP 301
    and then HTTP 404 with Content-Type text/html; charset=UTF-8 (2026-10-05)
  - >-
    The page's link "Public Utilities Home" opens https://www.sandiego.gov/public-utilities, which
    answers HTTP 200 with Content-Type text/html; charset=UTF-8, no redirect. Its <title> is
    "Public Utilities | City of San Diego Official Website"; inside an <article class="node
    node--type-department-parent node--view-mode-full background-white"> its <h1
    class="single-line dp-title"> is "Public Utilities", and the first <p> under that <h1> begins
    "The City of San Diego Public Utilities Department currently serves more than 2.3 million
    wastewater customers and provides clean and safe drinking water to 1.4 million residents." The
    string "Public Utilities Department" occurs once in its HTML (2026-10-05)
  - >-
    Run src/fetch/sandiego_mwqr_ploo.py, which sends the User-Agent "kelpcatalog/sandiego_mwqr_ploo",
    requests the eight hrefs of the "2026 Monthly Receiving Waters Monitoring Reports for the
    PLOO" list as absolute URLs under https://www.sandiego.gov in the list's order, stores each
    body under its served file name and keeps it only when it begins with the bytes %PDF-; no
    account, key or referrer is required. Each answered HTTP 200 with Content-Type application/pdf,
    no redirect, no Content-Disposition, a Last-Modified and an ETag, and each body begins
    %PDF-1.7. The files, each with its byte count, SHA-256, Last-Modified and ETag as served on
    2026-10-05, are
  - >-
    https://www.sandiego.gov/sites/default/files/2026-02/ploo_mwqr_jan_2026.pdf, 2,672,293 bytes,
    16c8003b3eb30f5e3cf3df4da5a8f06a6bec512b7159f73bfb2bcc1109d656ef, "Wed, 25 Feb 2026 18:48:36
    GMT", "699f4404-28c6a5"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-03/ploo_mwqr_feb_2026.pdf, 3,476,230 bytes,
    1c9f1a56c22e81da23c77e30b7be6d955bb45656faadee38d5431fd18e7adc54, "Mon, 23 Mar 2026 16:54:09
    GMT", "69c17031-350b06"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-04/ploo_mwqr_mar_2026.pdf, 2,464,391 bytes,
    b986ac3c048756e348721e229309ea67c4e2940d0682f051da2c287d00e1ebc7, "Wed, 22 Apr 2026 14:36:29
    GMT", "69e8dced-259a87"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-05/ploo_mwqr_apr_2026.pdf, 2,489,967 bytes,
    ebbc7610418dc621faf2d73fdadd108d11a62308dfa0a09209a3a9c7157d5974, "Wed, 27 May 2026 18:42:55
    GMT", "6a173b2f-25fe6f"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-07/ploo_mwqr_may_2026.pdf, 3,570,691 bytes,
    5b10a435735d5063f441773a09e60946c63967406fbeeb33f61ea56e55afb5e3, "Tue, 07 Jul 2026 17:01:32
    GMT", "6a4d30ec-367c03"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-07/ploo_mwqr_jun_2026.pdf, 2,399,457 bytes,
    693320960bfa633b5c00250a6091ffc52dc63eee4b1f835086927840115a67a4, "Wed, 22 Jul 2026 22:02:50
    GMT", "6a613e0a-249ce1"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-08/ploo_mwqr_jul_2026.pdf, 2,407,416 bytes,
    0334cf6f586e6958f6a171c1a3c01f7de6960949f173591fa7f6aabdfcc8a813, "Mon, 24 Aug 2026 22:10:57
    GMT", "6a8cc171-24bbf8"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-09/ploo_mwqr_aug_2026.pdf, 3,390,552 bytes,
    69a0034e493fa87e80e6614b42a22abb44a56cd80ffad06eda7b2264d2abac23, "Tue, 22 Sep 2026 18:04:29
    GMT", "6ab2c32d-33bc58"
  - >-
    Each file's first page prints, on separate lines in this order except where the May file
    differs as stated below, "POINT LOMA OCEAN OUTFALL",
    "MONTHLY RECEIVING WATERS", "MONITORING REPORT" (the three lines title joins with one space),
    "POINT LOMA", "WASTEWATER TREATMENT PLANT", "NPDES Permit No. CA0107409", a line beginning
    "SDRWQCB Order No." that reads "SDRWQCB Order No. R9-2017-0007" in the January, February,
    March, April, May and August files and "SDRWQCB Order No. R9-2026-0002" in the June and July
    files, a line naming the month and year, "JANUARY 2026", "FEBRUARY 2026", "MARCH 2026",
    "APRIL 2026", "MAY 2026", "JUNE 2026", "JULY 2026" and "AUGUST 2026" in turn, "Environmental
    Monitoring and Technical Services", "2392 Kincaid Road • Mail Station 45A • San Diego, CA
    92101" (the bullets U+2022) and "Tel (619) 758-2300 Fax (619) 758-2309", where the May file's
    address line ends "Tel", reading "2392 Kincaid Road • Mail Station 45A • San Diego, CA 92101
    Tel" over "(619) 758-2300 Fax (619) 758-2309". The first sentence of each file's INTRODUCTION
    names "Order No. R9-2017-0007" in the January, February, March, April and June files and
    "Order No. R9-2026-0002" in the May, July and August files, beside the cover's R9-2017-0007 in
    the January to May and August files and R9-2026-0002 in the June and July files. PDF page 3 of each of
    the January to July files is a letter headed "Public Utilities Department" over "Environmental
    Monitoring & Technical Services Division", dated the last day of the month after the month
    reported ("August 31, 2026" in the July file), addressed "Mr. David W. Gibson, Executive
    Officer", "California Regional Water Quality Control Board", "San Diego Region", "2375
    Northside Drive, Suite 100", "San Diego, CA 92108", "Attention: POTW Compliance Unit", whose
    second paragraph reads "This report includes raw ocean monitoring data and summaries of water
    quality parameters and ocean conditions measured during the month for the Point Loma outfall
    region. Also included are summaries of compliance with the bacterial water-contact standards
    specified in the California Ocean Plan.", signed "Peter S. Vroom, Ph. D." over "Deputy
    Director, Public Utilities Department", with "cc: U.S. Environmental Protection Agency, Region
    9" and the lines "2392 Kincaid Rd, MS 45A,", "San Diego, CA 92101,",
    "www.sandiego.gov/publicutilities", "T (858) 758-2300" and "sandiego.gov"; the August file's
    PDF page 3 comes out of both text extractions named in the next step as strings of digits and
    slashes rather than words. The string "Public Utilities" occurs twice in the text of each of
    the January to July files and 0 times in the August file's, and "Ocean Monitoring Program",
    "Submitted", "Prepared" and "Contract" 0 times in each of the eight; "City of San Diego"
    occurs once in each, in the sentence "See the City of San Diego’s most recent Biennial
    Receiving Waters Monitoring and Assessment Report for the Point Loma and South Bay Ocean
    Outfalls for details (https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports)."
    under SUMMARY OF RESULTS, Shore Stations, which the February, May and August files break at a
    line end after "ocean-", read with the hyphen kept and that break joined with no space as the
    next step states (2026-10-05)
  - >-
    The files have 90, 172, 98, 94, 144, 80, 74 and 148 PDF pages, January to August. In the July
    file PDF pages 5 to 8 print the page numbers 1 to 4 and are headed INTRODUCTION (PDF page 5),
    MATERIALS AND METHODS (5), with the sub-headings Shore Stations, Kelp Bed Stations, Offshore
    Stations and Bacteriological Reporting and Quality Assurance, and SUMMARY OF RESULTS (7), with
    the sub-headings Shore Stations, Kelp Bed Stations and Offshore Stations; PDF pages 9 to 14
    carry no text, MATERIALS AND METHODS, Shore Stations, referring to a "station locations map";
    the tables are
    captioned Table 2.1 to Table 2.8 (PDF pages 15 to 29, the shore stations), Table 3.1 to Table
    3.7 (PDF pages 33 to 53, the kelp stations), Figure 3.1 (PDF pages 54 to 69, each page's
    caption reading "Graphics of CTD profile data from the SBOO kelp stations for each sample
    date.") and Table A.1 (PDF page 73). The SUMMARY OF RESULTS of the January, February, March and
    April files names "2015 California Ocean Plan" 2, 3, 2 and 2 times and "2019 California Ocean
    Plan" 0 times, and that of the May, June, July and August files "2019 California Ocean Plan"
    1, 2, 2 and 1 times and "2015 California Ocean Plan" 0 times. Each file's document information
    dictionary states Creator "LaTeX via pandoc" and Author, Subject and Keywords ""; Producer
    "LuaTeX-1.18.0" in the January to May files and "LuaTeX-1.24.0" in the June to August files;
    and Title "SBOO Monthly WQ Report CA 2019" in the January, February, March and April files
    and "" in the May, June, July and August files. The strings pypdf 6.19.0's extract_text returns
    for the eight files total 100,421, 283,208, 113,451, 103,492, 291,392, 103,868, 92,175 and
    313,396 characters; pdftotext 4.00 with -enc UTF-8 returns, counted with LF line ends,
    110,157, 316,927, 124,716, 113,255, 330,479, 114,735, 101,375 and 353,769;
    .claude/skills/review-source/pdftext_literal.py prints
    "PAGES 0 CHARS 0" for the January file and "PAGES 3 CHARS 7653", "PAGES 3 CHARS 6743", "PAGES
    3 CHARS 7127", "PAGES 3 CHARS 7676", "PAGES 3 CHARS 6429", "PAGES 3 CHARS 6334" and "PAGES 3
    CHARS 7754" for the others, and pdftext_cmap.py was not run. Where a quotation from a file in
    this record runs across one of the file's line breaks, the break is joined with one space and
    the file's other spacing is kept, as pdftotext 4.00 prints it, except that a hyphen printed at
    the end of a line, which pdftotext drops, is kept, as pdftotext 4.00 with -layout prints it,
    and that break is joined with no space: "(F01-" ends a line over "F03," on PDF page 6 of the
    July file, and "ocean-" ends a line over "monitoring/reports)." on PDF page 7 of the February,
    May and August files. The strings "doi", "citation"
    and "cite" occur 0 times in the text of each of the eight files in any letter case
    (2026-10-05)
format: >-
  PDF; eight files served as Content-Type application/pdf, 2,672,293, 3,476,230, 2,464,391,
  2,489,967, 3,570,691, 2,399,457, 2,407,416 and 3,390,552 bytes, January to August, each
  beginning %PDF-1.7, of 90, 172, 98, 94, 144, 80, 74 and 148 pages
license: >-
  "Copyrighted © 2002-2026" over "City of San Diego. All rights reserved.", the footer of
  https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports/monthly-report-archives.
  The page that footer links as "Disclaimers", https://www.sandiego.gov/disclaimers, states under
  "Notice to City" "Except for the third party materials described below, the materials and
  information on this site were generated, compiled, or assembled at public expense and are freely
  available for non-commercial, non-profit making use, provided the user keeps intact all
  associated copyright, trademark, and other proprietary notices. The materials and information on
  this site may not be "mirrored" on another server without the written permission of the
  Department of Information Technology."; under "Restrictions on Use of Materials" "This site is
  operated and maintained by the City of San Diego through its Department of Information
  Technology. Except as provided herein, no material or information from this site may be copied,
  reproduced, republished, uploaded, posted, transmitted, or distributed except as authorized in
  this notice, expressly authorized within this site, or approved in writing by the Department of
  Information Technology."; under "Copyright Notice" "Unless a copyright is indicated, information
  on the City of San Diego Web site is in the public domain and may be reproduced, published or
  otherwise used with the City of San Diego's permission. We request only that the City of San
  Diego be cited as the source of the information and that any photo credits, graphics or byline
  be similarly credited to the photographer, author or City of San Diego, as appropriate.", "If a
  copyright is indicated on a photo, graphic, or any other material, permission to copy these
  materials must be obtained from the original source." and "Using or modifying this site's
  materials and information for commercial or profit making purposes is prohibited and may violate
  the copyrights and/or other proprietary rights of the City of San Diego or third parties."; and
  under "Third Party Materials" "Some materials and information used on the City of San Diego's
  Web site were generated by third parties who have consented to the City's use or placement of
  such materials on this site. These materials are owned by those parties. Use of these third
  party materials for any purpose is prohibited. Persons seeking to use or modify third party
  materials for any purpose should contact the owner of such materials directly. These materials
  include icons and graphics used in links to other organizations' sites, as well as various items
  of general content."
license_stated_at: >-
  Looked for first in the eight held PDFs, whose text contains none of "copyright", "licen",
  "rights", "terms", "disclaim", "permission" or "©" in any letter case; then on the landing page
  named in access, whose HTML contains "licen" 0 times, "terms" 0 times, "copyright" twice, in
  the class attribute of the footer <p> quoted first and in its text "Copyrighted", and "disclaim"
  4 times, in the href and text of "Translation Disclaimer", /disclaimers#translations, and of
  "Disclaimers", /disclaimers, the footer's list of links being "Disclaimers", "Privacy Policy",
  "Accessibility", "Language Translation" and "Contact the City"; then on
  https://www.sandiego.gov/disclaimers, which answers HTTP 200 with Content-Type text/html;
  charset=UTF-8, is headed <h1> "Disclaimers" and carries the <h2> headings "Notice to City",
  "Website Availability", "Investor Information", "Prohibitions", "Jurisdiction", "Language
  Translations", "Restrictions on Use of Materials", "Copyright Notice", "Third Party Materials",
  "Disclaimer of Endorsement", "Disclaimer for Hypertext Links", "DISCLAIMER OF LIABILITY",
  "DISCLAIMER OF WARRANTIES / ACCURACY AND USE OF INFORMATION", "EXCEPTION TO DISCLAIMERS, IF
  APPLICABLE" and "Indemnification": the quotation under "Notice to City" is the third and fourth
  sentences of the second paragraph there, the one under "Restrictions on Use of Materials" the
  whole paragraph, the three under "Copyright Notice" its first three paragraphs whole, and the one
  under "Third Party Materials" the whole paragraph. https://www.sandiego.gov/privacy-policy,
  headed <h1> "Privacy Notice", answers HTTP 200 and the text of its <main> element contains
  "licen" once, in "licenses and other business-related purposes", and "copyright" and "terms" 0
  times (all retrieved 2026-10-05)
variables: []
measures:
  - "fecal indicator bacteria (FIB)"
  - "Visual observations of water color and clarity, surf height, human or animal activity, and weather conditions"
  - "Wind speed and direction"
  - "Water column profiles of temperature, transmissivity, dissolved oxygen, pH, salinity, density, chlorophyll a"
  - "measurements of Enterococcus bacteria, water temperature, salinity, density, dissolved oxygen, pH, chlorophyll a, transmissivity, chromomorphic dissolved organic matter (CDOM), and visual observations of weather and water conditions"
  - "Water column temperatures"
  - "difference between surface and bottom waters"
  - "Chlorophyll a concentrations"
  - "compliance with the Ocean Plan’s 30-day Geometric Mean standard for fecal coliform bacteria"
  - "compliance with the Ocean Plan’s 6-week Geometric Mean standard for Enterococcus"
  - "compliance with the Ocean Plan’s 30-day Median standard for total coliform bacteria"
  - "water quality parameters"
  - "visual observations"
  - "CTD profile data"
  - "bacteriological quality assurance field and lab duplicate sample analyses"
  - "Densities of fecal coliform (Fecal) and Enterococcus (Entero)"
  - "Densities of fecal coliform (Fecal), and Enterococcus (Entero) bacteria"
  - "Densities of total coliform (Total), fecal coliform (Fecal), and Enterococcus (Entero)"
  - "Temp (°C)"
  - "XMS (%)"
  - "DO (mg/l)"
  - "Sal (ppt)"
  - "pH"
  - "Dens (σ-t)"
  - "Chlor (μg/L)"
  - "CDOM (ppb)"
findings: []
coverage: >-
  "The eight kelp bed water quality stations (A1, A6, A7, C4, C5, C6, C7, C8) were sampled on
  January 6, 12, 20, and 27."; "The eight kelp bed water quality stations (A1, A6, A7, C4, C5, C6,
  C7, C8) were sampled on February 2, 9, 19, and 24."; "The eight kelp bed water quality stations
  (A1, A6, A7, C4, C5, C6, C7, C8) were sampled on March 3, 10, 17, 24, and 30."; "The eight kelp
  bed water quality stations (A1, A6, A7, C4, C5, C6, C7, C8) were sampled on April 6, 14, 21, and
  28."; "The eight kelp bed water quality stations (A1, A6, A7, C4, C5, C6, C7, C8) were sampled on
  May 4, 11, 19, and 26."; "The eight kelp bed water quality stations (A1, A6, A7, C4, C5, C6, C7,
  C8) were sampled on June 2, 9, 16, 24, and 29."; "The eight kelp bed water quality stations (A1,
  A6, A7, C4, C5, C6, C7, C8) were sampled on July 6, 16, 20, and 30."; "The eight kelp bed water
  quality stations (A1, A6, A7, C4, C5, C6, C7, C8) were sampled on August 3, 10, 17, and 25.";
  "The eight shore stations (D4, D5, D7, D8, D9, D10, D11, D12) were sampled on July 1, 8, 15, 22,
  and 29."; "The eight shore stations (D4, D5, D7, D8-B, D9, D10, D11, D12) were sampled on
  February 4, 11, 12, 19, and 25."; "Quarterly water quality sampling was not conducted during July
  at the offshore stations. The next quarterly sampling is scheduled for August 2026.";
  "Quarterly offshore water quality sampling was conducted on February 10, 11, and 12.";
  "Quarterly offshore water quality sampling was conducted on May 12, 13, and 14."; "Quarterly
  offshore water quality sampling was conducted on August 18, 19, and 20."; "Monthly reports of
  water quality and ocean conditions for the San Diego coastal region surrounding the Point Loma
  Ocean Outfall are submitted to the San Diego Regional Water Quality Control Board and U.S. EPA
  Region 9 in accordance with Order No. R9-2026-0002, NPDES Permit No. CA0107409 for the Point
  Loma Wastewater Treatment Plant (PLWTP), Point Loma Ocean Outfall (PLOO)."; "Water quality
  conditions are required to be monitored at eight shoreline stations, including D4, D5, D7, D8,
  D9, D10, D11 and D12, which range from the tip of the Point Loma Peninsula to west of Mission
  Bay (see station locations map). Over the past several years, due to increasing instability in
  several cliffside areas of Point Loma, City staff have been unable to safely access and sample
  several stations at various times."; "Over the past several years, due to increasing instability
  in some cliffside areas of Point Loma, City staff have periodically been unable to safely access
  and sample some stations. As a result, the after consultation with and approval by the Regional
  Board, the sampling location has varied between D8, D8-A and D8-B. Access to site D8 was
  recently restored and sampling at D8 resumed in March 2025."; "The eight kelp stations are
  sampled weekly according to permit specifications to monitor water quality conditions within the
  Point Loma kelp forest. These stations include three sites located along the inshore edge of the
  kelp bed paralleling the 9-m depth contour (i.e., stations C4, C5 and C6), and five sites
  located near the offshore edge of the kelp bed along the 18-m depth contour (i.e., stations A1,
  A6, A7, C7 and C8)."; "Offshore water quality sampling is conducted quarterly typically during
  the months of February, May, August, and November. A total of 36 offshore stations (F01–F36) are
  sampled during each survey usually over a 3-day period. Three of the stations (F01–F03) are
  located along the 18 m depth contour, while 11 stations are located along each of the following
  contours: 60 m (stations F04–F14), 80 m (stations F15–F25), and 98 m (stations F26–F36). Of these
  36 stations, 15 (F01-F03, F06-F14, F18-F20) are located within State jurisdictional waters
  (i.e., within 3 nautical miles of shore) and are subject to the California Ocean Plan’s
  compliance standards." The City's monthly water quality reports page lists 140 files under its
  two PLOO headings, eight under "2026 Monthly Receiving Waters Monitoring Reports for the PLOO"
  and 132 under "PLOO Monthly Receiving Waters Monitoring Report Archives"; this record holds the
  eight under the 2026 heading (2026-10-05), whose first pages print "JANUARY 2026", "FEBRUARY
  2026", "MARCH 2026", "APRIL 2026", "MAY 2026", "JUNE 2026", "JULY 2026" and "AUGUST 2026", and
  none of the 132
coverage_stated_at: >-
  The first eight quotations are each the first bullet under Kelp Bed Stations in SUMMARY OF
  RESULTS of the January to August files in turn, on PDF page 7 (printed page 3) of the January,
  March, June and July files and PDF page 8 (printed page 4) of the February, April, May and
  August files. The ninth is the first bullet under Shore Stations in SUMMARY OF RESULTS of the
  July file, PDF page 7 (printed page 3), and the tenth the same bullet of the February file, PDF
  page 7; that bullet lists "D8" in the January, March, April, June and July files and "D8-B" in
  the February, May and August files. The eleventh is the one bullet under Offshore Stations in
  SUMMARY OF RESULTS of the July file, PDF page 8 (printed page 4), which the January, March,
  April and June files print with their own month and next survey month; the twelfth, thirteenth
  and fourteenth are that bullet of the February, May and August files in turn, each on PDF page 8
  (printed page 4). The fifteenth opens INTRODUCTION in the July file, PDF page 5 (printed page 1),
  the Order number in it differing between files as access states. The sixteenth is the first two
  sentences under MATERIALS AND METHODS, Shore Stations, in the July file, PDF page 5, which all
  eight files print; the January to May and August files follow them with "This has resulted in
  the following modifications:" and a bullet, and the seventeenth is that bullet of the February
  file, PDF page 5, which the June and July files do not print. The eighteenth is the first two
  sentences under MATERIALS AND METHODS, Kelp Bed Stations, in the July file, PDF page 5. The
  nineteenth is the paragraph under MATERIALS AND METHODS, Offshore Stations, in the July file, PDF
  page 6 (printed page 2), to the end of its fourth sentence; the February, May and August files
  print its first sentence with "February, May, August and November", without the comma after
  "August". All retrieved 2026-10-05. The two headings and the counts under them are on the City's
  monthly water quality reports page named in access, and the month lines are on PDF page 1 of
  each held file (2026-10-05)
retrieved: 2026-10-05
fetch_script: src/fetch/sandiego_mwqr_ploo.py
file: null
transcribed_from: null
derived_from: null
topics:
  - water-quality-harvest/discharges-outfalls
  - ocean-climate/temperature
  - ocean-climate/salinity
  - ocean-climate/oxygen-ph
  - ocean-climate
regions:
  - scb
beds: []
sites: []
site_key: []
references: []
human_task: null
---
