import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.app import DEPENDENCIES, assess_risk  # noqa: E402
from agent.deploy_agent import DeploymentPolicy, make_plan  # noqa: E402


class PlatformTests(unittest.TestCase):
    def test_payment_dependencies_are_explicit(self):
        self.assertEqual(DEPENDENCIES["payments"], ["accounts", "fraud", "ledger"])

    def test_risk_is_deterministic(self):
        self.assertEqual(assess_risk(250, "acct-demo-002"), assess_risk(250, "acct-demo-002"))

    def test_prod_requires_approval(self):
        policy = DeploymentPolicy.load(ROOT / "agent" / "policy.json")
        with self.assertRaises(ValueError):
            make_plan("prod", "ghcr.io/demo/banking:1.2.0", False, policy)

    def test_staging_plan_has_verify_and_rollback(self):
        policy = DeploymentPolicy.load(ROOT / "agent" / "policy.json")
        plan = make_plan("staging", "ghcr.io/demo/banking:1.2.0", False, policy)
        actions = [step["action"] for step in plan["steps"]]
        self.assertLess(actions.index("dry_run"), actions.index("apply"))
        self.assertIn("health_check", actions)
        self.assertIn("rollback_on_failure", actions)


if __name__ == "__main__":
    unittest.main()
