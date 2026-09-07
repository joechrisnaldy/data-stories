"""Pre-registered activity groupings and pairing rule for Post 24.

Committed BEFORE the first-line-supervisor comparison is run, per
docs/2026-09-07-second-job-design.md section 3.2 and 3.3.

Section 3.2 of that document records, against myself, that these groupings were written down
before any comparison was run but AFTER I had seen the same groupings applied to job zone, which
is a different question. Theory-driven and mechanically checkable, but not blind.

O*NET rates IMPORTANCE, not hours. Nothing here measures time spent.
"""

# Generalised work activities, O*NET content model element IDs.
PEOPLE_MANAGEMENT = {
    "4.A.4.b.1": "Coordinating the Work and Activities of Others",
    "4.A.4.b.2": "Developing and Building Teams",
    "4.A.4.b.4": "Guiding, Directing, and Motivating Subordinates",
    "4.A.4.b.5": "Coaching and Developing Others",
}

# Excluded on purpose, with the reason, so the exclusion cannot quietly return:
#   4.A.4.b.3 Training and Teaching Others      -> teachers score high without managing anyone
#   4.A.4.b.6 Providing Consultation and Advice -> advisory work with no subordinates
EXCLUDED_FROM_PEOPLE = {
    "4.A.4.b.3": "teachers and instructors score high without supervising anyone",
    "4.A.4.b.6": "consultants, doctors and lawyers advise without having subordinates",
}

HANDS_ON = {
    "4.A.3.a.1": "Performing General Physical Activities",
    "4.A.3.a.2": "Handling and Moving Objects",
    "4.A.3.a.3": "Controlling Machines and Processes",
    "4.A.3.b.1": "Working with Computers",
    "4.A.3.b.2": "Drafting, Laying Out, and Specifying Technical Devices, Parts, and Equipment",
    "4.A.3.b.4": "Repairing and Maintaining Mechanical Equipment",
}

# The pairing rule. No pair is chosen by hand: every O*NET occupation whose title begins with this
# prefix is a first-line supervisor, and its comparison group is every non-supervisory occupation
# sharing its SOC major group (the first two digits of the code).
SUPERVISOR_TITLE_PREFIX = "First-Line Supervisors"


def soc_major_group(onet_code):
    """'47-1011.00' -> '47'. The SOC major group both supervisor and workers share."""
    return onet_code.split("-")[0]


def is_supervisor(title):
    return title.startswith(SUPERVISOR_TITLE_PREFIX)


# Work Context elements for act 3, added 2026-09-07 AFTER act 1 was computed. Recorded as a
# post-hoc addition rather than presented as pre-registered: the design document says so too.
# Scale CX, the O*NET context scale, 1 to 5.
WORK_CONTEXT = {
    "4.C.1.b.1.g": "Coordinate or Lead Others in Accomplishing Work Activities",
    "4.C.1.d.1": "Conflict Situations",
    "4.C.3.a.2.a": "Impact of Decisions on Co-workers or Company Results",
    "4.C.3.a.4": "Freedom to Make Decisions",
    "4.C.3.a.1": "Consequence of Error",
}
