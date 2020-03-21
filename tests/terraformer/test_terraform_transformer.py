import json
import os
import unittest

from airiam.main import configure_logger
from airiam.models.RuntimeReport import RuntimeReport
from airiam.terraformer.TerraformTransformer import TerraformTransformer


class TestTerraformTransformer(unittest.TestCase):

    def test_terraformer_works(self):
        self.setup()
        self.terraform_transformer.transform(self.report, should_import=False)
        self.assertTrue(os.path.exists('main.tf'), 'Did not create a main file')
        self.assertTrue(os.path.exists('users.tf'), 'Did not create a users file')
        self.assertTrue(os.path.exists('policies.tf'), 'Did not create a policies file')

    def setup(self):
        self.unused_users = []
        self.unused_roles = []
        self.unattached_policies = []
        self.redundant_group = []
        self.user_clusters = {
            "Admins": ["wifi"],
            "Powerusers": {
                "Users": ["GanDalf"],
                "Policies": [
                    "arn:aws:iam::aws:policy/AmazonAthenaFullAccess",
                    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
                    "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
                    "arn:aws:iam::aws:policy/AmazonESFullAccess"
                ]
            },
            "ReadOnly": ["kangaroo", "talm"]
        }
        self.special_users = []
        self.roles_rightsizing = []
        self.terraform_transformer = TerraformTransformer(configure_logger())
        current_dir = os.path.abspath(os.path.dirname(__file__))
        with open("{}/{}".format(current_dir, "../iam_data.json")) as f:
            iam_data = json.load(f)
        self.report = RuntimeReport("012345678901", iam_data, self.unused_users, self.unused_roles, self.unattached_policies, self.redundant_group,
                                    self.user_clusters, self.roles_rightsizing)