---
description: Standard metadata model, controls, and AI assistant prompts for an internal policy library.
icon: tags
---

# Policy metadata and controls

Metadata makes a large policy library manageable. The same policy content can support browsing, search, review dashboards, and AI answers when ownership and approval signals are consistent.

## Standard metadata

| Field | Required | Example |
| --- | --- | --- |
| Policy ID | Yes | 4:1.1.A.i |
| Policy area | Yes | Account Servicing |
| Owner | Yes | Account Servicing Department |
| Reviewer | Yes | Compliance Operations |
| Source system | Recommended | Norman LMS |
| Approval date | Yes | 03/14/2024 |
| Next review date | Recommended | 06/30/2026 |
| Risk level | Recommended | High |

{% hint style="success" icon="sparkles" %}
With consistent metadata, GitBook AI can answer policy questions with clearer citations and policy owners can see which pages need review.
{% endhint %}

## Suggested AI assistant prompts

- Which Account Servicing policies were approved most recently?
- What are the rules for customer text and email communication?
- How should I handle a charge-off non-collect status?
- Which policy pages mention Norman LMS?
- What policies are overdue for review?

## Control checklist

- Every policy page has an owner.
- Every policy page has an approval date.
- High-risk procedures include warning callouts.
- Long exceptions are hidden behind expandable blocks.
- Source documents are attached for auditability.
- Feedback is reviewed during each policy cycle.

