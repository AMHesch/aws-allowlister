import unittest
import json
from click.testing import CliRunner
from aws_allowlister.command.generate import generate, generate_allowlist_scp


class AllowListerClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_allowlister_with_click(self):
        result = self.runner.invoke(generate, ["--pci"])
        print(result.output)
        self.assertTrue(result.exit_code == 0)


class GenerateAllowlistScpTestCase(unittest.TestCase):
    def test_generate_with_force_include(self):
        standards = ["PCI"]
        include = ["yolo"]
        exclude = []
        results = generate_allowlist_scp(standards, include=include, exclude=exclude)
        # print(json.dumps(results, indent=4))
        not_actions = results.get("Statement").get("NotAction")
        self.assertTrue("yolo:*" in not_actions)

    def test_generate_with_force_exclude(self):
        standards = ["PCI"]
        include = []
        exclude = ["iam"]
        results = generate_allowlist_scp(standards, include=include, exclude=exclude)
        # print(json.dumps(results, indent=4))
        not_actions = results.get("Statement").get("NotAction")
        # Even though we would never remove IAM from an SCP,
        # this is a good way to demonstrate how services can be forcibly removed from the SCP
        self.assertTrue("iam:*" not in not_actions)