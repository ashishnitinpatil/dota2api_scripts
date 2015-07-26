"""
Script to fetch history for the latest matches (global, public)
"""

from __future__ import print_function
from dota2py import api
from time import sleep as wait_for_next_fetch

def public_match_history(start_at_match_seq_num=None, fetch_delay=1,
                         matches_requested=10**5,
                         **kwargs):
    """
    Returns list of most recent public matches according to given kwargs
    Rate limits the API requests according to `fetch_delay` (in seconds)
    Output : last_response_status, last_response_detail, match_history
    """

    # tracking variables
    matches_fetched = 0
    last_match_id = start_at_match_seq_num
    last_response_status = 1
    match_history = []
    last_response_detail = "Fetch successful"

    while last_response_status == 1 and matches_fetched < matches_requested:
        cur_response = api.get_match_history_by_sequence_num(
            start_at_match_seq_num=last_match_id, **kwargs
        )
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
            if len(cur_response['result']['matches']) > 1:
                if not match_history:
                    # very first fetch
                    match_history.extend(cur_response['result']['matches'])
                    matches_fetched += len(cur_response['result']['matches'])
                else:
                    # 2nd fetch onwards, ignore the first common match
                    match_history.extend(cur_response['result']['matches'][1:])
                    matches_fetched += len(cur_response['result']['matches']) - 1
            else:
                break
            last_match_id = cur_response['result']['matches'][-1]['match_id']
        print("Matches fetched - #{}...".format(matches_fetched))
        wait_for_next_fetch(fetch_delay)
    print("{0}: {1}".format(last_response_status, last_response_detail))
    return {'status':last_response_status, 'statusDetail':last_response_detail,
            'matches':match_history}

DOTA2_API_KEY = "06A0619C384CFA31B4D956A805743BEF"
api.set_api_key(DOTA2_API_KEY)
#api.use_test_api()

#account_id = int(api.get_steam_id("shad0w_wa1k3r")["response"]["steamid"])

#print account_id

x = public_match_history(start_at_match_seq_num=None, matches_requested=1000, fetch_delay=1)