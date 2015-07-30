"""
Script to fetch data for latest matches (reverse chronological order).
"""

from __future__ import print_function
from dota2py import api
from time import sleep as wait_for_next_fetch

def latest_matches(account_id=None, start_at_match_id=None,
                   matches_requested=500, fetch_delay=1, debug=True, **kwargs):
    """
    Returns data for most recent matches according to given kwargs
    Rate limits the API requests according to `fetch_delay` (in seconds)
    Output : last_response_status, last_response_detail, match_history
    """

    # tracking variables
    matches_fetched = 0
    last_match_id = start_at_match_id
    last_response_status = 1
    match_history = []
    last_response_detail = "Fetch successful"

    while last_response_status == 1 and matches_fetched < matches_requested:
        cur_response = api.get_match_history(account_id=account_id,
                                             start_at_match_id=last_match_id,
                                             **kwargs)
        last_response_status = cur_response['result']['status']
        if not last_response_status == 1:
            # unsuccessful query
            if not 'statusDetail' in cur_response['result']:
                last_response_detail = "Unknown error"
            else:
                last_response_detail = cur_response['result']['statusDetail']
            break
        else:
            # successful data fetch
            cur_matches = cur_response['result']['matches']
            if len(cur_matches) >= 1:
                if not match_history:
                    # very first fetch
                    match_history.extend(cur_matches)
                    matches_fetched += len(cur_matches)
                else:
                    # 2nd fetch onwards, ignore the first common match
                    match_history.extend(cur_matches[1:])
                    matches_fetched += len(cur_matches) - 1
                if len(cur_matches) == 1 and cur_matches[0]['match_id'] == last_match_id:
                    break
            else:
                break
            last_match_id = cur_matches[-1]['match_id']
        if debug:
            print("Matches fetched - #{}...".format(matches_fetched))
        wait_for_next_fetch(fetch_delay)
    if debug:
        print("{0}: {1}".format(last_response_status, last_response_detail))
    return {'status':last_response_status, 'statusDetail':last_response_detail,
            'matches':match_history}
