"""
Script to fetch data for given list of match ids.
"""

from __future__ import print_function
from dota2py import api
from time import sleep as wait_for_next_fetch

def match_details(match_ids=[], fetch_delay=0.2, **kwargs):
    """
    Returns data for the requested match ids
    Rate limits the API requests according to `fetch_delay` (in seconds)
    Output : dict of 'match_id': {match_detail}
    """

    all_details = dict()
    times_failed = 0

    for match_id in match_ids:
        cur_response = api.get_match_details(match_id=match_id, **kwargs)
        if not 'match_id' in cur_response['result']:
            # unsuccessful query
            times_failed += 1
            if not 'statusDetail' in cur_response['result']:
                print("Match id", match_id, ": Unknown error")
            else:
                print("Match id", match_id, ":", cur_response['result']['statusDetail'])
        else:
            # successful data fetch
            all_details[match_id] = cur_response['result']
        wait_for_next_fetch(fetch_delay)
    print("Matches fetched = #", len(all_details), sep="")
    print("Unsuccessful fetches - #", times_failed, sep="")
    return all_details
