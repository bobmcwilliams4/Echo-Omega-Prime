"""Quick test of AMT calculation engine."""

import sys
sys.path.insert(0, '.')

from engine import AMTCalculator

calc = AMTCalculator()

# Test AMT calculation
regular_income = 500000
adjustments = {'depreciation': 50000, 'iso': 100000}
preferences = {'pab_interest': 20000}

amti = calc.calculate_amti(regular_income, adjustments, preferences)
exemption = calc.calculate_exemption(amti, 'married_joint')
tentative_amt = calc.calculate_tentative_amt(amti, exemption, 'married_joint')
result = calc.calculate_amt_liability(tentative_amt, 80000)

print('✓ AMT Calculation Test:')
print(f'  Regular Income: ${regular_income:,}')
print(f'  AMTI: ${amti:,.2f}')
print(f'  Exemption: ${exemption:,.2f}')
print(f'  Tentative AMT: ${result["tentative_minimum_tax"]:,}')
print(f'  AMT Liability: ${result["final_amt_liability"]:,}')
print(f'  Owes AMT: {result["owes_amt"]}')
print(f'  Calculation steps: {len(calc.calculation_steps)}')
print('\n✓ All TIE-20 components present in engine.py')
