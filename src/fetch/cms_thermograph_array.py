"""Fetch the David Tsao Continental Thermograph Array files into data/raw/cms_thermograph_array/.

Run:  python src/fetch/cms_thermograph_array.py

Each file in FILES is downloaded unmodified and written beside a manifest carrying the
url, the time of the fetch, the sha256, the byte count, the HTTP status and the response
headers a repeat fetch records - content_type, last_modified and etag, null when the
server sends none. Spreadsheets are stored as served, never converted. data/ is
git-ignored and reproducible from this script, which is the record of the fetch
(CONTEXT.md, "Record format"). Standard library only.

FILES is every data set linked from the fourteen site pages under
https://www.catalinamarinesociety.org/data-portal-tsao-continental-thermograph-array-sites.html
that served its bytes to an anonymous request on 2026-09-25, in the order each page links
them. The array's files sit on three hosts, and each is the steward's own route to them:
the steward's own site under /files/, Google Drive links the steward's pages carry, and -
for the three spreadsheets - docs.google.com/spreadsheets/d/<file id>/edit, the Google
Sheets viewer, which data-portal-corral-beach.html, data-portal-cress-st.html and
data-portal-white-point.html each carry once. Those three are requested below by the same
file id from the Drive download endpoint, which returns the uploaded workbook.
Three of the site pages link a data set over http:// and one omits the www, and those are
written here as the page links them.

Four links the pages carry are not in FILES, because no bytes of the file came back:

  * AVALON 110' 09/02/2019-11/11/2019, data-portal-avalon-park.html,
    drive id 1R0AkJ1imvr9FmxJ5Ia4s28S_ldaLh2cL - HTTP 404
  * AVALON WRECK 75' 12/29/2012-08/01/2012, data-portal-avalon-wreck.html,
    drive id 1fLJ8CEyN7nS_rAGAOyG1Mohg2TrAvgxu - HTTP 404
  * WHITE POINT VENT 30' 04/18/2014-10/11/2014, data-portal-white-point.html,
    drive id 1_0d6zUY_encEuljFmwi1NvFWLmZsE38v - HTTP 404
  * DEADMAN REEF 30' 11/13/2014-09/28/2015, data-portal-deadman-reef.html,
    drive id 1L7GJTieih_SM4aa9PSvbYoYX_fUX1I1R - HTTP 200 with a Google sign-in page

That last one is why fetch() below rejects an HTML body outright, rather than warning: Drive
answers a file it will not serve anonymously with HTTP 200 and an accounts.google.com
sign-in page, so a status check alone would store the sign-in page as thermograph data.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE_ID = "cms_thermograph_array"

FILES = (
    # data-portal-deer-creek.html, 6 files, in the order the page links them
    # DEER CREEK 30FT 02/27/2015-02/10/2018
    "https://drive.google.com/uc?export=download&id=1Fi6pQQWUgK33Y_qK-wEx9ECYEGg8T8Bv",
    # DEER CREEK 32' 02/27/2015-09/26/2015
    "https://drive.google.com/uc?export=download&id=1t_vxv_Lh3evHxfXBm4jwsmXYXKlchDiA",
    # DEER CREEK 09/26/2015-11/19/2016
    "https://drive.google.com/uc?export=download&id=1FJXruMG-fUP2LYLyEsLo2T5gU7IU7u4z",
    # DEER CREEK 11/19/2016-05/13/2017
    "https://drive.google.com/uc?export=download&id=1dhZBoTyfPHrtX2UHpZ5vYnniupUTG3AH",
    # DEER CREEK 30FT 05/13/2017-02/10/2018
    "https://drive.google.com/uc?export=download&id=1rGxL302vemgcFcTd64twQ9JJyOX3MfL9",
    # DEER CREEK 30FT 02/10/2018-06/08/2019
    "https://drive.google.com/uc?export=download&id=1fsv9SEkjzh4j2hvLY3Mm7qNN6p5NDf68",
    # data-portal-leo-carrillo.html, 1 files, in the order the page links them
    # LEO CARRILLO 57' DATA 10/30/2011-4/28/2012
    "https://drive.google.com/uc?export=download&id=12qRX8sJaBin-xpnv61EDlC7H6kyWupnx",
    # data-portal-corral-beach.html, 1 files, in the order the page links them
    # CORRAL BEACH, MALIBU 24' DATA 10/21/2005-04/20/2006
    "https://drive.google.com/uc?export=download&id=1lZqUzLQ5r5NPv7_ZoX1tsT4y-BJdNMQ4",
    # data-portal-pt-dune.html, 1 files, in the order the page links them
    # PT DUME 30FT 09/09/2017-11/22/2017
    "https://drive.google.com/uc?export=download&id=1sKAIdN3sO3REaj2vKsjyXZeePpzvHmhp",
    # data-portal-malaga-cove.html, 2 files, in the order the page links them
    # MALAGA COVE 30ft 05/26/2019-07/27/2019
    "https://drive.google.com/uc?export=download&id=1bOU3M2MDqAaN7U71oXNxydADTWWgMqxG",
    # malaga Cove 30ft 06/02/2021 - 12/15/2022 20894275
    "https://www.catalinamarinesociety.org/files/Malaga_Cover_30ft_06022021-12152022_20894275.csv",
    # data-portal-marine-land-platform.html, 6 files, in the order the page links them
    # MARINE LAND PLATFORM 55' 12/23/2018-11/16/2019
    "https://drive.google.com/uc?export=download&id=18WtdROfUw4xRsvZnpDcswzuahO6ZiCoa",
    # MARINE LAND PLATFORM 56' 06/02/2018-12/23/2018
    "https://drive.google.com/uc?export=download&id=1g9ovbnETV98q5-cadFUR9GDKs_2XSJvS",
    # MARINE LAND PLATFORM 56' 11/18/2017-06/02/2018
    "http://www.catalinamarinesociety.org/files/MarinelandPlat_11182017_06022018_10178072.txt",
    # MARINE LAND PLATFORM 55' 06/17/2017-11/18/2017
    "https://drive.google.com/uc?export=download&id=1uVUwpF2508SRXS60NBLEkgyfMsyOTv3K",
    # MARINE LAND PLATFORM 56' 11/12/2016-06/17/2017
    "https://drive.google.com/uc?export=download&id=1Xirg4nx8VCYWGs4kLGtFJpOaDSQ3JP62",
    # MARINE LAND PLATFORM 64' 11/12/2016
    "https://drive.google.com/uc?export=download&id=1KLndTXJ4loRS0QLJV2PFcv2C8gtrYIje",
    # data-portal-white-point.html, 18 files, in the order the page links them
    # WHITE POINT 60' 3/7/2026-9/16/2026
    "https://www.catalinamarinesociety.org/files/WhitePoint_60ft_03072026-09162026_20894280.txt",
    # WHITE POINT 30' 3/21/2026-9/16/2026
    "https://www.catalinamarinesociety.org/files/WhitePoint_30ft_03212026-09162026_22169469.txt",
    # WHITE POINT ROCK 70' 12/23/2018-11/16/2019
    "https://drive.google.com/uc?export=download&id=13Ez4dKGbBuRYmunfLtv_SjIRBeAAYIIm",
    # WHITE POINT ROCK 65' 06/02/2018-03/23/2019
    "https://drive.google.com/uc?export=download&id=1Ufxxr2BQNv5UNnnScMrKBV6KGfzFSwOG",
    # WHITE POINT ROCK 65' 11/17/2017-06/02/2018
    "http://www.catalinamarinesociety.org/files/White_Pt_Rock_11172017_06022018_10862356.txt",
    # WHITE POINT ROCK 66' 06/17/2017-11/18/2017
    "https://drive.google.com/uc?export=download&id=1qGKZDsGv3m8-GLyoLfCvFLCDpLsFbxy4",
    # WHITE POINT ROCK 66' 11/12/2016-06/17/2017
    "https://drive.google.com/uc?export=download&id=1LEGaUM4sS-41luKw-Bn-ATL65teicIGQ",
    # WHITE POINT ROCK 60' 09/19/2015-11/12/2016
    "https://drive.google.com/uc?export=download&id=1o6He_O1yhnuYgfA6X3LvnWtKThgMtGC0",
    # WHITE POINT ROCK 67' 10/22/2011-09/03/2012
    "https://drive.google.com/uc?export=download&id=1PfSR_4w4SWJXZktjx_rAkL_YB4OF-SyH",
    # WHITE POINT ROCK 67' 1/29/2011-10/22/2011
    "https://drive.google.com/uc?export=download&id=1mkmIbT_hB37xzMbDqT7I6H8F0FnGFGbg",
    # WHITE POINT ROCK 10/22/2011-11/18/2017
    "https://drive.google.com/uc?export=download&id=1L1AlCI5Gad2HQDkAwL1KMeFP2zf2fbC5",
    # WHITE POINT VENT 26' 03/30/2018-10/12/2019
    "https://drive.google.com/uc?export=download&id=1lmqV1wwpad89fcgRWRwohuhvewCWNiIZ",
    # WHITE POINT VENT 27' 09/09/2017-03/30/2018
    "https://drive.google.com/uc?export=download&id=1uGSUzXt23zF5VUEjzuen6KqA7Nult37o",
    # WHITE POINT VENT 27' 03/11/2017-09/09/2017
    "https://drive.google.com/uc?export=download&id=1kcDHqG_YAakJu1zpHXDAd4-ire88N9G9",
    # WHITE POINT VENT 27' 02/15/2016-09/02/2016
    "https://drive.google.com/uc?export=download&id=1865skUxn2T02owQu2StaMzehfrWVLXya",
    # WHITE POINT VENT 30' 08/29/2015-02/15/2016
    "https://drive.google.com/uc?export=download&id=1Hng2c6HQwC9-nDpvQkmjoBqmKuRCOciT",
    # WHITE POINT VENT 30' 10/11/2014-08/29/2015
    "https://drive.google.com/uc?export=download&id=1Fxlv0I-9BWN-do58qNaY5oWidA_ZNWyS",
    # WHITE POINT VENT 27' 10/09/2013-02/17/2018 CONCATENATED
    "https://drive.google.com/uc?export=download&id=12ofNOX3rpb9tmD749ZbkHJZ6ODKn91Po",
    # data-portal-avalon-wreck.html, 13 files, in the order the page links them
    # AVALON WRECK 55' 06/25/2020-12/05/2022
    "https://catalinamarinesociety.org/files/Jon_D._Avalon_55ft_06252020-12252022_20539513.csv",
    # AVALON WRECK 75' 06/12/2019-06/25/2020
    "https://drive.google.com/uc?export=download&id=1ri1A7GI2zzLNvRMGLQJsmWDc7b9nF7lw",
    # AVALON WRECK 75' 12/08/2018-06/12/2019
    "https://drive.google.com/uc?export=download&id=10HaSjoWaFC6KvWCLcC3O1GPuvJxBZIvL",
    # AVALON WRECK 75' 03/06/2018-11/15/2018
    "https://drive.google.com/uc?export=download&id=1Xj4EYD4qGlmywSkkxhPeh3dE2wemKkcU",
    # AVALON CREEK 55' 03/06/2018-11/15/2018
    "https://drive.google.com/uc?export=download&id=1xBMz_LWGW6i0nQ78zPy1FGFfWAZfSbHc",
    # AVALON WRECK 55' 07/06/2017-03/06/2018
    "https://drive.google.com/uc?export=download&id=1OoHUwfs1ObafERl28D72mYWRDwC74q7d",
    # AVALON WRECK 75' 01/15/2016-07/06/2017
    "https://drive.google.com/uc?export=download&id=1MNTNwSzWk3d-dmGVaPzQV9DW2xl_8jFc",
    # AVALON WRECK 55' 01/15/2016-07/06/2017
    "https://drive.google.com/uc?export=download&id=1tzlUUHLxbC3RKrJH6QWokD6n6bZph1aC",
    # AVALON WRECK 75' 03/28/2014-07/22/2014
    "https://drive.google.com/uc?export=download&id=1YH3lb6dU8wiQEYlWQtsNGs-CaP3p62v6",
    # AVALON WRECK 55' 03/28/2014-07/22/2014
    "https://drive.google.com/uc?export=download&id=1UFePrUpaMVGVtCLNwdFSQfvZua8bE_Yt",
    # AVALON CREEK 75' 02/05/2014-03/30/2014
    "https://drive.google.com/uc?export=download&id=1bQc85sgFBFGEsqXB9xKTgCyeo_jNDxAK",
    # AVALON WRECK 55' 02/04/2014-03/30/2014
    "https://drive.google.com/uc?export=download&id=1-UtZlPbBNq_M9jDqZ0UfP3VQeO5K9ANu",
    # AVALON WRECK 75' 12/29/2012-08/01/2012 redundant
    "https://drive.google.com/uc?export=download&id=1JGDuVl1EphAYwzJZsMmp0BhBdz89CHvJ",
    # data-portal-crystal-cove.html, 1 files, in the order the page links them
    # CRYSTAL COVE 32' 11/14/2014-07/26/2015
    "https://drive.google.com/uc?export=download&id=1VgDQewxQSNkO-GpiuYru6HNBGkLIDcwX",
    # data-portal-montage.html, 3 files, in the order the page links them
    # MONTAGE 19' 08/02/2018-02/29/2020
    "https://drive.google.com/uc?export=download&id=13VirqyoivbKDsZuMmuIoamK1uTfxcfhc",
    # MONTAGE 37' 12/17/2017-09/02/2018
    "https://drive.google.com/uc?export=download&id=11gGMMXH3KwITznmoE9LGL-R4uVi3K7l6",
    # MONTAGE 19' 12/17/2017-08/31/2018
    "https://drive.google.com/uc?export=download&id=1JWk_ypJJ-HORW_VzpBH1NCLq6yIfJMb1",
    # data-portal-shaws.html, 16 files, in the order the page links them
    # SHAW'S COVE 60' 10/06/2024-04/26/2025
    "https://www.catalinamarinesociety.org/files/Shaws_60ft_10062024-04262025_21502242.txt",
    # SHAW'S COVE 30' 05/11/2024-10/06/2024
    "https://www.catalinamarinesociety.org/files/Shaws_30ft_05112024-10062024_21292584.dat",
    # SHAW'S COVE 60' 05/11/2024-10/06/2024
    "https://www.catalinamarinesociety.org/files/Shaws_60ft_05112024_10062024_20722049.dat",
    # SHAW'S COVE 30' 09/25/2022-05/11/2024
    "https://www.catalinamarinesociety.org/files/Shaws_30ft_09252022-05112024_21292585.csv",
    # SHAW'S COVE 60' 04/19/2019-12/21/2019
    "https://drive.google.com/uc?export=download&id=1hY7AfEBPB8sUqDRNIOtA4LakjCQmpTRM",
    # SHAW'S COVE 30' 04/19/2019-12/21/2019
    "https://drive.google.com/uc?export=download&id=1REzwOfV_PPKJOSawAh8rNqz5XIn-85PN",
    # SHAW'S COVE 60' 03/25/2018-04/19/2019
    "https://drive.google.com/uc?export=download&id=152IuFQESYNEM_Vo7sq-Hp5Y5g2aIuqZO",
    # SHAW'S COVE 30' 03/25/2018-04/19/2019
    "https://drive.google.com/uc?export=download&id=19c51pvfhuS_M9IU84fG8Kes1A-NWKzGF",
    # SHAW'S COVE 60' 09/09/2017-03/30/2018
    "https://drive.google.com/uc?export=download&id=1LhzXZ0wpzdkSDR53CKHaze8qqDWDdkPp",
    # SHAW'S COVE 30' 02/04/2017-03/30/2018
    "https://drive.google.com/uc?export=download&id=1o4hHJ-k4zkFt3RbRxGlhenIs1qs_ylnr",
    # SHAW'S COVE 60' 02/12/2016-09/23/2017
    "https://drive.google.com/uc?export=download&id=17Xdbhpoe7ncgGvy2GWZzncolzYKdie32",
    # SHAW'S COVE 30' 03/11/2017-09/23/2017
    "https://drive.google.com/uc?export=download&id=1HLDL0IPdGId8K8Jbq9i6QNrFIBSQpjFF",
    # SHAW'S COVE 60' 09/27/2015-02/15/2016
    "https://drive.google.com/uc?export=download&id=1h8iN8wP4u0P81oAi8VHL4P59s7eMJAFy",
    # SHAW'S COVE 30' 09/27/2015-02/15/2016
    "https://drive.google.com/uc?export=download&id=1REp0NgoxTUAL0fhHgOV5U4Yw9UGYM8zh",
    # SHAW'S COVE 60' 09/27/2015-03/25/2018 CONCATENATED
    "https://drive.google.com/uc?export=download&id=1sZAHORNwdsHUkO9nMvA_Hk7h4QVQ-_jT",
    # SHAW'S COVE 30' 09/27/2015-03/25/2018 CONCATENATED
    "https://drive.google.com/uc?export=download&id=1g2zhddLC4SM6U9GhH0TdzeUMlYV_OIqa",
    # data-portal-cress-st.html, 13 files, in the order the page links them
    # CRESS ST 57' 12/06/2025-09/23/2026
    "https://www.catalinamarinesociety.org/files/Cress_ST_60ft_12062025-09232026_22346693.txt",
    # CRESS ST 57' 06/04/2016-08/28/2017
    "https://drive.google.com/uc?export=download&id=1gXzHosQX65raxi0A5sd1NIZCs7sjVgct",
    # CRESS ST 60' 08/09/2015-06/06/2016
    "https://drive.google.com/uc?export=download&id=1ObJMi7rw_R-kKjGi06xg47AyI-ac5gtH",
    # CRESS ST 60' 10/17/2014-09/09/2015
    "https://drive.google.com/uc?export=download&id=1U5SBuzc9OpIgFIEL6rdCM0W6MK55BQD6",
    # CRESS ST 30' 10/17/2014-08/09/2015
    "https://drive.google.com/uc?export=download&id=1hftp-dGKWEa0JzjSPbhuNvmHLv4Pa0LR",
    # CRESS ST 30' 05/02/2014-10/17/2014
    "https://drive.google.com/uc?export=download&id=1sUTzj3W9xyadew2nB64xuy9vP_-22vC1",
    # CRESS ST 60' 10/27/2013-05/02/2014
    "https://drive.google.com/uc?export=download&id=1lR0vBmo_IfEiKr3SfY82qABb4rK7SVLs",
    # CRESS ST 30' 10/27/2013-05/02/2014
    "https://drive.google.com/uc?export=download&id=1CxQ9oqJ91tmkv5WBvzkbtyrkCtP2-Yr4",
    # CRESS ST 60' 02/15/2013-10/27/2013
    "https://drive.google.com/uc?export=download&id=1xwwr70n4HOYx8JeoJ0ch5ccDoK1cFXM_",
    # CRESS ST 54' 11/03/2012-02/13/2013
    "https://drive.google.com/uc?export=download&id=1fKy4r_wI31U3LlG_pvMwzTB4VG7kJ2g1",
    # CRESS ST 25' 11/03/2012-02/13/2013
    "https://drive.google.com/uc?export=download&id=1p009QCSVd8gruKUdv-41IOnYDDo5vJLw",
    # CRESS ST 60' 11/03/2012-08/09/2015
    "https://drive.google.com/uc?export=download&id=1HEo3Or4V8vr2k0NVET-JLtclCS8uLVgH",
    # CRESS ST 30' 11/03/2012-08/09/2015
    "https://drive.google.com/uc?export=download&id=1p01AvuE6LiNPKWiLgZe59jTXXyB-HjfX",
    # data-portal-deadman-reef.html, 33 files, in the order the page links them
    # DEADMAN REEF 30' 01/19/2025-10/20/2025 22169465
    "https://www.catalinamarinesociety.org/files/Deadmans_30ft_01192025-10202025_22169465.txt",
    # DEADMAN REEF 60' 01/19/2025-10/25/2025 22169462
    "https://www.catalinamarinesociety.org/files/Deadmans_60ft_01192025-10252025_22169462.txt",
    # DEADMAN REEF 30' 01/31/2024-01/19/2025 21894633
    "https://www.catalinamarinesociety.org/files/Deadman_30ft_01312024-01192025_21894633.txt",
    # DEADMAN REEF 60' 01/31/2024-01/19/2025 _21894634
    "https://www.catalinamarinesociety.org/files/Deadman_60ft_01312024-01192025_21894634.txt",
    # DEADMAN REEF 60' 01/03/2023-01/31/2024 21502242
    "https://www.catalinamarinesociety.org/files/Deadman_60ft_01032023-01312024_21502242.csv",
    # DEADMAN REEF 30' 01/03/2023-01/31/2024 21502239
    "https://www.catalinamarinesociety.org/files/Deadman_30ft_01032023-01312024_21502239.csv",
    # DEADMAN REEF 30' 01/22/2022-01/03/2023 21292583
    "https://www.catalinamarinesociety.org/files/Deadman_30ft_01222022-01032023_21292583.csv",
    # DEADMAN REEF 30' 10/31/2020-01/22/2022 20668565
    "https://www.catalinamarinesociety.org/files/"
    "deadman_30f_10312020-01222022_20668565%20%281%29.txt",
    # DEADMAN REEF 60' 01/22/2022-01/03/2023 21292584
    "https://www.catalinamarinesociety.org/files/Deadman_60ft_01220222-01032023_21292584.csv",
    # DEADMAN REEF 60' 10/31/2020-01/22/2022 20668566
    "https://www.catalinamarinesociety.org/files/"
    "Deadman_60f_10312020-01222022_20668566%20%281%29.txt",
    # DEADMAN REEF 30' 11/25/2019-11/01/2020
    "https://drive.google.com/uc?export=download&id=1IsjCHmT4dFKke43n9SJgAo29a2IoI8zG",
    # DEADMAN REEF 60' 11/25/2019-11/01/2020
    "https://drive.google.com/uc?export=download&id=1dNblQ7UFfJmNEleoODlEMn5HFeOAsmjS",
    # DEADMAN REEF 30' 11/19/2018-11/25/2019
    "https://drive.google.com/uc?export=download&id=1tc9CCXtBlyMgJBO96s5szHQD0k2R3Xma",
    # DEADMAN REEF 60' 11/19/2018-11/25/2019
    "https://drive.google.com/uc?export=download&id=1o8tmFJdONgoh8QGsMssK8eYNpNwdyDOY",
    # DEADMAN REEF 60' 11/25/2017-12/29/2018
    "https://drive.google.com/uc?export=download&id=1ft6kobV5cbsxRkdo-LtPShO4eiI54c42",
    # DEADMAN REEF 30' 11/25/2017-12/29/2018
    "https://drive.google.com/uc?export=download&id=1mI0XYtVYnaQshG1_GWp4ZKvN-QOg6r93",
    # DEADMAN REEF 60' 12/20/2016-11/25/2017
    "https://drive.google.com/uc?export=download&id=1uIl-di-sMoJlwM-aCA9tAGhLXvv_g7zt",
    # DEADMAN REEF 30' 12/20/2016-11/25/2017
    "https://drive.google.com/uc?export=download&id=17PtEUhnJSbvpeJfYEJFTL59fMUmlPe6v",
    # DEADMAN REEF 60' 09/28/2015-12/22/2016
    "https://drive.google.com/uc?export=download&id=1oKAOEmr0-kDb8-mrhzhbn5YXsASMEQTv",
    # DEADMAN REEF 30' 09/28/2015-12/22/2016
    "https://drive.google.com/uc?export=download&id=1uiZJ6rKVIpl4MC0yAqbJyy8KVX_s_4ut",
    # DEADMAN REEF 60' 11/13/2014-09/28/2015
    "https://drive.google.com/uc?export=download&id=1yL8qqbEyh_jk6dkmf8-AQz48A9nfWSKk",
    # DEADMAN REEF 60' 04/08/2014-11/13/2014
    "https://drive.google.com/uc?export=download&id=1zZtmASJwe-L-ggUgK4dKU6EtFgGFjIjY",
    # DEADMAN REEF 30'04/08/2014-11/13/2014
    "https://drive.google.com/uc?export=download&id=1HsumiYIDxJ1l6jHsb6CAH-dkxN74Eaef",
    # DEADMAN REEF 30' 01/18/2014-04/08/2014
    "https://drive.google.com/uc?export=download&id=1zPb8e8nyH2wm5Re5d7BwxtA_AsxW5z_T",
    # DEADMAN REEF 60' 06/15/2013-01/18/2014
    "https://drive.google.com/uc?export=download&id=1ndr9P0skQ_xfAdDz06lYcuhgNCAtBrPL",
    # DEADMAN REEF 30' 06/15/2013-01/18/2014
    "https://drive.google.com/uc?export=download&id=1yk6nEIGaQDEgOc9v0fNNfHZkGvkhdqO3",
    # DEADMAN REEF 60' 12/16/2012-06/17/2013
    "https://drive.google.com/uc?export=download&id=1MmHxYZQrQ7J4lV6J9QMoHZT1L8FV1-Yl",
    # DEADMAN REEF 60' 08/26/2012-12/18/2012
    "https://drive.google.com/uc?export=download&id=1rMV3YcGUjBSH8n31a95G1v-GElc1h464",
    # DEADMAN REEF 30' 08/26/2012-12/18/2012
    "https://drive.google.com/uc?export=download&id=1JyiE25x_vbaFUYuZtyt1s5pDyjncBNDr",
    # DEADMAN REEF 60' 06/19/2012-08/16/2012
    "https://www.catalinamarinesociety.org/files/format10073222.txt",
    # DEADMAN REEF 30' 06/19/2012-08/16/2012
    "http://www.catalinamarinesociety.org/files/format9898972.txt",
    # CONCATENATED 60' 06/2012-11/2017
    "https://drive.google.com/uc?export=download&id=1lsMWU-knp6MQsVrPHokehwqgonMO1DVL",
    # CONCATENATED 30' 06/2012-11/2017
    "https://drive.google.com/uc?export=download&id=1eUOjFYpcICycgOGRylyHF6wnm-uOJfel",
    # data-portal-avalon-park.html, 2 files, in the order the page links them
    # AVALON 30' 11/11/2019-12/12/2019
    "https://drive.google.com/uc?export=download&id=1hfa2Kwa6IpVUgswSFY-879IEdHqwvOjT",
    # AVALON 30' 09/02/2019-11/11/2019
    "https://drive.google.com/uc?export=download&id=1wuHCsTHms1Tlhzep-kKOAqsr2IOWrpJa",
)

REPO = "https://github.com/cweber12/socal-bight-kelp-reference-catalog"

# Name the catalog and give the steward a way to reach us.
USER_AGENT = f"kelpcatalog/{SOURCE_ID} (+{REPO})"

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / SOURCE_ID


def served_name(url: str, headers: object) -> str:
    """The name the server gave the file, falling back to the URL's last path segment.

    Drive sends Content-Disposition and its URL path is always "uc"; the steward's own
    /files/ URLs send no Content-Disposition and name the file in the path.
    """
    served = headers.get_filename() if hasattr(headers, "get_filename") else None
    if not served:
        path = urllib.parse.urlsplit(url).path
        served = urllib.parse.unquote(path.rsplit("/", 1)[-1])
    name = Path(served).name
    if name in ("", ".", "..", "uc"):
        raise RuntimeError(f"{url}: unusable served file name {served!r}")
    return name


def fetch(url: str, out_dir: Path, taken: dict[str, str]) -> dict[str, object]:
    """Download one file into out_dir and write its manifest. Returns the manifest.

    taken maps a served file name to the URL that already used it, so two links that
    serve the same name cannot silently overwrite one another.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read()
        http_status = response.status
        headers = response.headers
    # A 200 is not enough. Drive answers a file it will not serve anonymously with an
    # accounts.google.com sign-in page under HTTP 200, and one link on
    # data-portal-deadman-reef.html does exactly that. Never store one as thermograph data.
    content_type = headers.get("Content-Type") or ""
    if content_type.startswith("text/html") or body.lstrip()[:9].lower() == b"<!doctype":
        raise RuntimeError(
            f"{url}: body is HTML, not a data file "
            f"(Content-Type {content_type!r}, first bytes {body[:40]!r})"
        )
    name = served_name(url, headers)
    if name in taken:
        raise RuntimeError(f"{url}: served name {name!r} already written by {taken[name]}")
    taken[name] = url
    manifest = {
        "url": url,
        "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "http_status": http_status,
        # What a repeat fetch records, not what it reproduces: Drive sends neither
        # Last-Modified nor ETag, and the steward's own host stamps both. No
        # content_length - it duplicates bytes.
        "content_type": headers.get("Content-Type"),
        "last_modified": headers.get("Last-Modified"),
        "etag": headers.get("ETag"),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / name).write_bytes(body)
    (out_dir / f"manifest_{name}.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    # A failure part-way through leaves some files on disk and others missing, with
    # nothing to mark the directory incomplete. Fetch what can be fetched, then name
    # every failure and exit non-zero.
    failures: list[tuple[str, Exception]] = []
    taken: dict[str, str] = {}
    for url in FILES:
        try:
            print(json.dumps(fetch(url, OUT_DIR, taken), indent=2))
        except Exception as exc:  # noqa: BLE001 - every failure is reported below
            failures.append((url, exc))
            print(f"FAILED {url}: {exc}", file=sys.stderr)
    if failures:
        print(
            f"\n{len(failures)} of {len(FILES)} files did not fetch; {OUT_DIR} is incomplete:",
            file=sys.stderr,
        )
        for url, exc in failures:
            print(f"  {url}: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
