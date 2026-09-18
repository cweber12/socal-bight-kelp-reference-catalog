---
id: cinp_kfm
title: >-
  Kelp Forest Monitoring at Channel Islands National Park (CHIS) by the Mediterranean Coast
  Inventory and Monitoring Network (MEDN) 1982-2025 : Data Package
steward: Channel Islands National Park
url: https://irma.nps.gov/DataStore/Reference/Profile/2318436
doi: 10.57830/2318436
status: NOT PUBLIC
tier: NOT HELD
access:
  - >-
    Open https://www.nps.gov/im/medn/kelp-forest-communities.htm, the Mediterranean Coast
    Inventory & Monitoring Network page headed "Kelp Forest Community Monitoring". It states
    "The Kelp Forest Monitoring Program was established by Channel Islands National Park in 1982
    to collect baseline information about the kelp forest ecosystem in the Park." and "The
    current monitoring protocol was adopted in 1997." Its "For More Information" sources are
    three NPS DataStore saved searches - Quick Reads
    https://irma.nps.gov/DataStore/SavedSearch/Profile/3544, Monitoring Reports
    https://irma.nps.gov/DataStore/SavedSearch/Profile/1508 and Protocol Documents
    https://irma.nps.gov/DataStore/SavedSearch/Profile/1520 - and it names no data package
    (HTTP 200, 2026-09-18)
  - >-
    Open https://irma.nps.gov/DataStore/ and follow Search, then Quick, to
    https://irma.nps.gov/DataStore/Search/Quick. Enter Search Text "kelp forest monitoring" and
    Reference Type Group "Datasets". On 2026-09-18 that search returned six results, of which
    this one is the Data Package; the other five are the Tabular Datasets titled "Channel
    Islands National Park: 2013 Kelp Forest Monitoring Results" through 2017. The result grid
    is an AJAX call, POST /DataStore/Search/QuickSearch with Text, Units, ReferenceTypeGroup,
    HasDigitalFile, Linked, page, start and limit
  - >-
    This record's source is the profile https://irma.nps.gov/DataStore/Reference/Profile/2318436.
    https://doi.org/10.57830/2318436 resolves to that same URL
  - >-
    The profile is served as an application shell. The HTML answers HTTP 200 and carries the
    Core Info values in a JSON literal passed to
    NPSDataStoreReferenceCoreModel.modelSerialize(...) inside a script element; the page's other
    panels are loaded by POSTs that each take referenceId=2318436&id=2318436 -
    /DataStore/Reference/GetAllReferenceMethods (the Methods text),
    /DataStore/Reference/GetCUIBanner, /DataStore/Reference/GetHoldings (Digital Files and
    Links), /DataStore/Reference/ProfileContentProducerUnitsModel and
    /DataStore/Reference/ProfileLinkedGeographicAreasModel. Grepping the delivered HTML for a
    phrase of the record body finds nothing; the values are in that JSON (2026-09-18)
  - >-
    The profile lists Content Producer Unit(s) "Channel Islands National Park", "Inventory and
    Monitoring Division" and "Mediterranean Coast Network", and its CUI banner states the
    producing unit as "Channel Islands National Park (CHIS)". Its citation gives the publisher
    as "National Park Service" and the place published as "Fort Collins CO", and the DataCite
    record for the DOI, https://api.datacite.org/dois/10.57830/2318436, gives publisher
    "National Park Service" (2026-09-18)
  - >-
    The eighteen files are not public. The profile states Downloadability "Internal", which the
    DataStore renders as the access level "Internal - Access limited to all NPS staff"
    (/DataStore/Resources/Scripts_Modern/Reference/DigitalResourcesPopup.js, holdingGridColumns).
    Every one of the eighteen holdings returned by /DataStore/Reference/GetHoldings states
    CanDownload false, /DataStore/Reference/CanUserDownloadFiles returns false without an
    account, and the profile's own JSON states "CanDownloadFiles":false and "HasCUI":true
    (2026-09-18)
  - >-
    An HTTP 200 from a holding URL is not the file. A GET on the first holding,
    https://irma.nps.gov/DataStore/DownloadFile/758684, answered HTTP 200 with Content-Type
    text/html and served the 21,937-byte DataStore home page at
    https://irma.nps.gov/DataStore/Home/Index, not the 30,638,504-byte CSV the tab lists; a
    Referer of the profile page made no difference, and
    https://irma.nps.gov/DataStore/Reference/DownloadBundle?referenceId=2318436 answered HTTP
    500. By contrast a holding of a sibling reference whose Downloadability is "Public",
    https://irma.nps.gov/DataStore/DownloadFile/620107, returned its 888,345 bytes over the
    same anonymous request (2026-09-18)
  - >-
    The profile carries a CUI banner. Its marking is "CUI//SP-NPSR", which the page prints as
    "CUI//SP-NPSR//DL ONLY", over the label "National Park System Resources" and the text "This
    material contains information concerning the nature and specific location of a National Park
    System resource that is endangered, threatened, rare, or commercially valuable, of mineral
    or paleontological objects within System units, or of objects of cultural patrimony within
    System units." The banner states "Controlled by: National Park Service", the producing unit
    "Channel Islands National Park (CHIS)" and the contact scott_gabara@nps.gov, and links
    https://www.archives.gov/cui/registry/category-detail/national-park-system-resources#authority-list
    (2026-09-18)
  - >-
    The page offers "Log In" at https://irma.nps.gov/DataStore/Account/LogOn. No account was
    used and no file was fetched, so nothing of this source is held here
format: >-
  the profile's Reference Type is "Data Package" and its Metadata Standard is EML,
  https://eml.ecoinformatics.org/eml-2.2.0. Its Digital Files and Links tab lists eighteen
  files, seventeen with MimeType text/csv, named chis_kelp_forest_ARM.csv, _band.csv,
  _disease.csv, _fish_size.csv, _gorgonian_size.csv, _macrocystis_size.csv,
  _nat_habitat_size.csv, _quadrat1m.csv, _quadrat5m.csv, _random_point_contact.csv,
  _roving_fish_count.csv, _shell_size.csv, _site_info.csv, _species_checklist.csv,
  _survey_schedule.csv, _taxa.csv and _visual_fish_transect.csv, and one with MimeType
  application/xml, chis_kelp_forest_metadata.xml; the tab states their sizes, which total
  358,013,370 bytes. The Description states the package "consists of 16 CSV files and an EML
  metadata file", where the tab lists seventeen .csv names; this record states both and
  resolves neither. No file was opened: see status and access (2026-09-18)
license: >-
  not stated: the profile's License Type field is empty - its JSON carries "LicenseTypeID":null,
  "LicenseTypeName":null and "LicenseTypeURL":null - and the delivered HTML of
  https://irma.nps.gov/DataStore/Reference/Profile/2318436 contains no occurrence of
  "copyright", "terms of use", "disclaimer", "public domain" or "rights reserved"; its five
  occurrences of "licen" are those three field names, the field name "LicenseType" and the field
  label "License". The files are where a licence would first be looked for, and they are not
  public (see access), so none was opened. The page has no footer: its only chrome links are
  "Log In", "Contact Us" (https://irma.nps.gov/Content/DataStore/Contact/) and "Help"
  (https://irma.nps.gov/Content/DataStore/Help/), and neither of those two pages contains any of
  those words or "licen" either. The DataCite record for the DOI,
  https://api.datacite.org/dois/10.57830/2318436, carries an empty rightsList (all retrieved
  2026-09-18)
variables: []
coverage: >-
  The program as the profile's Description states it: "The Channel Islands National Park Kelp
  Forest Monitoring Program (KFM) is a long-term ecological monitoring initiative established in
  1982 to assess the health and dynamics of kelp forest ecosystems at 33 sites across 5 islands
  off the coast of Southern California."; "The program systematically tracks over 70 species of
  algae, invertebrates, and fish using a suite of 12 underwater sampling techniques, including
  quadrats, transects, and visual surveys."; and "With over 40 years of data". The profile's
  Methods name the islands and the season: "While 16 sites were monitored during the early years
  of the program, a team of 6-8 scientific divers now monitor 33 sites, detailed in the
  site_info.csv table, across the 5 Channel Islands that comprise CHIS (Anacapa Island, Santa
  Cruz Island, San Miguel Island, Santa Rosa Island, and Santa Barbara Island) between May and
  October of each year."; "Each site is 2000 square meters, consisting of a 100-meter-long
  permanent transect line and extending 10 meters away from the transect on either side."; and
  "All sites are within the Channel Islands National Marine Sanctuary, and some are designated
  Marine Protected Areas." The Methods state "Every year, CHIS staff conduct 12 survey
  activities" and then number fourteen, each with a year range; this record states both and
  resolves neither. The widest of those ranges is "1982-2025", on "8. One Meter Quadrats" and
  "11. Random Point Contacts (RPCs)". The title states the span as "1982-2025"; the profile's
  Content Begin Date and Content End Date fields are empty. The profile's one linked
  geographic area is a bounding box described as "Geography for CHIS and
  linked Units", POLYGON ((-120.47299670003764 33.448088200310224, -119.00761850009366
  33.448088200310224, -119.00761850009366 34.249223699813967, -120.47299670003764
  34.249223699813967, -120.47299670003764 33.448088200310224))
coverage_stated_at: >-
  https://irma.nps.gov/DataStore/Reference/Profile/2318436 states the Description quoted first
  and, in the same Core Info, the Title, the Content Begin Date and the Content End Date; the
  Methods section of that profile (POST /DataStore/Reference/GetAllReferenceMethods,
  referenceId=2318436&id=2318436) states the sentences quoted next and the per-technique year
  ranges; POST /DataStore/Reference/ProfileLinkedGeographicAreasModel on the same reference
  states the bounding box (all retrieved 2026-09-18)
retrieved: null
fetch_script: null
file: null
transcribed_from: null
topics:
  - bed-state/diver-surveys
  - bed-state/community
  - grazers-predators-competitors/urchins
regions:
  - scb.islands.anacapa
  - scb.islands.san-miguel
  - scb.islands.santa-barbara
  - scb.islands.santa-cruz
  - scb.islands.santa-rosa
beds: []
sites: []
references: []
human_task: null
---
