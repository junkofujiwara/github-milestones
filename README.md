## GitHub milestone maintenance script

### Prerequisites
Python 3
`pip install -r requirements.txt`

### Usage: List Milestones
Purpose: Milestones information within a specified organization/repository.<br/>
How to Use: Execute following command-line with your organization name, repository name, and token (Personal Access Token). The list of milestone information is written to a csv file `milestones.csv` and list of issues / pull requests with milestones is written to a csv file `issues.csv`. 

- Command-line: 
`python3 milestone.py list -o <org-name> -r <repository> -t <token>`
- Output: 
`milestones.csv` and `issues.csv`
- Milestone Output Format: `<number>,<title>,<state>,<description>,<open_issues>,<closed_issues>,<due_on>`
- Issue/PR Output Format: `<issue_pr_number>,<milestone_number>,<title><issue_or_pullrequests>`
- Log File: 
`milestones.log`

### Usage: Create Milestones and apply Milestones in Issue and Pull Requests
Purpose: Create milestones and apply milestone in issue and pull reqeusts.<br/>
How to Use: Execute following command-line with your target organization name, repository name, and token (Personal Access Token). Processes milestone creations from the files `milestones.csv`. Then applies milestones for issues and pull requests from `issues.csv`.<br/>
Note: If SEARCH_MILESTONE_BY_NUMBER is True, script will use milestone number to search for existing milestones. If SEARCH_MILESTONE_BY_NUMBER is False, script will use milestone title to search for existing milestones. This script will not create issues or pull requests. It will only update existing issues and pull requests.

- Command-line
`python3 milestone.py update -o <org-name> -r <repository> -t <token>`
- Input
`milestone.csv`, `issues.csv`
- Log File: 
`milestones.log`


### Additional Notes
- The name of the output CSV files can be changed in settings.py
- API endpoint can be changed in settings.py for GitHub Enterprise Server
