from model.enums.ExtendedEnum import ExtendedEnum

class TransactionTypes(ExtendedEnum):
    UNKNOWN = -1
    FUNDS_OUT = 0
    FUNDS_IN = 1
    BALANCE_FORWARD = 2