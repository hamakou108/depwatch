from datetime import datetime


class History:
    def __init__(
            self,
            first_committed_at: datetime,
            merged_at: datetime,
            deployed_at: datetime | None,
    ):
        self.first_committed_at = first_committed_at
        self.merged_at = merged_at
        self.deployed_at = deployed_at

    @staticmethod
    def keys() -> list[str]:
        return [
            'first_committed_at',
            'merged_at',
            'deployed_at',
        ]

    def values(self) -> list[datetime]:
        return [
            self.first_committed_at,
            self.merged_at,
            self.deployed_at
        ]

    def __eq__(self, other: 'History'):
        return (self.first_committed_at == other.first_committed_at
                and self.merged_at == other.merged_at
                and self.deployed_at == other.deployed_at)


class RepositoryHistory:
    def __init__(
            self,
            first_committed_at: datetime,
            merged_at: datetime,
            merge_commit_sha: str
    ):
        self.first_committed_at = first_committed_at
        self.merged_at = merged_at
        self.merge_commit_sha = merge_commit_sha


class DeploymentHistory:
    def __init__(
            self,
            deployed_at: datetime,
    ):
        self.deployed_at = deployed_at
