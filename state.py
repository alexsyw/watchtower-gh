import json
import boto3
from typing import Dict, Optional

class StateManager:
    def __init__(self, endpoint_url: str, access_key_id: str, secret_access_key: str, bucket: str):
        self.s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
        self.bucket = bucket

    def get_stored_releases(self, repo_name: str) -> Dict:
        """
        Gets stored releases for the repository
        """
        try:
            response = self.s3.get_object(
                Bucket=self.bucket,
                Key=f'releases/{repo_name}.json'
            )
            return json.loads(response['Body'].read().decode('utf-8'))
        except self.s3.exceptions.NoSuchKey:
            return {}

    def store_releases(self, repo_name: str, releases: Dict):
        """
        Stores releases for the repository
        """
        self.s3.put_object(
            Bucket=self.bucket,
            Key=f'releases/{repo_name}.json',
            Body=json.dumps(releases),
            ContentType='application/json'
        ) 