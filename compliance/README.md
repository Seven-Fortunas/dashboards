# SOC 2 Compliance Dashboard

**Last Updated:** Initial setup (not yet collecting evidence)

## Overview

Real-time compliance posture for SOC 2 Trust Service Criteria.

---

## Control Posture

### Overall Compliance Score
**Status:** Not yet calculated
**Last Evidence Collection:** N/A

---

## Controls by Trust Service Criteria

### CC6.1: Logical and Physical Access Controls
- **GH-AC-001:** 2FA Required - ✅ Implemented
- **GH-AC-002:** Default Repo Permission: None - ✅ Implemented
- **GH-AC-003:** Team-Based Access - ✅ Implemented
- **GH-AC-004:** Branch Protection - ✅ Implemented

**Status:** 4/4 controls implemented

### CC7.1: System Operations - Detection and Monitoring
- **GH-MO-001:** Secret Detection - ✅ Implemented
- **GH-MO-002:** Dependabot Alerts - ✅ Implemented
- **GH-MO-003:** Code Scanning - ⏸️ Planned
- **GH-MO-004:** Audit Logging - ✅ Implemented

**Status:** 3/4 controls implemented

### CC8.1: Change Management
- **GH-CM-001:** Branch Protection - ✅ Implemented
- **GH-CM-002:** CODEOWNERS - ✅ Implemented
- **GH-CM-003:** Required Status Checks - ✅ Implemented
- **GH-CM-004:** Signed Commits - ⏸️ Planned

**Status:** 3/4 controls implemented

---

## Evidence Collection

**Frequency:** Daily at 9am UTC
**Last Run:** Not yet run
**Status:** Pending first collection

### Collected Evidence
- 2FA Status Report
- Access Control Configuration
- Secret Scanning Alerts
- Dependabot Alerts
- Branch Protection Status
- Audit Log (last 7 days)

**Storage:** `compliance/evidence/{YYYY-MM-DD}/`

---

## Open Findings

**Count:** 0
**Critical:** 0
**High:** 0
**Medium:** 0

*First audit not yet conducted*

---

## Control Drift Alerts

**Count:** 0

*Monitoring not yet active*

---

## CISO Assistant Integration

**Status:** Phase 1.5 (to be migrated)
**Repository:** To be forked from intuitem/ciso-assistant-community
**Organization:** Seven-Fortunas-Internal

---

## Next Steps

1. **Migrate CISO Assistant** - Fork and configure for Seven Fortunas
2. **Run First Evidence Collection** - Manually trigger workflow or wait for cron
3. **Import Control Mappings** - Load GitHub controls into CISO Assistant
4. **Configure Evidence Sync** - Set up automatic sync to CISO Assistant
5. **Conduct Internal Audit** - Review all controls and evidence

---

## Documentation

- [SOC 2 Control Mapping](../../docs/soc2-control-mapping.md)
- [Evidence Collection Script](../../scripts/collect_soc2_evidence.py)
- [GitHub Actions Workflow](../../.github/workflows/collect-soc2-evidence.yml)

---

*Part of the Seven Fortunas Security & Compliance program.*
