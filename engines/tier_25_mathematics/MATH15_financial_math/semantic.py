import hashlib

SEMANTIC_MAP_VERSION = "1.0.0"
SEMANTIC_MAP_AUTHOR = "MATH15_financial_math Team"
SEMANTIC_MAP_ENGINE = "MATH15_financial_math"

SEMANTIC_MAP = {
    # Interest
    "interest": "interest",
    "int": "interest",
    "intrst": "interest",
    "interst": "interest",
    "intrest": "interest",
    "interest rate": "interest",
    "rate of interest": "interest",
    "rate interest": "interest",
    "int.": "interest",
    "int rate": "interest",
    "int rates": "interest",
    "interest rates": "interest",
    "interest-rate": "interest",
    "int-rate": "interest",
    "intrest rate": "interest",
    "interest-rate": "interest",
    "interestrate": "interest",
    "interest_r": "interest",
    "interest_rte": "interest",
    "interest_rte.": "interest",
    "interest_rte": "interest",
    "interest_rate": "interest",
    "interest_rate.": "interest",
    "interest-r": "interest",
    "intrest-r": "interest",
    "interest-rte": "interest",
    "interest-rte.": "interest",
    "interest-rates": "interest",
    "interest-rates.": "interest",
    "intrest-rates": "interest",
    "intrest-rates.": "interest",
    # Principal
    "principal": "principal",
    "prin": "principal",
    "princ": "principal",
    "principle": "principal",
    "principle amount": "principal",
    "principal amount": "principal",
    "princ amt": "principal",
    "princ amount": "principal",
    "principal_amt": "principal",
    "principal-amt": "principal",
    "principalamount": "principal",
    "principal_amt.": "principal",
    "principal-amount": "principal",
    "principalamount.": "principal",
    "principal_amt.": "principal",
    # Compound Interest
    "compound interest": "compound_interest",
    "compound int": "compound_interest",
    "comp interest": "compound_interest",
    "comp int": "compound_interest",
    "compoundint": "compound_interest",
    "compound-int": "compound_interest",
    "compound_interest": "compound_interest",
    "comp_interest": "compound_interest",
    "compoundintrest": "compound_interest",
    "compoundintrest": "compound_interest",
    "compoundintrest": "compound_interest",
    "compoundintrest": "compound_interest",
    # Simple Interest
    "simple interest": "simple_interest",
    "simple int": "simple_interest",
    "simpleint": "simple_interest",
    "simple-int": "simple_interest",
    "simple_interest": "simple_interest",
    "simp_interest": "simple_interest",
    "simpleintrest": "simple_interest",
    "simpleintrest": "simple_interest",
    # Annuity
    "annuity": "annuity",
    "annuities": "annuity",
    "ann": "annuity",
    "annutiy": "annuity",
    "annuties": "annuity",
    "annu": "annuity",
    "annuity payment": "annuity",
    "annuity payments": "annuity",
    "annuity-payment": "annuity",
    "annuity_payments": "annuity",
    "annuity_payment": "annuity",
    # Present Value
    "present value": "present_value",
    "pv": "present_value",
    "presentval": "present_value",
    "present_val": "present_value",
    "present-value": "present_value",
    "presentvalue": "present_value",
    "present_value.": "present_value",
    "present_val.": "present_value",
    # Future Value
    "future value": "future_value",
    "fv": "future_value",
    "futureval": "future_value",
    "future_val": "future_value",
    "future-value": "future_value",
    "futurevalue": "future_value",
    "future_value.": "future_value",
    "future_val.": "future_value",
    # Discount Rate
    "discount rate": "discount_rate",
    "discount": "discount_rate",
    "disc rate": "discount_rate",
    "disc": "discount_rate",
    "discount-rate": "discount_rate",
    "discount_rate": "discount_rate",
    "discount_rate.": "discount_rate",
    "discount-r": "discount_rate",
    # Rate of Return
    "rate of return": "rate_of_return",
    "ror": "rate_of_return",
    "rate return": "rate_of_return",
    "rate-return": "rate_of_return",
    "rate_of_return": "rate_of_return",
    "rateofreturn": "rate_of_return",
    "rate-return": "rate_of_return",
    # Net Present Value
    "net present value": "net_present_value",
    "npv": "net_present_value",
    "net present val": "net_present_value",
    "net present-val": "net_present_value",
    "netpresentvalue": "net_present_value",
    "net_present_value": "net_present_value",
    "net_present_val": "net_present_value",
    # Internal Rate of Return
    "internal rate of return": "internal_rate_of_return",
    "irr": "internal_rate_of_return",
    "internal rate return": "internal_rate_of_return",
    "internal-rate-return": "internal_rate_of_return",
    "internal_rate_of_return": "internal_rate_of_return",
    "internalrateofreturn": "internal_rate_of_return",
    # Cash Flow
    "cash flow": "cash_flow",
    "cashflow": "cash_flow",
    "cf": "cash_flow",
    "cash-flow": "cash_flow",
    "cash_flows": "cash_flow",
    "cash-flows": "cash_flow",
    "cashflows": "cash_flow",
    # Loan
    "loan": "loan",
    "loans": "loan",
    "ln": "loan",
    "lone": "loan",
    "lon": "loan",
    "loan amount": "loan",
    "loanamt": "loan",
    "loan_amt": "loan",
    "loan-amt": "loan",
    "loanamount": "loan",
    # Mortgage
    "mortgage": "mortgage",
    "mortgages": "mortgage",
    "mortg": "mortgage",
    "mortgag": "mortgage",
    "mortgage loan": "mortgage",
    "mortgage-loan": "mortgage",
    "mortgage_loan": "mortgage",
    # Amortization
    "amortization": "amortization",
    "amortisation": "amortization",
    "amort": "amortization",
    "amortize": "amortization",
    "amortised": "amortization",
    "amortized": "amortization",
    "amortization schedule": "amortization",
    "amortisation schedule": "amortization",
    "amort schedule": "amortization",
    # Bond
    "bond": "bond",
    "bonds": "bond",
    "bnd": "bond",
    "bond yield": "bond",
    "bond-yield": "bond",
    "bond_yield": "bond",
    "bondyield": "bond",
    # Yield
    "yield": "yield",
    "yield rate": "yield",
    "yield-rate": "yield",
    "yield_rate": "yield",
    "yieldrate": "yield",
    "yield to maturity": "yield_to_maturity",
    "ytm": "yield_to_maturity",
    "yield-to-maturity": "yield_to_maturity",
    "yield_to_maturity": "yield_to_maturity",
    # Volatility
    "volatility": "volatility",
    "vol": "volatility",
    "volat": "volatility",
    "volatlity": "volatility",
    "volatilty": "volatility",
    "volatility index": "volatility",
    "volatility-index": "volatility",
    "volatility_index": "volatility",
    # Dividend
    "dividend": "dividend",
    "dividends": "dividend",
    "div": "dividend",
    "divd": "dividend",
    "dividend yield": "dividend_yield",
    "dividend-yield": "dividend_yield",
    "dividend_yield": "dividend_yield",
    "divyield": "dividend_yield",
    # Stock
    "stock": "stock",
    "stocks": "stock",
    "stk": "stock",
    "stck": "stock",
    "stock price": "stock_price",
    "stock-price": "stock_price",
    "stock_price": "stock_price",
    "stockprice": "stock_price",
    # Equity
    "equity": "equity",
    "equities": "equity",
    "eq": "equity",
    "equ": "equity",
    # Option
    "option": "option",
    "options": "option",
    "opt": "option",
    "opt.": "option",
    "option price": "option_price",
    "option-price": "option_price",
    "option_price": "option_price",
    "optionprice": "option_price",
    # Futures
    "future": "future",
    "futures": "future",
    "fut": "future",
    "futr": "future",
    # Derivative
    "derivative": "derivative",
    "derivatives": "derivative",
    "deriv": "derivative",
    "deriv.": "derivative",
    # Hedge
    "hedge": "hedge",
    "hedging": "hedge",
    "hedged": "hedge",
    # Portfolio
    "portfolio": "portfolio",
    "port": "portfolio",
    "portf": "portfolio",
    "portfol": "portfolio",
    # Risk
    "risk": "risk",
    "risks": "risk",
    "rsk": "risk",
    "riks": "risk",
    # Beta
    "beta": "beta",
    "bta": "beta",
    "bet": "beta",
    # Alpha
    "alpha": "alpha",
    "alph": "alpha",
    "alfa": "alpha",
    # Sharpe Ratio
    "sharpe ratio": "sharpe_ratio",
    "sharpe": "sharpe_ratio",
    "sharpe-ratio": "sharpe_ratio",
    "sharpe_ratio": "sharpe_ratio",
    # Sortino Ratio
    "sortino ratio": "sortino_ratio",
    "sortino": "sortino_ratio",
    "sortino-ratio": "sortino_ratio",
    "sortino_ratio": "sortino_ratio",
    # Capital Asset Pricing Model
    "capital asset pricing model": "capm",
    "capm": "capm",
    "capital asset pricing": "capm",
    "capital asset price model": "capm",
    "capital asset price": "capm",
    # Dividend Discount Model
    "dividend discount model": "ddm",
    "ddm": "ddm",
    "dividend discount": "ddm",
    "dividend discount model": "ddm",
    # Black-Scholes Model
    "black-scholes model": "black_scholes",
    "black scholes": "black_scholes",
    "black-scholes": "black_scholes",
    "black_scholes": "black_scholes",
    "bs model": "black_scholes",
    "bs": "black_scholes",
    # Monte Carlo Simulation
    "monte carlo simulation": "monte_carlo",
    "monte carlo": "monte_carlo",
    "monte-carlo": "monte_carlo",
    "monte_carlo": "monte_carlo",
    "mc simulation": "monte_carlo",
    "mc sim": "monte_carlo",
    # Time Value of Money
    "time value of money": "time_value_of_money",
    "time value money": "time_value_of_money",
    "time value": "time_value_of_money",
    "tvom": "time_value_of_money",
    "time_value_of_money": "time_value_of_money",
    "time-value-of-money": "time_value_of_money",
    # Inflation
    "inflation": "inflation",
    "inflation rate": "inflation",
    "inflation-rate": "inflation",
    "inflation_rate": "inflation",
    "infl": "inflation",
    # Deflation
    "deflation": "deflation",
    "deflation rate": "deflation",
    "deflation-rate": "deflation",
    "deflation_rate": "deflation",
    # Exchange Rate
    "exchange rate": "exchange_rate",
    "exchange-rate": "exchange_rate",
    "exchange_rate": "exchange_rate",
    "fx rate": "exchange_rate",
    "forex rate": "exchange_rate",
    "forex-rate": "exchange_rate",
    "forex_rate": "exchange_rate",
    # Currency
    "currency": "currency",
    "curr": "currency",
    "curr.": "currency",
    "currncy": "currency",
    "currncy": "currency",
    # Equity Risk Premium
    "equity risk premium": "equity_risk_premium",
    "equity risk": "equity_risk_premium",
    "equity premium": "equity_risk_premium",
    "equity-risk-premium": "equity_risk_premium",
    "equity_risk_premium": "equity_risk_premium",
    # Capital Gain
    "capital gain": "capital_gain",
    "capital gains": "capital_gain",
    "cap gain": "capital_gain",
    "cap gains": "capital_gain",
    "capital-gain": "capital_gain",
    "capital_gains": "capital_gain",
    # Capital Loss
    "capital loss": "capital_loss",
    "capital losses": "capital_loss",
    "cap loss": "capital_loss",
    "cap losses": "capital_loss",
    "capital-loss": "capital_loss",
    "capital_losses": "capital_loss",
    # Market Capitalization
    "market capitalization": "market_capitalization",
    "market cap": "market_capitalization",
    "market-cap": "market_capitalization",
    "market_cap": "market_capitalization",
    "marketcap": "market_capitalization",
    # Earnings Per Share
    "earnings per share": "earnings_per_share",
    "eps": "earnings_per_share",
    "earning per share": "earnings_per_share",
    "earnings/share": "earnings_per_share",
    "earnings_per_share": "earnings_per_share",
    # Price to Earnings Ratio
    "price to earnings ratio": "price_to_earnings",
    "price earnings ratio": "price_to_earnings",
    "pe ratio": "price_to_earnings",
    "p/e ratio": "price_to_earnings",
    "price-to-earnings": "price_to_earnings",
    "price_to_earnings": "price_to_earnings",
    # Price to Book Ratio
    "price to book ratio": "price_to_book",
    "price book ratio": "price_to_book",
    "pb ratio": "price_to_book",
    "p/b ratio": "price_to_book",
    "price-to-book": "price_to_book",
    "price_to_book": "price_to_book",
    # Debt to Equity Ratio
    "debt to equity ratio": "debt_to_equity",
    "debt equity ratio": "debt_to_equity",
    "debt/equity ratio": "debt_to_equity",
    "debt-to-equity": "debt_to_equity",
    "debt_to_equity": "debt_to_equity",
    # Return on Equity
    "return on equity": "return_on_equity",
    "roe": "return_on_equity",
    "return equity": "return_on_equity",
    "return-on-equity": "return_on_equity",
    "return_on_equity": "return_on_equity",
    # Return on Assets
    "return on assets": "return_on_assets",
    "roa": "return_on_assets",
    "return assets": "return_on_assets",
    "return-on-assets": "return_on_assets",
    "return_on_assets": "return_on_assets",
    # Earnings Before Interest and Taxes
    "earnings before interest and taxes": "ebit",
    "ebit": "ebit",
    "earnings before interest & taxes": "ebit",
    "earnings before interest": "ebit",
    "earnings before taxes": "ebit",
    # Earnings Before Interest, Taxes, Depreciation and Amortization
    "earnings before interest, taxes, depreciation and amortization": "ebitda",
    "ebitda": "ebitda",
    "earnings before interest and taxes depreciation amortization": "ebitda",
    # Free Cash Flow
    "free cash flow": "free_cash_flow",
    "fcf": "free_cash_flow",
    "free cashflow": "free_cash_flow",
    "free-cash-flow": "free_cash_flow",
    "free_cash_flow": "free_cash_flow",
    # Working Capital
    "working capital": "working_capital",
    "working-capital": "working_capital",
    "working_capital": "working_capital",
    # Leverage
    "leverage": "leverage",
    "leveraging": "leverage",
    "levarage": "leverage",
    # Liquidity
    "liquidity": "liquidity",
    "liquid": "liquidity",
    "liqudity": "liquidity",
    # Dividend Payout Ratio
    "dividend payout ratio": "dividend_payout_ratio",
    "dividend payout": "dividend_payout_ratio",
    "dividend-payout-ratio": "dividend_payout_ratio",
    "dividend_payout_ratio": "dividend_payout_ratio",
    # Earnings Growth Rate
    "earnings growth rate": "earnings_growth_rate",
    "earnings growth": "earnings_growth_rate",
    "earnings-growth-rate": "earnings_growth_rate",
    "earnings_growth_rate": "earnings_growth_rate",
    # Price to Sales Ratio
    "price to sales ratio": "price_to_sales",
    "price sales ratio": "price_to_sales",
    "ps ratio": "price_to_sales",
    "p/s ratio": "price_to_sales",
    "price-to-sales": "price_to_sales",
    "price_to_sales": "price_to_sales",
    # Market Risk Premium
    "market risk premium": "market_risk_premium",
    "market risk": "market_risk_premium",
    "market-risk-premium": "market_risk_premium",
    "market_risk_premium": "market_risk_premium",
    # Duration
    "duration": "duration",
    "dur": "duration",
    "duraton": "duration",
    # Convexity
    "convexity": "convexity",
    "convex": "convexity",
    # Yield Curve
    "yield curve": "yield_curve",
    "yield-curve": "yield_curve",
    "yield_curve": "yield_curve",
    # Capital Structure
    "capital structure": "capital_structure",
    "capital-structure": "capital_structure",
    "capital_structure": "capital_structure",
    # Beta Coefficient
    "beta coefficient": "beta",
    "beta coef": "beta",
    "beta-coefficient": "beta",
    "beta_coefficient": "beta",
    # Market Index
    "market index": "market_index",
    "market-index": "market_index",
    "market_index": "market_index",
    # Dividend Growth Model
    "dividend growth model": "dividend_growth_model",
    "dividend-growth-model": "dividend_growth_model",
    "dividend_growth_model": "dividend_growth_model",
    # Capital Budgeting
    "capital budgeting": "capital_budgeting",
    "capital-budgeting": "capital_budgeting",
    "capital_budgeting": "capital_budgeting",
    # Financial Leverage
    "financial leverage": "financial_leverage",
    "financial-leverage": "financial_leverage",
    "financial_leverage": "financial_leverage",
    # Operating Leverage
    "operating leverage": "operating_leverage",
    "operating-leverage": "operating_leverage",
    "operating_leverage": "operating_leverage",
    # Debt Service Coverage Ratio
    "debt service coverage ratio": "debt_service_coverage_ratio",
    "debt service coverage": "debt_service_coverage_ratio",
    "debt-service-coverage-ratio": "debt_service_coverage_ratio",
    "debt_service_coverage_ratio": "debt_service_coverage_ratio",
    # Cash Conversion Cycle
    "cash conversion cycle": "cash_conversion_cycle",
    "cash-conversion-cycle": "cash_conversion_cycle",
    "cash_conversion_cycle": "cash_conversion_cycle",
    # Working Capital Cycle
    "working capital cycle": "working_capital_cycle",
    "working-capital-cycle": "working_capital_cycle",
    "working_capital_cycle": "working_capital_cycle",
    # Earnings Yield
    "earnings yield": "earnings_yield",
    "earnings-yield": "earnings_yield",
    "earnings_yield": "earnings_yield",
    # Capital Expenditure
    "capital expenditure": "capital_expenditure",
    "capex": "capital_expenditure",
    "capital-expenditure": "capital_expenditure",
    "capital_expenditure": "capital_expenditure",
    # Operating Expense
    "operating expense": "operating_expense",
    "opex": "operating_expense",
    "operating-expense": "operating_expense",
    "operating_expense": "operating_expense",
    # Earnings Before Tax
    "earnings before tax": "ebt",
    "ebt": "ebt",
    "earnings before taxes": "ebt",
    # Market Order
    "market order": "market_order",
    "market-order": "market_order",
    "market_order": "market_order",
    # Limit Order
    "limit order": "limit_order",
    "limit-order": "limit_order",
    "limit_order": "limit_order",
    # Stop Loss Order
    "stop loss order": "stop_loss_order",
    "stop-loss-order": "stop_loss_order",
    "stop_loss_order": "stop_loss_order",
    # Bid Price
    "bid price": "bid_price",
    "bid-price": "bid_price",
    "bid_price": "bid_price",
    # Ask Price
    "ask price": "ask_price",
    "ask-price": "ask_price",
    "ask_price": "ask_price",
    # Spread
    "spread": "spread",
    "bid-ask spread": "spread",
    "bid ask spread": "spread",
    "bid_ask_spread": "spread",
    # Volume
    "volume": "volume",
    "vol": "volume",
    "trading volume": "volume",
    "trade volume": "volume",
    "trading-volume": "volume",
    "trade-volume": "volume",
    "trading_volume": "volume",
    "trade_volume": "volume",
    # Market Capitalization Weighted Index
    "market capitalization weighted index": "market_cap_weighted_index",
    "market cap weighted index": "market_cap_weighted_index",
    "market-cap-weighted-index": "market_cap_weighted_index",
    "market_cap_weighted_index": "market_cap_weighted_index",
    # Equal Weighted Index
    "equal weighted index": "equal_weighted_index",
    "equal-weighted-index": "equal_weighted_index",
    "equal_weighted_index": "equal_weighted_index",
    # Price Weighted Index
    "price weighted index": "price_weighted_index",
    "price-weighted-index": "price_weighted_index",
    "price_weighted_index": "price_weighted_index",
    # Exchange Traded Fund
    "exchange traded fund": "etf",
    "etf": "etf",
    "exchange-traded-fund": "etf",
    "exchange_traded_fund": "etf",
    # Mutual Fund
    "mutual fund": "mutual_fund",
    "mutual-fund": "mutual_fund",
    "mutual_fund": "mutual_fund",
    # Hedge Fund
    "hedge fund": "hedge_fund",
    "hedge-fund": "hedge_fund",
    "hedge_fund": "hedge_fund",
    # Money Market Fund
    "money market fund": "money_market_fund",
    "money-market-fund": "money_market_fund",
    "money_market_fund": "money_market_fund",
    # Asset Allocation
    "asset allocation": "asset_allocation",
    "asset-allocation": "asset_allocation",
    "asset_allocation": "asset_allocation",
    # Rebalancing
    "rebalancing": "rebalancing",
    "rebalance": "rebalancing",
    "re-balance": "rebalancing",
    # Diversification
    "diversification": "diversification",
    "diversify": "diversification",
    "diversified": "diversification",
    # Capital Gain Tax
    "capital gain tax": "capital_gain_tax",
    "capital gains tax": "capital_gain_tax",
    "cap gain tax": "capital_gain_tax",
    "cap gains tax": "capital_gain_tax",
    "capital-gain-tax": "capital_gain_tax",
    "capital_gain_tax": "capital_gain_tax",
    # Tax Shield
    "tax shield": "tax_shield",
    "tax-shield": "tax_shield",
    "tax_shield": "tax_shield",
    # Tax Rate
    "tax rate": "tax_rate",
    "tax-rate": "tax_rate",
    "tax_rate": "tax_rate",
    # After Tax Return
    "after tax return": "after_tax_return",
    "after-tax return": "after_tax_return",
    "after_tax_return": "after_tax_return",
    # Pre Tax Return
    "pre tax return": "pre_tax_return",
    "pre-tax return": "pre_tax_return",
    "pre_tax_return": "pre_tax_return",
    # Capital Asset Pricing Model Beta
    "capm beta": "beta",
    "capital asset pricing model beta": "beta",
    # Dividend Yield
    "dividend yield": "dividend_yield",
    "dividend-yield": "dividend_yield",
    "dividend_yield": "dividend_yield",
    # Earnings Before Interest, Taxes, Depreciation, Amortization
    "ebitda margin": "ebitda_margin",
    "ebitda-margin": "ebitda_margin",
    "ebitda_margin": "ebitda_margin",
    # Earnings Before Interest and Taxes Margin
    "ebit margin": "ebit_margin",
    "ebit-margin": "ebit_margin",
    "ebit_margin": "ebit_margin",
    # Net Income
    "net income": "net_income",
    "net-income": "net_income",
    "net_income": "net_income",
    "net profit": "net_income",
    "netprofit": "net_income",
    # Gross Profit
    "gross profit": "gross_profit",
    "gross-profit": "gross_profit",
    "gross_profit": "gross_profit",
    # Operating Income
    "operating income": "operating_income",
    "operating-income": "operating_income",
    "operating_income": "operating_income",
    # EBITDA
    "ebitda": "ebitda",
    "e.b.i.t.d.a": "ebitda",
    # EBIT
    "ebit": "ebit",
    "e.b.i.t": "ebit",
    # Net Working Capital
    "net working capital": "net_working_capital",
    "net-working-capital": "net_working_capital",
    "net_working_capital": "net_working_capital",
    # Capital Employed
    "capital employed": "capital_employed",
    "capital-employed": "capital_employed",
    "capital_employed": "capital_employed",
    # Operating Cash Flow
    "operating cash flow": "operating_cash_flow",
    "operating-cash-flow": "operating_cash_flow",
    "operating_cash_flow": "operating_cash_flow",
    # Free Cash Flow to Equity
    "free cash flow to equity": "free_cash_flow_to_equity",
    "free-cash-flow-to-equity": "free_cash_flow_to_equity",
    "free_cash_flow_to_equity": "free_cash_flow_to_equity",
    "fcfe": "free_cash_flow_to_equity",
    # Free Cash Flow to Firm
    "free cash flow to firm": "free_cash_flow_to_firm",
    "free-cash-flow-to-firm": "free_cash_flow_to_firm",
    "free_cash_flow_to_firm": "free_cash_flow_to_firm",
    "fcff": "free_cash_flow_to_firm",
    # Cost of Capital
    "cost of capital": "cost_of_capital",
    "cost-of-capital": "cost_of_capital",
    "cost_of_capital": "cost_of_capital",
    # Weighted Average Cost of Capital
    "weighted average cost of capital": "wacc",
    "weighted-average-cost-of-capital": "wacc",
    "weighted_average_cost_of_capital": "wacc",
    "wacc": "wacc",
    # Cost of Debt
    "cost of debt": "cost_of_debt",
    "cost-of-debt": "cost_of_debt",
    "cost_of_debt": "cost_of_debt",
    # Cost of Equity
    "cost of equity": "cost_of_equity",
    "cost-of-equity": "cost_of_equity",
    "cost_of_equity": "cost_of_equity",
    # Dividend Payout
    "dividend payout": "dividend_payout",
    "dividend-payout": "dividend_payout",
    "dividend_payout": "dividend_payout",
    # Dividend Cover
    "dividend cover": "dividend_cover",
    "dividend-cover": "dividend_cover",
    "dividend_cover": "dividend_cover",
    # Earnings Before Interest, Taxes, Depreciation, Amortization Margin
    "ebitda margin": "ebitda_margin",
    "ebitda-margin": "ebitda_margin",
    "ebitda_margin": "ebitda_margin",
    # Earnings Before Interest and Taxes Margin
    "ebit margin": "ebit_margin",
    "ebit-margin": "ebit_margin",
    "ebit_margin": "ebit_margin",
    # Price to Cash Flow Ratio
    "price to cash flow ratio": "price_to_cash_flow",
    "price cash flow ratio": "price_to_cash_flow",
    "pcf ratio": "price_to_cash_flow",
    "p/cf ratio": "price_to_cash_flow",
    "price-to-cash-flow": "price_to_cash_flow",
    "price_to_cash_flow": "price_to_cash_flow",
    # Price to Free Cash Flow Ratio
    "price to free cash flow ratio": "price_to_free_cash_flow",
    "price free cash flow ratio": "price_to_free_cash_flow",
    "pfcf ratio": "price_to_free_cash_flow",
    "p/fcf ratio": "price_to_free_cash_flow",
    "price-to-free-cash-flow": "price_to_free_cash_flow",
    "price_to_free_cash_flow": "price_to_free_cash_flow",
    # Operating Margin
    "operating margin": "operating_margin",
    "operating-margin": "operating_margin",
    "operating_margin": "operating_margin",
    # Net Margin
    "net margin": "net_margin",
    "net-margin": "net_margin",
    "net_margin": "net_margin",
    # Gross Margin
    "gross margin": "gross_margin",
    "gross-margin": "gross_margin",
    "gross_margin": "gross_margin",
    # EBITDA Margin
    "ebitda margin": "ebitda_margin",
    "ebitda-margin": "ebitda_margin",
    "ebitda_margin": "ebitda_margin",
    # Debt Ratio
    "debt ratio": "debt_ratio",
    "debt-ratio": "debt_ratio",
    "debt_ratio": "debt_ratio",
    # Debt to Capital Ratio
    "debt to capital ratio": "debt_to_capital",
    "debt to capital": "debt_to_capital",
    "debt-to-capital-ratio": "debt_to_capital",
    "debt_to_capital": "debt_to_capital",
    # Interest Coverage Ratio
    "interest coverage ratio": "interest_coverage_ratio",
    "interest coverage": "interest_coverage_ratio",
    "interest-coverage-ratio": "interest_coverage_ratio",
    "interest_coverage_ratio": "interest_coverage_ratio",
    # Cash Ratio
    "cash ratio": "cash_ratio",
    "cash-ratio": "cash_ratio",
    "cash_ratio": "cash_ratio",
    # Quick Ratio
    "quick ratio": "quick_ratio",
    "quick-ratio": "quick_ratio",
    "quick_ratio": "quick_ratio",
    # Current Ratio
    "current ratio": "current_ratio",
    "current-ratio": "current_ratio",
    "current_ratio": "current_ratio",
    # Operating Cycle
    "operating cycle": "operating_cycle",
    "operating-cycle": "operating_cycle",
    "operating_cycle": "operating_cycle",
    # Days Sales Outstanding
    "days sales outstanding": "days_sales_outstanding",
    "days-sales-outstanding": "days_sales_outstanding",
    "days_sales_outstanding": "days_sales_outstanding",
    "dso": "days_sales_outstanding",
    # Days Inventory Outstanding
    "days inventory outstanding": "days_inventory_outstanding",
    "days-inventory-outstanding": "days_inventory_outstanding",
    "days_inventory_outstanding": "days_inventory_outstanding",
    "dio": "days_inventory_outstanding",
    # Days Payable Outstanding
    "days payable outstanding": "days_payable_outstanding",
    "days-payable-outstanding": "days_payable_outstanding",
    "days_payable_outstanding": "days_payable_outstanding",
    "dpo": "days_payable_outstanding",
    # Cash Flow from Operations
    "cash flow from operations": "cash_flow_from_operations",
    "cash-flow-from-operations": "cash_flow_from_operations",
    "cash_flow_from_operations": "cash_flow_from_operations",
    "cfo": "cash_flow_from_operations",
    # Operating Profit
    "operating profit": "operating_profit",
    "operating-profit": "operating_profit",
    "operating_profit": "operating_profit",
    # Net Profit Margin
    "net profit margin": "net_profit_margin",
    "net-profit-margin": "net_profit_margin",
    "net_profit_margin": "net_profit_margin",
    # Earnings Per Share Growth
    "earnings per share growth": "eps_growth",
    "eps growth": "eps_growth",
    "earnings-per-share-growth": "eps_growth",
    "eps_growth": "eps_growth",
    # Price to Earnings Growth Ratio
    "price to earnings growth ratio": "peg_ratio",
    "peg ratio": "peg_ratio",
    "price-earnings-growth-ratio": "peg_ratio",
    "peg_ratio": "peg_ratio",
    # Book Value Per Share
    "book value per share": "book_value_per_share",
    "book-value-per-share": "book_value_per_share",
    "book_value_per_share": "book_value_per_share",
    # Market Value Added
    "market value added": "market_value_added",
    "market-value-added": "market_value_added",
    "market_value_added": "market_value_added",
    # Economic Value Added
    "economic value added": "economic_value_added",
    "economic-value-added": "economic_value_added",
    "economic_value_added": "economic_value_added",
    # Residual Income
    "residual income": "residual_income",
    "residual-income": "residual_income",
    "residual_income": "residual_income",
    # Free Cash Flow Yield
    "free cash flow yield": "free_cash_flow_yield",
    "free-cash-flow-yield": "free_cash_flow_yield",
    "free_cash_flow_yield": "free_cash_flow_yield",
    # Price to Tangible Book Ratio
    "price to tangible book ratio": "price_to_tangible_book",
    "price tangible book ratio": "price_to_tangible_book",
    "ptb ratio": "price_to_tangible_book",
    "p/tb ratio": "price_to_tangible_book",
    "price-to-tangible-book": "price_to_tangible_book",
    "price_to_tangible_book": "price_to_tangible_book",
    # Tangible Book Value
    "tangible book value": "tangible_book_value",
    "tangible-book-value": "tangible_book_value",
    "tangible_book_value": "tangible_book_value",
    # Net Asset Value
    "net asset value": "net_asset_value",
    "net-asset-value": "net_asset_value",
    "net_asset_value": "net_asset_value",
    # Price to Net Asset Value Ratio
    "price to net asset value ratio": "price_to_net_asset_value",
    "price net asset value ratio": "price_to_net_asset_value",
    "p/nav ratio": "price_to_net_asset_value",
    "price-to-net-asset-value": "price_to_net_asset_value",
    "price_to_net_asset_value": "price_to_net_asset_value",
    # Operating Expense Ratio
    "operating expense ratio": "operating_expense_ratio",
    "operating-expense-ratio": "operating_expense_ratio",
    "operating_expense_ratio": "operating_expense_ratio",
    # Expense Ratio
    "expense ratio": "expense_ratio",
    "expense-ratio": "expense_ratio",
    "expense_ratio": "expense_ratio",
    # Return on Investment
    "return on investment": "return_on_investment",
    "roi": "return_on_investment",
    "return-investment": "return_on_investment",
    "return_on_investment": "return_on_investment",
    # Return on Capital Employed
    "return on capital employed": "return_on_capital_employed",
    "roce": "return_on_capital_employed",
    "return-capital-employed": "return_on_capital_employed",
    "return_on_capital_employed": "return_on_capital_employed",
    # Dividend Coverage Ratio
    "dividend coverage ratio": "dividend_coverage_ratio",
    "dividend-coverage-ratio": "dividend_coverage_ratio",
    "dividend_coverage_ratio": "dividend_coverage_ratio",
    # Interest Expense
    "interest expense": "interest_expense",
    "interest-expense": "interest_expense",
    "interest_expense": "interest_expense",
    # Interest Income
    "interest income": "interest_income",
    "interest-income": "interest_income",
    "interest_income": "interest_income",
    # Operating Income Margin
    "operating income margin": "operating_income_margin",
    "operating-income-margin": "operating_income_margin",
    "operating_income_margin": "operating_income_margin",
    # Net Debt
    "net debt": "net_debt",
    "net-debt": "net_debt",
    "net_debt": "net_debt",
    # Debt to EBITDA Ratio
    "debt to ebitda ratio": "debt_to_ebitda",
    "debt-ebitda-ratio": "debt_to_ebitda",
    "debt_to_ebitda": "debt_to_ebitda",
    # EBITDA to Interest Coverage Ratio
    "ebitda to interest coverage ratio": "ebitda_to_interest_coverage",
    "ebitda-interest-coverage-ratio": "ebitda_to_interest_coverage",
    "ebitda_to_interest_coverage": "ebitda_to_interest_coverage",
    # Dividend Yield Ratio
    "dividend yield ratio": "dividend_yield_ratio",
    "dividend-yield-ratio": "dividend_yield_ratio",
    "dividend_yield_ratio": "dividend_yield_ratio",
    # Price to Cash Earnings Ratio
    "price to cash earnings ratio": "price_to_cash_earnings",
    "price-cash-earnings-ratio": "price_to_cash_earnings",
    "price_to_cash_earnings": "price_to_cash_earnings",
    # Cash Earnings
    "cash earnings": "cash_earnings",
    "cash-earnings": "cash_earnings",
    "cash_earnings": "cash_earnings",
    # Earnings Before Extraordinary Items
    "earnings before extraordinary items": "ebei",
    "ebei": "ebei",
    # Extraordinary Items
    "extraordinary items": "extraordinary_items",
    "extraordinary-items": "extraordinary_items",
    "extraordinary_items": "extraordinary_items",
    # Operating Leverage Ratio
    "operating leverage ratio": "operating_leverage_ratio",
    "operating-leverage-ratio": "operating_leverage_ratio",
    "operating_leverage_ratio": "operating_leverage_ratio",
    # Financial Leverage Ratio
    "financial leverage ratio": "financial_leverage_ratio",
    "financial-leverage-ratio": "financial_leverage_ratio",
    "financial_leverage_ratio": "financial_leverage_ratio",
    # Interest Rate Swap
    "interest rate swap": "interest_rate_swap",
    "interest-rate-swap": "interest_rate_swap",
    "interest_rate_swap": "interest_rate_swap",
    # Credit Default Swap
    "credit default swap": "credit_default_swap",
    "credit-default-swap": "credit_default_swap",
    "credit_default_swap": "credit_default_swap",
    # Total Shareholder Return
    "total shareholder return": "total_shareholder_return",
    "total-shareholder-return": "total_shareholder_return",
    "total_shareholder_return": "total_shareholder_return",
    # Earnings Before Interest, Taxes, Depreciation, Amortization and Rent
    "ebitdar": "ebitdar",
    "earnings before interest, taxes, depreciation, amortization and rent": "ebitdar",
    # Earnings Before Interest, Taxes, Depreciation, Amortization and Rent Margin
    "ebitdar margin": "ebitdar_margin",
    "ebitdar-margin": "ebitdar_margin",
    "ebitdar_margin": "ebitdar_margin",
    # Price to Earnings to Growth Ratio
    "price to earnings to growth ratio": "peg_ratio",
    # Cost of Goods Sold
    "cost of goods sold": "cost_of_goods_sold",
    "cost-of-goods-sold": "cost_of_goods_sold",
    "cost_of_goods_sold": "cost_of_goods_sold",
    "cogs": "cost_of_goods_sold",
    # Operating Cycle Days
    "operating cycle days": "operating_cycle_days",
    "operating-cycle-days": "operating_cycle_days",
    "operating_cycle_days": "operating_cycle_days",
    # Inventory Turnover
    "inventory turnover": "inventory_turnover",
    "inventory-turnover": "inventory_turnover",
    "inventory_turnover": "inventory_turnover",
    # Receivables Turnover
    "receivables turnover": "receivables_turnover",
    "receivables-turnover": "receivables_turnover",
    "receivables_turnover": "receivables_turnover",
    # Payables Turnover
    "payables turnover": "payables_turnover",
    "payables-turnover": "payables_turnover",
    "payables_turnover": "payables_turnover",
    # Asset Turnover
    "asset turnover": "asset_turnover",
    "asset-turnover": "asset_turnover",
    "asset_turnover": "asset_turnover",
    # Fixed Asset Turnover
    "fixed asset turnover": "fixed_asset_turnover",
    "fixed-asset-turnover": "fixed_asset_turnover",
    "fixed_asset_turnover": "fixed_asset_turnover",
    # Working Capital Turnover
    "working capital turnover": "working_capital_turnover",
    "working-capital-turnover": "working_capital_turnover",
    "working_capital_turnover": "working_capital_turnover",
    # Dividend Yield Percentage
    "dividend yield percentage": "dividend_yield",
    # Earnings Yield Percentage
    "earnings yield percentage": "earnings_yield",
    # Price to Earnings Percentage
    "price to earnings percentage": "price_to_earnings",
    # Price to Book Percentage
    "price to book percentage": "price_to_book",
    # Price to Sales Percentage
    "price to sales percentage": "price_to_sales",
    # Price to Cash Flow Percentage
    "price to cash flow percentage": "price_to_cash_flow",
    # Price to Free Cash Flow Percentage
    "price to free cash flow percentage": "price_to_free_cash_flow",
    # Debt to Equity Percentage
    "debt to equity percentage": "debt_to_equity",
    # Debt to Capital Percentage
    "debt to capital percentage": "debt_to_capital",
    # Return on Equity Percentage
    "return on equity percentage": "return_on_equity",
    # Return on Assets Percentage
    "return on assets percentage": "return_on_assets",
    # Return on Investment Percentage
    "return on investment percentage": "return_on_investment",
    # Return on Capital Employed Percentage
    "return on capital employed percentage": "return_on_capital_employed",
    # Operating Margin Percentage
    "operating margin percentage": "operating_margin",
    # Net Margin Percentage
    "net margin percentage": "net_margin",
    # Gross Margin Percentage
    "gross margin percentage": "gross_margin",
    # EBITDA Margin Percentage
    "ebitda margin percentage": "ebitda_margin",
    # Interest Coverage Ratio Percentage
    "interest coverage ratio percentage": "interest_coverage_ratio",
    # Cash Ratio Percentage
    "cash ratio percentage": "cash_ratio",
    # Quick Ratio Percentage
    "quick ratio percentage": "quick_ratio",
    # Current Ratio Percentage
    "current ratio percentage": "current_ratio",
    # Debt Ratio Percentage
    "debt ratio percentage": "debt_ratio",
    # Debt to EBITDA Percentage
    "debt to ebitda percentage": "debt_to_ebitda",
    # Dividend Payout Ratio Percentage
    "dividend payout ratio percentage": "dividend_payout_ratio",
    # Dividend Coverage Ratio Percentage
    "dividend coverage ratio percentage": "dividend_coverage_ratio",
    # Earnings Per Share Percentage
    "earnings per share percentage": "earnings_per_share",
    # Price to Earnings Growth Percentage
    "price to earnings growth percentage": "peg_ratio",
    # Price to Tangible Book Percentage
    "price to tangible book percentage": "price_to_tangible_book",
    # Price to Net Asset Value Percentage
    "price to net asset value percentage": "price_to_net_asset_value",
    # Operating Expense Ratio Percentage
    "operating expense ratio percentage": "operating_expense_ratio",
    # Expense Ratio Percentage
    "expense ratio percentage": "expense_ratio",
    # Market Capitalization Percentage
    "market capitalization percentage": "market_capitalization",
    # Market Index Percentage
    "market index percentage": "market_index",
    # Beta Percentage
    "beta percentage": "beta",
    # Alpha Percentage
    "alpha percentage": "alpha",
    # Sharpe Ratio Percentage
    "sharpe ratio percentage": "sharpe_ratio",
    # Sortino Ratio Percentage
    "sortino ratio percentage": "sortino_ratio",
    # Capital Asset Pricing Model Percentage
    "capital asset pricing model percentage": "capm",
    # Dividend Discount Model Percentage
    "dividend discount model percentage": "ddm",
    # Black-Scholes Model Percentage
    "black-scholes model percentage": "black_scholes",
    # Monte Carlo Simulation Percentage
    "monte carlo simulation percentage": "monte_carlo",
    # Time Value of Money Percentage
    "time value of money percentage": "time_value_of_money",
    # Inflation Percentage
    "inflation percentage": "inflation",
    # Deflation Percentage
    "deflation percentage": "deflation",
    # Exchange Rate Percentage
    "exchange rate percentage": "exchange_rate",
    # Currency Percentage
    "currency percentage": "currency",
}

_EXPECTED_ENTRY_COUNT = len(SEMANTIC_MAP)

def _compute_map_hash() -> str:
    hasher = hashlib.sha256()
    for key in sorted(SEMANTIC_MAP.keys()):
        value = SEMANTIC_MAP[key]
        hasher.update(key.encode('utf-8'))
        hasher.update(b'\0')
        hasher.update(value.encode('utf-8'))
        hasher.update(b'\0')
    return hasher.hexdigest()

_MAP_INTEGRITY_HASH = _compute_map_hash()

def verify_integrity() -> dict:
    current_count = len(SEMANTIC_MAP)
    current_hash = _compute_map_hash()
    is_valid = (current_count == _EXPECTED_ENTRY_COUNT) and (current_hash == _MAP_INTEGRITY_HASH)
    return {
        "status": "valid" if is_valid else "invalid",
        "entries": current_count,
        "expected_entries": _EXPECTED_ENTRY_COUNT,
        "hash": current_hash,
        "expected_hash": _MAP_INTEGRITY_HASH,
        "is_valid": is_valid,
    }

def normalize_term(term: str) -> str:
    if not isinstance(term, str):
        raise TypeError("term must be a string")
    key = term.strip().lower()
    return SEMANTIC_MAP.get(key, key)

def get_related_terms(term: str) -> list[str]:
    normalized = normalize_term(term)
    related = [k for k, v in SEMANTIC_MAP.items() if v == normalized]
    return related

def get_all_mappings() -> dict:
    return dict(SEMANTIC_MAP)