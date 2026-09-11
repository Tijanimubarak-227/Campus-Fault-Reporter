import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from hall_dues import calculate_hall_dues_v0

def test_T8_overpayment_should_be_rejected_by_default():
    """This is T8 as originally written against v0: overpayment must be
    rejected unless explicitly allowed. v0 has no allow_overpayment concept
    at all, so this fails -- which is exactly the defect that drove the
    OverpaymentError design in the final version."""
    remaining, status = calculate_hall_dues_v0(amount_due=100000, previous_payments=90000, new_payment=20000)
    assert status == "OVERPAID_REJECTED"   # v0 has no such status -> fails
