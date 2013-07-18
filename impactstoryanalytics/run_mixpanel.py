#!/usr/bin/env python

import os
import analytics
import logging
from impactstoryanalytics.lib import mixpanel_export
import imaplib
import re
import json

logger = logging.getLogger("analytics.run_mixpanel")



##############################################################################
#
#    functions
#
##############################################################################



def check_and_report_funnel(api, funnel, funnel_params):
    logger.info("Getting funnel data for " + funnel["name"])

    funnel_params["funnel_id"] = funnel["funnel_id"]
    funnel_data = api.request(['funnels'], funnel_params)

    print json.dumps(funnel_data, indent=4)

    logger.info("found data")

    for date in funnel_data["data"]:
        analytics.track(user_id="mixpanel", 
            event='Mixpanel funnel data', 
            properties={
                "funnel_name": funnel["name"], 
                "funnel_id" : funnel["funnel_id"],
                "data_date" : date,
                "step_data": funnel_data["data"][date]["steps"]
                })


def get_funnels(api):
    funnels = api.request(['funnels', 'list'], {})
    return funnels



##############################################################################
#
#    script
#
###############################################################################

# comments on params are from https://mixpanel.com/docs/api-documentation/data-export-api#funnels-list
# only currently-interesting ones are included here
funnel_params = {
    # The first date in yyyy-mm-dd format from which a user can begin the first step in the funnel. This date is inclusive.
    "from_date": "2013-07-17"  # first date we started getting data

    # The number of days each user has to complete the funnel, starting from the time they 
    # triggered the first step in the funnel. May not be greater than 60 days. 
    # Note that we will query for events past the end of to_date to look for funnel completions.
    #The default value is 14.
    ,"length": 30

    # The number of days you want your results bucketed into. The default value is 1
    ,"interval": 7
}

analytics.identify(user_id="mixpanel")

api = mixpanel_export.Mixpanel(
    api_key = os.getenv("MIXPANEL_API_KEY"), 
    api_secret = os.getenv("MIXPANEL_API_SECRET")
)

funnels = get_funnels(api)

for funnel in funnels:
    check_and_report_funnel(api, funnel, funnel_params)


analytics.flush(async=False)  # make sure all the data gets sent to segment.io



# https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count_unique?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Loaded%20own%20profile&filters=%5B%7B%22property_name%22%3A%22keen.timestamp%22%2C%22operator%22%3A%22lt%22%2C%22property_value%22%3A%222013%2F07%2F17%22%7D%2C%7B%22property_name%22%3A%22keen.timestamp%22%2C%22operator%22%3A%22gt%22%2C%22property_value%22%3A%222013%2F06%2F17%22%7D%5D&timezone=-25200&target_property=user.userId
# https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk

