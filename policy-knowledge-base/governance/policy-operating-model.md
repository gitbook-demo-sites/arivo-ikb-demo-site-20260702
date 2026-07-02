---
description: A lightweight operating model for managing many internal policies in GitBook.
icon: sitemap
---

# Policy operating model

Arivo can use GitBook as the front door for internal policy knowledge: one searchable policy library, clear ownership, and review signals that help teams trust what they are reading.

{% hint style="success" icon="shield-check" %}
The goal is not to flatten every policy into one long document. The goal is to make each policy findable, owned, reviewed, and easy to update.
{% endhint %}

## Recommended policy object

| Field | Example | Why it matters |
| --- | --- | --- |
| Policy area | Account Servicing | Groups related policies for navigation and permissions. |
| Owner | <code class="expression">space.vars.policy_owner</code> | Shows who can answer questions and approve changes. |
| Source system | <code class="expression">space.vars.source_system</code> | Connects guidance to the operating system teams use daily. |
| Review cycle | <code class="expression">space.vars.review_cycle</code> | Keeps policy freshness visible. |
| Approval date | 06/08/2026 | Helps teams verify whether guidance is current. |

## Library structure

{% tabs %}
{% tab title="Readers" %}
Readers start from a policy area, then choose the task or status they need. Pages should begin with the plain-language answer and move deeper into controls.
{% endtab %}

{% tab title="Policy owners" %}
Owners keep metadata current, add change notes, and route approvals before publishing updates.
{% endtab %}

{% tab title="Compliance" %}
Compliance reviews policy language, approves effective dates, and monitors gaps from feedback and search activity.
{% endtab %}
{% endtabs %}

## What scales well

- One page per meaningful policy or procedure.
- Shared metadata and review banners across policy pages.
- Clear ownership at the top of every page.
- Expandable details for exceptions and edge cases.
- Workflow pages for processes that cross teams.

