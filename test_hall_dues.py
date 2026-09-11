import pytest
from hall_dues import calculate_hall_dues, OverpaymentError, HallDuesResult


def test_T1_normal_partial_payment():
    """Normal case: a partial payment reduces the balance correctly."""
    result = calculate_hall_dues(amount_due=150000, previous_payments=0, new_payment=50000)
    assert result == HallDuesResult(new_balance_pesewas=100000, status="PARTIAL")


def test_T2_normal_paid_in_full():
    """Normal case: paying exactly the remaining balance settles the account."""
    result = calculate_hall_dues(amount_due=150000, previous_payments=100000, new_payment=50000)
    assert result == HallDuesResult(new_balance_pesewas=0, status="PAID_IN_FULL")


def test_T3_boundary_zero_amount_due():
    """Boundary: a student with zero dues who still pays is an overpayment
    unless explicitly allowed."""
    with pytest.raises(OverpaymentError):
        calculate_hall_dues(amount_due=0, previous_payments=0, new_payment=100)


def test_T4_boundary_exact_final_pesewa():
    """Boundary: paying exactly 1 pesewa short of full must remain PARTIAL,
    not silently round to PAID_IN_FULL (this is the floating-point trap the
    integer-pesewa design avoids)."""
    result = calculate_hall_dues(amount_due=100000, previous_payments=0, new_payment=99999)
    assert result.status == "PARTIAL"
    assert result.new_balance_pesewas == 1


def test_T5_invalid_negative_amount_due():
    """Invalid input: a negative amount_due is rejected, not coerced to 0."""
    with pytest.raises(ValueError):
        calculate_hall_dues(amount_due=-500, previous_payments=0, new_payment=100)


def test_T6_invalid_non_integer_payment_rejected():
    """Invalid input: a float (e.g. GHS-style 50.5) must be rejected because
    the contract requires an integer pesewa amount, not a float that can
    introduce rounding error."""
    with pytest.raises(ValueError):
        calculate_hall_dues(amount_due=100000, previous_payments=0, new_payment=50.5)


def test_T7_repeated_operation_duplicate_submission_is_explicit():
    """Repeated-operation case: applying the 'same' payment twice (e.g. a
    resubmitted form on a slow connection) is treated by the function as two
    independent payments; duplicate *detection* is the caller's job (e.g. an
    idempotency key), but the function itself must behave predictably and
    not corrupt the balance across repeated calls."""
    first = calculate_hall_dues(amount_due=200000, previous_payments=0, new_payment=100000)
    assert first.status == "PARTIAL"
    running_previous_payments = 100000  # caller adds the accepted payment to the running total
    second = calculate_hall_dues(amount_due=200000, previous_payments=running_previous_payments, new_payment=100000)
    assert second.status == "PAID_IN_FULL"


def test_T8_overpayment_allowed_when_explicit():
    """Overpayment is never silently accepted, but the caller may opt in
    explicitly (e.g. a student rounding up to cover a late fee)."""
    result = calculate_hall_dues(amount_due=100000, previous_payments=90000,
                                  new_payment=20000, allow_overpayment=True)
    assert result.status == "OVERPAID"
    assert result.new_balance_pesewas == 0
