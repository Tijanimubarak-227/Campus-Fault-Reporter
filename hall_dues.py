"""
hall_dues.py
Hall Dues Calculator - Practical 4 (Reliable Implementation and Testing)

Contract
--------
Inputs (all amounts are INTEGERS in pesewas, GHS 1.00 = 100 pesewas,
to avoid floating-point currency errors):
    amount_due:        int  >= 0   total hall dues owed for the semester
    previous_payments: int  >= 0   sum of payments already recorded
    new_payment:       int         payment being applied now (must be > 0)
    allow_overpayment: bool        explicit opt-in to allow paying more than
                                    the outstanding balance (default False)

Output: HallDuesResult(new_balance_pesewas, status)
    status is one of: "PAID_IN_FULL", "PARTIAL", "OVERPAID"

Preconditions
    - amount_due, previous_payments, new_payment are all integers
    - amount_due >= 0
    - previous_payments >= 0
    - new_payment > 0 (a zero or negative "payment" is rejected, it is not
      a payment)

Postconditions
    - new_balance_pesewas = max(amount_due - (previous_payments + new_payment), 0)
    - if allow_overpayment is False and previous_payments + new_payment > amount_due,
      the payment is REJECTED (raises OverpaymentError) rather than silently
      accepted, unless the caller explicitly passes allow_overpayment=True
    - status reflects whether the account is now settled, partially paid, or
      (only when overpayment is explicitly allowed) overpaid

Failure behaviour
    - Invalid types or invalid ranges raise ValueError with a message that
      does NOT include the student ID or any other personal data (the caller
      is responsible for not putting personal data into the message either).
    - Overpayment without explicit permission raises OverpaymentError
      (a subclass of ValueError) instead of quietly capping or ignoring the
      excess, so the caller/UI must handle the case explicitly.
    - No exception is ever swallowed silently: every error path raises,
      it never returns a sentinel like None or -1.
"""

from dataclasses import dataclass


class OverpaymentError(ValueError):
    """Raised when a payment would exceed the outstanding balance and
    the caller has not explicitly set allow_overpayment=True."""


@dataclass(frozen=True)
class HallDuesResult:
    new_balance_pesewas: int
    status: str  # "PAID_IN_FULL" | "PARTIAL" | "OVERPAID"


def _validate_non_negative_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer number of pesewas")
    if value < 0:
        raise ValueError(f"{name} cannot be negative")


def calculate_hall_dues(amount_due: int,
                         previous_payments: int,
                         new_payment: int,
                         allow_overpayment: bool = False) -> HallDuesResult:
    """Apply a new payment to a hall-dues account and return the updated
    balance and status. Raises ValueError / OverpaymentError on invalid
    or disallowed input rather than returning a partial/garbage result."""

    _validate_non_negative_int(amount_due, "amount_due")
    _validate_non_negative_int(previous_payments, "previous_payments")

    if isinstance(new_payment, bool) or not isinstance(new_payment, int):
        raise ValueError("new_payment must be an integer number of pesewas")
    if new_payment <= 0:
        raise ValueError("new_payment must be a positive amount")

    total_paid = previous_payments + new_payment
    remaining = amount_due - total_paid

    if remaining < 0:
        if not allow_overpayment:
            raise OverpaymentError(
                "payment exceeds the outstanding balance; "
                "resubmit with allow_overpayment=True to accept it"
            )
        return HallDuesResult(new_balance_pesewas=0, status="OVERPAID")

    if remaining == 0:
        return HallDuesResult(new_balance_pesewas=0, status="PAID_IN_FULL")

    return HallDuesResult(new_balance_pesewas=remaining, status="PARTIAL")
