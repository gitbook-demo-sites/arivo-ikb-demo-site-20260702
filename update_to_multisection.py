import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ORG_ID = "Dy9l5da3BlsUX4ZBnpxR"
SITE_ID = "site_g8qEK"
EXISTING_POLICY_SPACE = "tnQvXEk80OYCwPfvuklz"
EXISTING_POLICY_SECTION = "sitesc_US0Wl"
BASE = "https://api.gitbook.com/v1"
REPO = "arivo-ikb-demo-site-20260702"
REPO_OWNER = "gitbook-demo-sites"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO}.git"


SPACES = [
    {
        "key": "HOME",
        "folder": "home",
        "title": "Home",
        "emoji": "1f3e0",
        "icon": "house",
        "path": "home",
        "description": "Company context, search-first entry point, and demo navigation.",
    },
    {
        "key": "POLICIES",
        "folder": "policies",
        "title": "Policies",
        "emoji": "1f4d8",
        "icon": "file-shield",
        "path": "policies",
        "description": "Imported Account Servicing policy content and governance workflow.",
        "space_id": EXISTING_POLICY_SPACE,
        "section_id": EXISTING_POLICY_SECTION,
    },
    {
        "key": "CHANGELOG",
        "folder": "changelog",
        "title": "Changelog",
        "emoji": "1f550",
        "icon": "clock-rotate-left",
        "path": "changelog",
        "description": "Sample update history for policy and knowledge base changes.",
    },
]


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


def replace_sentinels(space_ids):
    replacements = {
        "XSPACE_HOME": space_ids["HOME"],
        "XSPACE_POLICIES": space_ids["POLICIES"],
        "XSPACE_CHANGELOG": space_ids["CHANGELOG"],
    }
    for path in [ROOT / "home"]:
        for md in path.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            original = text
            for old, new in replacements.items():
                text = text.replace(old, new)
            if text != original:
                md.write_text(text, encoding="utf-8")


def main():
    created = {"site": SITE_ID, "spaces": {}, "sections": {}, "site_spaces": {}}

    for item in SPACES:
        if "space_id" in item:
            space_id = item["space_id"]
            section_id = item["section_id"]
            _, section = api(
                "PATCH",
                f"/orgs/{ORG_ID}/sites/{SITE_ID}/sections/{section_id}",
                {"title": item["title"], "path": item["path"], "description": item["description"], "draft": False},
            )
            site_space_id = section.get("defaultSiteSpace") or section.get("siteSpaces", [{}])[0].get("id")
        else:
            _, space = api(
                "POST",
                f"/orgs/{ORG_ID}/spaces",
                {"title": item["title"], "emoji": item["emoji"], "empty": True, "editMode": "live"},
            )
            space_id = space["id"]
            _, section = api(
                "POST",
                f"/orgs/{ORG_ID}/sites/{SITE_ID}/sections",
                {"spaceId": space_id, "title": item["title"], "icon": item["icon"], "draft": False},
            )
            section_id = section["id"]
            site_space_id = section["siteSpaces"][0]["id"]
            api(
                "PATCH",
                f"/orgs/{ORG_ID}/sites/{SITE_ID}/sections/{section_id}",
                {"path": item["path"], "description": item["description"], "draft": False, "defaultSiteSpace": site_space_id},
            )
        created["spaces"][item["key"]] = space_id
        created["sections"][item["key"]] = section_id
        created["site_spaces"][item["key"]] = site_space_id

    api(
        "PATCH",
        f"/orgs/{ORG_ID}/sites/{SITE_ID}",
        {
            "title": "Arivo IKB Demo",
            "visibility": "share-link",
            "basename": "arivo-ikb-demo",
            "defaultSiteSection": created["sections"]["HOME"],
            "defaultSiteSpace": created["site_spaces"]["HOME"],
        },
    )

    replace_sentinels(created["spaces"])
    (ROOT / "gitbook-multisection-created.json").write_text(json.dumps(created, indent=2) + "\n", encoding="utf-8")
    git_commit_push("Restructure Arivo demo into multi-section site")

    imports = {}
    for item in SPACES:
        status, _ = api(
            "POST",
            f"/spaces/{created['spaces'][item['key']]}/git/import",
            {
                "url": REPO_URL,
                "ref": "refs/heads/main",
                "repoProjectDirectory": item["folder"],
                "repoTreeURL": f"https://github.com/{REPO_OWNER}/{REPO}/tree/main",
                "repoCommitURL": f"https://github.com/{REPO_OWNER}/{REPO}/commit",
                "force": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            expected=(204,),
        )
        imports[item["key"]] = {"status": status, "space": created["spaces"][item["key"]], "folder": item["folder"]}
    (ROOT / "gitbook-multisection-imports.json").write_text(json.dumps(imports, indent=2) + "\n", encoding="utf-8")

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
                {"title": "Home", "to": {"kind": "space", "space": created["spaces"]["HOME"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Policies", "to": {"kind": "space", "space": created["spaces"]["POLICIES"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Changelog", "to": {"kind": "space", "space": created["spaces"]["CHANGELOG"]}, "style": "link", "links": [], "localizedTitle": {}},
                {"title": "Arivo", "to": {"kind": "url", "url": "https://arivo.com/"}, "style": "button-secondary", "links": [], "localizedTitle": {}},
            ],
        },
        "footer": {
            "logo": {"light": logo_light, "dark": logo_dark},
            "groups": [
                {
                    "title": "Sections",
                    "localizedTitle": {},
                    "links": [
                        {"title": "Home", "to": {"kind": "space", "space": created["spaces"]["HOME"]}, "localizedTitle": {}},
                        {"title": "Policies", "to": {"kind": "space", "space": created["spaces"]["POLICIES"]}, "localizedTitle": {}},
                        {"title": "Changelog", "to": {"kind": "space", "space": created["spaces"]["CHANGELOG"]}, "localizedTitle": {}},
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
                "Search the Account Servicing policy",
                "What changed in the latest policy update?",
                "How does the payment waterfall work?",
                "Which customer communication rules are compliance-sensitive?",
                "Which policies are due for review?",
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
    _, customized = api("PUT", f"/orgs/{ORG_ID}/sites/{SITE_ID}/customization", customization)
    (ROOT / "gitbook-multisection-customization.json").write_text(json.dumps(customized, indent=2) + "\n", encoding="utf-8")

    publish_status, publish = api("POST", f"/orgs/{ORG_ID}/sites/{SITE_ID}/publish")
    final = {
        "publish_status": publish_status,
        "publish": publish,
        "published_url": "https://arivo.gitbook.io/arivo-ikb-demo/wtXQsjhPIRhxUvQ3k7Tv/",
        "app_url": publish["urls"]["app"],
        "preview_url": publish["urls"]["preview"],
        "repo": f"https://github.com/{REPO_OWNER}/{REPO}",
    }
    (ROOT / "gitbook-multisection-publish.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    git_commit_push("Publish Arivo multi-section demo")
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()

