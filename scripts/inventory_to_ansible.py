#!/usr/bin/env python3
"""
Convert `docs/configs/inventory.csv` into a simple Ansible inventory YAML.

The script produces `ansible/generated_inventory.yml` where each CSV item becomes a host
with metadata variables. Hostnames are derived from the Item field (sanitized).

Usage:
  python3 scripts/inventory_to_ansible.py
"""
import csv
import os
import re
import yaml

SRC = os.path.join(os.path.dirname(__file__), '..', 'docs', 'configs', 'inventory.csv')
OUT = os.path.join(os.path.dirname(__file__), '..', 'ansible', 'generated_inventory.yml')

def sanitize(s):
    s = s.strip().lower()
    # replace spaces and slashes with hyphen
    s = re.sub(r'[\s/]+', '-', s)
    # remove chars other than alnum, hyphen, underscore, dot
    s = re.sub(r'[^a-z0-9_.-]', '', s)
    # ensure doesn't start with digit-only
    if not s:
        s = 'host'
    return s

def main():
    if not os.path.exists(SRC):
        print(f"Source CSV not found: {SRC}")
        return 2

    hosts = {}
    groups = {}
    seen = {}

    with open(SRC, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = (row.get('Category') or '').strip() or 'unknown'
            item = (row.get('Item') or '').strip() or 'unknown'
            specs = (row.get('Specs') or '').strip()
            notes = (row.get('Status / Notes') or row.get('Status') or row.get('Notes') or '').strip()

            base = sanitize(item)
            key = base
            i = 1
            while key in seen:
                i += 1
                key = f"{base}-{i}"
            seen[key] = True

            host_entry = {
                'item': item,
                'category': category,
                'specs': specs,
                'notes': notes,
            }
            # Tags: read comma-separated tags into a list
            tag_val = (row.get('Tags') or row.get('Tag') or row.get('tags') or '').strip()
            if tag_val:
                tags = [t.strip() for t in re.split(r'[;,]|\s+', tag_val) if t.strip()]
                if tags:
                    host_entry['tags'] = tags
            # Detect common IP/address column names and set ansible_host if present
            for col in ('ansible_host', 'ansible-host', 'ip', 'address', 'host', 'hostname'):
                val = row.get(col) or row.get(col.upper()) or row.get(col.title())
                if val:
                    val = val.strip()
                    if val:
                        host_entry['ansible_host'] = val
                        break

            hosts[key] = host_entry

            # Category group (existing behavior)
            groups.setdefault(category, {})
            groups[category].setdefault('hosts', {})
            groups[category]['hosts'][key] = {}

            # Additional groups from CSV (Group, Groups, Group(s))
            group_cols = ['Group', 'Groups', 'Group(s)', 'group', 'groups', 'group(s)']
            grp_val = ''
            for gc in group_cols:
                gv = row.get(gc)
                if gv:
                    grp_val = gv.strip()
                    break
            if grp_val:
                # allow comma/semicolon/separator
                for g in re.split(r'[;,]|\s*\|\s*', grp_val):
                    g = g.strip()
                    if not g:
                        continue
                    groups.setdefault(g, {})
                    groups[g].setdefault('hosts', {})
                    groups[g]['hosts'][key] = {}

    # build YAML structure
    inv = {'all': {'hosts': {'controller': {'ansible_host': 'localhost'}}, 'children': {}}}
    # add hardware groups
    for cat, body in groups.items():
        inv['all']['children'][cat] = body

    # add host vars under all -> hosts
    for h, meta in hosts.items():
        inv['all']['hosts'][h] = meta

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        yaml.safe_dump(inv, f, sort_keys=False)

    print(f"Wrote {OUT}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
