import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ORG_ID = "Dy9l5da3BlsUX4ZBnpxR"
BASE = "https://api.gitbook.com/v1"
REPO = "arivo-ikb-demo-site-20260702"
REPO_OWNER = "gitbook-demo-sites"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO}.git"


SPACE = {
    "key": "POLICY",
    "folder": "policy-knowledge-base",
    "title": "Policy Knowledge Base",
    "emoji": "1f4d8",
    "icon": "file-shield",
    "path": "policy-knowledge-base",
    "description": "Internal policy documentation, approvals, and servicing workflows.",
}


def api(method: str, path: str, body=None, expected=(200, 201, 204)):
    token = os.environ["GITBOOK_TOKEN"]
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            text = resp.read().decode()
            payload = json.loads(text) if text else None
            if resp.status not in expected:
                raise RuntimeError(f"{method} {path} returned {resp.status}: {text}")
            return resp.status, payload
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"{method} {path} returned {exc.code}: {detail}") from exc


def git_commit_push(message: str):
    subprocess.run(["git", "add", "."], cwd=ROOT, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", message], cwd=ROOT, check=True)
    subprocess.run(["git", "push"], cwd=ROOT, check=True)


def main():
    _, site = api(
        "POST",
        f"/orgs/{ORG_ID}/sites",
        {
            "type": "ultimate",
            "title": "Arivo IKB Demo",
            "visibility": "share-link",
        },
    )
    site_id = site["id"]
    api(
        "PATCH",
        f"/orgs/{ORG_ID}/sites/{site_id}",
        {
            "title": "Arivo IKB Demo",
            "visibility": "share-link",
            "basename": "arivo-ikb-demo",
        },
    )

    _, space = api(
        "POST",
        f"/orgs/{ORG_ID}/spaces",
        {"title": SPACE["title"], "emoji": SPACE["emoji"], "empty": True, "editMode": "live"},
    )
    space_id = space["id"]

    _, section = api(
        "POST",
        f"/orgs/{ORG_ID}/sites/{site_id}/sections",
        {"spaceId": space_id, "title": SPACE["title"], "icon": SPACE["icon"], "draft": False},
    )
    section_id = section["id"]
    site_space_id = section["siteSpaces"][0]["id"]
    api(
        "PATCH",
        f"/orgs/{ORG_ID}/sites/{site_id}/sections/{section_id}",
        {
            "path": SPACE["path"],
            "description": SPACE["description"],
            "draft": False,
            "defaultSiteSpace": site_space_id,
        },
    )
    api(
        "PATCH",
        f"/orgs/{ORG_ID}/sites/{site_id}",
        {"defaultSiteSection": section_id, "defaultSiteSpace": site_space_id},
    )

    created = {
        "org": ORG_ID,
        "site": site_id,
        "space": space_id,
        "section": section_id,
        "site_space": site_space_id,
        "site_object": site,
    }
    (ROOT / "gitbook-created.json").write_text(json.dumps(created, indent=2) + "\n", encoding="utf-8")
    git_commit_push("Add Arivo IKB demo content")

    status, _ = api(
        "POST",
        f"/spaces/{space_id}/git/import",
        {
            "url": REPO_URL,
            "ref": "refs/heads/main",
            "repoProjectDirectory": SPACE["folder"],
            "repoTreeURL": f"https://github.com/{REPO_OWNER}/{REPO}/tree/main",
            "repoCommitURL": f"https://github.com/{REPO_OWNER}/{REPO}/commit",
            "force": True,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
        expected=(204,),
    )
    (ROOT / "gitbook-import-results.json").write_text(
        json.dumps({"status": status, "space": space_id, "folder": SPACE["folder"]}, indent=2) + "\n",
        encoding="utf-8",
    )

    logo_light = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/arivo-logo-color.png"
    logo_dark = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/arivo-logo-white.png"
    brandmark = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO}/main/assets/arivou-brandmark-color.png"
    customization = {
        "title": "Arivo IKB Demo",
        "localizedTitle": {},
        "internationalization": {"locale": "en"},
        "styling": {
            "theme": "clean",
            "primaryColor": {"light": "#F68D21", "dark": "#F68D21"},
            "infoColor": {"light": "#1976D2", "dark": "#E2E8F0"},
            "successColor": {"light": "#388E3C", "dark": "#388E3C"},
            "warningColor": {"light": "#F68D21", "dark": "#FFCC80"},
            "dangerColor": {"light": "#D32F2F", "dark": "#D32F2F"},
            "tint": {"color": {"light": "#F1F5F9", "dark": "#151B26"}},
            "corners": "rounded",
            "depth": "flat",
            "links": "accent",
            "font": "Inter",
            "monospaceFont": "IBMPlexMono",
            "icons": "regular",
            "background": "plain",
            "sidebar": {"background": "filled", "list": "line"},
            "codeTheme": {
                "default": {"light": "default-light", "dark": "default-dark"},
                "openapi": {"light": "default-light", "dark": "default-dark"},
            },
            "search": "prominent",
        },
        "favicon": {"icon": {"light": brandmark, "dark": brandmark}},
        "header": {
            "preset": "default",
            "logo": {"light": logo_light, "dark": logo_dark},
            "links": [
                {"title": "Arivo", "to": {"kind": "url", "url": "https://arivo.com/"}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Arivo One", "to": {"kind": "url", "url": "https://one.arivo.com"}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Policy library", "to": {"kind": "space", "space": space_id}, "style": "button-secondary", "links": [], "localizedTitle": {}},
            ],
        },
        "footer": {
            "logo": {"light": logo_light, "dark": logo_dark},
            "groups": [
                {
                    "title": "Demo paths",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Policy Knowledge Base", "to": {"kind": "space", "space": space_id}, "localizedTitle": {}},
                        {"title": "Policy review workflow", "to": {"kind": "url", "url": f"https://app.gitbook.com/s/{space_id}/workflows/policy-review-workflow"}, "localizedTitle": {}},
                    ],
                },
                {
                    "title": "Sources",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Source repo", "to": {"kind": "url", "url": f"https://github.com/{REPO_OWNER}/{REPO}"}, "localizedTitle": {}},
                        {"title": "Arivo website", "to": {"kind": "url", "url": "https://arivo.com/"}, "localizedTitle": {}},
                    ],
                },
            ],
            "copyright": "Arivo IKB Demo - built for GitBook review.",
        },
        "themes": {"default": "light", "toggeable": True},
        "pdf": {"enabled": True},
        "feedback": {"enabled": True},
        "ai": {
            "mode": "assistant",
            "suggestions": [
                "Which Account Servicing policies need review?",
                "What does the payment waterfall say?",
                "How should I update customer communication preferences?",
                "Which policies mention Norman LMS?",
                "What approval metadata should every policy include?",
            ],
        },
        "advancedCustomization": {"enabled": True},
        "trademark": {"enabled": True},
        "externalLinks": {"target": "self"},
        "pagination": {"enabled": True},
        "pageActions": {"externalAI": True, "markdown": True, "mcp": True, "items": ["assistant", "markdown", "external-ai", "mcp", "pdf"]},
        "git": {"showEditLink": False},
        "privacyPolicy": {"url": "https://arivo.com/privacy-policy"},
        "socialPreview": {"url": brandmark},
        "socialAccounts": [],
        "insights": {"trackingCookie": True},
    }
    _, customized = api("PUT", f"/orgs/{ORG_ID}/sites/{site_id}/customization", customization)
    (ROOT / "gitbook-customization-result.json").write_text(json.dumps(customized, indent=2) + "\n", encoding="utf-8")

    publish_status, publish = api("POST", f"/orgs/{ORG_ID}/sites/{site_id}/publish")
    share_status, share = api("POST", f"/orgs/{ORG_ID}/sites/{site_id}/share-links", {"name": "Arivo IKB demo review"})
    final = {
        "publish_status": publish_status,
        "publish": publish,
        "share_status": share_status,
        "share": share,
        "published_url": share["urls"]["published"],
        "app_url": publish["urls"]["app"],
        "preview_url": publish["urls"]["preview"],
        "repo": f"https://github.com/{REPO_OWNER}/{REPO}",
    }
    (ROOT / "gitbook-publish-share.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    git_commit_push("Add Arivo GitBook publish artifacts")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()

