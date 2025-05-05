# rebalancer.py – Portföy yeniden dengeleme önerileri

from typing import Dict, Tuple

class Rebalancer:
    """
    Kullanıcının mevcut portföyü ile hedef portföy oranlarını karşılaştırır ve
    yeniden dengeleme için öneriler üretir.
    """

    def rebalance(self, portfolio: Dict[str, float], target_weights: Dict[str, float]) -> Dict[str, float]:
        """
        Hangi varlıktan ne kadar alınıp satılmalı? TL cinsinden öneri döndürür.
        
        Parameters:
            portfolio (dict): Örn. {"stocks": 10000, "crypto": 4000, "cash": 2000}
            target_weights (dict): Örn. {"stocks": 0.5, "crypto": 0.3, "cash": 0.2}

        Returns:
            dict: Örn. {"stocks": -500, "crypto": 1000, "cash": -500}
                  Negatifse azaltılmalı, pozitifse artırılmalı
        """
        total_value = sum(portfolio.values())
        recommendations = {}

        for asset, current_value in portfolio.items():
            target_value = total_value * target_weights.get(asset, 0)
            difference = round(target_value - current_value, 2)
            recommendations[asset] = difference

        return recommendations
