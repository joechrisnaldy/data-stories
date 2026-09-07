# Data for Post 24

Nothing in this folder is committed. Everything below is public and free.

| File | Source | How |
|---|---|---|
| `onet_work_activities.csv` | O*NET 31.0, 41 generalised work activities by occupation, Importance and Level scales | `onetcenter.org/dl_files/database/db_31_0_csv/work_activities.csv` |
| `onet_work_context.csv` | O*NET 31.0 work context, CX scale | same directory, `work_context.csv` |
| `onet_job_zones.csv` | O*NET 31.0 job zone per occupation | same directory, `job_zones.csv` |
| `onet_occupation_data.csv` | Occupation titles | same directory, `occupation_data.csv` |
| `onet_content_model_reference.csv` | Element IDs to names | same directory, `content_model_reference.csv` |
| `nber-w20102.pdf` | Bloom, Lemos, Sadun, Scur and Van Reenen (2014), for the self-assessment finding | `nber.org/system/files/working_papers/w20102/w20102.pdf` |

O*NET is released under Creative Commons Attribution 4.0 and needs no registration.

## Traps hit while building this

1. **The World Management Survey is behind a login.** The public-data page returns a WordPress
   login form, not data. That is why the 0.03 self-assessment correlation is cited from the paper
   rather than recomputed. It also cost the post its original headline, which was going to be a
   reproduction of that finding.
2. **Job zone is not hierarchy.** It is education plus training plus experience. A surgeon is the
   top zone and manages nobody, so job zone cannot answer a question about promotion. Using it that
   way was the first design and it was thrown out.
3. **"Working with Computers" sits inside the hands-on group and it climbs.** Reporting the net
   hands-on shift alone (+0.18) hides that physical work falls while computer and technical work
   rises. Always decompose a net that is the average of opposite movements.
4. **O*NET rates importance, not hours.** The original framing of this post was about time. It had
   to change, because this data cannot support a claim about how a day divides.
5. **`cep.lse.ac.uk` timed out and the AEA PDF returns 403.** The NBER copies of the same papers
   work and were used instead.
