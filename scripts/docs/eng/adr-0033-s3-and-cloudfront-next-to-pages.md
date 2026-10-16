title: ADR-0033: The site moves to S3 and CloudFront, built with Terraform, and deploys there next to GitHub Pages until the cutover
summary: Every push to main that passes the gate also syncs the same build to a private S3 bucket behind CloudFront, through a GitHub OIDC role that may write one bucket and invalidate one distribution; the infrastructure is the public Terraform repository site-infra, and GitHub Pages stays deployed as the rollback until the apex has run on CloudFront without one.
parent: decision-log
order: 33
adr: 33
status: accepted
created: 2026-10-15
labels: adr, decision, hosting, deploy, cloudfront, terraform, privacy
owner: Stefan Coetzee
reviewed: 2026-10-15
review_by: 2027-01-13
type: explanation
---
## Context

GitHub Pages serves the site and keeps no access logs, so nothing counts visits: not page views, not countries, not which crawlers read the site. It also cannot send response headers, which blocks HSTS and the other security headers (#26). On 2026-10-15 Stefan Coetzee chose S3 and CloudFront, built with Terraform, and asked that the Terraform pipeline double as a public example of infrastructure as code, with AWS credentials on the operator's home server only.

## Decision

The infrastructure is the public repository [uncovertechtalent-git/site-infra](https://github.com/uncovertechtalent-git/site-infra): a private bucket per site that only its CloudFront distribution reads (origin access control), a certificate from ACM, a response headers policy (HSTS, nosniff, frame and referrer policy, Permissions-Policy), Route 53 records, and CloudFront standard logs that never record an IP address, a cookie or a query string. CI there runs static checks and unit tests with a mocked provider and holds no cloud credentials; plans and applies run on the operator's host, the one place with AWS credentials.

This repository's workflow gets a job "Deploy to S3 and CloudFront" after the Pages deploy. It downloads the build the Pages job uploaded, so both hosts serve the same bytes, and runs the deploy script of site-infra at a reviewed commit: sync to the bucket with the content types and `Cache-Control` GitHub Pages sends, then invalidate the distribution. AWS access is a 15-minute session of a role that trusts this repository's main branch through GitHub OIDC (audience and subject matched exactly) and may only list and write the one bucket and invalidate the one distribution. GitHub stores no AWS credential. The role ARN, bucket and distribution are repository secrets, though none of them is a credential: GitHub masks only secrets in a step's log, and the account id is in the ARN. The job skips until the repository variable `S3_DEPLOY` is `on`.

The cutover runs in stages, each one Terraform variable: the test host `next.machinebehavior.io` first, then the apex and www attached to CloudFront with DNS unchanged, then the apex records switched. Each stage is checked with the parity script of site-infra against GitHub Pages: status, redirect target, content type, `Cache-Control`, canonical link and body hash of every file of the build. The steps are the [cutover runbook](https://github.com/uncovertechtalent-git/site-infra/blob/main/docs/cutover-machinebehavior.io.md).

## Consequences

Until the cutover the site deploys twice from one build, and a failure of the S3 job leaves the Pages deploy live. After the cutover GitHub Pages stays deployed as the rollback (one variable sends the apex back) until Stefan retires it; GitHub cannot renew its certificate once the apex points away, so the rollback window ends when that certificate expires. Then the pages that name GitHub Pages as the host change: [site architecture](doc:eng/site-architecture) and the rollback runbook.

www is a CNAME to the apex instead of into github.io, because github.io publishes CAA records that exclude Amazon and ACM refuses a certificate for www otherwise.

AWS becomes a processor of visitor data: CloudFront handles the IP address to deliver a page, and the access log keeps the time, path, status, referrer, User-Agent and country. The privacy notice (#11) needs that line before the apex switches. Visit statistics come from those logs: a job on the operator's host pushes them to Loki without the User-Agent string or the full referrer, and the Grafana dashboard "Site traffic" shows counts only.
