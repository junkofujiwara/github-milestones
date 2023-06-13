#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""github_query.py"""
import logging
import requests

def list_milestones(endpoint, token):
    """list milestones"""
    data = []
    next_page = True
    logging.info("Executing list milestones query")
    url = f'{endpoint}/milestones?state=all&per_page=100'
    while next_page:
        response = run_get(url, token)
        result = response.json()
        for item in result:
            data.append([item["number"],
                item["title"],
                item["state"],
                item["description"],
                item["open_issues"],
                item["closed_issues"],
                item["due_on"]])
        next_page = 'next' in response.links.keys()
        if next_page:
            url = response.links['next']['url']
    return data

def get_milestone(endpoint, token, number, exist_check=False):
    """get milestone"""
    logging.info("Executing get milestone query")
    url = f'{endpoint}/milestones/{number}'
    response = run_get(url, token, exist_check=exist_check)
    if response is not None:
        result = response.json()
        return result["number"]
    return None

def list_issues(endpoint, token):
    """list issues or pull requests with milestones"""
    data = []
    next_page = True
    logging.info("Executing list issues/pull requests with milestone query")
    url = f'{endpoint}/issues?milestone=*&per_page=100'
    while next_page:
        response = run_get(url, token)
        result = response.json()
        for item in result:
            issue_pr = "Issue"
            if "pull_request" in item.keys():
                issue_pr = "PR"
            data.append([item["number"],
                item["milestone"]["number"],
                item["title"],
                issue_pr])
        next_page = 'next' in response.links.keys()
        if next_page:
            url = response.links['next']['url']
    return data

def create_milestones(endpoint, token, milestones, search_by_number=False):
    """create milestones"""
    counter = 0
    for milestone in milestones:
        title = milestone[1] # title
        state = milestone[2] # state
        description = milestone[3] # description
        due_on = milestone[6] # due_on
        if search_by_number:
            logging.info("Search milestone by number. number=%s", milestone[0])
            milestone_id = get_milestone(endpoint, token, milestone[0], exist_check=True)
            if milestone_id is not None:
                logging.info("Skip creating milestone milestone=%s", title)
                continue
        logging.info("Create milestone title=%s", title)
        url = f'{endpoint}/milestones'
        value = {'title' : title, 'state' : state}
        if len(due_on) > 0:
            value.update({'due_on' : due_on})
        if len(description) > 0:
            value.update({'description' : description})
        result = run_post(url, value, token)
        if result is not None:
            counter += 1
            logging.info("Created milestone milestone=%s", milestone[0])
    return counter

def apply_milestones(endpoint, token, issues, milestone, search_by_number=False):
    """apply milestone to issues or pull requests"""
    counter = 0
    if search_by_number is False:
        current_milestone = list_milestones(endpoint, token)
    for issue in issues:
        issue_number = issue[0] # issue number
        milestone_number = issue[1] # milestone number
        if search_by_number is False:
            milestone_number = adjust_milestone_number(milestone_number,
                                                       milestone,
                                                       current_milestone)
        url = f'{endpoint}/issues/{issue_number}'
        logging.info("Apply milestone to issue/PR. issue=%s, milestone=%s",
                     issue_number, milestone_number)
        value = {'milestone' : milestone_number}
        result = run_patch(url, value, token)
        if result is not None:
            counter += 1
            logging.info("Applied milestone to issue/PR. issue=%s, milestone=%s",
                    issue_number, milestone_number)
    return counter

def adjust_milestone_number(milestone_number, milestone, current_milestone):
    """Adjust milestone number. Search milestone by title and return number."""
    search_title = None
    search_number = None
    for item in milestone:
        number = item[0] # number
        title = item[1] # title
        if milestone_number == number:
            search_title = title
            break
    for current_item in current_milestone:
        current_number = current_item[0] # number
        current_title = current_item[1] # title
        if search_title == current_title:
            search_number = current_number
            break
    logging.info("Adjust milestone number. original=%s, current=%s",
                 milestone_number,
                 search_number)
    return search_number

def run_get(url, token, throw_exception=False, exist_check=False):
    """run get (REST)"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.get(url,
          headers=headers)
        if exist_check and request.status_code == 404:
            return None
        request.raise_for_status()
        return request
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Url: %s", url)
        if throw_exception:
            raise SystemExit(exception) from exception
    return None

def run_post(url, value, token, throw_exception=False):
    """run post (REST)"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.post(url,
          json=value,
          headers=headers)
        request.raise_for_status()
        return request.json()
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Url: %s, Value: %s", url, value)
        if throw_exception:
            raise SystemExit(exception) from exception
    return None

def run_patch(url, value, token, throw_exception=False):
    """run patch (REST)"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.patch(url,
          json=value,
          headers=headers)
        request.raise_for_status()
        return request.json()
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Url: %s, Value: %s", url, value)
        if throw_exception:
            raise SystemExit(exception) from exception
    return None
