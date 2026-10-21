# Triage Labels

The skills speak in terms of five canonical triage roles. This repo uses those strings verbatim,
so the mapping is the identity.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Not yet evaluated; an agent does that    |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding
label string from this table.

## The other two labels

Two labels are not triage roles, and no skill applies them on its own judgement:

| label             | meaning                                |
| ----------------- | -------------------------------------- |
| `bug`             | Something is broken                    |
| `found-in-flight` | Found while implementing another issue |

They travel together with `needs-triage` under rule 3 of the in-flight bug policy in `CLAUDE.md`.

These seven are the whole vocabulary — GitHub's defaults were deleted. Do not invent an eighth; an
idea that wants one goes in the Parking lot.
