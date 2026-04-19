# Nautilus Trader Rules
1. Never use Pandas dataframes in the core Event Loop execution.
2. Rely strictly on `nautilus_trader.core.data` object streams.
3. Market regimes must be governed by Step/SJM inferences prior to position sizing.
