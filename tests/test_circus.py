import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from circus import decide

class GateTests(unittest.TestCase):
    def base(self):
        return {"pipeline": [{"stage": s, "provenance_status":"documented"} for s in ("definition","data_selection","labels","scoring","validation")], "dependencies": [], "risks": [], "independent_checks": [{"status":"passed","frozen":True,"independently_sourced":True}]}
    def test_pass_requires_complete_independent_check(self):
        self.assertEqual(decide(self.base()), "PASS")
    def test_material_feedback_fails(self):
        r=self.base(); r["dependencies"]=[{"materiality":"material","feedback":True}]
        self.assertEqual(decide(r), "FAIL")
    def test_missing_provenance_is_na_not_pass(self):
        r=self.base(); r["pipeline"][2]["provenance_status"]="missing"
        self.assertEqual(decide(r), "N/A")
    def test_pending_check_is_not_pass(self):
        r=self.base(); r["independent_checks"][0]["status"]="pending"
        self.assertEqual(decide(r), "N/A")
    def test_material_open_risk_fails(self):
        r=self.base(); r["risks"]=[{"materiality":"material","status":"unresolved"}]
        self.assertEqual(decide(r), "FAIL")

if __name__ == "__main__": unittest.main()
