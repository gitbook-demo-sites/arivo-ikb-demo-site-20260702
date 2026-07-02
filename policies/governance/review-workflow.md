---
description: Sample review workflow for keeping policies current.
icon: arrows-rotate
---

# Review workflow

{% stepper %}
{% step %}
### Identify the change

Capture the impacted policy, owner, source system, and requested effective date.
{% endstep %}

{% step %}
### Edit the GitBook page

Update the policy page directly so the approved guidance is readable, searchable, and available to AI.
{% endstep %}

{% step %}
### Review with compliance

Route high-risk updates through compliance review and record the approval date in page metadata.
{% endstep %}

{% step %}
### Publish and announce

Publish the update and add an entry to the changelog section for affected teams.
{% endstep %}
{% endstepper %}

```mermaid
flowchart LR
    Draft --> Review
    Review --> Approved
    Review --> NeedsEdits
    NeedsEdits --> Draft
    Approved --> Published
    Published --> Changelog
```

