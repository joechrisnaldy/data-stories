# Provenance audit, Post 31

Every variable the post leans on, with its defining text quoted from the stored copy (`sources/<folder>/<folder>.txt`).

## Microsoft's service health record (`penn-ms-incidents`)

- **The stated impact window.** EX1550543, final status (2026-11-14T04:15:46Z): "Start time: Thursday, November 12, 2026, at 4:20 PM UTC" and "End time: Friday, November 13, 2026, at 4:10 PM UTC". The record's header shows a start of 10:05 UTC, which Microsoft's text never explains; the post uses the final status.
- **The first post.** EX1550543's first update is timed 16:20:07 UTC on 12 November (the Time row of the record); the timeline counts hours from it.
- **The cause.** Final status: "The incident was introduced by an issue during an earlier network capacity upgrade that surfaced following a recent network change." Called preliminary in the post: Microsoft's full post-incident report sits behind an admin login.
- **Not an attack.** Final status: "This was a technical issue not related to cyber or AI / agents."
- **Listed as impacted.** MO1550821, final status (2026-11-14T04:17:52Z): "Features of the Microsoft 365 services below that interact with Exchange Online and email services were impacted." So a listed service had features affected through its dependency on Exchange Online; it was not necessarily down. The services are the "- Name: impact" lines of each update, or the list after "Potentially impacted services include:", read by `build_analysis.py`.
- **The 48-hour timeout.** The EX1550543 update that first mentions it (2026-11-13T09:55:42Z), as the timeline label.
- **The preliminary account, in plain words.** EX1550543 final status, "Preliminary root cause": "traffic shifts during standard network maintenance and upgrades exposed a latent bug causing a rapidly increasing number of requests to queue for processing. As this accumulated, the affected servers exhausted their available processing capacity and could no longer accept new connections". On the slow recovery, same status: "Given the scale of demand, we restored services gradually, validating stability at each stage. While this took longer, it helped ensure a stable restoration."
- **The first list.** MO1550821's first update (2026-11-12T18:27:35Z): "Potentially impacted services include: - Exchange Online - Microsoft Teams - SharePoint Online - Microsoft Copilot 365 - Microsoft Defender XDR". The post names the four besides Exchange Online.
- **The workday items.** MO1550821 final status: Teams, "Calendar related failures with scheduling, invites, viewing, and meeting edits"; SharePoint Online, "issues when sharing SharePoint Online files with people outside their organization"; Planner, "Plan and Task operation reliability issues"; Universal Print, "errors submitting print jobs"; Power Apps, "Users may be intermittently unable to sign-in to the Power Apps or Field Service mobile apps."
- **Sign-in through Exchange.** CR1551339's first update (2026-11-13T06:05:57Z): "an internal upstream service dependency, Exchange, which supports the sign-in functionality, is experiencing a service outage. This service outage has caused sign-in requests to intermittently fail at the authorization step." Scoped in the post to the Field Service mobile app, as Microsoft scoped it.
- **What stayed open.** MO1550821 final status: "Elements of those services that do not depend on interaction with Exchange Online remained functional."; Teams, "Most of the core functionality including joining calls, meetings, group chats, and channel messages are not impacted."; SharePoint Online, "Accessing files stored directly in SharePoint Online remains functional."

## News facts without a figure

The fallbacks are paraphrased from the stored Reuters article (`reuters-faxes-phones`, byline Iain Withers, Liang-sa Loh and Inti Landauro): telephones, faxes and Bluetooth; Euronext's phone advice and caller checks; Aviva's phone numbers, Bluetooth and recent outage test; the Taiwan fax confirmations (attributed there to a person familiar with the situation); Maersk's advice; HSBC's reminder (attributed there to a person within the banks). Western Australia's notice (`wa-planning-notice`): "We are currently experiencing issues due to the global Microsoft outage, including portals, telephone and email."

## DataReportal, GWI survey data

- **Email, GWI's surveyed markets** (`datareportal-2027-global-overview`): "More than three quarters of online adults say that they've used email within the past 30 days, with 76.4 percent of respondents to GWI's survey answering in the affirmative in the company's Q2 2026 wave of research."
- **WhatsApp, GWI's surveyed markets** (same report): the platform ranking is of "internet users aged 16 and above saying they used the platform within the past 30 days"; "WhatsApp claims fourth place, with 54.9 percent". The survey wave is not named for this figure.
- **WhatsApp, Indonesia** (`datareportal-2027-indonesia`): chart heading "SELF-DECLARED SOCIAL MEDIA PLATFORM USE PERCENTAGE OF INTERNET USERS AGED 16+ WHO SAY THAT THEY USED THE RESPECTIVE PLATFORM AT LEAST ONCE WITHIN THE PAST MONTH INDONESIA", value "92.7% WHATSAPP" (dated OCT 2026 on the chart).
- All three are self-reported shares of internet users aged 16 and over who used the service in the past month. They are not counts of people, and no figure from another survey is set beside them.

## News figures (bound through `docs/sources.json`)

Downdetector's report counts (Reuters 2026; Habib 2026) count reports from people who visit Downdetector, not affected users; Al Jazeera says as much. The cost estimates (Stelter et al. 2026 for Anderson Economic Group; Souter 2026 for Morningstar DBRS and CyberCube) measure different things (lost productivity, insured losses), and none of the stored articles gives a method.
