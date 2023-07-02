"""A simple script that collects issues from a repo and generate a markdown
file (report.md).

A personal access token will need to be configured. Also the repo name will
need to be provided. Add these in `config.py`.

Requirements: pygithub.

`pip install --user pygithub`
"""
from github import Github

import config

REPO = config.REPO
github = Github(config.TOKEN)

SEVERITY_LABELS = ['Critical', 'High', 'Medium', 'Low', 'Gas', 'Informational']

issue_dict : dict[str, list[str]] = {}

for issue in github.get_repo(REPO).get_issues():
    if issue.state == 'open' and issue.pull_request is None:
        # filter issue labels for only severity labels
        severity_labels_in_issue = [label.name for label in issue.labels if label.name in SEVERITY_LABELS]

        assert len(severity_labels_in_issue) == 1, f"Issue {issue.html_url} has more than one (or no) severity label."
        label = issue.labels[0].name
        if label not in issue_dict:
           issue_dict[label] = []
        issue_dict[label].append(f"### $*^@^!. {label} - {issue.title}\n\n{issue.body}\n\n")

with open("report.md", "w") as report:
    for label in SEVERITY_LABELS:
        num = 1
        title = f"{label} Findings"
        if label == "Gas":
            title = "Gas Saving Findings"
        report.write(f"## {title}\n\n")
        if label in issue_dict.keys():
            for content in issue_dict[label]:
                replaced = content.replace("\r\n", "\n")
                replaced = replaced.replace("$*^@^!", f"{num}")
                report.write(replaced)
                num += 1
    report.write(f"## Final remarks\n\nTODO")
