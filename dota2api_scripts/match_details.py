"""
Script to fetch data for given list of match ids.
"""

from __future__ import print_function
from dota2py import api
from time import sleep as wait_for_next_fetch

def match_details(match_ids=[], fetch_delay=2, debug=True, **kwargs):
    """
    Returns data for the requested match ids
    Rate limits the API requests according to `fetch_delay` (in seconds)
    Output : dict of 'match_id': {match_detail}
    """

    all_details = dict()
    times_failed = 0

    for i, match_id in enumerate(match_ids):
        if debug:
            print(i, "Trying match id", match_id)
        cur_response = api.get_match_details(match_id=match_id, **kwargs)
        if not 'match_id' in cur_response['result']:
            # unsuccessful query
            times_failed += 1
            if debug:
                print("Match id", match_id, ":", "Unsuccessful fetch / bad id")
        else:
            # successful data fetch
            all_details[match_id] = cur_response['result']
            if debug:
                print("Match id", match_id, ":", "Successful fetch")
        wait_for_next_fetch(fetch_delay)
    if debug:
        print("Matches fetched = #", len(all_details), sep="")
        print("Unsuccessful fetches - #", times_failed, sep="")
    return all_details
