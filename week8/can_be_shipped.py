"""An interface-style abstract base class for shippable objects."""

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return a shipping charge in dollars."""
