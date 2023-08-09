from enum import Enum


class ApplyMode(Enum):
    dry_run = "dry_run"
    apply = "apply"
    pull_request = "pull_request"
