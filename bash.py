#!/usr/bin/python
# encoding: utf-8

import sys
import os
import json

from workflow import Workflow
import helpers

log = None
CONFIG = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bash.json')


def keys_for_search(item):
    host = item['part'].encode('ascii', 'ignore').decode('utf-8')
    ip = item['cmd'].encode('ascii', 'ignore').decode('utf-8')
    remark = item['comment'].encode('ascii', 'ignore').decode('utf-8')
    return '{} {} {}'.format(host, ip, remark)


def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`

    # Your imports here if you want to catch import errors
    # import somemodule
    # import anothermodule

    # Get args from Workflow as normalized Unicode
    args = wf.args

    # Set `query` if a value was passed (it may be an empty string)
    if len(wf.args):
        query = wf.args[0]

    with open(CONFIG) as json_data:
        json_list = json.load(json_data)

    items = json_list  # Load data from blah

    if query:  # Only call `filter()` if there's a `query`
        items = wf.filter(query, json_list, keys_for_search)

    # Show error if there are no results. Otherwise, Alfred will show
    # its fallback searches (i.e. "Search Google for 'XYZ'")
    if not items:
        wf.add_item(title='Command not found!',
                    icon=helpers.get_icon(wf, 'info'))

    # Generate list of results. If `items` is an empty list,
    # nothing will happen

    for item in items:
        summary = u'' + item['comment']
        full_text = u'' + item['cmd'] + ' ' + item['comment']

        wf.add_item(title=item['cmd'],
                    subtitle=summary,
                    # modifier_subtitles={
                    #     u'shift': item['cmd'],
                    #     # u'fn': u'Subtext when fn is pressed',
                    #     u'ctrl': item['cmd'],
                    #     u'alt': item['cmd'],
                    #     u'cmd': item['cmd']
                    # },
                    autocomplete=item['cmd'],
                    arg=item['cmd'],
                    copytext=item['cmd'],
                    valid=True,
                    icon=helpers.get_icon(wf, 'bash'))
# Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable for convenience
    log = wf.logger
    sys.exit(wf.run(main))
