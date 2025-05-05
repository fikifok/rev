# retirement_planning.py – Emeklilik hedefi ve birikim hesaplamaları
from typing import Optional

class RetirementPlanner:
    def __init__(self, current_age: int, retirement_age: int, current_savings: float, monthly_contribution: float, expected_return: float):
        """
        current_age: Mevcut yaş
        retirement_age: Emeklilik hedef yaşı
        current_savings: Şu anki birikim
        monthly_contribution: Her ay eklenen miktar
        expected_return: Yıllık beklenen getiri oranı (örneğin 0.07 = %7)
        """
        self.current_age = current_age
        self.retirement_age = retirement_age
        self.current_savings = current_savings
        self.monthly_contribution = monthly_contribution
        self.expected_return = expected_return

    def calculate_future_value(self) -> float:
        """
        Emeklilik yaşında toplam birikim tahmini
        """
        months = (self.retirement_age - self.current_age) * 12
        monthly_rate = (1 + self.expected_return) ** (1/12) - 1
        future_value = self.current_savings * ((1 + monthly_rate) ** months)

        for _ in range(months):
            future_value += self.monthly_contribution
            future_value *= (1 + monthly_rate)

        return round(future_value, 2)

    def years_left(self) -> int:
        """Emekliliğe kalan yıl sayısı"""
        return max(0, self.retirement_age - self.current_age)
