Ansible skeleton for d2lab homelab.

This folder contains a minimal inventory and a skeleton `site.yml` to be expanded.

Usage (example):

```bash
ansible-playbook -i ansible/inventory.yml ansible/site.yml --check
```

Replace hosts in `ansible/inventory.yml` with your real host entries or generate an inventory from `docs/configs/inventory.csv`.


Generate inventory
------------------
Run the helper to convert the CSV into an Ansible inventory YAML (or let the wrapper generate it automatically):

```bash
python3 scripts/inventory_to_ansible.py
# output: ansible/generated_inventory.yml
```

Wrapper inventory
-----------------
`ansible/inventory.yml` is now a small dynamic-inventory wrapper. You can point Ansible at it directly and it will generate the CSV-derived inventory when needed:

```bash
ansible-playbook -i ansible/inventory.yml ansible/site.yml --check
```

Optional CSV columns
--------------------
If your CSV contains an IP or address column (common names: `ansible_host`, `ip`, `address`, `host`, `hostname`), the generator will populate `ansible_host` for that host in the generated inventory so you can run Ansible directly against the address.

Groups & Tags
-------------
The generator now recognizes optional CSV columns for grouping and tagging:

- `Group`, `Groups`, or `Group(s)`: comma/semicolon/pipe-separated group names. Each name becomes an Ansible group and the host will be a member.
- `Tags` or `Tag`: comma/semicolon/space-separated tags. Tags are emitted as a `tags` list under each host's vars in `ansible/generated_inventory.yml`.

Example CSV rows:

```
Category,Item,Specs,Status / Notes,Groups,Tags,ansible_host
Server,main-media,16C/32G,Deployed,MHV;media,plex,10.10.20.11
```

Regenerate the inventory after editing the CSV:

```bash
python3 scripts/inventory_to_ansible.py
```



