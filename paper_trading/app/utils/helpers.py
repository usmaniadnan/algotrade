from decimal import Decimal, ROUND_HALF_UP
from typing import Union

def round_decimal(value: Union[float, Decimal], places: int = 2) -> Decimal:
    """Round decimal to specified places"""
    if isinstance(value, float):
        value = Decimal(str(value))
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calculate_percentage(part: Union[float, Decimal], whole: Union[float, Decimal]) -> float:
    """Calculate percentage"""
    if whole == 0:
        return 0
    return float((part / whole) * 100)

def format_currency(amount: Union[float, Decimal]) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"
