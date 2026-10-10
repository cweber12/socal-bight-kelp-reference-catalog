---
id: sandiego_mwqr_sboo
title: SOUTH BAY OCEAN OUTFALL MONTHLY RECEIVING WATERS MONITORING REPORT
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
    which the page prints twice, once in each of two of its navigation menus (2026-10-10)
  - >-
    Under "2026 Monthly Receiving Waters Monitoring Reports for the SBOO" the page prints a list
    of eight links whose texts are "January", "February", "March", "April", "May", "June", "July"
    and "August" and whose hrefs are, in that order, /sites/default/files/2026-02/sbwrp_mwqr_jan_2026.pdf,
    /sites/default/files/2026-03/sbwrp_mwqr_feb_2026.pdf,
    /sites/default/files/2026-04/sbwrp_mwqr_mar_2026.pdf,
    /sites/default/files/2026-05/sbwrp_mwqr_apr_2026.pdf,
    /sites/default/files/2026-07/sbwrp_mwqr_may_2026.pdf,
    /sites/default/files/2026-07/sbwrp_mwqr_jun_2026.pdf,
    /sites/default/files/2026-08/sbwrp_mwqr_jul_2026.pdf and
    /sites/default/files/2026-09/sbwrp_mwqr_aug_2026.pdf; the eight files this record holds. Under
    "SBOO Monthly Receiving Waters Monitoring Report Archives" it prints eleven accordions, each
    headed by a link whose text is a year, "2025" down to "2015", each holding twelve links whose
    texts are the month names "January" to "December", 132 links in all, which this record does not
    hold: 129 of their hrefs end in a file name beginning sbwrp_mwqr_, and 3, the "2020"
    accordion's "September", "October" and "November", end in sbwrp_monthly_sep_2020.pdf,
    sbwrp_monthly_oct_2020.pdf and south_bay_quarterly_nov_2020.pdf. The page also links 11 of the
    129, the "2024" accordion's "January" and "March" to "December", with the same hrefs under "PLOO
    Monthly Receiving Waters Monitoring Report Archives", whose "2024" accordion links "February" to
    a file named ploo_mwqr_feb_2024.pdf. Of the 140 hrefs under the two SBOO headings, 36 are
    relative paths under /sites/default/files/, 101 begin
    http://www.sandiego.gov/sites/default/files/ and 3 begin
    https://www.sandiego.gov/sites/default/files/; each of the 101 answers HTTP 301 with Location
    the same path under https://www.sandiego.gov; and to a HEAD request 139 of the 140 answered
    HTTP 200 with Content-Type application/pdf, while the "2022" accordion's "June",
    http://www.sandiego.gov/sites/default/files/sbwrp_mwqr_jun_2022.pdf, answered HTTP 301 and then
    HTTP 404 with Content-Type text/html; charset=UTF-8 (2026-10-10)
  - >-
    The page's link "Public Utilities Home" opens https://www.sandiego.gov/public-utilities, which
    answers HTTP 200 with Content-Type text/html; charset=UTF-8, no redirect. Its <title> is
    "Public Utilities | City of San Diego Official Website"; inside an <article class="node
    node--type-department-parent node--view-mode-full background-white"> its <h1
    class="single-line dp-title"> is "Public Utilities", and the first <p> under that <h1> begins
    "The City of San Diego Public Utilities Department currently serves more than 2.3 million
    wastewater customers and provides clean and safe drinking water to 1.4 million residents." The
    string "Public Utilities Department" occurs once in its HTML (2026-10-10)
  - >-
    Run src/fetch/sandiego_mwqr_sboo.py, which sends the User-Agent "kelpcatalog/sandiego_mwqr_sboo",
    requests the eight hrefs of the "2026 Monthly Receiving Waters Monitoring Reports for the
    SBOO" list as absolute URLs under https://www.sandiego.gov in the list's order, stores each
    body under its served file name and keeps it only when it begins with the bytes %PDF-; no
    account, key or referrer is required. Each answered HTTP 200 with Content-Type application/pdf,
    no redirect, no Content-Disposition, a Last-Modified and an ETag, and each body begins
    %PDF-1.7. The files, each with its byte count, SHA-256, Last-Modified and ETag as served on
    2026-10-10, are
  - >-
    https://www.sandiego.gov/sites/default/files/2026-02/sbwrp_mwqr_jan_2026.pdf, 2,298,711 bytes,
    97e77f4a19626b6cae6b72667628505ec1189203f44d22a036cf542c4d3df9bd, "Wed, 25 Feb 2026 18:49:20
    GMT", "699f4430-231357"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-03/sbwrp_mwqr_feb_2026.pdf, 2,597,912 bytes,
    6a9102259f0a8d8e6d3b0875e48e5d069e17783368bd39442df81708593fa4c0, "Mon, 23 Mar 2026 16:54:49
    GMT", "69c17059-27a418"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-04/sbwrp_mwqr_mar_2026.pdf, 2,314,123 bytes,
    70b353c682cb8ff8feedb306dc471ee75d6881ea5b4137e976c50ac6e7a6f5f6, "Wed, 22 Apr 2026 14:37:04
    GMT", "69e8dd10-234f8b"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-05/sbwrp_mwqr_apr_2026.pdf, 2,346,508 bytes,
    1b9274cad384286dbc3b9097536b22cf6e7507461ec879331f02c6ad83e4b89d, "Wed, 27 May 2026 18:43:50
    GMT", "6a173b66-23ce0c"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-07/sbwrp_mwqr_may_2026.pdf, 3,317,690 bytes,
    41c87257d37d67f635ab5b5f5814e46541d20f1f3f6578caaabbd58df6ecb19b, "Tue, 07 Jul 2026 17:03:29
    GMT", "6a4d3161-329fba"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-07/sbwrp_mwqr_jun_2026.pdf, 2,350,172 bytes,
    9b6b88da004e67f192672cec4550eec0bef7387cb6df711014d240952104d461, "Wed, 22 Jul 2026 22:03:47
    GMT", "6a613e43-23dc5c"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-08/sbwrp_mwqr_jul_2026.pdf, 2,335,824 bytes,
    87809833f1f2f25e75624822241966375f711973ca232c76c568c0921aa6ee6e, "Mon, 24 Aug 2026 22:11:43
    GMT", "6a8cc19f-23a450"
  - >-
    https://www.sandiego.gov/sites/default/files/2026-09/sbwrp_mwqr_aug_2026.pdf, 3,113,564 bytes,
    05e691cf42e966a5aff3ecc5f2b945e8a2fd1c61d66d60001ef6b9e7b74f4d87, "Tue, 22 Sep 2026 18:05:07
    GMT", "6ab2c353-2f825c"
  - >-
    Each file's first page prints, on separate lines in this order, "SOUTH BAY OCEAN OUTFALL",
    "MONTHLY RECEIVING WATERS", "MONITORING REPORT" (the three lines title joins with one space),
    "SOUTH BAY WATER RECLAMATION PLANT", "NPDES Permit No. CA0109045", a line beginning "SDRWQCB
    Order No." that reads "SDRWQCB Order No. R9-2021-0011" in the January to June files and
    "SDRWQCB Order No. R9-2026-0006" in the July and August files, a line naming the month and
    year, "JANUARY 2026", "FEBRUARY 2026", "MARCH 2026", "APRIL 2026", "MAY 2026", "JUNE 2026",
    "JULY 2026" and "AUGUST 2026" in turn, "Environmental Monitoring and Technical Services", "2392
    Kincaid Road • Mail Station 45A • San Diego, CA 92101" (the bullets U+2022) and "Tel (619)
    758-2300 Fax (619) 758-2309". The first sentence of each file's INTRODUCTION names "Order No.
    R9-2021-0011" in the January, February, March, April and June files, "Order No. R9-2021-0011 as
    amended by Order No. R9-2026-0006" in the May file and "Order No. R9-2026-0006" in the July and
    August files. PDF page 3 of each of the January to July files is a letter headed "Public
    Utilities Department" over "Environmental Monitoring & Technical Services Division", dated the
    last day of the month after the month reported ("August 31, 2026" in the July file), addressed
    "Mr. David W. Gibson, Executive Officer", "California Regional Water Quality Control Board",
    "San Diego Region", "2375 Northside Drive, Suite 100", "San Diego, CA 92108", "Attention: POTW
    Compliance Unit", whose first paragraph reads in the July file "Enclosed is the July 2026
    Monthly Receiving Waters Monitoring Report for the South Bay Ocean Outfall, South Bay Water
    Reclamation Plant as required per Order No. R9-2021-0011 as amended by Order No. R9-2026-0006,
    NPDES Permit No. CA0109045.", the other files naming their own month, the May and June files
    the same Order clause and the January to April files "as required per Order No. R9-2021-0011,
    NPDES Permit No. CA0109045.", and whose second paragraph reads "This report includes raw ocean
    monitoring data and summaries of water quality parameters and ocean conditions measured during
    the month for the South Bay outfall region. Also included are summaries of compliance with the
    bacterial water-contact standards specified in the California Ocean Plan. These data are also
    presented in the monthly report submitted by the International Boundary and Water Commission,
    U.S. Section for discharge from the South Bay International Wastewater Treatment Plant (Order
    No. R9-2021-0001, NPDES Permit No. CA0108928).", signed "Peter S. Vroom, Ph. D." over "Deputy
    Director, Public Utilities Department", with "cc: U.S. Environmental Protection Agency, Region
    9" and the lines "2392 Kincaid Rd, MS 45A,", "San Diego, CA 92101,",
    "www.sandiego.gov/publicutilities", "T (858) 758-2300" and "sandiego.gov"; the August file's
    PDF page 3 comes out of both text extractions named in the next step as strings of digits,
    punctuation and control characters rather than words. The string "Public Utilities" occurs
    twice in the text of each of the January to July files and 0 times in the August file's, and
    "Ocean Monitoring Program", "Submitted", "Prepared" and "Contract" 0 times in each of the
    eight; "City of San Diego" occurs once in each, in the sentence "See the City of San Diego’s
    most recent Biennial Receiving Waters Monitoring and Assessment Report for the Point Loma and
    South Bay Ocean Outfalls for details
    (https://www.sandiego.gov/public-utilities/sustainability/ocean-monitoring/reports)." under
    SUMMARY OF RESULTS, Shoreline Water Quality Sampling, which each of the eight files breaks at a
    line end after "public-", read with the hyphen kept and that break joined with no space as the
    next step states (2026-10-10)
  - >-
    The files have 72, 124, 78, 76, 116, 80, 72 and 114 PDF pages, January to August. In the
    August file PDF pages 5 to 8 print the page numbers 1 to 4 and are headed INTRODUCTION (PDF
    page 5), MATERIALS AND METHODS (5), with the sub-headings Shore Stations, Kelp Bed Stations,
    Offshore Stations and Bacteriological Reporting and Quality Assurance, each of the first three
    referring to a "station locations map", and SUMMARY OF RESULTS (7), with the bullets Shoreline
    Water Quality Sampling, Kelp Bed Water Quality Sampling and Offshore Water Quality Sampling;
    pdftotext returns no text for its PDF pages 2, 4, 9 to 14, 32 to 34, 68 to 70, 111, 112 and
    114; and the tables are captioned Table 2.1 to Table 2.8 (PDF pages 15 to 31, the shore
    stations), Table 3.1 to Table 3.9 (PDF pages 35 to 53, the kelp stations), Figure 3.1 (PDF
    pages 54 to 67, each page's caption reading "Graphics of CTD profile data from the SBOO kelp
    stations for each sample date."), Table 4.1 to Table 4.6 (PDF pages 71 to 93, the offshore
    stations), Figure 4.1 (PDF pages 94 to 110, each page's caption reading "Graphics of CTD
    profile data from the SBOO offshore stations for each sample date.") and Table A.1 (PDF page
    113). The February and May files carry Table 4.1 to Table 4.6 and Figure 4.1 too, and the
    January, March, April, June and July files none of them. Each file prints under MATERIALS AND
    METHODS, Bacteriological Reporting and Quality Assurance, "The six standards are defined as
    follows:" and, after them, "Compliance with the seven Ocean Plan standards are summarized below
    for the stations located in USA waters.", and names "2019 California Ocean Plan" twice and
    "2015 California Ocean Plan" 0 times. Each file's document information dictionary states
    Creator "LaTeX via pandoc" and Author, Subject and Keywords ""; Producer "LuaTeX-1.18.0" in the
    January to June files and "LuaTeX-1.24.0" in the July and August files; and Title "SBOO
    Monthly WQ Report CA 2019" in the January, February, March and April files and "" in the May,
    June, July and August files. The strings pypdf 6.19.0's extract_text returns for the eight
    files total 89,894, 170,098, 99,253, 93,008, 163,077, 100,468, 85,334 and 164,162 characters;
    pdftotext 4.00 with -enc UTF-8 returns, counted with LF line ends, 97,219, 187,003, 107,643,
    100,546, 178,794, 108,607, 91,985 and 178,447; .claude/skills/review-source/pdftext_literal.py
    prints "PAGES 3 CHARS 8928", "PAGES 4 CHARS 9777", "PAGES 3 CHARS 8819", "PAGES 3 CHARS 8625",
    "PAGES 3 CHARS 9454", "PAGES 3 CHARS 8574", "PAGES 3 CHARS 8342" and "PAGES 4 CHARS 9342", and
    pdftext_cmap.py was not run. Where a quotation from a file in this record runs across one of
    the file's line breaks, the break is joined with one space and the file's other spacing is
    kept, as pdftotext 4.00 prints it, an en dash printed at the end of a line included ("S4–"
    ends a line over "S6 and S8–S12)." on PDF page 5 of each file, read "S4– S6"), except that a
    hyphen printed at the end of a line, which pdftotext drops, is kept, as pdftotext 4.00 with
    -layout prints it, and that break is joined with no space: "public-" ends a line over
    "utilities/sustainability/ocean-monitoring/reports)." on PDF page 8 of each file. The strings
    "doi", "citation" and "cite" occur 0 times in the text of each of the eight files in any
    letter case (2026-10-10)
format: >-
  PDF; eight files served as Content-Type application/pdf, 2,298,711, 2,597,912, 2,314,123,
  2,346,508, 3,317,690, 2,350,172, 2,335,824 and 3,113,564 bytes, January to August, each
  beginning %PDF-1.7, of 72, 124, 78, 76, 116, 80, 72 and 114 pages
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
  "rights", "disclaim", "permission" or "©" in any letter case, and "terms" once in each, in "this
  kelp bed has been historically transient and variable in terms of size and density"; then on
  the landing page named in access, whose HTML contains "licen" 0 times, "terms" 0 times,
  "copyright" twice, in the class attribute of the footer <p> quoted first and in its text
  "Copyrighted", and "disclaim" 4 times, in the href and text of "Translation Disclaimer",
  /disclaimers#translations, and of "Disclaimers", /disclaimers, the footer's list of links being
  "Disclaimers", "Privacy Policy", "Accessibility", "Language Translation" and "Contact the City";
  then on https://www.sandiego.gov/disclaimers, which answers HTTP 200 with Content-Type
  text/html; charset=UTF-8, is headed <h1> "Disclaimers" and carries the <h2> headings "Notice to
  City", "Website Availability", "Investor Information", "Prohibitions", "Jurisdiction",
  "Language Translations", "Restrictions on Use of Materials", "Copyright Notice", "Third Party
  Materials", "Disclaimer of Endorsement", "Disclaimer for Hypertext Links", "DISCLAIMER OF
  LIABILITY", "DISCLAIMER OF WARRANTIES / ACCURACY AND USE OF INFORMATION", "EXCEPTION TO
  DISCLAIMERS, IF APPLICABLE" and "Indemnification": the quotation under "Notice to City" is the
  third and fourth sentences of the second paragraph there, the one under "Restrictions on Use of
  Materials" the whole paragraph, the three under "Copyright Notice" its first three paragraphs
  whole, and the one under "Third Party Materials" the whole paragraph.
  https://www.sandiego.gov/privacy-policy, headed <h1> "Privacy Notice", answers HTTP 200 and the
  text of its <main> element contains "licen" once, in "licenses and other business-related
  purposes", and "copyright" and "terms" 0 times (all retrieved 2026-10-10)
variables: []
measures:
  - "total coliform, fecal coliform, and Enterococcus bacteria"
  - "Visual observations of water color and clarity, surf height, human or animal activity, and weather conditions"
  - "Wind speed and direction"
  - "bacteriological analyses (total coliforms, fecal coliforms, and Enterococcus bacteria)"
  - "water column profiles of various physical/chemical parameters"
  - "Visual observations of weather and water conditions"
  - "Water column profiles of the various physical/chemical parameters"
  - "CTD profile data"
  - "measurements of various physical/chemical parameters"
  - "Water column temperatures"
  - "difference between surface and bottom waters"
  - "Concentrations of chlorophyll a"
  - "Chlorophyll a concentrations"
  - "sewage-like odor"
  - "compliance with the Ocean Plan’s 30-day Geometric Mean standard for fecal coliform bacteria"
  - "compliance with the Ocean Plan’s 6-week Geometric Mean standard for Enterococcus"
  - "compliance with the Ocean Plan’s 30-day Median standard for total coliform bacteria"
  - "water quality parameters"
  - "Densities of total coliform (Total), fecal coliform (Fecal) and Enterococcus (Entero)"
  - "Densities of total coliform (Total), fecal coliform (Fecal), and Enterococcus (Entero) bacteria"
  - "visual observations"
  - "bacteriological quality assurance field and lab duplicate sample analyses"
  - "Densities of total coliform (Total), fecal coliform (Fecal), and Enterococcus (Entero)"
  - "Temp (°C)"
  - "XMS (%)"
  - "DO (mg/l)"
  - "Sal (ppt)"
  - "pH"
  - "Dens (σ-t)"
  - "Chlor (μg/L)"
findings: []
coverage: >-
  "The seven kelp bed water quality stations (I19, I24, I25, I26, I32, I39, I40) were sampled on
  January 6, 12, 20, and 27."; "The seven kelp bed water quality stations (I19, I24, I25, I26, I32,
  I39, I40) were sampled on February 2, 9, 19, and 24."; "The seven kelp bed water quality
  stations (I19, I24, I25, I26, I32, I39, I40) were sampled on March 3, 10, 17, 24, and 30."; "The
  seven kelp bed water quality stations (I19, I24, I25, I26, I32, I39, I40) were sampled on April
  6, 14, 21, and 28."; "The seven kelp bed water quality stations (I19, I24, I25, I26, I32, I39,
  I40) were sampled on May 4, 11, 19, and 26."; "The seven kelp bed water quality stations (I19,
  I24, I25, I26, I32, I39, I40) were sampled on June 2, 9, 16, 24, and 29."; "The seven kelp bed
  water quality stations (I19, I24, I25, I26, I32, I39, I40) were sampled on July 6, 16, 20, and
  30."; "The seven kelp bed water quality stations (I19, I24, I25, I26, I32, I39, I40) were
  sampled on August 3, 10, 17, and 25."; "Quarterly sampling was not conducted during January at
  the offshore stations. The next quarterly sampling is scheduled for February 2026."; "Quarterly
  sampling was not conducted during June at the offshore stations. The next quarterly sampling is
  scheduled for August 2026."; "Quarterly offshore water quality sampling was conducted over three
  days during the month (i.e., February 4, 5, 6)."; "Quarterly offshore water quality sampling was
  conducted over three days during the month (i.e., May 6, 7, 8)."; "Quarterly offshore water
  quality sampling was conducted over three days during the month (i.e., August 11, 13, 14).";
  "Monthly reports of water quality and ocean conditions from Playa Blanco, Mexico to Coronado, USA
  are submitted to the San Diego Regional Water Quality Control Board and U.S. EPA Region 9 in
  accordance with Order No. R9-2026-0006, NPDES Permit No. CA0109045, for the South Bay Water
  Reclamation Plant (SBWRP), South Bay Ocean Outfall (SBOO). This report includes receiving waters
  monitoring data collected from all shore, kelp and offshore stations specified in the above
  order. Data for influent and effluent monitoring activities for the SBWRP are presented in
  separate reports."; "Water quality monitoring was conducted at 11 stations located along the
  shore from Playa Blanca, Mexico to Coronado, USA (see station locations map). Three sites are
  located south of the international border (stations S0, S2, S3), while eight sites are in the
  United States (stations S4– S6 and S8–S12)."; "Due to site access restrictions in Mexico, the
  South Bay shoreline sampling is typically carried out on the same day each week (i.e., Tuesday)
  to coordinate sampling between the Mexican and USA based stations. Seawater samples at the three
  shore stations located south of the USA/Mexico border (i.e., stations S0, S2 and S3) are
  presently collected by the Comisión Internacional de Límites y Aguas (CILA) and transported to
  the USIBWC for subsequent delivery to the City’s Marine Microbiology Lab, while samples from the
  eight stations located in USA waters are sampled by City staff."; "Seven kelp bed and other
  nearshore stations (I19, I24, I25, I26, I32, I39, I40; collectively referred to as “kelp”
  stations herein) were sampled weekly according to NPDES permit specifications. Six stations
  (I19, I24, I25, I26, I32, I40) are located along the 9-m depth contour, and one (I39) is located
  along the 18-m depth contour. Three of these stations, I25, I26, and I39, were selected based on
  their proximity to suitable substrates for the Imperial Beach kelp bed (see station locations
  map); however, this kelp bed has been historically transient and variable in terms of size and
  density. Thus, these three stations are only occasionally located within an area where kelp is
  actually found."; "Quarterly offshore water quality sampling is typically conducted over three
  days during February, May, August, and November for a total of 40 stations during each month
  (see station locations map). These offshore stations (I1–I40) are arranged in a grid surrounding
  the discharge site, and are generally located along the 9, 19, 28, 38, and 55-m depth contours.
  The seven offshore sites designated as kelp bed stations (described above) are included as part
  of the quarterly offshore water quality sampling, however the data from these seven stations are
  reported within the kelp bed station section of the report with the other days of kelp bed
  water quality sampling. Monitoring at all sites included measurements of various
  physical/chemical parameters, including water temperature, salinity, density, dissolved oxygen,
  pH, chlorophyll a, transmissivity, and chromomorphic dissolved organic matter (CDOM). Visual
  observations of weather and water conditions were also recorded at all stations. Seawater
  samples for the analysis of indicator bacteria were collected at 28 of the stations.";
  "Compliance with the seven Ocean Plan standards are summarized below for the stations located in
  USA waters. In contrast, no such compliance summaries are presented for the three shore
  stations located in Mexican waters south of the International Border (i.e., S0, S2, and S3)
  since this region is not subject to the Ocean Plan standards." The City's monthly water quality
  reports page lists 140 files under its two SBOO headings, eight under "2026 Monthly Receiving
  Waters Monitoring Reports for the SBOO" and 132 under "SBOO Monthly Receiving Waters Monitoring
  Report Archives"; this record holds the eight under the 2026 heading (2026-10-10), whose first
  pages print "JANUARY 2026", "FEBRUARY 2026", "MARCH 2026", "APRIL 2026", "MAY 2026", "JUNE 2026",
  "JULY 2026" and "AUGUST 2026", and none of the 132
coverage_stated_at: >-
  The first eight quotations are each the first bullet under Kelp Bed Water Quality Sampling in
  SUMMARY OF RESULTS of the January to August files in turn, on PDF page 8 (printed page 4) of
  each. The ninth is the first bullet under Offshore Water Quality Sampling in SUMMARY OF RESULTS
  of the January file, PDF page 8, which the March, April and June files print with their own
  month and "May 2026", "May 2026" and "August 2026" in turn; the tenth is that bullet of the July
  file, PDF page 8, which names June rather than July, as the June file's bullet does; and the
  eleventh, twelfth and thirteenth are the first bullet under Offshore Water Quality Sampling of the February, May and August files
  in turn, each on PDF page 8. The fourteenth is the paragraph under INTRODUCTION in the August
  file, PDF page 5 (printed page 1), which each file prints with the Order number access states
  for it. The fifteenth is the first paragraph under MATERIALS AND METHODS, Shore Stations, in the
  August file, PDF page 5, which names "Playa Blanca" where the fourteenth names "Playa Blanco".
  The sixteenth is the first bullet under Shoreline Water Quality Sampling in SUMMARY OF RESULTS of
  the August file, PDF page 7 (printed page 3). The seventeenth is the first paragraph under
  MATERIALS AND METHODS, Kelp Bed Stations, in the August file, PDF page 5. The eighteenth is the
  first paragraph under MATERIALS AND METHODS, Offshore Stations, in the August file, PDF page 6
  (printed page 2). The nineteenth is the paragraph after the Water-Contact Objectives under
  MATERIALS AND METHODS, Bacteriological Reporting and Quality Assurance, in the August file, PDF
  page 7. Each of the eight files prints the fifteenth to nineteenth as quoted. All retrieved
  2026-10-10. The two headings and the counts under them are on the City's monthly water quality
  reports page named in access, and the month lines are on PDF page 1 of each held file
  (2026-10-10)
retrieved: 2026-10-10
fetch_script: src/fetch/sandiego_mwqr_sboo.py
file: null
transcribed_from: null
derived_from: null
topics:
  - water-quality-harvest/discharges-outfalls
  - water-quality-harvest/runoff-sedimentation
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
