from dataclasses import dataclass, field


@dataclass
class Cliente:
    CustomerId: int
    FirstName: str
    LastName: str
    Country: str
    spesa: float                                 # somma di Total nell'intervallo
    artisti: set = field(default_factory=set)    # id degli artisti acquistati

    def __hash__(self):
        return hash(self.CustomerId)

    def __eq__(self, other):
        return isinstance(other, Cliente) and self.CustomerId == other.CustomerId

    def __str__(self):
        return f"{self.LastName} {self.FirstName}"