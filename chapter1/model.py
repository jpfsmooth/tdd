from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass( repr=True,frozen=True)
class OrderLine: 
    orderid: str
    sku: str
    qty: int 

class Batch:
    def __init__( self, ref: str, sku: str, qty: int, eta: Optional[ date] ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        #self.available_quantity = qty
        self._purchased_quantity = qty
        self._allocations = set()

    def can_allocate( self, line: OrderLine):
        return self.sku == line.sku and self.available_quantity >= line.qty

    def allocate( self, line: OrderLine):
        #self.available_quantity -= line.qty
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate( self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove( line)

    @property
    def allocated_quantity( self) -> int:
        return sum( line.qty for line in self._allocations)
  
    @property
    def available_quantity( self) -> int:
        return self._purchased_quantity - self.allocated_quantity






if __name__ == '__main__':
    order = OrderLine("order_id1", "97404378", 40)
    print(order)


