#!/usr/bin/env python3
import sys
import re

# Allowed commit ACTIONS and modules
ACTIONS = {"Feat", "Refactor", "Fix", "Chore"}
MODULES = {
    "frontend",
    "backend",
    "db",
    "tests",
    "infra",
    "docs",
}
DESC_LEN = 60


def main():
    commit_msg_file = sys.argv[1]
    with open(commit_msg_file, "r", encoding="utf-8") as f:
        commit_msg = f.readline().strip()

    pattern = r"^(?P<action>\w+)\((?P<module>[\w\-/]+)\): (?P<desc>.+)$"
    match = re.match(pattern, commit_msg)

    if not match:
        print("❌ Commit message format is wrong.")
        print("Expected format: Action(Module): description")
        sys.exit(1)

    action = match.group("action")
    module = match.group("module")
    desc = match.group("desc")

    if action not in ACTIONS:
        print(f"❌ Invalid commit action: {action}")
        print(f"Allowed ACTIONS: {', '.join(ACTIONS)}")
        sys.exit(1)

    if module not in MODULES:
        print(f"❌ Invalid module: {module}")
        print(f"Allowed modules: {', '.join(MODULES)}")
        sys.exit(1)

    if len(desc) > DESC_LEN:
        print(f"❌ Description too long ({len(desc)} chars). Max {DESC_LEN} allowed.")
        sys.exit(1)

    print("✅ Commit message looks good! Good job ^^")


if __name__ == "__main__":
    main()
