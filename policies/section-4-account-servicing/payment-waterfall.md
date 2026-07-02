---
description: Payment waterfall policy imported from the supplied Account Servicing document.
icon: water
---

# Payment waterfall

| Policy item | Source approval date |
| --- | --- |
| Payment Waterfall | 06/08/2026 |
| Active Balance Reduction | 06/08/2026 |
| Active Status Pre-Payment Balance Reduction | 06/08/2026 |
| Fee and Charge Recovery Balance Reduction | 06/08/2026 |
| Principal Balance Reduction (Cost Recovery Method) | 06/08/2026 |

## Procedure

{% stepper %}
{% step %}
### Confirm account status

Verify the account is eligible for standard payment handling before applying the waterfall.
{% endstep %}

{% step %}
### Apply active balance reduction

Use the active balance reduction policy before applying fee, charge, or principal handling.
{% endstep %}

{% step %}
### Recover fees and charges

Apply approved fee and charge recovery rules where applicable.
{% endstep %}

{% step %}
### Reduce principal

Apply principal balance reduction using the cost recovery method when required.
{% endstep %}
{% endstepper %}

{% hint style="warning" icon="triangle-exclamation" %}
Source notes marked with "*NOTE:" should become warning or info callouts so exceptions are visible during servicing.
{% endhint %}

