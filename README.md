# ai-factory

AI Factory data and model assets for **prepaid churn** (demo, synthetic data).

## churn_features (Data Engineering, owner: Nigar H.)

A 4-step feature pipeline: **extract → validate → build_features → publish**.

| What | Where |
|---|---|
| Job | AWS Glue Python shell job `churn_features_daily`, every 30 minutes (eu-central-1) |
| Input | Billing CDC export `s3://<data-bucket>/raw/recharge_events/dt=<date>/export.csv` |
| Contract | `pipeline/contracts/recharge_events.json` |
| Output | `s3://<data-bucket>/features/churn_features/dt=<date>/` · Athena `ai_factory.churn_features` |
| Run manifests | `s3://<data-bucket>/features/_runs/dt=<date>/<run_id>.json` (used as training snapshots) |
| Logs | CloudWatch Logs `/aws-glue/python-jobs/output` (JSON lines) and `/aws-glue/python-jobs/error` |
| Metrics | CloudWatch `AIFactory/ChurnFeatures`: `RunSuccess`, `RowsWritten`, `StepFailed`, `StepDurationSeconds` |
| Alarm | `churn_features_daily-run-failed` |
| Release | Every merge to `main` is packaged and published to `s3://<data-bucket>/code/pipeline.zip`; the next run uses it |

When a run fails, `churn_features` is not refreshed: training and scoring keep using the previous snapshot.

Run locally: `LOCAL_DATA_ROOT=./data python3 -m pipeline.run` (expects a raw export under `./data/raw/...`).
Tests: `python3 -m unittest discover -s tests -v`.

## prepaid churn models (Data Science: Elvin R. · MLOps · AI Steward)

- Registry: SageMaker Model Registry group `prepaid-churn` (v2 approved, newer versions as candidates).
- Release rules: `models/prepaid_churn/acceptance_criteria.md`.
- Model Card template: `models/prepaid_churn/model_card_template.md`.
- Feature definitions and usage policy: `docs/data_dictionary.md`.
