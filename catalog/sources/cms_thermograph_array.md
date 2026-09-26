---
id: cms_thermograph_array
title: David Tsao Continental Thermograph Array
steward: Catalina Marine Society
url: https://www.catalinamarinesociety.org/data-portal-tsao-continental-thermograph-array-sites.html
doi: null
citations: []
status: VERIFIED
tier: FETCHED
access:
- >-
  Open https://www.catalinamarinesociety.org/data-portal.html, which answered HTTP 200 with 179,424
  bytes of Content-Type "text/html" and is headed "cms data portal". It states "Welcome to the Catalina
  Marine Society Data Portal. Our Portal is intended to be the go-to-page to find data collected or
  maintained by the CMS." and "Below are links to our scientific mooring data, temperature data collected
  as part of our David Tsao Continental Thermograph Array (CTA) project, and some temperature data collected
  by the Catalina Conservancy Divers." Its link labelled "David Tsao Continental Thermograph Array"
  is this record's url (2026-09-25)
- >-
  https://www.catalinamarinesociety.org/data-portal-tsao-continental-thermograph-array-sites.html answered
  HTTP 200 with 193,437 bytes and is headed "DAVID TSAO CONTINENTAL THERMOGRAPH ARRAY SITES". It states
  "We use Onset Computer's U22-0001 thermographs to record temperatures. CMS data sets are linked below.
  The thermograph manual is here." - the word "here" carries no link on the copy taken. The page links
  the fourteen site pages of the next step and no data set of its own (2026-09-25)
- >-
  Each site page is https://www.catalinamarinesociety.org/data-portal-<site>.html. All fourteen answered
  HTTP 200 on 2026-09-25, at these byte counts: deer-creek 171,284, leo-carrillo 147,434, corral-beach
  151,094, pt-dune 155,514, malaga-cove 156,316, marine-land-platform 166,904, white-point 217,706,
  avalon-wreck 196,455, crystal-cove 147,437, montage 157,292, shaws 202,889, cress-st 193,320, deadman-reef
  260,651, avalon-park 157,368. Each prints its site's name as a heading, most print SPONSOR, MANAGER
  and LOCATION lines, and each links its own data sets; coverage quotes those headings and lines. Seven
  of the fourteen also print a line reading "Format of Concatenated data:" over a column list, and data-portal-shaws.html
  prints "Formats vary, but should be obvious." above it
- >-
  The data sets sit on three hosts, each a route the steward's own pages give: the steward's own site
  under https://www.catalinamarinesociety.org/files/, Google Drive links the site pages carry, each
  fetched as https://drive.google.com/uc?export=download&id=<file id>, which answers HTTP 200 with the
  file and a Content-Disposition naming it. Run src/fetch/cms_thermograph_array.py, which sends the
  User-Agent "kelpcatalog/cms_thermograph_array (+https://github.com/cweber12/socal-bight-kelp-reference-catalog)"
  and requests the 116 URLs listed below; no account, key or referrer is required, and each answered
  HTTP 200. Three site pages link a data set over http:// and one omits the www, and each is requested
  as the page links it. Three data sets are linked on a third host, not on drive.google.com: data-portal-corral-beach.html,
  data-portal-cress-st.html and data-portal-white-point.html each carry one as https://docs.google.com/spreadsheets/d/<file
  id>/edit, the Google Sheets viewer, with the query string usp=sharing, an ouid, rtpof=true and sd=true.
  Those three are the three spreadsheets, and this record requests each by the same file id from the
  drive.google.com download endpoint above, which returns the uploaded workbook: Corral899247.xls, CTA_Cress_ST_60ft_10178072.xlsx
  and WhitePointRock9852411-2011.xls. Spreadsheets are kept as served, never converted (2026-09-25)
- >-
  Four links the site pages carry are not held, because no bytes of the file came back. Three answered
  HTTP 404: drive ids 1R0AkJ1imvr9FmxJ5Ia4s28S_ldaLh2cL ("AVALON 110' 09/02/2019-11/11/2019" on data-portal-avalon-park.html),
  1fLJ8CEyN7nS_rAGAOyG1Mohg2TrAvgxu ("AVALON WRECK 75' 12/29/2012-08/01/2012" on data-portal-avalon-wreck.html)
  and 1_0d6zUY_encEuljFmwi1NvFWLmZsE38v ("WHITE POINT VENT 30' 04/18/2014-10/11/2014" on data-portal-white-point.html).
  The fourth, 1L7GJTieih_SM4aa9PSvbYoYX_fUX1I1R ("DEADMAN REEF 30' 11/13/2014-09/28/2015" on data-portal-deadman-reef.html),
  answered HTTP 200 with 943,037 bytes of Content-Type "text/html; charset=utf-8" whose first bytes
  are "<!doctype html>" and whose base href is "https://accounts.google.com/v3/signin/" (2026-09-25)
- >-
  data-portal-deer-creek.html links 6 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=1Fi6pQQWUgK33Y_qK-wEx9ECYEGg8T8Bv -> Deer_Creek_30ft_concatenated.dat
  (2,267,033 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1t_vxv_Lh3evHxfXBm4jwsmXYXKlchDiA -> Antelope_Valley_Desert_Divers_2_9852409.csv
  (316,427 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1FJXruMG-fUP2LYLyEsLo2T5gU7IU7u4z -> Deer_Creek_test.csv
  (565,142 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1dhZBoTyfPHrtX2UHpZ5vYnniupUTG3AH -> AntelopeValleyDD_11192016_05132017_9852409.csv
  (336,600 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1rGxL302vemgcFcTd64twQ9JJyOX3MfL9 -> Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  (474,690 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1fsv9SEkjzh4j2hvLY3Mm7qNN6p5NDf68 -> AVDD_02102018_06082019_10281202.csv
  (859,524 bytes, 2026-09-25)
- >-
  data-portal-leo-carrillo.html links 1 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=12qRX8sJaBin-xpnv61EDlC7H6kyWupnx -> 9987952-Malibu_deployment_0.csv
  (454,432 bytes, 2026-09-25)
- >-
  data-portal-corral-beach.html links 1 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=1lZqUzLQ5r5NPv7_ZoX1tsT4y-BJdNMQ4 -> Corral899247.xls
  (587,231 bytes, 2026-09-25)
- >-
  data-portal-pt-dune.html links 1 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=1sKAIdN3sO3REaj2vKsjyXZeePpzvHmhp -> PtDume_30ft_09092017_11222017_formatted.dat
  (146,811 bytes, 2026-09-25)
- >-
  data-portal-malaga-cove.html links 2 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=1bOU3M2MDqAaN7U71oXNxydADTWWgMqxG -> Malaga_Cove_05262019_07272019_20481388.csv
  (108,778 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Malaga_Cover_30ft_06022021-12152022_20894275.csv -> Malaga_Cover_30ft_06022021-12152022_20894275.csv
  (1,300,530 bytes, 2026-09-25)
- >-
  data-portal-marine-land-platform.html links 6 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=18WtdROfUw4xRsvZnpDcswzuahO6ZiCoa -> OldMarineLand_12232018_11162019_10629315.csv
  (575,339 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1g9ovbnETV98q5-cadFUR9GDKs_2XSJvS -> OML_06022018_12232018_10862354_AoP_Desda.csv
  (352,156 bytes, 2026-09-25)
- http://www.catalinamarinesociety.org/files/MarinelandPlat_11182017_06022018_10178072.txt -> MarinelandPlat_11182017_06022018_10178072.txt
  (321,411 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1uVUwpF2508SRXS60NBLEkgyfMsyOTv3K -> AoP_06172017_11182017_10779230_AoP_Desda.csv
  (319,470 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1Xirg4nx8VCYWGs4kLGtFJpOaDSQ3JP62 -> MarineLandPlatform_111216_061717_10120264_56ft.csv
  (818,752 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1KLndTXJ4loRS0QLJV2PFcv2C8gtrYIje -> Marineland_test.csv
  (610,445 bytes, 2026-09-25)
- >-
  data-portal-white-point.html links 18 of the held files, in this order:
- https://www.catalinamarinesociety.org/files/WhitePoint_60ft_03072026-09162026_20894280.txt -> WhitePoint_60ft_03072026-09162026_20894280.txt
  (304,678 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/WhitePoint_30ft_03212026-09162026_22169469.txt -> WhitePoint_30ft_03212026-09162026_22169469.txt
  (282,500 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=13Ez4dKGbBuRYmunfLtv_SjIRBeAAYIIm -> WhitePtRock_12232018_11162019_10281199.csv
  (493,383 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1Ufxxr2BQNv5UNnnScMrKBV6KGfzFSwOG -> WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  (511,462 bytes, 2026-09-25)
- http://www.catalinamarinesociety.org/files/White_Pt_Rock_11172017_06022018_10862356.txt -> White_Pt_Rock_11172017_06022018_10862356.txt
  (312,079 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1qGKZDsGv3m8-GLyoLfCvFLCDpLsFbxy4 -> Question_06172017_11182017_10779230_AoP_Desda.csv
  (343,938 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1LEGaUM4sS-41luKw-Bn-ATL65teicIGQ -> WhitePtRock_111216_0617171077929_66ft.csv
  (411,030 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1o6He_O1yhnuYgfA6X3LvnWtKThgMtGC0 -> white_pt_rock_test.csv
  (610,448 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1PfSR_4w4SWJXZktjx_rAkL_YB4OF-SyH -> Data_Collect_1_9852409.csv
  (1,596,505 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1mkmIbT_hB37xzMbDqT7I6H8F0FnGFGbg -> WhitePointRock9852411-2011.xls
  (1,792,512 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1L1AlCI5Gad2HQDkAwL1KMeFP2zf2fbC5 -> 9987954_AoP_WhtPt_10112014_08292015.csv
  (521,990 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1lmqV1wwpad89fcgRWRwohuhvewCWNiIZ -> Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
  (1,128,285 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1uGSUzXt23zF5VUEjzuen6KqA7Nult37o -> Wht_Pt_Vent_27ft_09092017_03302018_20155868.prn
  (338,429 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1kcDHqG_YAakJu1zpHXDAd4-ire88N9G9 -> Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  (290,251 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1865skUxn2T02owQu2StaMzehfrWVLXya -> AoP_3_White_Point_27ft_09012016_10779229.csv
  (437,371 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1Hng2c6HQwC9-nDpvQkmjoBqmKuRCOciT -> 10120264_for_AOP_02152015.csv
  (264,291 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1Fxlv0I-9BWN-do58qNaY5oWidA_ZNWyS -> White_Point_Vent_30ft_10120264_04182014_10112014.csv
  (246,354 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=12ofNOX3rpb9tmD749ZbkHJZ6ODKn91Po -> WhtPtVent_10092013_02172018_concatenated.dat
  (2,445,091 bytes, 2026-09-25)
- >-
  data-portal-avalon-wreck.html links 13 of the held files, in this order:
- https://catalinamarinesociety.org/files/Jon_D._Avalon_55ft_06252020-12252022_20539513.csv -> Jon_D._Avalon_55ft_06252020-12252022_20539513.csv
  (1,596,851 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1ri1A7GI2zzLNvRMGLQJsmWDc7b9nF7lw -> Jon_Davies_06122019_06252020_20539517.csv
  (662,351 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=10HaSjoWaFC6KvWCLcC3O1GPuvJxBZIvL -> Jon_Davies_70ft_12082018_06122019_20235931.csv
  (320,152 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1Xj4EYD4qGlmywSkkxhPeh3dE2wemKkcU -> AvalonWreck_70ft_03062018_11152018_20235931.csv
  (483,655 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1xBMz_LWGW6i0nQ78zPy1FGFfWAZfSbHc -> AvalonWreck_55ft_03062018_11152018_10281204.csv
  (483,698 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1OoHUwfs1ObafERl28D72mYWRDwC74q7d -> AvalonWreck_55ft_07062017_03062018_9852409.csv
  (421,914 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1MNTNwSzWk3d-dmGVaPzQV9DW2xl_8jFc -> Jon_Davies_Deep_10178072_012016_072017.csv
  (966,055 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1tzlUUHLxbC3RKrJH6QWokD6n6bZph1aC -> Jon_Davies_Shallow_10076909_012016_072017.csv
  (966,169 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1YH3lb6dU8wiQEYlWQtsNGs-CaP3p62v6 -> SSAvalon_Jon_Davies_10248271_MARCH2014_DEEP.csv
  (162,217 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1UFePrUpaMVGVtCLNwdFSQfvZua8bE_Yt -> Jon_Davies_10281204_SSavalon_march2014_shallow.csv
  (162,718 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1bQc85sgFBFGEsqXB9xKTgCyeo_jNDxAK -> CTA_Jon_Davies_10248272_2014.csv
  (68,409 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1-UtZlPbBNq_M9jDqZ0UfP3VQeO5K9ANu -> CTA_Jon_Davies_10248269_2014.csv
  (63,762 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1JGDuVl1EphAYwzJZsMmp0BhBdz89CHvJ -> CTA_Jon_Davies10248271
  (1).csv (454,726 bytes, 2026-09-25)
- >-
  data-portal-crystal-cove.html links 1 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=1VgDQewxQSNkO-GpiuYru6HNBGkLIDcwX -> N._Caruso_deployment_second_thermograph_edited.csv
  (351,772 bytes, 2026-09-25)
- >-
  data-portal-montage.html links 3 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=13VirqyoivbKDsZuMmuIoamK1uTfxcfhc -> Montage_19ft_08022018_02292020_20155870.csv
  (1,109,935 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=11gGMMXH3KwITznmoE9LGL-R4uVi3K7l6 -> Montage_37ft_12172017_09022018_10779230.csv
  (449,984 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1JWk_ypJJ-HORW_VzpBH1NCLq6yIfJMb1 -> Montage_19ft_12172017_08312018_10281199.csv
  (446,314 bytes, 2026-09-25)
- >-
  data-portal-shaws.html links 16 of the held files, in this order:
- https://www.catalinamarinesociety.org/files/Shaws_60ft_10062024-04262025_21502242.txt -> Shaws_60ft_10062024-04262025_21502242.txt
  (289,074 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Shaws_30ft_05112024-10062024_21292584.dat -> Shaws_30ft_05112024-10062024_21292584.dat
  (256,192 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Shaws_60ft_05112024_10062024_20722049.dat -> Shaws_60ft_05112024_10062024_20722049.dat
  (256,207 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Shaws_30ft_09252022-05112024_21292585.csv -> Shaws_30ft_09252022-05112024_21292585.csv
  (1,027,972 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1hY7AfEBPB8sUqDRNIOtA4LakjCQmpTRM -> Shaws_60ft_04192019_12212019_20539516.csv
  (457,099 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1REzwOfV_PPKJOSawAh8rNqz5XIn-85PN -> Shaws_30ft_04192019_12212019_10862354.csv
  (457,212 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=152IuFQESYNEM_Vo7sq-Hp5Y5g2aIuqZO -> ShawsCove_60ft_03252018_04192019_20235928.csv
  (682,895 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=19c51pvfhuS_M9IU84fG8Kes1A-NWKzGF -> ShawsCove_30ft_03252018_04192019_10779228.csv
  (682,901 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1LhzXZ0wpzdkSDR53CKHaze8qqDWDdkPp -> ShawsCove_60ft_09092017_03302018_10120264.csv
  (328,762 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1o4hHJ-k4zkFt3RbRxGlhenIs1qs_ylnr -> ShawsCove_30ft_02042017_03302018_10629315.csv
  (693,586 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=17Xdbhpoe7ncgGvy2GWZzncolzYKdie32 -> Shaws_60ft_02122016_09232017_10281199.csv
  (960,881 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1HLDL0IPdGId8K8Jbq9i6QNrFIBSQpjFF -> Shaws_30ft_03112017_09232017_10862357.csv
  (313,971 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1h8iN8wP4u0P81oAi8VHL4P59s7eMJAFy -> 10779228_AoP_A.S.02152016_deep.csv
  (258,368 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1REp0NgoxTUAL0fhHgOV5U4Yw9UGYM8zh -> 10248272_AoP_A._S.02152016_shallow.csv
  (268,495 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1sZAHORNwdsHUkO9nMvA_Hk7h4QVQ-_jT -> ShawsCove_60ft_09272015_03252018_concatenated.dat
  (1,877,440 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1g2zhddLC4SM6U9GhH0TdzeUMlYV_OIqa -> ShawsCove_30ft_09272015_03252018_concatenated.dat
  (1,086,420 bytes, 2026-09-25)
- >-
  data-portal-cress-st.html links 13 of the held files, in this order:
- https://www.catalinamarinesociety.org/files/Cress_ST_60ft_12062025-09232026_22346693.txt -> Cress_ST_60ft_12062025-09232026_22346693.txt
  (463,715 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1gXzHosQX65raxi0A5sd1NIZCs7sjVgct -> AoP_Cress_Street_06042016_08282017_10779228_.csv
  (628,843 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1ObJMi7rw_R-kKjGi06xg47AyI-ac5gtH -> AoP_CressST_10281202_deep_08092015_06062016.csv
  (417,710 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1U5SBuzc9OpIgFIEL6rdCM0W6MK55BQD6 -> 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  (479,302 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1hftp-dGKWEa0JzjSPbhuNvmHLv4Pa0LR -> 10248272_AoP_CressSt_10172014_08092015de_Page1.csv
  (408,292 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1sUTzj3W9xyadew2nB64xuy9vP_-22vC1 -> AoP_CressST_10281200_shallow_05022014_10172014.csv
  (235,558 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1lR0vBmo_IfEiKr3SfY82qABb4rK7SVLs -> Cress_St_60ft_May2014_10281198.csv
  (274,458 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1CxQ9oqJ91tmkv5WBvzkbtyrkCtP2-Yr4 -> Cress_St_30ft_May2014_10281199.csv
  (274,932 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1xwwr70n4HOYx8JeoJ0ch5ccDoK1cFXM_ -> CTA_Cress_ST_60ft_10178072.xlsx
  (363,503 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1fKy4r_wI31U3LlG_pvMwzTB4VG7kJ2g1 -> Data_Collect_2_9852409_1.csv
  (246,249 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1p009QCSVd8gruKUdv-41IOnYDDo5vJLw -> 9898972_CTA_D.TSAO_1.csv
  (246,212 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1HEo3Or4V8vr2k0NVET-JLtclCS8uLVgH -> Cress_60ft_11032012_08272017_concatenated.dat
  (3,192,969 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1p01AvuE6LiNPKWiLgZe59jTXXyB-HjfX -> Cress_30ft_11032012_08092015_concatenated_1_.dat
  (1,555,836 bytes, 2026-09-25)
- >-
  data-portal-deadman-reef.html links 33 of the held files, in this order:
- https://www.catalinamarinesociety.org/files/Deadmans_30ft_01192025-10202025_22169465.txt -> Deadmans_30ft_01192025-10202025_22169465.txt
  (475,273 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Deadmans_60ft_01192025-10252025_22169462.txt -> Deadmans_60ft_01192025-10252025_22169462.txt
  (470,718 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Deadman_30ft_01312024-01192025_21894633.txt -> Deadman_30ft_01312024-01192025_21894633.txt
  (602,108 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Deadman_60ft_01312024-01192025_21894634.txt -> Deadman_60ft_01312024-01192025_21894634.txt
  (602,108 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Deadman_60ft_01032023-01312024_21502242.csv -> Deadman_60ft_01032023-01312024_21502242.csv
  (771,767 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Deadman_30ft_01032023-01312024_21502239.csv -> Deadman_30ft_01032023-01312024_21502239.csv
  (771,845 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Deadman_30ft_01222022-01032023_21292583.csv -> Deadman_30ft_01222022-01032023_21292583.csv
  (654,113 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/deadman_30f_10312020-01222022_20668565%20%281%29.txt ->
  deadman_30f_10312020-01222022_20668565 (1).txt (788,692 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Deadman_60ft_01220222-01032023_21292584.csv -> Deadman_60ft_01220222-01032023_21292584.csv
  (654,121 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/Deadman_60f_10312020-01222022_20668566%20%281%29.txt ->
  Deadman_60f_10312020-01222022_20668566 (1).txt (788,599 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1IsjCHmT4dFKke43n9SJgAo29a2IoI8zG -> Deadman_30ft_11252019_11012020_20481388.csv
  (610,694 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1dNblQ7UFfJmNEleoODlEMn5HFeOAsmjS -> Deadman_60ft_11252019_11012020.csv
  (664,855 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1tc9CCXtBlyMgJBO96s5szHQD0k2R3Xma -> Deadman_30ft_11192018_11252019_20481386.csv
  (662,535 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1o8tmFJdONgoh8QGsMssK8eYNpNwdyDOY -> Deadman_60ft_11192018_11252019_20481387.csv
  (662,498 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1ft6kobV5cbsxRkdo-LtPShO4eiI54c42 -> Deadman_60ft_12012017_11292018_20155869t.csv
  (647,140 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1mI0XYtVYnaQshG1_GWp4ZKvN-QOg6r93 -> Deadman_30ft_12012017_11292018_10862357.csv
  (647,066 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1uIl-di-sMoJlwM-aCA9tAGhLXvv_g7zt -> Sharshan-2_deep_12202016_11252017_10281204.csv
  (625,301 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=17PtEUhnJSbvpeJfYEJFTL59fMUmlPe6v -> Sharshan_shallow_121202016_11252017_10281202.csv
  (625,221 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1oKAOEmr0-kDb8-mrhzhbn5YXsASMEQTv -> Deadman_deep_09282015_12222016_10779230.dat
  (600,572 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1uiZJ6rKVIpl4MC0yAqbJyy8KVX_s_4ut -> Deadman_shallow_09282015_12222016_10248269.dat
  (600,614 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1yL8qqbEyh_jk6dkmf8-AQz48A9nfWSKk -> Ted_Sharshan_deep_11132014_09282015_10178072.csv
  (515,845 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1zZtmASJwe-L-ggUgK4dKU6EtFgGFjIjY -> deadmans_60ft_04082014_11132014_10281201.csv
  (298,900 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1HsumiYIDxJ1l6jHsb6CAH-dkxN74Eaef -> Deadmans_30ft_04082014_11132014_9898972.csv
  (299,242 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1zPb8e8nyH2wm5Re5d7BwxtA_AsxW5z_T -> Deadman_30ft_04102014.csv
  (125,562 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1ndr9P0skQ_xfAdDz06lYcuhgNCAtBrPL -> Ted_Sharshan_Laguna_deep_04.csv
  (426,945 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1yk6nEIGaQDEgOc9v0fNNfHZkGvkhdqO3 -> Ted_Sharhan_Laguna_shallow_04.csv
  (426,944 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1MmHxYZQrQ7J4lV6J9QMoHZT1L8FV1-Yl -> Ted_Sharshan_Laguna_deep_03.csv
  (345,210 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1rMV3YcGUjBSH8n31a95G1v-GElc1h464 -> Ted_Sharshan_Laguna_deep_02.csv
  (321,005 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1JyiE25x_vbaFUYuZtyt1s5pDyjncBNDr -> Ted_Sharhan_Laguna_shallow_02.csv
  (321,005 bytes, 2026-09-25)
- https://www.catalinamarinesociety.org/files/format10073222.txt -> format10073222.txt (197,457 bytes,
  2026-09-25)
- http://www.catalinamarinesociety.org/files/format9898972.txt -> format9898972.txt (98,767 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1lsMWU-knp6MQsVrPHokehwqgonMO1DVL -> deadman_60ft_concatenated.dat
  (3,913,884 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1eUOjFYpcICycgOGRylyHF6wnm-uOJfel -> deadman_30ft_concatenated.dat
  (3,521,879 bytes, 2026-09-25)
- >-
  data-portal-avalon-park.html links 2 of the held files, in this order:
- https://drive.google.com/uc?export=download&id=1hfa2Kwa6IpVUgswSFY-879IEdHqwvOjT -> Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  (79,475 bytes, 2026-09-25)
- https://drive.google.com/uc?export=download&id=1wuHCsTHms1Tlhzep-kKOAqsr2IOWrpJa -> Avalon_Park_30ft_09022019_11112019_10281202
  (1).csv (120,448 bytes, 2026-09-25)
format: >-
  The collection page states "We use Onset Computer's U22-0001 thermographs to record temperatures."
  and that "CMS data sets are linked below"; data-portal-shaws.html adds "Formats vary, but should be
  obvious." Those two sentences and the seven concatenated column lists below are the only statements
  about format in the text of the sixteen pages this record cites - the portal page, the collection
  page and the fourteen site pages - and none of the sixteen states a format for an individual file.
  This record holds 116 files, 74,539,512 bytes as served: 60 whose bytes decode as cp1252 and not as
  UTF-8, 40 as UTF-8, 13 as UTF-8 behind a byte-order mark, and three spreadsheets - CTA_Cress_ST_60ft_10178072.xlsx,
  an Office Open XML workbook, and Corral899247.xls and WhitePointRock9852411-2011.xls, both BIFF workbooks.
  Because the encoding differs from file to file the degree sign in a column label is the two bytes
  C2 B0 in the UTF-8 files and the single byte B0 in the cp1252 ones, and Shaws_60ft_10062024-04262025_21502242.txt
  writes it as a literal question mark, so its temperature column reads "Temp, ?F (LGR S/N: 21502242,
  SEN S/N: 21502242, LBL: AoP deep)"; variables enters each label as the file or the page that states
  it spells it. 29 of the 113 held text files begin with a line starting "Plot Title" and 39 with a
  line starting a double quote and then "Plot Title", 68 in all, and the workbook's first row holds
  "Plot Title: CTA D. Tsao" in its first cell, so 69 of the 116 files carry such a line; none of them
  is a column line. This record reads a file's column names from its first line, or from its second
  where the first begins "Plot Title" either bare or behind a double quote; it treats the line it lands
  on as a column line where that line's first field is "#" or carries a letter, and as a data row otherwise;
  and it splits the line on tab where the line holds one, else on comma, else on whitespace, running
  an unquoted field on until its parentheses balance and the next field opens none, so that "Date-Time
  (PST PDT)" is one column and not three. A double-quoted field's own surrounding quotes delimit that
  field and are not part of the name, so a header written '"#","Date Time, GMT-08:00"' enters the first
  column as "#" and not as '"#"'; no name this record enters carries a double quote. On that reading
  76 files state column names - 64 splitting on comma, 4 on tab, 7 on whitespace and one being the workbook,
  whose row 2 cells are the names - and 40 state none, those being 38 files whose first line is already
  a data row and the two BIFF workbooks, which this record does not read because BIFF is not reachable
  from the standard library and no dependency is added for it. A reading that took the first line of
  those 38 files as a column line would enter their first data row as column names. Across the 76 files
  that state names there are 76 distinct column names. The site pages state 8 spellings for the five
  files they label CONCATENATED, of which 4 are names no header line states - "hour-after-start-2010",
  "day-of-month", "temperature C", "temperature, C" - while the other 4 - "year", "month", "hour", "minute"
  - are already among those 76, each stated by the header line of format10073222.txt and format9898972.txt,
  so naming the five concatenated files for them adds files to an entry that exists rather than an entry.
  variables therefore carries 76 plus 4, 80 entries over 578 name-and-file pairs. Where a label carries
  a unit at all it carries it inside the label, as "Temp, °C" and "Batt, V" do, while a label such as
  "Coupler Detached" or "index" carries none; no page or file this record cites states a unit or a description
  apart from the label, so every entry reads unit: null and description: null; a reading that split
  a label at its comma would enter a shorter name and take the unit from the label's tail, and would
  have to choose where each label ends. Seven site pages print a line reading "Format of Concatenated
  data:" over a column list: data-portal-avalon-wreck.html, data-portal-deadman-reef.html, data-portal-deer-creek.html
  and data-portal-pt-dune.html print "hour-after-start-2010 year month day-of-month hour minute temperature
  C", and data-portal-cress-st.html, data-portal-shaws.html and data-portal-white-point.html print "hour-after-start-2010
  year month day-of-month hour minute temperature, C", with a comma before the C. Five links across
  three of those pages carry the word CONCATENATED in their own label - two on data-portal-deadman-reef.html,
  two on data-portal-shaws.html and one on data-portal-white-point.html - and variables names those
  five files for those seven columns, taking each spelling from the page the file is linked from. The
  other four pages print the format but label no link CONCATENATED, and no page states which of its
  files the format describes, so this record names no other file for those columns; a reading that attached
  them to each page's longest-span file would name four more
license: not stated
license_stated_at: >-
  Looked for first in the held files themselves, as add-source step 3's ladder starts there: none of
  the 116 contains any of "licen", "copyright", "creative", "terms", "cite", "citation", "disclaim",
  "public domain", "all rights reserved" or "attribut" in any letter case. Then looked for on twenty-two
  pages, all retrieved 2026-09-25: https://www.catalinamarinesociety.org/data-portal.html; https://www.catalinamarinesociety.org/data-portal-tsao-continental-thermograph-array-sites.html;
  the fourteen site pages; the three the site footer links by name - documents.html, archives.html and
  cms-magazine.html; and about.html, projects.html and index.html. The footer links no terms, licence
  or disclaimer page at all. It carries twelve links: those three pages, the Conflict of Interest Policy,
  the IRS determination letter and the Bylaws as PDFs, a PayPal donation URL, Facebook, Twitter, Instagram
  and YouTube, and a mailto: whose address is the placeholder "mail@domain.tld". Searching the text
  of all twenty-two pages for "licen", "copyright", "creative commons", "terms of use", "public domain",
  "attribut", "all rights reserved", "cite", "citation" and "disclaim" in any letter case, two pages
  match and twenty do not, on three matches between them. index.html matches "licen" once, in "a licensed
  NAUI Scuba Instructor", a person's diving certification. cms-magazine.html matches "copyright" twice,
  under a heading reading "COPYRIGHT", where it states "The CMS has copyright to the article and any
  publication wishing to reprint it must ask permission from the CMS. Author has personal use of the
  article."; that page is the magazine's guidance to authors submitting articles and states nothing
  about the thermograph data, so it is not this source's licence. The same page matches "cite" once,
  inside the word "unsolicited" in "We consider unsolicited articles for our magazine." None of the
  three matches is a grant or a condition on the data. The nearest statement about using the data is
  on the portal page, "The Catalina Marine Society (CMS) assumes no responsibility for the accuracy
  of the data and we strongly suggest that you contact the CMS before using the data for any matter
  of significance.", which grants no permission and states no condition, so it is not entered as a licence
  either
variables:
- name: '#'
  description: null
  unit: null
  file:
  - 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  - 9898972_CTA_D.TSAO_1.csv
  - 9987954_AoP_WhtPt_10112014_08292015.csv
  - AVDD_02102018_06082019_10281202.csv
  - AntelopeValleyDD_11192016_05132017_9852409.csv
  - Antelope_Valley_Desert_Divers_2_9852409.csv
  - AoP_06172017_11182017_10779230_AoP_Desda.csv
  - AoP_3_White_Point_27ft_09012016_10779229.csv
  - AvalonWreck_55ft_03062018_11152018_10281204.csv
  - AvalonWreck_55ft_07062017_03062018_9852409.csv
  - AvalonWreck_70ft_03062018_11152018_20235931.csv
  - Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
  - CTA_Cress_ST_60ft_10178072.xlsx
  - CTA_Jon_Davies10248271 (1).csv
  - CTA_Jon_Davies_10248272_2014.csv
  - Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  - Cress_ST_60ft_12062025-09232026_22346693.txt
  - Data_Collect_1_9852409.csv
  - Data_Collect_2_9852409_1.csv
  - Deadman_30ft_01032023-01312024_21502239.csv
  - Deadman_30ft_01222022-01032023_21292583.csv
  - Deadman_30ft_01312024-01192025_21894633.txt
  - Deadman_30ft_04102014.csv
  - Deadman_30ft_11192018_11252019_20481386.csv
  - Deadman_30ft_11252019_11012020_20481388.csv
  - Deadman_30ft_12012017_11292018_10862357.csv
  - Deadman_60f_10312020-01222022_20668566 (1).txt
  - Deadman_60ft_01032023-01312024_21502242.csv
  - Deadman_60ft_01220222-01032023_21292584.csv
  - Deadman_60ft_01312024-01192025_21894634.txt
  - Deadman_60ft_11192018_11252019_20481387.csv
  - Deadman_60ft_11252019_11012020.csv
  - Deadman_60ft_12012017_11292018_20155869t.csv
  - Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  - Jon_D._Avalon_55ft_06252020-12252022_20539513.csv
  - Jon_Davies_06122019_06252020_20539517.csv
  - Jon_Davies_70ft_12082018_06122019_20235931.csv
  - Jon_Davies_Deep_10178072_012016_072017.csv
  - Jon_Davies_Shallow_10076909_012016_072017.csv
  - Malaga_Cove_05262019_07272019_20481388.csv
  - Malaga_Cover_30ft_06022021-12152022_20894275.csv
  - MarineLandPlatform_111216_061717_10120264_56ft.csv
  - Montage_19ft_08022018_02292020_20155870.csv
  - Montage_19ft_12172017_08312018_10281199.csv
  - Montage_37ft_12172017_09022018_10779230.csv
  - OML_06022018_12232018_10862354_AoP_Desda.csv
  - Question_06172017_11182017_10779230_AoP_Desda.csv
  - Sharshan-2_deep_12202016_11252017_10281204.csv
  - Sharshan_shallow_121202016_11252017_10281202.csv
  - ShawsCove_30ft_03252018_04192019_10779228.csv
  - ShawsCove_60ft_03252018_04192019_20235928.csv
  - Shaws_30ft_03112017_09232017_10862357.csv
  - Shaws_30ft_04192019_12212019_10862354.csv
  - Shaws_30ft_09252022-05112024_21292585.csv
  - Shaws_60ft_02122016_09232017_10281199.csv
  - Shaws_60ft_04192019_12212019_20539516.csv
  - Shaws_60ft_05112024_10062024_20722049.dat
  - Shaws_60ft_10062024-04262025_21502242.txt
  - Ted_Sharhan_Laguna_shallow_02.csv
  - Ted_Sharhan_Laguna_shallow_04.csv
  - Ted_Sharshan_Laguna_deep_02.csv
  - Ted_Sharshan_Laguna_deep_03.csv
  - Ted_Sharshan_Laguna_deep_04.csv
  - Ted_Sharshan_deep_11132014_09282015_10178072.csv
  - WhitePoint_30ft_03212026-09162026_22169469.txt
  - WhitePoint_60ft_03072026-09162026_20894280.txt
  - WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  - WhitePtRock_111216_0617171077929_66ft.csv
  - Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  - Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
  - deadman_30f_10312020-01222022_20668565 (1).txt
- name: Temp, °C
  description: null
  unit: null
  file:
  - 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  - 9898972_CTA_D.TSAO_1.csv
  - 9987954_AoP_WhtPt_10112014_08292015.csv
  - AVDD_02102018_06082019_10281202.csv
  - AntelopeValleyDD_11192016_05132017_9852409.csv
  - Antelope_Valley_Desert_Divers_2_9852409.csv
  - AoP_06172017_11182017_10779230_AoP_Desda.csv
  - AoP_3_White_Point_27ft_09012016_10779229.csv
  - AvalonWreck_55ft_03062018_11152018_10281204.csv
  - AvalonWreck_55ft_07062017_03062018_9852409.csv
  - AvalonWreck_70ft_03062018_11152018_20235931.csv
  - Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
  - CTA_Cress_ST_60ft_10178072.xlsx
  - CTA_Jon_Davies10248271 (1).csv
  - CTA_Jon_Davies_10248269_2014.csv
  - CTA_Jon_Davies_10248272_2014.csv
  - Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  - Data_Collect_1_9852409.csv
  - Data_Collect_2_9852409_1.csv
  - Deadman_30ft_04102014.csv
  - Deadman_30ft_11192018_11252019_20481386.csv
  - Deadman_30ft_11252019_11012020_20481388.csv
  - Deadman_30ft_12012017_11292018_10862357.csv
  - Deadman_60f_10312020-01222022_20668566 (1).txt
  - Deadman_60ft_11192018_11252019_20481387.csv
  - Deadman_60ft_11252019_11012020.csv
  - Deadman_60ft_12012017_11292018_20155869t.csv
  - Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  - Jon_Davies_06122019_06252020_20539517.csv
  - Jon_Davies_70ft_12082018_06122019_20235931.csv
  - Jon_Davies_Deep_10178072_012016_072017.csv
  - Jon_Davies_Shallow_10076909_012016_072017.csv
  - Malaga_Cove_05262019_07272019_20481388.csv
  - MarineLandPlatform_111216_061717_10120264_56ft.csv
  - Montage_19ft_08022018_02292020_20155870.csv
  - Montage_19ft_12172017_08312018_10281199.csv
  - Montage_37ft_12172017_09022018_10779230.csv
  - OML_06022018_12232018_10862354_AoP_Desda.csv
  - Question_06172017_11182017_10779230_AoP_Desda.csv
  - Sharshan-2_deep_12202016_11252017_10281204.csv
  - Sharshan_shallow_121202016_11252017_10281202.csv
  - ShawsCove_30ft_03252018_04192019_10779228.csv
  - ShawsCove_60ft_03252018_04192019_20235928.csv
  - Shaws_30ft_03112017_09232017_10862357.csv
  - Shaws_30ft_04192019_12212019_10862354.csv
  - Shaws_60ft_02122016_09232017_10281199.csv
  - Shaws_60ft_04192019_12212019_20539516.csv
  - Ted_Sharhan_Laguna_shallow_02.csv
  - Ted_Sharhan_Laguna_shallow_04.csv
  - Ted_Sharshan_Laguna_deep_02.csv
  - Ted_Sharshan_Laguna_deep_03.csv
  - Ted_Sharshan_Laguna_deep_04.csv
  - Ted_Sharshan_deep_11132014_09282015_10178072.csv
  - WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  - WhitePtRock_111216_0617171077929_66ft.csv
  - Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  - Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
  - deadman_30f_10312020-01222022_20668565 (1).txt
- name: Coupler Detached
  description: null
  unit: null
  file:
  - 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  - 9898972_CTA_D.TSAO_1.csv
  - 9987954_AoP_WhtPt_10112014_08292015.csv
  - AVDD_02102018_06082019_10281202.csv
  - AntelopeValleyDD_11192016_05132017_9852409.csv
  - Antelope_Valley_Desert_Divers_2_9852409.csv
  - AoP_06172017_11182017_10779230_AoP_Desda.csv
  - AoP_3_White_Point_27ft_09012016_10779229.csv
  - AvalonWreck_55ft_03062018_11152018_10281204.csv
  - AvalonWreck_55ft_07062017_03062018_9852409.csv
  - AvalonWreck_70ft_03062018_11152018_20235931.csv
  - Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
  - CTA_Jon_Davies10248271 (1).csv
  - Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  - Data_Collect_1_9852409.csv
  - Data_Collect_2_9852409_1.csv
  - Deadman_30ft_04102014.csv
  - Deadman_30ft_11192018_11252019_20481386.csv
  - Deadman_30ft_11252019_11012020_20481388.csv
  - Deadman_30ft_12012017_11292018_10862357.csv
  - Deadman_60f_10312020-01222022_20668566 (1).txt
  - Deadman_60ft_11192018_11252019_20481387.csv
  - Deadman_60ft_11252019_11012020.csv
  - Deadman_60ft_12012017_11292018_20155869t.csv
  - Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  - Jon_Davies_06122019_06252020_20539517.csv
  - Jon_Davies_70ft_12082018_06122019_20235931.csv
  - Jon_Davies_Deep_10178072_012016_072017.csv
  - Jon_Davies_Shallow_10076909_012016_072017.csv
  - Malaga_Cove_05262019_07272019_20481388.csv
  - MarineLandPlatform_111216_061717_10120264_56ft.csv
  - Montage_19ft_08022018_02292020_20155870.csv
  - Montage_19ft_12172017_08312018_10281199.csv
  - Montage_37ft_12172017_09022018_10779230.csv
  - OML_06022018_12232018_10862354_AoP_Desda.csv
  - Question_06172017_11182017_10779230_AoP_Desda.csv
  - Sharshan-2_deep_12202016_11252017_10281204.csv
  - Sharshan_shallow_121202016_11252017_10281202.csv
  - ShawsCove_30ft_03252018_04192019_10779228.csv
  - ShawsCove_60ft_03252018_04192019_20235928.csv
  - Shaws_30ft_03112017_09232017_10862357.csv
  - Shaws_30ft_04192019_12212019_10862354.csv
  - Shaws_60ft_02122016_09232017_10281199.csv
  - Shaws_60ft_04192019_12212019_20539516.csv
  - Ted_Sharhan_Laguna_shallow_02.csv
  - Ted_Sharhan_Laguna_shallow_04.csv
  - Ted_Sharshan_Laguna_deep_02.csv
  - Ted_Sharshan_Laguna_deep_03.csv
  - Ted_Sharshan_Laguna_deep_04.csv
  - Ted_Sharshan_deep_11132014_09282015_10178072.csv
  - WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  - WhitePtRock_111216_0617171077929_66ft.csv
  - Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  - Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
  - deadman_30f_10312020-01222022_20668565 (1).txt
- name: End Of File
  description: null
  unit: null
  file:
  - 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  - 9898972_CTA_D.TSAO_1.csv
  - 9987954_AoP_WhtPt_10112014_08292015.csv
  - AVDD_02102018_06082019_10281202.csv
  - AntelopeValleyDD_11192016_05132017_9852409.csv
  - Antelope_Valley_Desert_Divers_2_9852409.csv
  - AoP_06172017_11182017_10779230_AoP_Desda.csv
  - AoP_3_White_Point_27ft_09012016_10779229.csv
  - AvalonWreck_55ft_03062018_11152018_10281204.csv
  - AvalonWreck_55ft_07062017_03062018_9852409.csv
  - AvalonWreck_70ft_03062018_11152018_20235931.csv
  - Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
  - CTA_Jon_Davies10248271 (1).csv
  - Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  - Data_Collect_1_9852409.csv
  - Data_Collect_2_9852409_1.csv
  - Deadman_30ft_04102014.csv
  - Deadman_30ft_11192018_11252019_20481386.csv
  - Deadman_30ft_11252019_11012020_20481388.csv
  - Deadman_30ft_12012017_11292018_10862357.csv
  - Deadman_60f_10312020-01222022_20668566 (1).txt
  - Deadman_60ft_11192018_11252019_20481387.csv
  - Deadman_60ft_11252019_11012020.csv
  - Deadman_60ft_12012017_11292018_20155869t.csv
  - Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  - Jon_Davies_06122019_06252020_20539517.csv
  - Jon_Davies_70ft_12082018_06122019_20235931.csv
  - Jon_Davies_Deep_10178072_012016_072017.csv
  - Jon_Davies_Shallow_10076909_012016_072017.csv
  - Malaga_Cove_05262019_07272019_20481388.csv
  - MarineLandPlatform_111216_061717_10120264_56ft.csv
  - Montage_19ft_08022018_02292020_20155870.csv
  - Montage_19ft_12172017_08312018_10281199.csv
  - Montage_37ft_12172017_09022018_10779230.csv
  - OML_06022018_12232018_10862354_AoP_Desda.csv
  - Question_06172017_11182017_10779230_AoP_Desda.csv
  - Sharshan-2_deep_12202016_11252017_10281204.csv
  - Sharshan_shallow_121202016_11252017_10281202.csv
  - ShawsCove_30ft_03252018_04192019_10779228.csv
  - ShawsCove_60ft_03252018_04192019_20235928.csv
  - Shaws_30ft_03112017_09232017_10862357.csv
  - Shaws_30ft_04192019_12212019_10862354.csv
  - Shaws_60ft_02122016_09232017_10281199.csv
  - Shaws_60ft_04192019_12212019_20539516.csv
  - Ted_Sharhan_Laguna_shallow_02.csv
  - Ted_Sharhan_Laguna_shallow_04.csv
  - Ted_Sharshan_Laguna_deep_02.csv
  - Ted_Sharshan_Laguna_deep_03.csv
  - Ted_Sharshan_Laguna_deep_04.csv
  - Ted_Sharshan_deep_11132014_09282015_10178072.csv
  - WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  - WhitePtRock_111216_0617171077929_66ft.csv
  - Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  - Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
  - deadman_30f_10312020-01222022_20668565 (1).txt
- name: Coupler Attached
  description: null
  unit: null
  file:
  - 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  - 9898972_CTA_D.TSAO_1.csv
  - 9987954_AoP_WhtPt_10112014_08292015.csv
  - AVDD_02102018_06082019_10281202.csv
  - AntelopeValleyDD_11192016_05132017_9852409.csv
  - AoP_06172017_11182017_10779230_AoP_Desda.csv
  - AoP_3_White_Point_27ft_09012016_10779229.csv
  - AvalonWreck_55ft_03062018_11152018_10281204.csv
  - AvalonWreck_55ft_07062017_03062018_9852409.csv
  - AvalonWreck_70ft_03062018_11152018_20235931.csv
  - Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
  - CTA_Jon_Davies10248271 (1).csv
  - Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  - Data_Collect_2_9852409_1.csv
  - Deadman_30ft_04102014.csv
  - Deadman_30ft_11192018_11252019_20481386.csv
  - Deadman_30ft_11252019_11012020_20481388.csv
  - Deadman_30ft_12012017_11292018_10862357.csv
  - Deadman_60f_10312020-01222022_20668566 (1).txt
  - Deadman_60ft_11192018_11252019_20481387.csv
  - Deadman_60ft_11252019_11012020.csv
  - Deadman_60ft_12012017_11292018_20155869t.csv
  - Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  - Jon_Davies_06122019_06252020_20539517.csv
  - Jon_Davies_70ft_12082018_06122019_20235931.csv
  - Jon_Davies_Deep_10178072_012016_072017.csv
  - Jon_Davies_Shallow_10076909_012016_072017.csv
  - Malaga_Cove_05262019_07272019_20481388.csv
  - MarineLandPlatform_111216_061717_10120264_56ft.csv
  - Montage_19ft_08022018_02292020_20155870.csv
  - Montage_19ft_12172017_08312018_10281199.csv
  - Montage_37ft_12172017_09022018_10779230.csv
  - OML_06022018_12232018_10862354_AoP_Desda.csv
  - Question_06172017_11182017_10779230_AoP_Desda.csv
  - Sharshan-2_deep_12202016_11252017_10281204.csv
  - Sharshan_shallow_121202016_11252017_10281202.csv
  - ShawsCove_30ft_03252018_04192019_10779228.csv
  - ShawsCove_60ft_03252018_04192019_20235928.csv
  - Shaws_30ft_03112017_09232017_10862357.csv
  - Shaws_30ft_04192019_12212019_10862354.csv
  - Shaws_60ft_02122016_09232017_10281199.csv
  - Shaws_60ft_04192019_12212019_20539516.csv
  - Ted_Sharhan_Laguna_shallow_02.csv
  - Ted_Sharhan_Laguna_shallow_04.csv
  - Ted_Sharshan_Laguna_deep_02.csv
  - Ted_Sharshan_Laguna_deep_03.csv
  - Ted_Sharshan_Laguna_deep_04.csv
  - Ted_Sharshan_deep_11132014_09282015_10178072.csv
  - WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  - WhitePtRock_111216_0617171077929_66ft.csv
  - Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  - Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
  - deadman_30f_10312020-01222022_20668565 (1).txt
- name: Host Connected
  description: null
  unit: null
  file:
  - 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  - 9898972_CTA_D.TSAO_1.csv
  - 9987954_AoP_WhtPt_10112014_08292015.csv
  - AVDD_02102018_06082019_10281202.csv
  - AntelopeValleyDD_11192016_05132017_9852409.csv
  - AoP_06172017_11182017_10779230_AoP_Desda.csv
  - AoP_3_White_Point_27ft_09012016_10779229.csv
  - AvalonWreck_55ft_03062018_11152018_10281204.csv
  - AvalonWreck_55ft_07062017_03062018_9852409.csv
  - AvalonWreck_70ft_03062018_11152018_20235931.csv
  - Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
  - CTA_Jon_Davies10248271 (1).csv
  - Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  - Data_Collect_2_9852409_1.csv
  - Deadman_30ft_04102014.csv
  - Deadman_30ft_11192018_11252019_20481386.csv
  - Deadman_30ft_11252019_11012020_20481388.csv
  - Deadman_30ft_12012017_11292018_10862357.csv
  - Deadman_60f_10312020-01222022_20668566 (1).txt
  - Deadman_60ft_11192018_11252019_20481387.csv
  - Deadman_60ft_11252019_11012020.csv
  - Deadman_60ft_12012017_11292018_20155869t.csv
  - Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  - Jon_Davies_06122019_06252020_20539517.csv
  - Jon_Davies_70ft_12082018_06122019_20235931.csv
  - Jon_Davies_Deep_10178072_012016_072017.csv
  - Jon_Davies_Shallow_10076909_012016_072017.csv
  - Malaga_Cove_05262019_07272019_20481388.csv
  - MarineLandPlatform_111216_061717_10120264_56ft.csv
  - Montage_19ft_08022018_02292020_20155870.csv
  - Montage_19ft_12172017_08312018_10281199.csv
  - Montage_37ft_12172017_09022018_10779230.csv
  - OML_06022018_12232018_10862354_AoP_Desda.csv
  - Question_06172017_11182017_10779230_AoP_Desda.csv
  - Sharshan-2_deep_12202016_11252017_10281204.csv
  - Sharshan_shallow_121202016_11252017_10281202.csv
  - ShawsCove_30ft_03252018_04192019_10779228.csv
  - ShawsCove_60ft_03252018_04192019_20235928.csv
  - Shaws_30ft_03112017_09232017_10862357.csv
  - Shaws_30ft_04192019_12212019_10862354.csv
  - Shaws_60ft_02122016_09232017_10281199.csv
  - Shaws_60ft_04192019_12212019_20539516.csv
  - Ted_Sharhan_Laguna_shallow_02.csv
  - Ted_Sharhan_Laguna_shallow_04.csv
  - Ted_Sharshan_Laguna_deep_02.csv
  - Ted_Sharshan_Laguna_deep_03.csv
  - Ted_Sharshan_Laguna_deep_04.csv
  - Ted_Sharshan_deep_11132014_09282015_10178072.csv
  - WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  - WhitePtRock_111216_0617171077929_66ft.csv
  - Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  - Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
  - deadman_30f_10312020-01222022_20668565 (1).txt
- name: Stopped
  description: null
  unit: null
  file:
  - 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  - 9898972_CTA_D.TSAO_1.csv
  - 9987954_AoP_WhtPt_10112014_08292015.csv
  - AVDD_02102018_06082019_10281202.csv
  - AntelopeValleyDD_11192016_05132017_9852409.csv
  - AoP_06172017_11182017_10779230_AoP_Desda.csv
  - AoP_3_White_Point_27ft_09012016_10779229.csv
  - AvalonWreck_55ft_03062018_11152018_10281204.csv
  - AvalonWreck_55ft_07062017_03062018_9852409.csv
  - AvalonWreck_70ft_03062018_11152018_20235931.csv
  - Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
  - CTA_Jon_Davies10248271 (1).csv
  - Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  - Data_Collect_2_9852409_1.csv
  - Deadman_30ft_04102014.csv
  - Deadman_30ft_11192018_11252019_20481386.csv
  - Deadman_30ft_11252019_11012020_20481388.csv
  - Deadman_30ft_12012017_11292018_10862357.csv
  - Deadman_60f_10312020-01222022_20668566 (1).txt
  - Deadman_60ft_11192018_11252019_20481387.csv
  - Deadman_60ft_11252019_11012020.csv
  - Deadman_60ft_12012017_11292018_20155869t.csv
  - Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  - Jon_Davies_06122019_06252020_20539517.csv
  - Jon_Davies_70ft_12082018_06122019_20235931.csv
  - Jon_Davies_Deep_10178072_012016_072017.csv
  - Jon_Davies_Shallow_10076909_012016_072017.csv
  - Malaga_Cove_05262019_07272019_20481388.csv
  - MarineLandPlatform_111216_061717_10120264_56ft.csv
  - Montage_19ft_08022018_02292020_20155870.csv
  - Montage_19ft_12172017_08312018_10281199.csv
  - Montage_37ft_12172017_09022018_10779230.csv
  - OML_06022018_12232018_10862354_AoP_Desda.csv
  - Question_06172017_11182017_10779230_AoP_Desda.csv
  - Sharshan-2_deep_12202016_11252017_10281204.csv
  - Sharshan_shallow_121202016_11252017_10281202.csv
  - ShawsCove_30ft_03252018_04192019_10779228.csv
  - ShawsCove_60ft_03252018_04192019_20235928.csv
  - Shaws_30ft_03112017_09232017_10862357.csv
  - Shaws_30ft_04192019_12212019_10862354.csv
  - Shaws_60ft_02122016_09232017_10281199.csv
  - Shaws_60ft_04192019_12212019_20539516.csv
  - Ted_Sharhan_Laguna_shallow_02.csv
  - Ted_Sharhan_Laguna_shallow_04.csv
  - Ted_Sharshan_Laguna_deep_02.csv
  - Ted_Sharshan_Laguna_deep_03.csv
  - Ted_Sharshan_Laguna_deep_04.csv
  - Ted_Sharshan_deep_11132014_09282015_10178072.csv
  - WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  - WhitePtRock_111216_0617171077929_66ft.csv
  - Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  - Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
  - deadman_30f_10312020-01222022_20668565 (1).txt
- name: Date Time, GMT-08:00
  description: null
  unit: null
  file:
  - AVDD_02102018_06082019_10281202.csv
  - AntelopeValleyDD_11192016_05132017_9852409.csv
  - AoP_3_White_Point_27ft_09012016_10779229.csv
  - AvalonWreck_55ft_03062018_11152018_10281204.csv
  - AvalonWreck_70ft_03062018_11152018_20235931.csv
  - CTA_Jon_Davies10248271 (1).csv
  - CTA_Jon_Davies_10248269_2014.csv
  - Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
  - Data_Collect_1_9852409.csv
  - Deadman_30ft_01222022-01032023_21292583.csv
  - Deadman_30ft_04102014.csv
  - Deadman_30ft_11192018_11252019_20481386.csv
  - Deadman_30ft_11252019_11012020_20481388.csv
  - Deadman_30ft_12012017_11292018_10862357.csv
  - Deadman_60ft_01220222-01032023_21292584.csv
  - Deadman_60ft_11192018_11252019_20481387.csv
  - Deadman_60ft_11252019_11012020.csv
  - Deadman_60ft_12012017_11292018_20155869t.csv
  - Jon_Davies_70ft_12082018_06122019_20235931.csv
  - Jon_Davies_Deep_10178072_012016_072017.csv
  - Jon_Davies_Shallow_10076909_012016_072017.csv
  - Malaga_Cove_05262019_07272019_20481388.csv
  - Malaga_Cover_30ft_06022021-12152022_20894275.csv
  - MarineLandPlatform_111216_061717_10120264_56ft.csv
  - Montage_19ft_12172017_08312018_10281199.csv
  - Montage_37ft_12172017_09022018_10779230.csv
  - Sharshan-2_deep_12202016_11252017_10281204.csv
  - Sharshan_shallow_121202016_11252017_10281202.csv
  - ShawsCove_30ft_03252018_04192019_10779228.csv
  - ShawsCove_60ft_03252018_04192019_20235928.csv
  - Shaws_30ft_03112017_09232017_10862357.csv
  - Shaws_60ft_02122016_09232017_10281199.csv
  - Ted_Sharshan_Laguna_deep_03.csv
  - Ted_Sharshan_deep_11132014_09282015_10178072.csv
  - Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
  - Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
- name: Date Time, GMT-07:00
  description: null
  unit: null
  file:
  - 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
  - 9898972_CTA_D.TSAO_1.csv
  - 9987954_AoP_WhtPt_10112014_08292015.csv
  - Antelope_Valley_Desert_Divers_2_9852409.csv
  - AoP_06172017_11182017_10779230_AoP_Desda.csv
  - AvalonWreck_55ft_07062017_03062018_9852409.csv
  - Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
  - CTA_Cress_ST_60ft_10178072.xlsx
  - CTA_Jon_Davies_10248272_2014.csv
  - Data_Collect_2_9852409_1.csv
  - Deadman_60f_10312020-01222022_20668566 (1).txt
  - Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
  - Jon_D._Avalon_55ft_06252020-12252022_20539513.csv
  - Jon_Davies_06122019_06252020_20539517.csv
  - Montage_19ft_08022018_02292020_20155870.csv
  - OML_06022018_12232018_10862354_AoP_Desda.csv
  - Question_06172017_11182017_10779230_AoP_Desda.csv
  - Shaws_30ft_04192019_12212019_10862354.csv
  - Shaws_30ft_09252022-05112024_21292585.csv
  - Shaws_60ft_04192019_12212019_20539516.csv
  - Ted_Sharhan_Laguna_shallow_02.csv
  - Ted_Sharhan_Laguna_shallow_04.csv
  - Ted_Sharshan_Laguna_deep_02.csv
  - Ted_Sharshan_Laguna_deep_04.csv
  - WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
  - WhitePtRock_111216_0617171077929_66ft.csv
  - deadman_30f_10312020-01222022_20668565 (1).txt
- name: hour
  description: null
  unit: null
  file:
  - ShawsCove_30ft_09272015_03252018_concatenated.dat
  - ShawsCove_60ft_09272015_03252018_concatenated.dat
  - WhtPtVent_10092013_02172018_concatenated.dat
  - deadman_30ft_concatenated.dat
  - deadman_60ft_concatenated.dat
  - format10073222.txt
  - format9898972.txt
- name: minute
  description: null
  unit: null
  file:
  - ShawsCove_30ft_09272015_03252018_concatenated.dat
  - ShawsCove_60ft_09272015_03252018_concatenated.dat
  - WhtPtVent_10092013_02172018_concatenated.dat
  - deadman_30ft_concatenated.dat
  - deadman_60ft_concatenated.dat
  - format10073222.txt
  - format9898972.txt
- name: month
  description: null
  unit: null
  file:
  - ShawsCove_30ft_09272015_03252018_concatenated.dat
  - ShawsCove_60ft_09272015_03252018_concatenated.dat
  - WhtPtVent_10092013_02172018_concatenated.dat
  - deadman_30ft_concatenated.dat
  - deadman_60ft_concatenated.dat
  - format10073222.txt
  - format9898972.txt
- name: year
  description: null
  unit: null
  file:
  - ShawsCove_30ft_09272015_03252018_concatenated.dat
  - ShawsCove_60ft_09272015_03252018_concatenated.dat
  - WhtPtVent_10092013_02172018_concatenated.dat
  - deadman_30ft_concatenated.dat
  - deadman_60ft_concatenated.dat
  - format10073222.txt
  - format9898972.txt
- name: day-of-month
  description: null
  unit: null
  file:
  - ShawsCove_30ft_09272015_03252018_concatenated.dat
  - ShawsCove_60ft_09272015_03252018_concatenated.dat
  - WhtPtVent_10092013_02172018_concatenated.dat
  - deadman_30ft_concatenated.dat
  - deadman_60ft_concatenated.dat
- name: hour-after-start-2010
  description: null
  unit: null
  file:
  - ShawsCove_30ft_09272015_03252018_concatenated.dat
  - ShawsCove_60ft_09272015_03252018_concatenated.dat
  - WhtPtVent_10092013_02172018_concatenated.dat
  - deadman_30ft_concatenated.dat
  - deadman_60ft_concatenated.dat
- name: Date Time  GMT-06 00
  description: null
  unit: null
  file:
  - Deadman_30ft_01312024-01192025_21894633.txt
  - Deadman_60ft_01312024-01192025_21894634.txt
  - Shaws_60ft_05112024_10062024_20722049.dat
- name: temperature, C
  description: null
  unit: null
  file:
  - ShawsCove_30ft_09272015_03252018_concatenated.dat
  - ShawsCove_60ft_09272015_03252018_concatenated.dat
  - WhtPtVent_10092013_02172018_concatenated.dat
- name: 2011yearhour
  description: null
  unit: null
  file:
  - format10073222.txt
  - format9898972.txt
- name: Date Time, GMT-06:00
  description: null
  unit: null
  file:
  - Deadman_30ft_01032023-01312024_21502239.csv
  - Deadman_60ft_01032023-01312024_21502242.csv
- name: Date-Time (PST PDT)
  description: null
  unit: null
  file:
  - Cress_ST_60ft_12062025-09232026_22346693.txt
  - WhitePoint_60ft_03072026-09162026_20894280.txt
- name: 'End Of File (LGR S/N: 21502242)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01032023-01312024_21502242.csv
  - Shaws_60ft_10062024-04262025_21502242.txt
- name: GMT-8:00
  description: null
  unit: null
  file:
  - Cress_St_30ft_May2014_10281199.csv
  - Cress_St_60ft_May2014_10281198.csv
- name: Temp. C
  description: null
  unit: null
  file:
  - Cress_St_30ft_May2014_10281199.csv
  - Cress_St_60ft_May2014_10281198.csv
- name: day
  description: null
  unit: null
  file:
  - format10073222.txt
  - format9898972.txt
- name: index
  description: null
  unit: null
  file:
  - Cress_St_30ft_May2014_10281199.csv
  - Cress_St_60ft_May2014_10281198.csv
- name: temperature C
  description: null
  unit: null
  file:
  - deadman_30ft_concatenated.dat
  - deadman_60ft_concatenated.dat
- name: temperatureC
  description: null
  unit: null
  file:
  - format10073222.txt
  - format9898972.txt
- name: Batt, V
  description: null
  unit: null
  file:
  - CTA_Cress_ST_60ft_10178072.xlsx
- name: 'Coupler Attached (LGR S/N: 20894275)'
  description: null
  unit: null
  file:
  - Malaga_Cover_30ft_06022021-12152022_20894275.csv
- name: 'Coupler Attached (LGR S/N: 21292583)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01222022-01032023_21292583.csv
- name: 'Coupler Attached (LGR S/N: 21292584)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01220222-01032023_21292584.csv
- name: 'Coupler Attached (LGR S/N: 21292585)'
  description: null
  unit: null
  file:
  - Shaws_30ft_09252022-05112024_21292585.csv
- name: 'Coupler Attached (LGR S/N: 21502239)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01032023-01312024_21502239.csv
- name: 'Coupler Attached (LGR S/N: 21502242)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01032023-01312024_21502242.csv
- name: 'Coupler Detached (LGR S/N: 20539513)'
  description: null
  unit: null
  file:
  - Jon_D._Avalon_55ft_06252020-12252022_20539513.csv
- name: 'Coupler Detached (LGR S/N: 20894275)'
  description: null
  unit: null
  file:
  - Malaga_Cover_30ft_06022021-12152022_20894275.csv
- name: 'Coupler Detached (LGR S/N: 21292583)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01222022-01032023_21292583.csv
- name: 'Coupler Detached (LGR S/N: 21292584)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01220222-01032023_21292584.csv
- name: 'Coupler Detached (LGR S/N: 21292585)'
  description: null
  unit: null
  file:
  - Shaws_30ft_09252022-05112024_21292585.csv
- name: 'Coupler Detached (LGR S/N: 21502239)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01032023-01312024_21502239.csv
- name: 'Coupler Detached (LGR S/N: 21502242)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01032023-01312024_21502242.csv
- name: Cress St 30 ft 10281199
  description: null
  unit: null
  file:
  - Cress_St_30ft_May2014_10281199.csv
- name: Cress St. 60 ft. , °C
  description: null
  unit: null
  file:
  - Cress_ST_60ft_12062025-09232026_22346693.txt
- name: Cress Str. AoP 10281198
  description: null
  unit: null
  file:
  - Cress_St_60ft_May2014_10281198.csv
- name: Date Time, GMT-05:00
  description: null
  unit: null
  file:
  - Shaws_60ft_10062024-04262025_21502242.txt
- name: Date-Time (PDT)
  description: null
  unit: null
  file:
  - WhitePoint_30ft_03212026-09162026_22169469.txt
- name: End Of File (LGR S N  20733049)
  description: null
  unit: null
  file:
  - Shaws_60ft_05112024_10062024_20722049.dat
- name: End Of File (LGR S N  21894633)
  description: null
  unit: null
  file:
  - Deadman_30ft_01312024-01192025_21894633.txt
- name: End Of File (LGR S N  21894634)
  description: null
  unit: null
  file:
  - Deadman_60ft_01312024-01192025_21894634.txt
- name: 'End Of File (LGR S/N: 20539513)'
  description: null
  unit: null
  file:
  - Jon_D._Avalon_55ft_06252020-12252022_20539513.csv
- name: 'End Of File (LGR S/N: 20894275)'
  description: null
  unit: null
  file:
  - Malaga_Cover_30ft_06022021-12152022_20894275.csv
- name: 'End Of File (LGR S/N: 21292583)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01222022-01032023_21292583.csv
- name: 'End Of File (LGR S/N: 21292584)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01220222-01032023_21292584.csv
- name: 'End Of File (LGR S/N: 21292585)'
  description: null
  unit: null
  file:
  - Shaws_30ft_09252022-05112024_21292585.csv
- name: 'End Of File (LGR S/N: 21502239)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01032023-01312024_21502239.csv
- name: 'Host Connected (LGR S/N: 20894275)'
  description: null
  unit: null
  file:
  - Malaga_Cover_30ft_06022021-12152022_20894275.csv
- name: 'Host Connected (LGR S/N: 21292583)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01222022-01032023_21292583.csv
- name: 'Host Connected (LGR S/N: 21292584)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01220222-01032023_21292584.csv
- name: 'Host Connected (LGR S/N: 21292585)'
  description: null
  unit: null
  file:
  - Shaws_30ft_09252022-05112024_21292585.csv
- name: 'Host Connected (LGR S/N: 21502239)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01032023-01312024_21502239.csv
- name: 'Host Connected (LGR S/N: 21502242)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01032023-01312024_21502242.csv
- name: 'Stopped (LGR S/N: 20894275)'
  description: null
  unit: null
  file:
  - Malaga_Cover_30ft_06022021-12152022_20894275.csv
- name: 'Stopped (LGR S/N: 21292583)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01222022-01032023_21292583.csv
- name: 'Stopped (LGR S/N: 21292584)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01220222-01032023_21292584.csv
- name: 'Stopped (LGR S/N: 21292585)'
  description: null
  unit: null
  file:
  - Shaws_30ft_09252022-05112024_21292585.csv
- name: 'Stopped (LGR S/N: 21502239)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01032023-01312024_21502239.csv
- name: 'Stopped (LGR S/N: 21502242)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01032023-01312024_21502242.csv
- name: Temp  °F (LGR S N  20733049  SEN S N  20733049)
  description: null
  unit: null
  file:
  - Shaws_60ft_05112024_10062024_20722049.dat
- name: Temp  °F (LGR S N  21894633  SEN S N  21894633)
  description: null
  unit: null
  file:
  - Deadman_30ft_01312024-01192025_21894633.txt
- name: Temp  °F (LGR S N  21894634  SEN S N  21894634)
  description: null
  unit: null
  file:
  - Deadman_60ft_01312024-01192025_21894634.txt
- name: 'Temp, ?F (LGR S/N: 21502242, SEN S/N: 21502242, LBL: AoP deep)'
  description: null
  unit: null
  file:
  - Shaws_60ft_10062024-04262025_21502242.txt
- name: 'Temp, °C (LGR S/N: 20539513, SEN S/N: 20539513)'
  description: null
  unit: null
  file:
  - Jon_D._Avalon_55ft_06252020-12252022_20539513.csv
- name: 'Temp, °F (LGR S/N: 20894275, SEN S/N: 20894275)'
  description: null
  unit: null
  file:
  - Malaga_Cover_30ft_06022021-12152022_20894275.csv
- name: 'Temp, °F (LGR S/N: 21292583, SEN S/N: 21292583)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01222022-01032023_21292583.csv
- name: 'Temp, °F (LGR S/N: 21292584, SEN S/N: 21292584)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01220222-01032023_21292584.csv
- name: 'Temp, °F (LGR S/N: 21292585, SEN S/N: 21292585)'
  description: null
  unit: null
  file:
  - Shaws_30ft_09252022-05112024_21292585.csv
- name: 'Temp, °F (LGR S/N: 21502239, SEN S/N: 21502239, LBL: Deadman)'
  description: null
  unit: null
  file:
  - Deadman_30ft_01032023-01312024_21502239.csv
- name: 'Temp, °F (LGR S/N: 21502242, SEN S/N: 21502242, LBL: Deadman 2)'
  description: null
  unit: null
  file:
  - Deadman_60ft_01032023-01312024_21502242.csv
- name: Temperature   °C
  description: null
  unit: null
  file:
  - WhitePoint_60ft_03072026-09162026_20894280.txt
- name: temp   °C
  description: null
  unit: null
  file:
  - WhitePoint_30ft_03212026-09162026_22169469.txt
coverage: >-
  The array as the portal states it: "temperature data collected as part of our David Tsao Continental
  Thermograph Array (CTA) project", recorded with "Onset Computer's U22-0001 thermographs" as the collection
  page states. The collection page links fourteen site pages, which between them carry 121 data-set
  links naming 120 distinct files; this record holds 116 of those 120, 74,539,512 bytes as served. One
  drive id is linked twice, under "WHITE POINT VENT 30' 10/11/2014-08/29/2015" and "WHITE POINT VENT
  30' 10/06/2013-04/18/2014" on data-portal-white-point.html, which is why the links outnumber the files
  by one. The four of the 120 this record does not hold are the four the fifth access step names, none
  of which returned any bytes of a file. All fourteen site pages print a heading; twelve state a MANAGER
  line, ten a SPONSOR line and ten a LOCATION line, and data-portal-leo-carrillo.html and data-portal-crystal-cove.html
  state none of the three. This record enters them as printed: data-portal-deer-creek.html headed "DEER
  CREEK, VENTURA COUNTY", stating "SPONSOR: ANTELOPE VALLEY DESERT DIVERS" and "MANAGER: ANTELOPE VALLEY
  DESERT DIVERS" and "LOCATION: 34 03.592 N 118 59.316W", 6 files held; data-portal-leo-carrillo.html
  headed "LEO CARRILLO, MALIBU", stating no sponsor, manager or location, 1 file held; data-portal-corral-beach.html
  headed "CORRAL BEACH, MALIBU", stating "MANAGER: CRAIG GELPI", 1 file held; data-portal-pt-dune.html
  headed "POINT DUME, LOS ANGELES", stating "SPONSOR: CMS" and "MANAGER: CALIFORNIA SCIENCE CENTER"
  and "LOCATION: 34 00.02 N 118 48.62 W", 1 file held; data-portal-malaga-cove.html headed "MALAGA COVE,
  PALOS VERDES", stating "SPONSOR: CMS" and "MANAGER: CALIFORNIA SCIENCE CENTER" and "LOCATION: BEACH
  IS NW", 2 files held; data-portal-marine-land-platform.html headed "MARINE LAND PLATFORM, PALOS VERDES",
  stating "SPONSOR: CMS" and "MANAGER: AQUARIUM OF THE PACIFIC" and "LOCATION: 33 44.1879N, 118 23.4614W",
  6 files held; data-portal-white-point.html headed "WHITE POINT SITES, PALOS VERDES", stating "SPONSOR:
  CMS" and "MANAGER: AQUARIUM OF THE PACIFIC" and "LOCATION: WHITE POINT 9/16/2026" and "LOCATION: WHITE
  PT. ROCK, 33.42'468 N 118.90'038 W" and "LOCATION: WHITE PT VENT, 33.42'8473 N 118.19'1471 W", 18
  files held; data-portal-avalon-wreck.html headed "AVALON WRECK, PALOS VERDES", stating "SPONSOR: CMS"
  and "MANAGER: JON DAVIES" and "LOCATION: 33 47.317 N 118 25.680", 13 files held; data-portal-crystal-cove.html
  headed "CRYSTAL COVE, ORANGE COUNTY", stating no sponsor, manager or location, 1 file held; data-portal-montage.html
  headed "MONTAGE - NEW SITE", stating "MANAGER: AQUARIUM OF THE PACIFIC", 3 files held; data-portal-shaws.html
  headed "SHAW'S COVE, LAGUNA BEACH", stating "SPONSOR: CMS" and "MANAGER: AQUARIUM OF THE PACIFIC"
  and "LOCATION: 30 FSW TEMPERATURE SENSOR 33 32.6265N, 117 42.9607W" and "LOCATION: 60 FSW TEMPERATURE
  SENSOR 33 32.5679N, 117 48.0330W", 16 files held; data-portal-cress-st.html headed "CRESS ST, LAGUNA
  BEACH", stating "SPONSOR: CMS" and "MANAGER: AQUARIUM OF THE PACIFIC" and "LOCATION: 33.530716 N 117.779946
  W", 13 files held; data-portal-deadman-reef.html headed "DEADMAN REEF, LAGUNA BEACH", stating "SPONSOR:
  CMS" and "MANAGER: TED SHARSHAN" and "LOCATION: BEACH IS 33.5465 N 117.8018 W", 33 files held; data-portal-avalon-park.html
  headed "AVALON PARK, SANTA CATALINA ISLAND", stating "SPONSOR: CMS" and "MANAGER: FLEMING FAMILY"
  and "LOCATION: SOUTHEAST SIDE OF CASINO PARK", 2 files held. data-portal-montage.html states no location
  and no sponsor, so nothing the source prints places that site. Most link labels state a depth in feet
  and a deployment window, but not all of the 121: "DEER CREEK 09/26/2015-11/19/2016", "DEER CREEK 11/19/2016-05/13/2017",
  "WHITE POINT ROCK 10/22/2011-11/18/2017" state no depth, and "CONCATENATED 60' 06/2012-11/2017", "CONCATENATED
  30' 06/2012-11/2017", "MARINE LAND PLATFORM 64' 11/12/2016" state no window resolved to a day. Over
  the 118 labels that do state a day-resolved window, the earliest start is "CORRAL BEACH, MALIBU 24'
  DATA 10/21/2005-04/20/2006" and the latest end is "CRESS ST 57' 12/06/2025-09/23/2026", each of them
  the only label at its extreme. The latest start among those 118 is "WHITE POINT 30' 3/21/2026-9/16/2026",
  whose own end date falls before that latest end. This record states no span read off the files' own
  rows
coverage_stated_at: >-
  https://www.catalinamarinesociety.org/data-portal.html states the CTA sentence quoted first; https://www.catalinamarinesociety.org/data-portal-tsao-continental-thermograph-array-sites.html
  states the thermograph sentence and links the fourteen site pages; each site page named above states
  that site's heading, its links' labels and, where it prints them, its sponsor, manager and location
  lines, and, on seven of them, the concatenated column list; and the byte counts are those of the copies
  retrieved 2026-09-25, each recorded in the fetch manifest beside its file in data/raw/cms_thermograph_array/
  (all fourteen site pages and both portal pages retrieved 2026-09-25)
retrieved: '2026-09-25'
fetch_script: src/fetch/cms_thermograph_array.py
file: null
transcribed_from: null
derived_from: null
topics:
- ocean-climate/temperature
regions:
- scb
- scb.mainland.ventura
- scb.mainland.los-angeles
- scb.mainland.orange
- scb.islands.santa-catalina
beds: []
sites: []
site_key:
- file: Deer_Creek_30ft_concatenated.dat
- file: Antelope_Valley_Desert_Divers_2_9852409.csv
- file: Deer_Creek_test.csv
- file: AntelopeValleyDD_11192016_05132017_9852409.csv
- file: Deer_Creek_05132017_02102018_10862354_AVDD_White.csv
- file: AVDD_02102018_06082019_10281202.csv
- file: 9987952-Malibu_deployment_0.csv
- file: Corral899247.xls
- file: PtDume_30ft_09092017_11222017_formatted.dat
- file: Malaga_Cove_05262019_07272019_20481388.csv
- file: Malaga_Cover_30ft_06022021-12152022_20894275.csv
- file: OldMarineLand_12232018_11162019_10629315.csv
- file: OML_06022018_12232018_10862354_AoP_Desda.csv
- file: MarinelandPlat_11182017_06022018_10178072.txt
- file: AoP_06172017_11182017_10779230_AoP_Desda.csv
- file: MarineLandPlatform_111216_061717_10120264_56ft.csv
- file: Marineland_test.csv
- file: WhitePoint_60ft_03072026-09162026_20894280.txt
- file: WhitePoint_30ft_03212026-09162026_22169469.txt
- file: WhitePtRock_12232018_11162019_10281199.csv
- file: WhitePtRock_06022018_03232019_10120264_AoP_Desda.csv
- file: White_Pt_Rock_11172017_06022018_10862356.txt
- file: Question_06172017_11182017_10779230_AoP_Desda.csv
- file: WhitePtRock_111216_0617171077929_66ft.csv
- file: white_pt_rock_test.csv
- file: Data_Collect_1_9852409.csv
- file: WhitePointRock9852411-2011.xls
- file: 9987954_AoP_WhtPt_10112014_08292015.csv
- file: Wht_Pt_Vent_26ft_03302018_10122019_20235929.csv
- file: Wht_Pt_Vent_27ft_09092017_03302018_20155868.prn
- file: Wht_Pt_Vent_03112017_09092017_10779231_Desda.csv
- file: AoP_3_White_Point_27ft_09012016_10779229.csv
- file: 10120264_for_AOP_02152015.csv
- file: White_Point_Vent_30ft_10120264_04182014_10112014.csv
- file: WhtPtVent_10092013_02172018_concatenated.dat
- file: Jon_D._Avalon_55ft_06252020-12252022_20539513.csv
- file: Jon_Davies_06122019_06252020_20539517.csv
- file: Jon_Davies_70ft_12082018_06122019_20235931.csv
- file: AvalonWreck_70ft_03062018_11152018_20235931.csv
- file: AvalonWreck_55ft_03062018_11152018_10281204.csv
- file: AvalonWreck_55ft_07062017_03062018_9852409.csv
- file: Jon_Davies_Deep_10178072_012016_072017.csv
- file: Jon_Davies_Shallow_10076909_012016_072017.csv
- file: SSAvalon_Jon_Davies_10248271_MARCH2014_DEEP.csv
- file: Jon_Davies_10281204_SSavalon_march2014_shallow.csv
- file: CTA_Jon_Davies_10248272_2014.csv
- file: CTA_Jon_Davies_10248269_2014.csv
- file: CTA_Jon_Davies10248271 (1).csv
- file: N._Caruso_deployment_second_thermograph_edited.csv
- file: Montage_19ft_08022018_02292020_20155870.csv
- file: Montage_37ft_12172017_09022018_10779230.csv
- file: Montage_19ft_12172017_08312018_10281199.csv
- file: Shaws_60ft_10062024-04262025_21502242.txt
- file: Shaws_30ft_05112024-10062024_21292584.dat
- file: Shaws_60ft_05112024_10062024_20722049.dat
- file: Shaws_30ft_09252022-05112024_21292585.csv
- file: Shaws_60ft_04192019_12212019_20539516.csv
- file: Shaws_30ft_04192019_12212019_10862354.csv
- file: ShawsCove_60ft_03252018_04192019_20235928.csv
- file: ShawsCove_30ft_03252018_04192019_10779228.csv
- file: ShawsCove_60ft_09092017_03302018_10120264.csv
- file: ShawsCove_30ft_02042017_03302018_10629315.csv
- file: Shaws_60ft_02122016_09232017_10281199.csv
- file: Shaws_30ft_03112017_09232017_10862357.csv
- file: 10779228_AoP_A.S.02152016_deep.csv
- file: 10248272_AoP_A._S.02152016_shallow.csv
- file: ShawsCove_60ft_09272015_03252018_concatenated.dat
- file: ShawsCove_30ft_09272015_03252018_concatenated.dat
- file: Cress_ST_60ft_12062025-09232026_22346693.txt
- file: AoP_Cress_Street_06042016_08282017_10779228_.csv
- file: AoP_CressST_10281202_deep_08092015_06062016.csv
- file: 10248269_AoP_Cress_St_10172014_08092015_Page1.csv
- file: 10248272_AoP_CressSt_10172014_08092015de_Page1.csv
- file: AoP_CressST_10281200_shallow_05022014_10172014.csv
- file: Cress_St_60ft_May2014_10281198.csv
- file: Cress_St_30ft_May2014_10281199.csv
- file: CTA_Cress_ST_60ft_10178072.xlsx
- file: Data_Collect_2_9852409_1.csv
- file: 9898972_CTA_D.TSAO_1.csv
- file: Cress_60ft_11032012_08272017_concatenated.dat
- file: Cress_30ft_11032012_08092015_concatenated_1_.dat
- file: Deadmans_30ft_01192025-10202025_22169465.txt
- file: Deadmans_60ft_01192025-10252025_22169462.txt
- file: Deadman_30ft_01312024-01192025_21894633.txt
- file: Deadman_60ft_01312024-01192025_21894634.txt
- file: Deadman_60ft_01032023-01312024_21502242.csv
- file: Deadman_30ft_01032023-01312024_21502239.csv
- file: Deadman_30ft_01222022-01032023_21292583.csv
- file: deadman_30f_10312020-01222022_20668565 (1).txt
- file: Deadman_60ft_01220222-01032023_21292584.csv
- file: Deadman_60f_10312020-01222022_20668566 (1).txt
- file: Deadman_30ft_11252019_11012020_20481388.csv
- file: Deadman_60ft_11252019_11012020.csv
- file: Deadman_30ft_11192018_11252019_20481386.csv
- file: Deadman_60ft_11192018_11252019_20481387.csv
- file: Deadman_60ft_12012017_11292018_20155869t.csv
- file: Deadman_30ft_12012017_11292018_10862357.csv
- file: Sharshan-2_deep_12202016_11252017_10281204.csv
- file: Sharshan_shallow_121202016_11252017_10281202.csv
- file: Deadman_deep_09282015_12222016_10779230.dat
- file: Deadman_shallow_09282015_12222016_10248269.dat
- file: Ted_Sharshan_deep_11132014_09282015_10178072.csv
- file: deadmans_60ft_04082014_11132014_10281201.csv
- file: Deadmans_30ft_04082014_11132014_9898972.csv
- file: Deadman_30ft_04102014.csv
- file: Ted_Sharshan_Laguna_deep_04.csv
- file: Ted_Sharhan_Laguna_shallow_04.csv
- file: Ted_Sharshan_Laguna_deep_03.csv
- file: Ted_Sharshan_Laguna_deep_02.csv
- file: Ted_Sharhan_Laguna_shallow_02.csv
- file: format10073222.txt
- file: format9898972.txt
- file: deadman_60ft_concatenated.dat
- file: deadman_30ft_concatenated.dat
- file: Casino_Pt_Shallow30ft_11102019_12122019_10779228.csv
- file: Avalon_Park_30ft_09022019_11112019_10281202 (1).csv
references: []
human_task: null
---
