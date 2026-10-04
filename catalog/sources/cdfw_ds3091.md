---
id: cdfw_ds3091
title: Predicted Nearshore Benthic Substrates of California - R7 - CDFW [ds3091]
steward: California Department of Fish and Wildlife
url: https://data.cnra.ca.gov/dataset/predicted-nearshore-benthic-substrates-of-california-r7-cdfw-ds3091
doi: null
citations: []
status: VERIFIED
tier: FETCHED
access:
  - >-
    Open
    https://data.cnra.ca.gov/dataset/predicted-nearshore-benthic-substrates-of-california-r7-cdfw-ds3091,
    the dataset page on California Natural Resources Agency Open Data, which answers HTTP 200 with
    Content-Type text/html; charset=utf-8. Its <h1> is this record's title, and the paragraph
    under it reads "This dataset uses rugosity measurements collected during the California
    Seafloor Mapping Project (CSMP) as a proxy to classify benthic habitat as either Hard or Soft.
    While originally developed for MPA planning and MLPA implementation, this dataset provides a
    comprehensive estimate of benthic habitat for California waters. Two versions of this data are
    available:Statewide mosaic raster of all data resampled at 10m (shown here). Vector format for
    visualization and analysis. Substrate classifications are binned into depth ranges and 1
    degree latitude/longitude grids." Under "Additional Info" it prints "Publisher" over
    "California Department of Fish and Wildlife". The page contains "doi", "cite" and "kelp" 0
    times each in any letter case (2026-10-03)
  - >-
    Under "Data and Resources" the page lists four resources: "ArcGIS Hub Dataset", format "HTML",
    linking
    https://data-cdfw.opendata.arcgis.com/content/CDFW::predicted-nearshore-benthic-substrates-of-california-r7-cdfw-ds3091;
    "ArcGIS GeoService", format "ArcGIS GeoServices REST API", linking
    https://tiledimageservices2.arcgis.com/Uq9r85Potqm3MfRV/arcgis/rest/services/biosds3091_cru/ImageServer;
    an "Unnamed resource" linking https://wildlife.ca.gov/Data/BIOS; and an "Unnamed resource",
    format "ZIP", linking
    https://filelib.wildlife.ca.gov/Public/BDB/GIS/BIOS/Public_Datasets/3000_3099/ds3091.zip,
    which is what this record fetches. The same four are the resources of
    https://data.cnra.ca.gov/api/3/action/package_show?id=predicted-nearshore-benthic-substrates-of-california-r7-cdfw-ds3091,
    which answers HTTP 200 with Content-Type application/json;charset=utf-8 and states
    organization title "California Department of Fish and Wildlife", publisher "California
    Department of Fish and Wildlife", license_title "Creative Commons Attribution" and a "guid"
    extra of "https://www.arcgis.com/home/item.html?id=40dc0b4522b94bcf95910801e322be0a"
    (2026-10-03)
  - >-
    The "ArcGIS GeoService" link's "?f=json" response states "type": "ImageServer",
    "capabilities": "Image,TilesOnly", "serviceItemId": "40dc0b4522b94bcf95910801e322be0a",
    "bandCount": 1, "pixelType": "U4", "serviceDataType": "esriImageServiceDataTypeThematic",
    "hasRasterAttributeTable": true and "exportTilesAllowed": false. The item it names,
    https://www.arcgis.com/sharing/rest/content/items/40dc0b4522b94bcf95910801e322be0a?f=json,
    answers HTTP 200 with "type": "Image Service", "owner": "BIOS_Admin" and the title above
    (2026-10-03)
  - >-
    Run src/fetch/cdfw_ds3091.py, which sends the User-Agent "kelpcatalog/cdfw_ds3091", requests
    https://filelib.wildlife.ca.gov/Public/BDB/GIS/BIOS/Public_Datasets/3000_3099/ds3091.zip and
    keeps the body only when it begins with the zip local file header. It answered HTTP 200 with
    150,952,600 bytes, no redirect, Content-Type application/x-zip-compressed, Last-Modified "Mon,
    01 Dec 2025 16:19:02 GMT" and ETag "aa6bc634de62dc1:0" (2026-10-03). No account, key or
    referrer is required. The metadata document "v1_final/tiff/ds3091.tif.xml" in the zip
    states, in the last paragraph of the
    element metadata/dataIdInfo/idPurp, "A vector version at the original resolution can be
    downloaded with this raster through BIOS.", and the zip holds the file geodatabases
    "v1_final/ds3091.gdb/" and "v1_final/ds3091_vector.gdb/" and the directory "v1_final/tiff/"
    that format names
format: >-
  The dataset page lists the fetched file with format "ZIP"; the server sends it as Content-Type
  application/x-zip-compressed. The held zip has 161 entries, 4 of them directories, all under
  "v1_final/": the file geodatabases "v1_final/ds3091.gdb/" (97 files) and
  "v1_final/ds3091_vector.gdb/" (49 files), the directory "v1_final/tiff/" (8 files: ds3091.tif,
  ds3091.tfw, ds3091.tif.aux.xml, ds3091.tif.ovr, ds3091.tif.vat.cpg, ds3091.tif.vat.dbf,
  ds3091.tif.xml and legend.clr) and the layer files "v1_final/ds3091.lyr",
  "v1_final/ds3091.lyrx" and "v1_final/DS3091_20230420.lyr". The metadata document
  "v1_final/tiff/ds3091.tif.xml" states formatName "Raster Dataset", rowcount "107325", colcount
  "74349", rastxsz and rastysz "10.000000", rastband "1" and rastdtyp "pixel codes". The
  ImageServer the third access step names publishes its raster attribute table at
  https://tiledimageservices2.arcgis.com/Uq9r85Potqm3MfRV/arcgis/rest/services/biosds3091_cru/ImageServer/rasterAttributeTable?f=json,
  which answers HTTP 200 with Content-Type application/json; charset=utf-8 and states the fields
  "Value" of type "esriFieldTypeInteger", "Count" of type "esriFieldTypeDouble", "Sub" of type
  "esriFieldTypeString" with length 8, "CLASSNAME" of type "esriFieldTypeString" with length 254,
  and "Red", "Green" and "Blue" of type "esriFieldTypeDouble", each with "domain": null; and two
  features, the first with "Value":1, "Count":15025362, "Sub":"Hard", "CLASSNAME":"Hard",
  "Red":0.56863, "Green":0.39216 and "Blue":0.08627, the second with "Value":2,
  "Count":171495150, "Sub":"Soft", "CLASSNAME":"Soft", "Red":0.98039, "Green":0.85882 and
  "Blue":0.64706 (2026-10-04)
license: >-
  "License: This work is licensed under Creative Commons Attribution 4.0 International License
  (https://creativecommons.org/licenses/by/4.0/). Using the citation standards recommended for
  BIOS datasets (https://www.wildlife.ca.gov/Data/BIOS/Citing-BIOS) satisfies the attribution
  requirements of this license." "Disclaimer: The State makes no claims, promises, or guarantees
  about the accuracy, completeness, reliability, or adequacy of these data and expressly disclaims
  liability for errors and omissions in these data. No warranty of any kind, implied, expressed, or
  statutory, including but not limited to the warranties of non-infringement of third party rights,
  title, merchantability, fitness for a particular purpose, and freedom from computer virus, is
  given with respect to these data."
license_stated_at: >-
  The two paragraphs quoted are the two <P> elements of the HTML that the element
  metadata/dataIdInfo/resConst/Consts/useLimit carries in "v1_final/tiff/ds3091.tif.xml" in the
  held zip, taken as the text of each element with its markup removed and its entities decoded.
  The "licenseInfo" of the ArcGIS item
  https://www.arcgis.com/sharing/rest/content/items/40dc0b4522b94bcf95910801e322be0a?f=json states
  the same text with no space between "license." and "Disclaimer:". The dataset page prints the
  heading "License" over a link whose text is "Creative Commons Attribution", to
  http://www.opendefinition.org/licenses/cc-by (2026-10-03)
variables:
  - name: OID
    description: Internal feature number.
    unit: null
  - name: Value
    description: null
    unit: null
  - name: Count
    description: null
    unit: null
  - name: sub
    description: Substrate classification of 'Hard' or 'Soft' benthic habitat.
    unit: null
  - name: CLASSNAME
    description: null
    unit: null
  - name: Red
    description: null
    unit: null
  - name: Green
    description: null
    unit: null
  - name: Blue
    description: null
    unit: null
measures: []
coverage: >-
  The dataset page states "While originally developed for MPA planning and MLPA implementation,
  this dataset provides a comprehensive estimate of benthic habitat for California waters." and
  "Two versions of this data are available:Statewide mosaic raster of all data resampled at 10m
  (shown here)." Its "spatial" extra is the polygon "{"type": "Polygon", "coordinates":
  [[[-124.6329,32.3947],[-124.6329,42.1032],[-116.2959,42.1032],[-116.2959,32.3947],[-124.6329,32.3947]]]}".
  The metadata document in the held zip states "This version is a statewide mosaic of all data
  resampled at 10m.", and its bounding box westBL "-125.264867", eastBL "-116.295895", northBL
  "42.157317" and southBL "32.394712". This record holds the one zip the dataset page lists, whole
coverage_stated_at: >-
  The first two sentences are the second and third sentences of the paragraph under the <h1> of
  https://data.cnra.ca.gov/dataset/predicted-nearshore-benthic-substrates-of-california-r7-cdfw-ds3091;
  the polygon is the value of the "spatial" extra in that dataset's package_show response, which
  the second access step names; the next sentence is the first sentence of the last paragraph of
  the element metadata/dataIdInfo/idPurp, and the bounding box the element
  metadata/dataIdInfo/dataExt/geoEle/GeoBndBox, of "v1_final/tiff/ds3091.tif.xml" in the zip
  retrieved 2026-10-03 into data/raw/cdfw_ds3091/ by src/fetch/cdfw_ds3091.py
retrieved: 2026-10-03
fetch_script: src/fetch/cdfw_ds3091.py
file: null
transcribed_from: null
derived_from: null
topics:
  - substrate/rock-mapping
regions:
  - scb
beds: []
sites: []
site_key: []
references: []
human_task: null
---
