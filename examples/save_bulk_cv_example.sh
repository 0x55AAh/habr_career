#!/usr/bin/env bash

career resumes list \
--sort salary_asc \
--with-salary \
--qualification 6 \
--skills 446 \
--salary 500000 \
--currency rur \
--locations c_707 \
--per-page 5 \
--relocation \
--work-state search \
--json \
| jq ".resumes.objects.[] | .id" \
| xargs -L1 -I {} \
career users cv -u {} -o "{}_cv.pdf"
