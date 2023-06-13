#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""list_repo.py"""
import logging
import settings
from util.utility import init, write_file, read_file
from util.github_query import list_milestones, list_issues, create_milestones, apply_milestones

def main():
    """main"""
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler("milestones.log"),
            logging.StreamHandler()
        ])
    github_org, github_repo, github_token, operation = init()
    endpoint = f'{settings.API_ENDPOINT}/repos/{github_org}/{github_repo}'
    if operation.casefold() == settings.OPERATION_LIST:
        logging.info("List milestones")
        milestone_count = write_file(
            list_milestones(endpoint, github_token),
            settings.OUTPUT_FILE_MILESTONES)
        logging.info("Filed %s milestones (%s)",
                     milestone_count,
                     settings.OUTPUT_FILE_MILESTONES)
        logging.info("List issues/pull requests with milestones")
        issue_count = write_file(
            list_issues(endpoint, github_token),
            settings.OUTPUT_FILE_ISSUES)
        logging.info("Filed %s issues/pull requests (%s)",
                     issue_count,
                     settings.OUTPUT_FILE_ISSUES)
    elif operation.casefold() == settings.OPERATION_UPDATE:
        logging.info("Create milestones")
        milestone_data = read_file(settings.OUTPUT_FILE_MILESTONES)
        milestone_count = create_milestones(
            endpoint,
            github_token,
            milestone_data,
            settings.SEARCH_MILESTONE_BY_NUMBER)
        logging.info("Created %s milestones", milestone_count)
        logging.info("Update issues and pull requests with milestones")
        issue_data = read_file(settings.OUTPUT_FILE_ISSUES)
        issue_count = apply_milestones(
            endpoint,
            github_token,
            issue_data,
            milestone_data,
            settings.SEARCH_MILESTONE_BY_NUMBER)
        logging.info("Updated %s issues and pull requests", issue_count)

if __name__ == "__main__":
    main()
