#!/usr/bin/env python3
"""
apply_editorial.py — one-time application of drafted one-liners, summary bullets,
and a series reclassification to series.json.

Run once, review the result, then delete. Ordinary editorial edits after this
should be made directly in series.json; sync_series.py never overwrites these
fields.

    python3 apply_editorial.py series.json
"""

import json
import sys
from collections import Counter

COPY = {
 # ---------------- ClearSync Connect ----------------
 "cc-006": ("The energy and AI infrastructure market got loud. This is the filter.",
   ["Why announcement volume has decoupled from actual delivered capacity",
    "What separates a rendering from a project with a signed interconnect",
    "The questions Richard asks before treating a buildout claim as real"]),
 "cc-005": ("Everyone is announcing microgrids. Most of what's being announced isn't one.",
   ["The definitional slippage letting grid-tied projects claim microgrid status",
    "Why the distinction decides who carries reliability risk when the grid fails",
    "What data center operators and corporate energy teams should ask developers"]),
 "dc-012": ("Everyone in this buildout is selling speed. Trust is the input nobody prices.",
   ["Why faster permits and modular builds still stall on counterparty confidence",
    "How trust compounds across interconnects, offtake, and capital in sequence",
    "Where speed claims break down between announcement and energization"]),
 "dc-010": ("Locking a turbine slot solves the first problem. The fuel contract is the second.",
   ["Why firm power requires firm fuel, and firm fuel is a contract not a reserve estimate",
    "The second backlog forming behind the turbine queue everyone is watching",
    "What gas supply exposure looks like on a project already declared financed"]),
 "dc-006": ("Chips, power, capital. There's a fourth input, and it's the one that stops projects.",
   ["Why the three-input model for AI buildout is already out of date",
    "How permission — regulatory, community, political — became the binding constraint",
    "Where projects with secured capital and hardware are stalling anyway"]),

 # ---------------- Desert Capital ----------------
 "dc-022": ("A structural break in how the Middle East manages its oil wealth, mid-supply-shock.",
   ["What the Vienna decision changes about UAE production autonomy",
    "Why it lands during the most severe supply disruption on record",
    "The signal for operators and investors positioned around OPEC discipline"]),
 "dc-021": ("A $4.2bn pipeline built in peacetime became the reason UAE crude kept moving.",
   ["How the Fujairah bypass was capitalized before there was a war to justify it",
    "What it means to hold export capacity that routes around a closed strait",
    "The infrastructure lesson: strategic redundancy only reads as foresight later"]),
 "dc-020": ("Drones hit the Fujairah Oil Industry Zone. The port matters more now, not less.",
   ["What the May 4 strikes damaged, and what kept operating",
    "Why Fujairah's role expands precisely because it was targeted",
    "How storage and bypass capacity absorb shocks the strait cannot"]),
 "dc-019": ("A $150 billion capital plan, tested by drone strikes on the facilities it funds.",
   ["Which commitments held and which were quietly repriced",
    "How the UAE's capital program absorbed direct physical attack",
    "What sustained allocation under fire signals to inbound investors"]),
 "dc-018": ("ADNOC is fast-tracking a second Fujairah line to double bypass capacity by 2027.",
   ["Scope, timeline, and what doubling bypass capacity actually delivers",
    "Why the second line is being built now rather than after the conflict",
    "What it changes for buyers pricing Hormuz exposure into term contracts"]),
 "dc-017": ("The easiest move was to leave. Tracking who did, and what it cost them.",
   ["How international operators and capital behaved once the shooting started",
    "What departure cost in re-entry terms once conditions stabilized",
    "Why the stay-or-go decision separated relationship depth from transactional presence"]),
 "dc-016": ("The US-Iran arrangement is an unfinished framework, not a settled peace.",
   ["What a 60-day ceasefire extension does and does not commit either side to",
    "Which Hormuz reopening provisions remain unresolved",
    "How to read the framework without pricing in a resolution that hasn't happened"]),
 "dc-015": ("The capital flow everyone missed runs the other direction.",
   ["How much UAE capital was already deployed inside the United States",
    "Why the reverse flow reframes Abu Dhabi as allocator rather than destination",
    "What that positioning survives when regional conflict escalates"]),
 "dc-014": ("A memorandum got signed on June 15. What it actually commits anyone to is thinner.",
   ["Who signed, in what capacity, and what that says about enforceability",
    "The gap between an MOU and a binding settlement",
    "What has to happen next for the framework to hold"]),
 "dc-013": ("Capital kept moving through the war. That's the finding worth sitting with.",
   ["Which deals closed on schedule while the conflict was active",
    "What continuity under disruption reveals about Gulf market depth",
    "Why the pattern challenges assumptions about regional risk premia"]),
 "dc-011": ("Etihad Rail is quietly rewriting how goods and people move across the UAE.",
   ["How rail changes the Fujairah corridor for freight and energy logistics",
    "What compressed transit times mean for port economics and industrial siting",
    "Why the network reads as infrastructure strategy, not transport policy"]),
 "dc-009": ("Fresh US strikes, attacks on commercial shipping, a Qatari LNG tanker hit.",
   ["The sequence that reopened hostilities after the ceasefire framework",
    "What targeting LNG shipping signals about escalation thresholds",
    "Where the strait stands for operators with cargo committed"]),
 "dc-008": ("Phase One closes at a moment of genuine transition, not resolution.",
   ["Why the Islamabad MoU is on weaker footing than its announcement suggested",
    "What field reporting shows about conditions on the ground",
    "The through-line connecting eight months of infrastructure and capital coverage"]),
 "dc-007": ("Phase Two opens where Phase One ended — with escalation, not settlement.",
   ["Why the Islamabad MoU lasted a fraction of its intended term",
    "How to price a chokepoint no single party controls",
    "What the next phase of coverage will track"]),
 "dc-005": ("The UAE's newest export isn't oil. It's the operating system around it.",
   ["What Abu Dhabi is packaging and selling beyond hydrocarbons and real estate",
    "How operating models travel as exportable products",
    "Why this reframes the UAE's role in markets it doesn't produce in"]),
}

# These carry "Richard's Take" and cover the AI/power buildout — ClearSync, not
# Desert Capital. The main feed had no tags to classify them.
RECLASSIFY = {
    "dc-012": "clearsync-connect",
    "dc-010": "clearsync-connect",
    "dc-006": "clearsync-connect",
}


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "series.json"
    doc = json.load(open(path, encoding="utf-8"))

    n_copy = n_move = 0
    for a in doc["articles"]:
        if a["id"] in RECLASSIFY:
            a["series_id"] = RECLASSIFY[a["id"]]
            a["thumb_label"] = "CC"
            a["verticals"] = ["Power", "AI & Tech"]
            n_move += 1
        if a["id"] in COPY:
            one, bullets = COPY[a["id"]]
            a["one_liner"] = one
            a["summary_bullets"] = bullets
            a.pop("needs_editorial", None)
            n_copy += 1

    for s in doc["series"]:
        mine = [a["date"] for a in doc["articles"]
                if a["series_id"] == s["id"] and a.get("date")]
        if mine:
            s["updated"] = max(mine)

    json.dump(doc, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"copy written: {n_copy}   reclassified: {n_move}")
    print("by series:", dict(Counter(a["series_id"] for a in doc["articles"])))
    print("still needing editorial:",
          len([a for a in doc["articles"] if a.get("needs_editorial")]))


if __name__ == "__main__":
    main()
