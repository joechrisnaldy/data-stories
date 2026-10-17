# Post 27 design: testing the fear chain after MSCI's Standalone proposal for Indonesia

Status: **pre-registration, written before any data was downloaded** (2026-10-16); approved by the
owner on 2026-10-16. Amendments are added in place under section 8 with their date and reason; nothing above
section 8 is edited after the data comes in except to mark it AMENDED with a pointer.

## 1. Origin and stance

On 15 October 2026 MSCI opened a consultation on a proposal to reclassify Indonesia from Emerging
Market to Standalone Market status, with feedback until 30 April 2027 and a decision on or before
30 June 2027. On 16 October the IHSG fell sharply, with a trading halt at the open. (These details
come from press coverage of MSCI's release; they are verified against the release itself, stored
in `sources/`, before any of them reaches the draft.)

The fear people repeat is a chain: the downgrade makes **stocks crash and stay down**, the
**rupiah weakens**, **foreign investors leave**, and the **cost of living rises**.

- **Stance:** test each link against Indonesia's own history and say which links that history
  supports. The post is not a forecast and not financial advice.
- **Hook:** "Standalone" is read as "poor, corrupt, at war", because of the company it keeps. MSCI's
  own criteria are size and liquidity and market accessibility (economic development counts only
  for Developed status). The post quotes MSCI's definition from its classification page.
- **Personal angle:** my family and the prices they pay.
- **Reader:** Indonesians worried by the 16 October headlines. **Takeaway:** which fears history
  supports, which it does not, and what to watch before the June 2027 decision.
- **Close:** practical: what to worry about, what not to, and one or two signals to watch.
- **Title direction:** the family question, for example "What Should My Family Worry About If MSCI
  Drops Indonesia?"; final wording after the results.

## 2. Comparison set and its limit

- **Indonesia's own history only** (owner decision). No other country's reclassification is used.
- **Limit, stated in the post:** no past Indonesian shock was an MSCI reclassification. The stock
  link therefore compares this fall with past falls; it does not measure what a downgrade does. The
  January 2026 MSCI freeze is the one MSCI-driven Indonesian event; it is reported separately if its
  dates and the market's reaction are verified from a stored source.
- **1997 to 1998** is shown, as the outer bound, but excluded from every verdict count: it combined a
  banking and currency crisis with the end of the managed rupiah. Each verdict is also reported with
  it included, alongside.

## 3. Shock days, fixed in advance

- **Data:** the IHSG daily close (source chosen at the vet).
- **Shock day:** a trading day on which the IHSG closes 7% or more below the previous close. Shock
  days within 20 trading days of an earlier one belong to that earlier day's episode.
- **Fallback, decided by count alone before any outcome is computed:** if fewer than 4 episodes
  (excluding 1997 to 1998 and October 2026) meet the 7% rule, the threshold becomes 5%.
- **Day 0** is the shock day; **"before"** is the close on the trading day before day 0.
  **Horizons:** 20, 60 and 250 trading days after day 0 (about a month, three months, a year).
- **October 2026:** day 0 is 16 October 2026. Its outcomes are reported only as far as the data
  reaches (the post's as-of date); it is never counted in a verdict.

## 4. The four links: measures and verdict rules

**Verdict words**, from the share of past episodes (excluding 1997 to 1998 and October 2026) that meet
the link's condition, always with n: two thirds or more, **holds by my test**; one third or fewer,
**does not hold by my test**; otherwise, **mixed**.

- **L1. Stocks crash and stay down.** The crash itself is a fact for October 2026; the test is "stay
  down". Condition: the IHSG at day 250 is still below "before". Also reported: the lowest close
  within 250 days relative to "before", and the trading days until the IHSG closes back at or above
  "before".
- **L2. The rupiah weakens.** Condition: rupiah per US dollar at day 60 is at least 5% weaker than
  "before". Changes at days 20 and 250 are reported too. Episodes before the rupiah's float in
  August 1997 are excluded from L2.
- **L3. Foreign investors leave.** Condition: foreign investors are net sellers of Indonesian equities
  from day 0 to day 60 (daily exchange data), or, where only quarterly data exists, over the quarter
  of day 0 and the next. The size of that selling is reported as a share of the market's value where
  the data allows. An external estimate of index-driven selling under Standalone status is used only
  with a stored, citable source; otherwise it is omitted.
- **L4. The cost of living rises.** Its episodes are **rupiah slides**, not stock shock days: a month
  in which the rupiah is 10% or more weaker against the US dollar than three months earlier (month
  end to month end), after the August 1997 float. Slides within 12 months of an earlier one belong to
  its episode; fallback, decided by count alone: if fewer than 4 episodes (excluding 1997 to 1998)
  meet 10%, the threshold becomes 7%. Condition: consumer-price inflation over the 12 months after
  the slide starts exceeds the 12 months before it by 2 percentage points or more. Food prices are
  reported alongside if BPS publishes a consistent food series for the window. The post also reports
  whether the rupiah has made a slide by this rule since 16 October.

## 5. Charts (exactly four, each at most 2000 px on its long edge)

1. **IHSG lined up on shock days:** 100 = "before"; each past episode a thin line, 1997 to 1998 drawn
   apart, October 2026 bold up to the as-of date; days 0 to 250.
2. **Rupiah lined up on the same shock days:** 100 = "before", with the axis labelled so a higher
   line plainly means a weaker rupiah.
3. **Foreign equity net flows after each shock**, October 2026 so far marked as incomplete.
4. **Inflation before and after each rupiah slide** (12 months each side), food prices alongside if
   available.

## 6. What the post will not claim

- No forecast: history gives ranges, each reported "by my test" with its n.
- No causal claim that a downgrade produces any link; the episodes are falls, not downgrades.
- No investment advice; the post carries a not-financial-advice line.
- MSCI's reasons only in MSCI's own words, quoted from the stored release.
- "Steepest since 1998" or any such ranking only if the data or a cited source shows it.

## 7. Sources and rights (each checked at the vet, before use)

**Owner requirement (2026-10-16): the data must be real.** Every figure comes from a file downloaded
from its primary publisher and frozen by SHA-256, or from a stored source document with a verbatim
quote; nothing is typed from memory or from press summaries. Each series is cross-checked at the
vet against at least one independent published figure (for example, a reported IHSG close or a
BPS inflation release) before it is used.


- **MSCI:** the 15 October 2026 release and the Market Classification page, quoted and stored. MSCI
  index data is proprietary and is not used.
- **IHSG daily close:** IDX or another primary source; licence checked before download.
- **Rupiah per US dollar:** Bank Indonesia's JISDOR for recent years; an earlier daily series from a
  primary source; licence checked.
- **Foreign equity flows:** IDX statistics and Bank Indonesia's balance of payments.
- **Consumer prices:** BPS (Statistics Indonesia).
- Credits go in the post's method notes, each chart's footer and `data/README.md`; the blog is
  non-commercial.

## 8. Amendments

None yet.
