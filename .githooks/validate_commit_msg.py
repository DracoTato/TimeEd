#!/usr/bin/env python3
import sys
import re

# Allowed commit types and modules
TYPES = {"Feat", "Refactor", "Fix", "Chore"}
MODULES = {
    "front-end",
    "routes",
    "logs",
    "forms",
    "config",
    "db",
    "utils",
    "docs",
    "messages",
    "poetry",
    "gitignore",
    "hooks",
}
DESC_LEN = 60


def main():
    commit_msg_file = sys.argv[1]
    with open(commit_msg_file, "r", encoding="utf-8") as f:
        commit_msg = f.readline().strip()

    pattern = r"^(?P<type>\w+)\((?P<module>[\w\-/]+)\): (?P<desc>.+)$"
    match = re.match(pattern, commit_msg)

    if not match:
        print("❌ Commit message format is wrong.")
        print("Expected format: Type(Module): description")
        sys.exit(1)

    type_ = match.group("type")
    module = match.group("module")
    desc = match.group("desc")

    if type_ not in TYPES:
        print(f"❌ Invalid commit type: {type_}")
        print(f"Allowed types: {', '.join(TYPES)}")
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
