---
description: Review workflow for keeping internal policies current across many owners and policy areas.
icon: arrows-rotate
---

# Review and approval workflow

This workflow shows how Arivo could manage policy changes in GitBook while making ownership and approval state visible to internal teams.

{% stepper %}
{% step %}
### Intake the change

Capture the requested policy change, affected teams, related source systems, and target effective date.
{% endstep %}

{% step %}
### Draft in context

Edit the affected GitBook page, keeping reader-facing guidance separate from long exception details.
{% endstep %}

{% step %}
### Route compliance review

Assign the reviewer, capture comments, and confirm whether the page needs legal, operations, or leadership sign-off.
{% endstep %}

{% step %}
### Publish and notify

Publish the approved update and notify impacted servicing teams with the page link, change summary, and effective date.
{% endstep %}

{% step %}
### Monitor feedback

Use page feedback, search terms, and repeated support questions to decide where guidance needs to be clarified.
{% endstep %}
{% endstepper %}

## Approval states

```mermaid
flowchart LR
    Draft --> InReview[In review]
    InReview --> NeedsEdits[Needs edits]
    NeedsEdits --> Draft
    InReview --> Approved
    Approved --> Published
    Published --> ScheduledReview[Scheduled review]
    ScheduledReview --> Draft
```

## Review dashboard concept

| Signal | Example | Action |
| --- | --- | --- |
| Policy stale date | Payix approved 08/30/2018 | Prioritize review. |
| High-risk topic | Customer communication | Require compliance reviewer. |
| Search gap | "door knock order" has poor results | Add aliases or restructure page. |
| Page feedback | "Need state-specific rules" | Add expandable state guidance. |

