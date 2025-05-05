# src/modules/scenario_simulation.py
"""
scenario_simulation.py – Monte Carlo simülasyonu ile fiyat projeksiyonu yapar.
"""

import numpy as np
import pandas as pd

def monte_carlo_simulation(
    start_price: float,
    mu: float,
    sigma: float,
    days: int,
    num_simulations: int
) -> pd.DataFrame:
    """
    Monte Carlo yöntemiyle fiyat simülasyonu üretir.

    Args:
        start_price (float): Başlangıç fiyatı
        mu (float): Yıllık ortalama getiri
        sigma (float): Yıllık volatilite
        days (int): Simülasyon süresi (gün)
        num_simulations (int): Kaç farklı senaryo üretilecek

    Returns:
        pd.DataFrame: Her kolonu bir senaryoyu temsil eden fiyat verileri
    """
    dt = 1 / 252  # Günlük adım
    prices = np.zeros((days, num_simulations))
    prices[0] = start_price

    for t in range(1, days):
        rand = np.random.normal(0, 1, num_simulations)
        prices[t] = prices[t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * rand)

    df = pd.DataFrame(prices)
    return df

class ScenarioSimulation:
    """Test importları için boş sınıf."""
    pass
