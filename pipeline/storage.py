"""Where the pipeline reads and writes: S3 when running in AWS Glue, a local folder in CI and on laptops."""

import os
from pathlib import Path

BUCKET = os.environ.get("DATA_BUCKET")
LOCAL_ROOT = Path(os.environ.get("LOCAL_DATA_ROOT", "data"))


def _s3():
    import boto3

    return boto3.client("s3")


def read_text(key: str) -> str:
    if BUCKET:
        return _s3().get_object(Bucket=BUCKET, Key=key)["Body"].read().decode()
    return (LOCAL_ROOT / key).read_text()


def write_text(key: str, body: str) -> None:
    if BUCKET:
        _s3().put_object(Bucket=BUCKET, Key=key, Body=body.encode())
        return
    path = LOCAL_ROOT / key
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
