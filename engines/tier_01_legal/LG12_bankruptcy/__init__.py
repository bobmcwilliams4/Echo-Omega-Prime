"""
LG12 Bankruptcy Law Engine
============================
Production-grade bankruptcy law analysis engine implementing all 20 TIE
components for Chapter 7 liquidation, Chapter 11 reorganization, Chapter 13
wage earner plans, Chapter 12 family farmer, Chapter 15 cross-border,
means test, automatic stay, discharge/dischargeability, exemptions
(federal vs state/TX homestead), preference actions, fraudulent transfers,
proof of claim, plan confirmation, adversary proceedings, reaffirmation
agreements, student loan discharge (Brunner test), tax debt discharge,
lien stripping/cramdown, trustee powers, US Trustee oversight, BAPCPA,
Bankruptcy Code (Title 11 USC), FRBP, and Texas exemptions.

Port: 8402
Engine: LG12 Bankruptcy Law
Version: 2.0.0
"""

ENGINE_ID: str = "LG12"
ENGINE_NAME: str = "Bankruptcy Law Engine"
ENGINE_VERSION: str = "2.0.0"
ENGINE_PORT: int = 8402

__all__ = ["ENGINE_ID", "ENGINE_NAME", "ENGINE_VERSION", "ENGINE_PORT"]
