# Study plan

## Eight-day plan (90–120 minutes/day)

| Day | Read | Lab |
|-----|------|-----|
| 1 | Foundations | Lab 0: prove your lab OS |
| 2 | Users, files, disks | Labs 1–2 |
| 3 | systemd and logs | Lab 3 |
| 4 | Host networking | Lab 4 |
| 5 | Bash | Lab 5 |
| 6 | Enterprise ops | Lab 6 (hardening checklist) |
| 7 | Q&A out loud | Failure drills in labs |
| 8 | Capstone | Capstone |

## Rubric

| Level | Signal |
|-------|--------|
| Tutorial | You ran commands; you cannot explain output |
| Working | You find logs, restart a unit, free disk |
| Proficient | You prove *which* layer failed (disk, perm, DNS, port, unit) |
| Advanced | You automate checks, harden SSH/sudo, design golden images |
| Teaching | Another engineer can follow your runbook on a cold host |

Do not skip quoting and `pipefail`. Most “Bash in prod” incidents are unquoted variables and ignored exit codes.
