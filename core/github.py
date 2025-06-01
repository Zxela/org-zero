# core/github.py
"""
GitHub integration utilities for OAuth/App authentication and committing code.
"""
import os
import requests
from core.config import get_settings

settings = get_settings()

GITHUB_API_URL = "https://api.github.com"


def get_github_headers():
    """Return headers for GitHub API requests using OAuth or App token."""
    token = settings.GITHUB_ACCESS_TOKEN
    if not token:
        raise ValueError("GITHUB_ACCESS_TOKEN is not set in environment/config.")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }


def create_commit(file_path: str, content: str, commit_message: str):
    """
    Commit a file to the configured GitHub repository using the REST API.
    This is a minimal example and does not handle all edge cases.
    """
    owner = settings.GITHUB_REPO_OWNER
    repo = settings.GITHUB_REPO_NAME
    if not owner or not repo:
        raise ValueError("GITHUB_REPO_OWNER and GITHUB_REPO_NAME must be set.")

    # Get the SHA of the latest commit on the default branch
    branch = "main"
    ref_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/refs/heads/{branch}"
    ref_resp = requests.get(ref_url, headers=get_github_headers())
    ref_resp.raise_for_status()
    latest_commit_sha = ref_resp.json()["object"]["sha"]

    # Get the tree SHA
    commit_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/commits/{latest_commit_sha}"
    commit_resp = requests.get(commit_url, headers=get_github_headers())
    commit_resp.raise_for_status()
    tree_sha = commit_resp.json()["tree"]["sha"]

    # Create a new blob (file content)
    blob_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/blobs"
    blob_resp = requests.post(blob_url, headers=get_github_headers(), json={
        "content": content,
        "encoding": "utf-8"
    })
    blob_resp.raise_for_status()
    blob_sha = blob_resp.json()["sha"]

    # Create a new tree
    tree_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/trees"
    tree_resp = requests.post(tree_url, headers=get_github_headers(), json={
        "base_tree": tree_sha,
        "tree": [{
            "path": file_path,
            "mode": "100644",
            "type": "blob",
            "sha": blob_sha
        }]
    })
    tree_resp.raise_for_status()
    new_tree_sha = tree_resp.json()["sha"]

    # Create a new commit
    new_commit_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/commits"
    new_commit_resp = requests.post(new_commit_url, headers=get_github_headers(), json={
        "message": commit_message,
        "tree": new_tree_sha,
        "parents": [latest_commit_sha]
    })
    new_commit_resp.raise_for_status()
    new_commit_sha = new_commit_resp.json()["sha"]

    # Update the reference to point to the new commit
    update_ref_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/refs/heads/{branch}"
    update_ref_resp = requests.patch(update_ref_url, headers=get_github_headers(), json={
        "sha": new_commit_sha
    })
    update_ref_resp.raise_for_status()
    return update_ref_resp.json()

# Example usage (uncomment to use):
# create_commit("test.txt", "Hello from Org-Zero!", "Add test.txt via API")
