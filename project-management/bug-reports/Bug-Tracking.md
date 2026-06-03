# Bug Tracking Log

## Bug ID: BR-01
- **Title:** Activity recommendation returns irrelevant results
- **Reported In Sprint:** Sprint 2
- **Module:** Recommendation Engine
- **Bug Type:** Functional
- **Severity:** Medium
- **Priority:** High

### Description
The system suggests activities that do not match the selected age group.

### Steps to Reproduce
1. Login as teacher
2. Select class profile (5–6 age group)
3. Request activity recommendation

### Expected Result
Activities appropriate for the selected age group should be listed.

### Actual Result
Activities for unrelated age groups are shown.

### Root Cause Analysis
Class profile age constraints were not correctly passed to the recommendation module.

### Fix / Resolution Plan
Age filtering logic will be added to the recommendation engine input.

### Status
Planned

## Bug ID: BR-04

- Title: Activity adaptation draft not saved correctly
- Reported In Sprint: Sprint 7
- Module: AI Adaptation
- Bug Type: Functional
- Severity: Medium
- Priority: Medium

### Description
AI-generated activity drafts were created successfully but were difficult to identify after saving.

### Root Cause Analysis
The adapted activity title was changed by the AI model and became difficult to locate in the activity list.

### Resolution
The system now appends a suffix to adapted activities to improve traceability.

### Status
Resolved
