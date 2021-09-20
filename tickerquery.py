# This function takes a stock ticker and returns the values (closing prices) for a given time period
def search4ticker(phrase: str = 'GOOG') -> dict:
	"""Return a dict of dates and prices."""
	query_result = {}
	query_result['dates'] = []
	query_result['prices'] = []
	return query_result