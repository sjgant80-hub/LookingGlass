"""Frumkin Equation: ∂F/∂t = α·F(1-F) - β·F - g·F²"""
import math

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI  # ≈ 0.618


class FrumkinModel:
    """Stability analysis via entropy ratio κ."""

    def __init__(self, alpha=1.0, beta=0.1, g=0.0):
        self.alpha = alpha
        self.beta = beta
        self.g = g

    def equilibrium(self):
        return PHI_INV

    def dfdt(self, f):
        a, b, g = self.alpha, self.beta, self.g
        return a * f * (1 - f) - b * f - g * f * f

    def kappa(self, order, entropy):
        if entropy == 0:
            return 0.0
        return order / entropy

    def health(self, kappa):
        return 1.0 - abs(kappa - PHI_INV)

    def predict_stability(self, kappa):
        if kappa < 0.2:
            return "terminal"
        if kappa < 0.4:
            return "critical"
        if kappa < 0.55:
            return "unstable"
        if kappa < 0.65:
            return "stable"
        return "robust"
