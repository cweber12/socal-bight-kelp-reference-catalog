"""The notebook plan: what CONTEXT.md's "Notebooks" section states as prose, as data.

A notebook holds no facts; it renders records. But laying one out needs facts that live
in no record: the question a topic asks, the folder and number its notebook carries, and
the order the region groups run in. CONTEXT.md states all three, and until now stated them
only in prose.

Seams:
    TOPIC_QUESTIONS[topic] -> str              the question, verbatim
    NOTEBOOK_PATHS[topic]  -> str              "1_physical_environment/11_ocean_climate.ipynb"
    region_sort_key(region_id) -> tuple        a total order over every value `regions` holds
    region_heading(region_id, catalog) -> str  the group heading a notebook prints

Nothing here reads CONTEXT.md: CLAUDE.md forbids a parser for any prose file, so these are
transcriptions, kept in step by hand and pinned by tests. CONTEXT.md is the authority; if
the two disagree, this file is the bug.
"""

from __future__ import annotations

from .schema import GLOBAL_REGION, Catalog

# --- the ten questions -------------------------------------------------------------
#
# CONTEXT.md, "Topics: the ten questions": the question is section 1 of the topic's
# notebook, printed verbatim. Order follows TOPICS, which is the notebook order.

TOPIC_QUESTIONS: dict[str, str] = {
    "ocean-climate": (
        "What thermal, salinity, nutrient, oxygen and pH climate are the beds exposed to, "
        "and how is it trending?"
    ),
    "canyon-dynamics": (
        "How much cool, nutrient-rich water do canyon internal tides deliver, and when?"
    ),
    "waves-storms-sediment": (
        "When do swells and storms remove kelp, and what is the sand doing at the bed margins?"
    ),
    "substrate": "Where is the rock, how complex is it, and what does that predict?",
    "canopy": "How has surface canopy extent changed since 1911, bed by bed?",
    "bed-state": "What are the kelp and its community doing on the reef, where, and since when?",
    "grazers-predators-competitors": (
        "What sets urchin and competitor pressure on the beds, and what holds it in check?"
    ),
    "recruitment-connectivity": (
        "How do spores, larvae and genes move between beds, and what does that mean for recovery?"
    ),
    "water-quality-harvest": (
        "What do discharges, runoff, power plants and kelp harvest do to the beds?"
    ),
    "restoration-mitigation": (
        "What has been tried to restore or offset kelp loss, and what did it do?"
    ),
}

# --- the eleven notebooks ----------------------------------------------------------
#
# CONTEXT.md, "Notebooks": one notebook per topic in a folder per group, plus an index.
# The paths are written out rather than derived from GROUPS so that they are the fact
# CONTEXT.md prints, and so a test can check the derivation instead of restating it.

INDEX_PATH = "00_index.ipynb"

GROUP_FOLDERS: dict[str, str] = {
    "physical-environment": "1_physical_environment",
    "kelp-and-community": "2_kelp_and_community",
    "human-uses-management": "3_human_uses_management",
}

NOTEBOOK_PATHS: dict[str, str] = {
    "ocean-climate": "1_physical_environment/11_ocean_climate.ipynb",
    "canyon-dynamics": "1_physical_environment/12_canyon_dynamics.ipynb",
    "waves-storms-sediment": "1_physical_environment/13_waves_storms_sediment.ipynb",
    "substrate": "1_physical_environment/14_substrate.ipynb",
    "canopy": "2_kelp_and_community/21_canopy.ipynb",
    "bed-state": "2_kelp_and_community/22_bed_state.ipynb",
    "grazers-predators-competitors": (
        "2_kelp_and_community/23_grazers_predators_competitors.ipynb"
    ),
    "recruitment-connectivity": "2_kelp_and_community/24_recruitment_connectivity.ipynb",
    "water-quality-harvest": "3_human_uses_management/31_water_quality_harvest.ipynb",
    "restoration-mitigation": "3_human_uses_management/32_restoration_mitigation.ipynb",
}

# --- the region order --------------------------------------------------------------
#
# CONTEXT.md, "Notebooks", "The region order": the tree traversed depth-first - a node,
# then all its descendants, before the next sibling - with siblings in the order
# CONTEXT.md lists them, siblings it does not order sorted by id, and `global` last.
#
# The sibling lists are transcribed from "The region tree" because they are a fact stated
# once there and derivable from no record: north to south for the counties, and the
# stratum split for level 2. The order must hold before the county and island records
# exist (6.3), so it is a property of the region id alone - which is why this walks the
# dotted id rather than a loaded catalog.

ROOT_REGION = "scb"
NO_REGIONAL_BOUND = "No regional bound"

SIBLING_ORDER: dict[str, tuple[str, ...]] = {
    "": (ROOT_REGION,),
    "scb": ("scb.mainland", "scb.islands"),
    "scb.mainland": (
        "scb.mainland.santa-barbara",
        "scb.mainland.ventura",
        "scb.mainland.los-angeles",
        "scb.mainland.orange",
        "scb.mainland.san-diego",
    ),
    "scb.islands": ("scb.islands.northern", "scb.islands.southern"),
}

# `global` is the absence of a regional bound, not a node of the tree, so it is not
# interleaved with nodes: it sorts after every one of them.
_IN_THE_TREE = 0
_AFTER_THE_TREE = 1


def region_sort_key(region_id: str) -> tuple[int, tuple[tuple[int, str], ...]]:
    """Where a region id falls in the notebook's region order.

    Total over every value a `regions` field can hold - every region id the tree has or
    gains, down to the islands beneath each group, and `global`. Beds and sites are levels
    of the tree but not region ids, so they have no place in it: they raise ValueError,
    as does anything else that is neither `global` nor a node under `scb`.
    """
    if region_id == GLOBAL_REGION:
        return (_AFTER_THE_TREE, ())
    parts = region_id.split(".")
    if parts[0] != ROOT_REGION or "" in parts:
        raise ValueError(
            f"{region_id!r} has no place in the region order: not {GLOBAL_REGION!r} "
            f"and not a node under {ROOT_REGION!r}"
        )
    levels: list[tuple[int, str]] = []
    for depth in range(len(parts)):
        node = ".".join(parts[: depth + 1])
        listed = SIBLING_ORDER.get(".".join(parts[:depth]), ())
        # A listed sibling sorts where it is listed; one CONTEXT.md does not order - the
        # islands within a group - sorts by id. Putting the unlisted ones after the listed
        # ones is this file's choice, not a transcription: CONTEXT.md lists every sibling
        # set except the islands, and lists that one not at all, so no sibling set today
        # holds both kinds and nothing observable turns on it. See the PR for #41.
        levels.append((listed.index(node), "") if node in listed else (len(listed), node))
    return (_IN_THE_TREE, tuple(levels))


def region_heading(region_id: str, catalog: Catalog) -> str:
    """The heading a notebook prints over a region's group of sources.

    A group's heading is its node's `name`; `global` has no record and is headed
    "No regional bound". A node whose record does not exist yet has no heading - unlike
    the order, which holds for it - and no source can tag one, since `regions` links are
    checked against the records that exist.
    """
    if region_id == GLOBAL_REGION:
        return NO_REGIONAL_BOUND
    for rec in catalog.records["regions"]:
        if rec.id == region_id:
            return str(rec.data["name"])
    raise KeyError(f"no region record for {region_id!r}; a group's heading is its node's name")
