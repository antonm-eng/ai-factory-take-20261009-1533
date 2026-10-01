# Data dictionary: prepaid churn features

Published daily by the `churn_features_daily` Glue job to `s3://<data-bucket>/features/churn_features/dt=<date>/`
and queryable in Athena as `ai_factory.churn_features` (approved view for modelling: `cvm.recharge_30d_v2`).
All values are illustrative demo data.

| Feature | Definition | Source | Classification | Owner |
|---|---|---|---|---|
| `recharge_cnt_30d` | Number of top-ups in the trailing 30 days | `recharge_events` | Internal, no PII | Data Engineering |
| `avg_recharge_30d` | Average top-up amount (AZN) over the trailing 30 days | `recharge_events.amount_azn` | Internal, no PII | Data Engineering |
| `digital_share_30d` | Share of top-ups made through the digital channel, trailing 30 days | `recharge_events.channel` | Internal, no PII | Data Engineering |
| `channel_cnt_30d` | Number of distinct top-up channels used, trailing 30 days | `recharge_events.channel` | Internal, no PII | Data Engineering |
| `last_recharge_ts` | Timestamp of the latest top-up | `recharge_events.recharge_ts` | Internal, no PII | Data Engineering |
| `days_since_last_recharge` | Days between the run time and the latest top-up | `recharge_events.recharge_ts` | Internal, no PII | Data Engineering |
| `min_recharge_30d` / `max_recharge_30d` | Smallest / largest top-up (AZN), trailing 30 days | `recharge_events.amount_azn` | Internal, no PII | Data Engineering |

## Usage policy

- Allowed for CVM modelling (prepaid churn v2 and v3) and for CVM campaign selection.
- `msisdn_hash` is a pseudonymous key: never join it back to MSISDNs outside the approved CVM views.
- Freshness: refreshed every 30 minutes; consumers must not train or score on a snapshot older than 24 hours.

## Upstream contract

`recharge_events` follows `pipeline/contracts/recharge_events.json`. Billing owns the CDC export;
Data Engineering owns the contract and the feature SQL in `pipeline/features/`.
