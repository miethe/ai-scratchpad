# Phase 5: Launch Preparation

**Knit-Wit MVP Implementation Plan**

**Phase Duration:** 1 week (Week 16)
**Sprint:** Sprint 11
**Capacity:** 30-40 story points
**Team:** Full team + on-call rotation
**Priority:** P0 (Launch Blocker)

---

## Phase Overview

### Purpose

Final phase validates production readiness and executes deployment. Success criteria: zero critical production issues, monitoring operational, go-live approved.

### Context

**Input:** Phase 4 complete (QA & Polish - all MVP features validated, performance targets met, accessibility compliant, documentation ready)
**Output:** Production deployment live, monitoring active, launch communications published
**Next:** Post-launch monitoring and incident response

### Goals

1. **Production Deployment:** Backend + frontend live with zero downtime
2. **Monitoring & Alerting:** Dashboards operational, alerts active, on-call rotation configured
3. **Go/No-Go Decision:** Stakeholder approval for public launch based on launch checklist
4. **Launch Communications:** Release notes, social, blog post, documentation site updated
5. **Incident Response:** On-call procedures, rollback plan tested

### Non-Goals

- v1.1 features
- Post-launch roadmap planning (handle post-launch)
- Community/social management ongoing (handled by separate team)

---

## Launch Checklist

### Pre-Launch Validation (24 hours before)

**Environment Verification:**
- [ ] Production backend server healthy (uptime, response times normal)
- [ ] Production database migrations complete and verified
- [ ] CDN cache purged, static assets deployed
- [ ] SSL certificates valid and auto-renewal configured
- [ ] DNS records pointing to production endpoints
- [ ] API rate limiting configured (100 req/s per IP)
- [ ] CORS headers whitelist includes frontend domain only

**Code Verification:**
- [ ] Main branch CI/CD pipeline passes (all checks green)
- [ ] Production build artifacts signed and verified
- [ ] Feature flags configured (disable v1.1 features if merged)
- [ ] Environment variables loaded (secrets manager checked)
- [ ] Database backups automated and tested

**Monitoring Setup:**
- [ ] Monitoring dashboards live and displaying data
- [ ] Alert rules active (error rate, latency, availability)
- [ ] Log aggregation capturing events
- [ ] Error tracking (Sentry) receiving events
- [ ] Telemetry pipeline operational

**Documentation:**
- [ ] Release notes finalized and published
- [ ] API documentation accessible at `/docs`
- [ ] User guide and FAQ accessible
- [ ] Developer onboarding guide current
- [ ] Status page created (or external status service configured)

### Deployment Steps

**T-0 (Start of deployment window)**

1. **Pre-Flight Check:**
   - [ ] Create deployment ticket with timestamp
   - [ ] Notify stakeholders (deployment starting)
   - [ ] Start incident log (Google Doc or Slack thread)
   - [ ] On-call engineers logged in and monitoring

2. **Database Layer:**
   ```bash
   # Run migrations in staging first (verify output)
   ./scripts/migrate.sh staging

   # Perform backup
   pg_dump -h prod-db production_db | gzip > backup_$(date +%s).sql.gz

   # Run migrations in production
   ./scripts/migrate.sh production
   ```
   - [ ] Migration completes without errors
   - [ ] Rollback scripts tested

3. **Backend Deployment:**
   ```bash
   # Build and tag image
   docker build -t knitwit-api:v1.0.0 .
   docker tag knitwit-api:v1.0.0 registry.example.com/knitwit-api:v1.0.0
   docker push registry.example.com/knitwit-api:v1.0.0

   # Deploy to production (blue-green)
   kubectl set image deployment/api api=registry.example.com/knitwit-api:v1.0.0 --record
   kubectl rollout status deployment/api
   ```
   - [ ] New backend pods healthy and passing health checks
   - [ ] API responds to test requests (`/health` endpoint)
   - [ ] Error rate stays < 0.1%

4. **Frontend Deployment:**
   ```bash
   # Deploy Expo build to production slot
   eas build --platform all --auto-submit

   # Or deploy web app
   pnpm --filter mobile build
   netlify deploy --prod --dir=dist
   ```
   - [ ] Build succeeds without errors
   - [ ] Frontend loads and connects to production API
   - [ ] Critical flows verified (generate → visualize → export)

5. **CDN & Cache:**
   ```bash
   # Purge CDN cache
   cloudflare-cli cache-purge --zone example.com

   # Verify new assets served
   curl -I https://knitwit.app/assets/app.js | grep "Cache-Control"
   ```
   - [ ] CDN serving new assets
   - [ ] Cache headers correct (immutable for versioned, short TTL for index)

**T+15 min (Post-deployment verification)**

- [ ] Application fully operational (test all critical flows manually)
- [ ] Monitoring dashboards show healthy metrics
- [ ] Error rate normal (< 0.5%)
- [ ] API response times normal (p95 < 500ms)
- [ ] No alert storms in monitoring system
- [ ] Analytics events flowing

### Post-Deployment Verification (First hour)

**Smoke Tests (manual execution):**

1. **Pattern Generation:**
   - [ ] Default sphere (10cm, 14/16 gauge) generates
   - [ ] Generation time logged (target: < 200ms)
   - [ ] Result includes valid DSL and estimate

2. **Visualization:**
   - [ ] Pattern renders correctly
   - [ ] Round scrubber functional
   - [ ] Stitch highlighting works
   - [ ] Frame rate smooth (60 FPS observation)

3. **Export:**
   - [ ] PDF export completes (target: < 3s)
   - [ ] SVG export completes
   - [ ] JSON export valid and parseable

4. **Settings & Accessibility:**
   - [ ] Settings persist across sessions
   - [ ] Kid Mode toggle works
   - [ ] High contrast mode applies
   - [ ] US/UK terminology switch functional
   - [ ] Screen reader announces elements (quick check)

5. **Error Handling:**
   - [ ] Invalid gauge shows error message
   - [ ] Network error displays gracefully
   - [ ] Error is logged (visible in error tracking)

**Real User Verification:**
- [ ] Invite 3-5 alpha testers to use production app
- [ ] Collect feedback (any blocking issues?)
- [ ] Monitor their sessions in analytics
- [ ] Verify no unexpected errors

### Rollback Plan

**If critical issue found post-launch:**

```bash
# Rollback frontend (revert DNS or redeploy previous build)
git revert HEAD
pnpm --filter mobile build
netlify deploy --prod --dir=dist

# OR rollback backend
kubectl rollout undo deployment/api
kubectl rollout status deployment/api

# Restore database (only if data corruption detected)
pg_restore -h prod-db production_db < backup_*.sql.gz
```

**Decision Criteria:**
- **Rollback immediately if:** App crash on load, authentication broken, database corruption
- **Rollback if not fixed within 30 min:** Core feature completely broken
- **Keep production + hotfix branch if:** Minor UI issue, edge case bug (communicated to users)

**Post-Rollback:**
1. Notify stakeholders (incident occurred)
2. Document root cause
3. Fix in development
4. Re-test before second deployment attempt

---

## Sprint 11 Plan

### Daily Breakdown

**Monday (Day 1):**
- 8 AM: Team standup + deployment readiness review
- Morning: Final smoke testing (staging environment)
- Afternoon: Stakeholder sign-off on go/no-go criteria
- 5 PM: Deployment readiness meeting (confirm all boxes checked)

**Tuesday (Day 2) - Deployment Day:**
- 9 AM: Final pre-flight checks
- 10 AM: Begin deployment window (start at low-traffic time)
- 10-11 AM: Execute deployment steps (database → backend → frontend)
- 11 AM-12 PM: Post-deployment verification
- 12-4 PM: Monitoring window (on-call team watching dashboards)
- 4 PM: Launch communications sent (tweets, blog, email)
- 5 PM: Incident review if any issues found

**Wednesday-Friday (Days 3-5):**
- Daily: 8 AM standup + monitoring check
- As needed: Address any production issues
- Collect user feedback
- Document launch metrics (users, patterns generated, errors)
- Update status page

### Stories

| ID | Title | Effort | Owner | Status |
|----|----|--------|-------|--------|
| LAUNCH-1 | Deployment runbook + testing | 5 | DevOps Lead | In Progress |
| LAUNCH-2 | Execute production deployment | 8 | DevOps Lead + Backend Lead | Planned |
| LAUNCH-3 | Post-deployment smoke tests | 5 | QA Lead | Planned |
| LAUNCH-4 | Monitoring dashboards live | 5 | Backend Lead | In Progress |
| LAUNCH-5 | Launch communications (notes, tweets, blog) | 3 | Product Lead | In Progress |
| LAUNCH-6 | On-call rotation setup (PagerDuty/Opsgenie) | 3 | DevOps Lead | In Progress |
| LAUNCH-7 | Rollback procedure testing | 3 | DevOps Engineer | Planned |
| LAUNCH-8 | Status page + incident response docs | 2 | DevOps Engineer | In Progress |

**Total:** 34 story points

---

## Go/No-Go Criteria

### Launch Readiness Checklist

**Pass all of these to proceed:**

| Criterion | Owner | Status | Notes |
|-----------|-------|--------|-------|
| Phase 4 complete + all stories closed | Dev Lead | ✓ | Zero critical bugs remaining |
| Production environment stable (24h baseline) | DevOps | ✓ | No unexplained errors/latency |
| Monitoring operational + alerts tested | Backend Lead | ✓ | Dashboards show real data |
| Smoke tests pass on production | QA Lead | ✓ | All critical flows validated |
| Performance targets met (< 200ms, 60 FPS) | Backend/Frontend Lead | ✓ | Verified on production load |
| WCAG AA compliance confirmed | Accessibility Lead | ✓ | 0 critical issues from Phase 4 audit |
| Documentation complete + published | Tech Writer | ✓ | API docs, user guide, FAQ live |
| Release notes finalized | Product Lead | ✓ | Approved by stakeholders |
| Incident response plan tested | On-Call Lead | ✓ | Rollback procedure validated |
| Stakeholder approval | Project Manager | ⏳ | PMs, Tech Leads, Product sign off |

### Stakeholder Approvals

**Required sign-offs before launch:**
- [ ] Product Lead: Feature completeness, release notes approved
- [ ] Tech Lead (Backend): Performance, monitoring, deployment readiness
- [ ] Tech Lead (Frontend): UX, accessibility, cross-device validation
- [ ] DevOps Lead: Infrastructure, deployment, rollback tested
- [ ] Project Manager: Timeline, team capacity, launch communications

**If any stakeholder votes no-go:**
1. Document reason (e.g., "Performance p95 > 500ms")
2. Determine if blocker or deferrable (e.g., "Defer to v1.1")
3. Add work to Sprint 11 extension (Tuesday + 3 days)
4. Re-run launch checklist and vote

### No-Go Scenarios

**Launch is blocked if:**
- [ ] Any critical bug (P0) still open
- [ ] Performance p95 > 500ms (failure to meet target)
- [ ] WCAG AA compliance < 80% pass rate
- [ ] Monitoring/alerting not operational
- [ ] Database or infrastructure unstable
- [ ] Documentation missing or out of date

**Example:** "Performance tests show p95 = 650ms. Production deployment blocked until optimization completes. Extend Sprint 11 by 2 days; re-test; reschedule launch for Thursday."

---

## Monitoring & Alerting

### Dashboards (Live during launch + 7 days)

**Backend Health:**
- API request rate (req/min, target: stable baseline)
- Error rate % (target: < 0.5%)
- Response time percentiles (p50, p95, p99; target: < 500ms p95)
- Active connections / concurrent users
- Database query times
- Cache hit rate

**Application Metrics:**
- Patterns generated per hour
- Visualization frames rendered
- Exports by format (PDF, SVG, JSON)
- User session duration
- Stitch generation time distribution

**Infrastructure:**
- Server CPU, memory, disk usage
- Network I/O, bandwidth
- Database connection pool usage
- CDN cache hit rate

### Alert Rules (Active 24/7)

| Alert | Threshold | Action | Escalation |
|-------|-----------|--------|------------|
| Error rate > 1% | 5 min sustained | Page on-call | 15 min if not acknowledged |
| API response time p95 > 1s | 10 min sustained | Email on-call | Page if > 5 min |
| Service unavailable (HTTP 503) | Immediate | Page on-call | Immediate escalation |
| Database connection pool > 90% | 5 min sustained | Email ops | Page if not resolved |
| Disk usage > 85% | Immediate | Email ops | Page if > 90% |
| API crash detected (exception spike) | 3 errors in 1 min | Page on-call | Immediate |

### On-Call Rotation (Post-Launch)

**Week 1 (Launch week):**
- Primary: DevOps Lead (24/7)
- Secondary: Backend Lead (business hours)
- Escalation: CTO/Tech Lead (emergency only)

**Week 2+:**
- 1 engineer per week (24/7 on-call rotation)
- Sleeping on-call after week 1

**On-Call Responsibilities:**
- Monitor dashboards during business hours
- Respond to alerts within 15 min (page-level SLA)
- Triage issues (restart service? rollback? hotfix?)
- Document all incidents in incident tracker
- Hand off to next on-call with status

---

## Launch Communications

### Release Notes (CHANGELOG.md)

**Format:**
```
# v1.0.0 - [Launch Date]

## New Features
- Parametric crochet pattern generation (sphere, cylinder, cone)
- Interactive step-by-step visualization
- Multi-format export (PDF, SVG, JSON)
- Beginner-friendly Kid Mode
- WCAG AA accessibility

## Known Limitations (MVP Scope)
- Spiral rounds only (joined rounds in v1.1)
- Single crochet stitches (HDC/DC in v1.1)
- No colorwork or stripes
- No pattern persistence (generate on-demand)

## Performance
- Pattern generation: < 200ms
- Visualization: 60 FPS
- Deployment: [Cloud provider] region [primary]

## Browser Support
- iOS 14+ (Safari)
- Android 10+ (Chrome)
- Chrome 120+, Safari 17+, Firefox 120+ (web)
```

### Social Media
- **Twitter:** "Knit-Wit MVP is live! Generate custom crochet patterns instantly. iOS, Android, web. https://knitwit.app"
- **Blog Post:** "We're thrilled to launch Knit-Wit..." (500 words, 2 screenshots)
- **Product Hunt:** Launch post with demo video (if time permits)

### Email
- **Beta testers:** "Thanks for testing! Knit-Wit is now live for everyone."
- **Stakeholders:** "Knit-Wit MVP successfully deployed. Monitoring active."

---

## Success Metrics (First 7 days)

| Metric | Target | Owner |
|--------|--------|-------|
| Uptime | > 99.5% | DevOps |
| Error rate | < 0.5% | Backend |
| Patterns generated | > 100 | Product |
| User feedback | > 80% positive | Product |
| Performance p95 | < 500ms | Backend |
| Zero critical incidents | Yes | On-Call |

---

**Phase 5 Status:** Ready to Plan
**Launch Date:** End of Sprint 11 (Week 16)
**Next Activity:** Post-launch retrospective (Week 17)
