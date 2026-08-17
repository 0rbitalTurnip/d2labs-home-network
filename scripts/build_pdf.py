#!/usr/bin/env python3
"""
Build the d2lab Network Architecture PDF overview.
Vector-rendered with ReportLab — fully embedded fonts, hyperlinks, and no raster images.
"""
import os
import urllib.request
import argparse
from reportlab.lib.pagesizes import landscape, A3, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Polygon, Group, Circle, Ellipse
)

# Default to repo-relative paths; allow override via CLI `--out` (dir or file)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
parser = argparse.ArgumentParser(description="Build d2lab network overview PDF")
parser.add_argument("--out", "-o", help="Output directory or PDF file path (overrides default)", default=None)
args = parser.parse_args()
if args.out:
    out_arg = os.path.abspath(args.out)
    if os.path.isdir(out_arg):
        OUT_DIR = out_arg
    else:
        # treat as file path — use its parent directory as OUT_DIR
        OUT_DIR = os.path.dirname(out_arg) or BASE_DIR
else:
    OUT_DIR = BASE_DIR
PDF_PATH = os.path.join(OUT_DIR, "diagrams", "d2lab-network-overview.pdf")
FONTS_DIR = os.path.join(BASE_DIR, ".cache", "d2lab_fonts")
os.makedirs(FONTS_DIR, exist_ok=True)

# ---------- Fonts (DM Sans + JetBrains Mono) ----------
FONT_URLS = {
    "DMSans-Regular.ttf":   "https://github.com/googlefonts/dm-fonts/raw/main/Sans/Exports/ttf/DMSans-Regular.ttf",
    "DMSans-Medium.ttf":    "https://github.com/googlefonts/dm-fonts/raw/main/Sans/Exports/ttf/DMSans-Medium.ttf",
    "DMSans-Bold.ttf":      "https://github.com/googlefonts/dm-fonts/raw/main/Sans/Exports/ttf/DMSans-Bold.ttf",
    "JetBrainsMono-Regular.ttf": "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Regular.ttf",
    "JetBrainsMono-Bold.ttf":    "https://github.com/JetBrains/JetBrainsMono/raw/master/fonts/ttf/JetBrainsMono-Bold.ttf",
}
for name, url in FONT_URLS.items():
    p = os.path.join(FONTS_DIR, name)
    if not os.path.exists(p):
        try:
            urllib.request.urlretrieve(url, p)
        except Exception as e:
            print(f"Font fetch failed for {name}: {e}")

# Built-in fonts only — keep it simple, no external font fetches needed.
BODY = "Helvetica"; HEAD = "Helvetica-Bold"; MONO = "Courier"; MONOB = "Courier-Bold"

# ---------- Palette (Nexus light) ----------
BG       = colors.HexColor("#F7F6F2")
SURFACE  = colors.HexColor("#F9F8F5")
BORDER   = colors.HexColor("#D4D1CA")
TEXT     = colors.HexColor("#28251D")
MUTED    = colors.HexColor("#7A7974")
PRIMARY  = colors.HexColor("#01696F")
WAN      = colors.HexColor("#A12C7B")
LAN10G   = colors.HexColor("#01696F")
MGMT     = colors.HexColor("#006494")
IOT      = colors.HexColor("#964219")
GUEST    = colors.HexColor("#7A39BB")
TEST     = colors.HexColor("#437A22")
TS       = colors.HexColor("#D19900")
DARK     = colors.HexColor("#1B474D")
ACCENT2  = colors.HexColor("#A84B2F")
NUC_BLUE = colors.HexColor("#006494")
NAS_BR   = colors.HexColor("#6E522B")
MEDIA    = colors.HexColor("#944454")

# ============================================================
#  TOPOLOGY DIAGRAM (vector, 1 page, A3 landscape)
# ============================================================
def topology_drawing(width, height):
    d = Drawing(width, height)
    # Background
    d.add(Rect(0, 0, width, height, fillColor=BG, strokeColor=None))

    def box(x, y, w, h, fill, stroke=None, radius=8):
        r = Rect(x, y, w, h, fillColor=fill, strokeColor=stroke or fill, strokeWidth=1.2, rx=radius, ry=radius)
        d.add(r)

    def label(text, x, y, size=9, font=BODY, color=TEXT, anchor="start"):
        s = String(x, y, text, fontName=font, fontSize=size, fillColor=color)
        s.textAnchor = anchor
        d.add(s)

    def multiline(lines, x, y, size=8, font=BODY, color=TEXT, leading=11, anchor="start"):
        for i, ln in enumerate(lines):
            label(ln, x, y - i * leading, size=size, font=font, color=color, anchor=anchor)

    def link(x1, y1, x2, y2, color, w=2.0, dash=None):
        ln = Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=w)
        if dash:
            ln.strokeDashArray = dash
        d.add(ln)

    # ---------- INTERNET cloud ----------
    box(width/2 - 110, height - 110, 220, 70, colors.HexColor("#E8F0F2"), WAN, 14)
    label("INTERNET", width/2, height - 60, size=14, font=HEAD, color=WAN, anchor="middle")
    label("ISP WAN  •  d2.lol → Cloudflare DNS", width/2, height - 80, size=8, font=BODY, color=MUTED, anchor="middle")

    # ---------- OPNsense ----------
    opn_x, opn_y, opn_w, opn_h = width/2 - 200, height - 280, 400, 130
    box(opn_x, opn_y, opn_w, opn_h, PRIMARY, DARK, 10)
    label("OPNsense g3 — Edge Firewall + Router", opn_x + 12, opn_y + opn_h - 22, size=12, font=HEAD, color=colors.white)
    multiline([
        "igb0 WAN (DHCP)   |   igb1 LAN trunk (all VLANs)",
        "Tailscale subnet router + exit node",
        "WireGuard remote admin   |   Suricata IDS",
        "Zenarmor + ntopng monitoring",
        "HAProxy → *.d2.lol  •  AdGuard Home (split-DNS)",
    ], opn_x + 12, opn_y + opn_h - 42, size=8.5, color=colors.white, leading=14)

    # WAN link
    link(width/2, height - 110, width/2, opn_y + opn_h, WAN, 3)
    label("WAN Cat6A → igb0", width/2 + 8, height - 130, size=8, font=HEAD, color=WAN)

    # ---------- Future 10G core switch ----------
    sw_x, sw_y, sw_w, sw_h = 80, opn_y - 150, width - 160, 95
    box(sw_x, sw_y, sw_w, sw_h, DARK, colors.black, 8)
    label("FUTURE 10G CORE SWITCH  (planned: MikroTik CRS305 / CRS309 or QNAP QSW-M2108)",
          sw_x + sw_w/2, sw_y + sw_h - 22, size=12, font=HEAD, color=colors.white, anchor="middle")
    label("8× 10GbE SFP+/RJ45  •  802.1Q VLAN trunk  •  Replaces SG105E in core role",
          sw_x + sw_w/2, sw_y + sw_h - 40, size=9, color=colors.white, anchor="middle")
    label("Cat6A 10G uplink ←→ igb1 trunk (all VLANs tagged)",
          sw_x + sw_w/2, sw_y + 18, size=8, font=MONOB, color=colors.HexColor("#BCE2E7"), anchor="middle")

    # OPNsense → 10G core
    link(width/2, opn_y, width/2, sw_y + sw_h, LAN10G, 4)

    # ---------- SG105E + hEX row ----------
    sg_y = sw_y - 140
    sg_x, sg_w, sg_h = 80, 540, 120
    box(sg_x, sg_y, sg_w, sg_h, colors.HexColor("#20808D"), DARK, 8)
    label("TP-Link SG105E  (current 1GbE Easy Smart)", sg_x + 12, sg_y + sg_h - 18, size=10.5, font=HEAD, color=colors.white)
    multiline([
        "P1 trunk → OPNsense igb1  (all VLANs, 10 native)",
        "P2 trunk → MHV enp1s0f1  (10,20,30,50,60 tagged)",
        "P3 access v20 → Media Server",
        "P4 access v20 → NAS / NUC / G4 (downstream)",
        "P5 trunk → hEX  (carries v30 + v40 + v50)",
    ], sg_x + 12, sg_y + sg_h - 36, size=7.8, font=MONO, color=colors.white, leading=12)

    hex_x, hex_w, hex_h = sg_x + sg_w + 40, 320, 120
    box(hex_x, sg_y, hex_w, hex_h, ACCENT2, colors.HexColor("#6E1F0F"), 8)
    label("MikroTik hEX RB750Gr3", hex_x + 12, sg_y + sg_h - 18, size=10.5, font=HEAD, color=colors.white)
    multiline([
        "5× 1GbE  •  RouterOS 7",
        "Hosts TEST VLAN 50 sandbox",
        "Downstream AP: IoT v30 + Guest v40",
        "Strict FW: no v10 / v20 reachability",
    ], hex_x + 12, sg_y + sg_h - 36, size=7.8, color=colors.white, leading=12)

    # 10G core → SG / hEX
    link(sw_x + 100, sw_y, sg_x + sg_w/2, sg_y + sg_h, LAN10G, 3)
    link(sw_x + 380, sw_y, hex_x + hex_w/2, sg_y + sg_h, IOT, 2.5)

    # ---------- IoT / Guest / Test row (sits to the right of hEX, above MHV row) ----------
    iot_y = sg_y - 90
    iot_w, iot_h = 145, 70
    iot_x_start = hex_x - 30
    iot_cards = [
        ("IoT VLAN 30",   "TV • Hue • smart plugs",       colors.HexColor("#FFC553"), IOT),
        ("Guest VLAN 40", "Visitor SSID • internet only", colors.HexColor("#BCE2E7"), GUEST),
        ("TEST VLAN 50",  "Sandbox lab • hEX-routed",     colors.HexColor("#BCE2E7"), TEST),
    ]
    for i, (name, sub, color, accent) in enumerate(iot_cards):
        x = iot_x_start + i * (iot_w + 10)
        box(x, iot_y, iot_w, iot_h, color, accent, 8)
        label(name, x + iot_w/2, iot_y + iot_h - 22, size=10, font=HEAD, color=TEXT, anchor="middle")
        label(sub,  x + iot_w/2, iot_y + iot_h - 42, size=7.5, color=TEXT, anchor="middle")
        # link to hEX
        link(x + iot_w/2, iot_y + iot_h, hex_x + hex_w/2, sg_y, accent, 1.5)

    # ---------- MHV (large) ----------
    mhv_y = iot_y - 200
    mhv_x, mhv_w, mhv_h = 80, 540, 170
    box(mhv_x, mhv_y, mhv_w, mhv_h, TEXT, colors.black, 8)
    label("MHV — Main Hypervisor (Proxmox VE)", mhv_x + 12, mhv_y + mhv_h - 22, size=12, font=HEAD, color=colors.white)
    multiline([
        "eno1     1GbE  →  MGMT v10 (.10)   |   IPMI .110",
        "enp1s0f0 10G  →  WAN failover / direct test link",
        "enp1s0f1 10G  →  LAN trunk (v10/20/30/50/60)",
        "",
        "Guests: AdGuard, Gluetun-VPN-CT, *arr stack,",
        "Uptime Kuma, Grafana, Tailscale, dev sandboxes",
    ], mhv_x + 12, mhv_y + mhv_h - 40, size=8.5, font=MONO, color=colors.white, leading=13)

    # MHV ↔ 10G core (LAN trunk 10G)
    link(mhv_x + mhv_w/2, mhv_y + mhv_h, sw_x + 200, sw_y, LAN10G, 4)
    label("enp1s0f1 10G LAN trunk", mhv_x + mhv_w/2 - 60, mhv_y + mhv_h + 6, size=8, font=HEAD, color=LAN10G)

    # MHV ↔ OPNsense (WAN failover dashed)
    link(mhv_x + mhv_w, mhv_y + mhv_h - 30, opn_x, opn_y + 30, WAN, 1.8, dash=[4, 4])
    label("enp1s0f0 10G WAN failover", mhv_x + mhv_w + 8, mhv_y + mhv_h - 28, size=7, color=WAN)

    # MHV eno1 → SG105E
    link(mhv_x + 120, mhv_y + mhv_h, sg_x + 80, sg_y, MGMT, 2.2)
    label("eno1 MGMT → SG P2", mhv_x + 130, mhv_y + mhv_h + 18, size=7, font=HEAD, color=MGMT)

    # ---------- Server row ----------
    srv_y = mhv_y
    srv_h = mhv_h
    cards = [
        ("Main Media Server",  ["Plex / Jellyfin", "*arr stack", "v20 .11", "plex.d2.lol"], MEDIA),
        ("NUC i5",             ["Proxmox node", "quorum + lite VMs", "v20 .12"],            NUC_BLUE),
        ("G4 Mini",            ["Proxmox node", "edge services", "v20 .13"],                NUC_BLUE),
        ("i3 NAS Build",       ["TrueNAS / Unraid", "ZFS  •  NFS / SMB", "v20 .20", "nas.d2.lol"], NAS_BR),
        ("WGR — Win Gaming",   ["Tailscale client", "v20 .50", "wgr.d2.lol"],               GUEST),
    ]
    cx = mhv_x + mhv_w + 30
    cw = (width - cx - 40) / len(cards) - 12
    for i, (title, lines, color) in enumerate(cards):
        x = cx + i * (cw + 12)
        box(x, srv_y, cw, srv_h, color, colors.black, 8)
        label(title, x + 10, srv_y + srv_h - 22, size=10.5, font=HEAD, color=colors.white)
        multiline(lines, x + 10, srv_y + srv_h - 42, size=8.5, color=colors.white, leading=13)
        # link up to 10G core
        link(x + cw/2, srv_y + srv_h, sw_x + 350 + i * 90, sw_y, LAN10G, 2)

    # ---------- VPN torrent bubble ----------
    vpn_x, vpn_y, vpn_w, vpn_h = width - 430, mhv_y - 110, 380, 100
    box(vpn_x, vpn_y, vpn_w, vpn_h, DARK, colors.black, 10)
    label("VPN Torrent Path  —  VLAN 60", vpn_x + 12, vpn_y + vpn_h - 22, size=11, font=HEAD, color=colors.white)
    multiline([
        "Gluetun LXC on MHV → Mullvad / ProtonVPN WG",
        "qBittorrent + Prowlarr bound to tun0 only",
        "Kill-switch via OPNsense policy route",
        "Sonarr/Radarr → NAS (v20) → Plex",
    ], vpn_x + 12, vpn_y + vpn_h - 42, size=8, font=MONO, color=colors.white, leading=12)
    link(vpn_x, vpn_y + vpn_h/2, mhv_x + mhv_w, mhv_y + 30, DARK, 1.8, dash=[6, 4])

    # ---------- Tailscale overlay annotation ----------
    ts_x, ts_y = 80, mhv_y - 30
    label("Tailscale overlay  100.64.0.0/10  —  subnet router on OPNsense advertises 10.10.0.0/16  •  MagicDNS *.d2.lol via AdGuard split-horizon",
          ts_x, ts_y, size=8.5, font=MONOB, color=TS)
    # dashed overlay line spanning width
    for x0 in range(int(ts_x), int(width - 80), 10):
        link(x0, ts_y - 8, x0 + 5, ts_y - 8, TS, 1.5)

    # ---------- Legend (top-right corner) ----------
    lg_x, lg_y, lg_w, lg_h = width - 340, height - 280, 300, 160
    box(lg_x, lg_y, lg_w, lg_h, SURFACE, BORDER, 8)
    label("LEGEND — Cabling (Cat6A RJ45)", lg_x + 12, lg_y + lg_h - 20, size=10, font=HEAD)
    legend_items = [
        ("WAN — ISP / Internet",          WAN,    None),
        ("LAN 10 GbE — X540 / 10G core",  LAN10G, None),
        ("MGMT 1 GbE — eno1 / IPMI",      MGMT,   None),
        ("IoT VLAN 30",                   IOT,    None),
        ("Guest VLAN 40",                 GUEST,  None),
        ("TEST VLAN 50 / sandbox",        TEST,   None),
        ("Tailscale overlay (WG)",        TS,     [4, 4]),
    ]
    for i, (txt, c, dash) in enumerate(legend_items):
        ly = lg_y + lg_h - 40 - i * 16
        ln = Line(lg_x + 14, ly, lg_x + 56, ly, strokeColor=c, strokeWidth=3)
        if dash:
            ln.strokeDashArray = dash
        d.add(ln)
        label(txt, lg_x + 64, ly - 3, size=8.5, color=TEXT)

    return d


# ============================================================
#  PDF document build
# ============================================================
def build():
    os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)
    # Topology gets its own larger landscape page; rest of the doc uses A3 landscape.
    pagesize_topo = (17 * 72, 14 * 72)
    pagesize = landscape(A3)

    topo_path = PDF_PATH.replace(".pdf", "_topo.pdf")
    rest_path = PDF_PATH.replace(".pdf", "_rest.pdf")

    from reportlab.pdfgen.canvas import Canvas
    from reportlab.graphics import renderPDF
    c = Canvas(topo_path, pagesize=pagesize_topo)
    c.setTitle("d2lab Master Network Architecture"); c.setAuthor("Perplexity Computer")
    page_w, page_h = pagesize_topo
    c.setFont(HEAD, 22); c.setFillColor(TEXT)
    c.drawString(28, page_h - 38, "d2lab \u2014 Master Homelab Network Architecture")
    c.setFont(BODY, 10); c.setFillColor(MUTED)
    c.drawString(28, page_h - 56,
        "Domain d2.lol  \u2022  Hypervisor MHV (Proxmox VE)  \u2022  Cabling Cat6A RJ45  \u2022  Tailscale tailnet enabled  \u2022  Future 10G core")
    drw = topology_drawing(page_w - 56, page_h - 100)
    renderPDF.draw(drw, c, 28, 30)
    c.setFont(BODY, 8); c.setFillColor(MUTED)
    c.drawString(28, 14, "d2lab \u2014 Master Network Architecture  \u2022  Generated by Perplexity Computer  \u2022  d2.lol")
    c.drawRightString(page_w - 28, 14, "Page 1")
    c.showPage(); c.save()

    doc = SimpleDocTemplate(
        rest_path,
        pagesize=pagesize,
        leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24,
        title="d2lab Master Network Architecture",
        author="Perplexity Computer",
    )

    styles = getSampleStyleSheet()
    H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName=HEAD, fontSize=22, leading=26, textColor=TEXT, spaceAfter=2)
    H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName=HEAD, fontSize=14, leading=18, textColor=PRIMARY, spaceBefore=14, spaceAfter=6)
    SUB = ParagraphStyle("SUB", parent=styles["Normal"], fontName=BODY, fontSize=10, leading=14, textColor=MUTED)
    BODYS = ParagraphStyle("Body", parent=styles["Normal"], fontName=BODY, fontSize=9.5, leading=13, textColor=TEXT)
    MONOSTY = ParagraphStyle("Mono", parent=styles["Normal"], fontName=MONO, fontSize=8.5, leading=12, textColor=TEXT)

    story = []

    # ---------- Page 2: VLAN / IP plan ----------
    story.append(Paragraph("VLAN &amp; IP Plan", H1))
    story.append(Spacer(1, 4))

    vlan_data = [
        ["VLAN", "Name",   "Subnet",          "Gateway", "Purpose"],
        ["10",   "MGMT",   "10.10.10.0/24",   ".1",      "Proxmox eno1, IPMI, switch admin, OPNsense mgmt"],
        ["20",   "LAN",    "10.10.20.0/24",   ".1",      "Servers, NAS, gaming rig, *arr stack consumers"],
        ["30",   "IoT",    "10.10.30.0/24",   ".1",      "TV, Hue Bridge, smart plugs — no LAN reach"],
        ["40",   "GUEST",  "10.10.40.0/24",   ".1",      "Visitor SSID — internet only, fully isolated"],
        ["50",   "TEST",   "10.10.50.0/24",   ".1",      "Sandbox / break-things lab routed via hEX"],
        ["60",   "VPN",    "10.10.60.0/24",   ".1",      "Gluetun torrent egress — policy-routed, kill-switched"],
        ["—",    "TS",     "100.64.0.0/10",   "—",       "Tailscale overlay — MagicDNS + split-horizon d2.lol"],
    ]
    t = Table(vlan_data, colWidths=[40, 60, 110, 60, 800-270])
    t.setStyle(TableStyle([
        ("FONT",       (0,0), (-1,0), HEAD, 10),
        ("FONT",       (0,1), (-1,-1), MONO, 9),
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [SURFACE, BG]),
        ("LINEBELOW",  (0,0), (-1,0), 1, DARK),
        ("LINEBELOW",  (0,-1), (-1,-1), 1, BORDER),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",(0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
    ]))
    story.append(t)

    # Static host table
    story.append(Paragraph("Static Host Assignments", H2))
    host_data = [
        ["Host",                "VLAN(s)",                 "IP(s)",                       "DNS (d2.lol)",   "Notes"],
        ["OPNsense g3",         "10/20/30/40/50/60 trunk", "all .1 + ISP WAN",            "fw.d2.lol",      "Edge FW, Tailscale exit, AdGuard"],
        ["TP-Link SG105E",      "10 mgmt",                 "10.10.10.2",                  "sw1.d2.lol",     "Easy-Smart, 802.1Q trunks"],
        ["MikroTik hEX RB750Gr3","10 mgmt + 30/40/50",     "10.10.10.3",                  "hex.d2.lol",     "Test-net router, IoT/Guest gw"],
        ["Future 10G core sw",  "10 mgmt",                 "10.10.10.4",                  "sw10g.d2.lol",   "CRS305/CRS309 or QSW-M2108"],
        ["MHV (Proxmox)",       "10 + 20 + IPMI",          "eno1 .10  •  enp1s0f1 .10  •  IPMI .110", "mhv.d2.lol",     "X540 dual 10G, eno1 mgmt"],
        ["Main Media Server",   "20  (IPMI on 10)",        "10.10.20.11  •  IPMI .111",   "plex.d2.lol",    "Plex/Jellyfin + *arr"],
        ["NUC i5",              "20",                      "10.10.20.12",                 "nuc.d2.lol",     "Proxmox node, quorum"],
        ["G4 Mini",             "20",                      "10.10.20.13",                 "g4.d2.lol",      "Proxmox node, edge svcs"],
        ["i3 NAS Build",        "20",                      "10.10.20.20",                 "nas.d2.lol",     "TrueNAS/Unraid, ZFS"],
        ["WGR (Windows)",       "20",                      "10.10.20.50",                 "wgr.d2.lol",     "Tailscale client"],
        ["TV / Hue Bridge",     "30",                      "10.10.30.30 / .31",           "—",              "IoT — no v10/v20 reach"],
        ["Visitor SSID pool",   "40",                      "10.10.40.100–.200 DHCP",      "—",              "Captive portal optional"],
        ["Gluetun-VPN-CT",      "60",                      "10.10.60.60",                 "vpn-ct.d2.lol",  "LXC on MHV, kill-switched"],
    ]
    th = Table(host_data, colWidths=[120, 130, 200, 100, 280])
    th.setStyle(TableStyle([
        ("FONT",       (0,0), (-1,0), HEAD, 9.5),
        ("FONT",       (0,1), (-1,-1), MONO, 8.2),
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [SURFACE, BG]),
        ("LINEBELOW",  (0,0), (-1,0), 1, DARK),
        ("LINEBELOW",  (0,-1), (-1,-1), 1, BORDER),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",(0,0), (-1,-1), 6),
        ("RIGHTPADDING",(0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ]))
    story.append(th)

    story.append(PageBreak())

    # ---------- Page 3: Cabling map + Port map ----------
    story.append(Paragraph("Cabling Layout &amp; Port Map", H1))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "All physical links are <b>Cat6A RJ45</b>. Color encodes role; runs marked 10G use the future 10G core "
        "switch (or X540 direct between MHV and OPNsense for the WAN-failover/test path).", BODYS))

    story.append(Paragraph("MHV (Proxmox) Interfaces", H2))
    mhv_iface = [
        ["Interface",  "Speed", "Role",                 "Cable",  "Other End",                   "VLANs"],
        ["eno1",       "1 GbE", "Management",           "Cat6A",  "SG105E P2",                   "v10 (untagged)"],
        ["enp1s0f0",   "10G",   "WAN failover / direct","Cat6A",  "OPNsense (igb0 alt) — direct","WAN"],
        ["enp1s0f1",   "10G",   "LAN trunk",            "Cat6A",  "Future 10G core (uplink 1)",  "v10/20/30/50/60 tagged"],
        ["IPMI/BMC",   "100M",  "Out-of-band mgmt",     "Cat6A",  "SG105E P2 (shared mgmt)",     "v10"],
    ]
    t1 = Table(mhv_iface, colWidths=[100, 60, 160, 60, 200, 250])
    t1.setStyle(TableStyle([
        ("FONT",(0,0),(-1,0), HEAD, 10),
        ("FONT",(0,1),(-1,-1), MONO, 9),
        ("BACKGROUND",(0,0),(-1,0), TEXT),
        ("TEXTCOLOR",(0,0),(-1,0), colors.white),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[SURFACE, BG]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(t1)

    story.append(Paragraph("SG105E Port Map (5 ports, 802.1Q)", H2))
    sg_ports = [
        ["Port", "Mode",     "VLANs",                       "Connected To"],
        ["P1",   "Trunk",    "10 (native), 20/30/40/50/60 tagged", "OPNsense igb1"],
        ["P2",   "Trunk",    "10 (native), 20/30/50/60 tagged",    "MHV enp1s0f1 (and shared eno1 mgmt)"],
        ["P3",   "Access",   "v20",                         "Main Media Server"],
        ["P4",   "Access",   "v20",                         "Downstream NUC / G4 / NAS"],
        ["P5",   "Trunk",    "30/40/50 tagged",             "MikroTik hEX RB750Gr3"],
    ]
    t2 = Table(sg_ports, colWidths=[60, 80, 280, 410])
    t2.setStyle(t1.getStyle() if hasattr(t1, "getStyle") else TableStyle([
        ("FONT",(0,0),(-1,0), HEAD, 10),
        ("FONT",(0,1),(-1,-1), MONO, 9),
        ("BACKGROUND",(0,0),(-1,0), colors.HexColor("#20808D")),
        ("TEXTCOLOR",(0,0),(-1,0), colors.white),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[SURFACE, BG]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(t2)

    story.append(Paragraph("hEX RB750Gr3 Port Map", H2))
    hex_ports = [
        ["Port",  "Role",                 "VLAN(s)",      "Connected To"],
        ["ether1","Trunk uplink",         "30/40/50",     "SG105E P5"],
        ["ether2","Access — TEST lab",    "v50",          "Lab patch panel / sandbox VMs"],
        ["ether3","Access — IoT",         "v30",          "TV, Hue Bridge, smart plugs"],
        ["ether4","Access — Guest AP",    "v40",          "Guest wireless AP (visitor SSID)"],
        ["ether5","Spare / out-of-band",  "v10",          "Mgmt patch (optional)"],
    ]
    t3 = Table(hex_ports, colWidths=[80, 200, 100, 450])
    t3.setStyle(TableStyle([
        ("FONT",(0,0),(-1,0), HEAD, 10),
        ("FONT",(0,1),(-1,-1), MONO, 9),
        ("BACKGROUND",(0,0),(-1,0), ACCENT2),
        ("TEXTCOLOR",(0,0),(-1,0), colors.white),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[SURFACE, BG]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(t3)

    story.append(PageBreak())

    # ---------- Page 4: Tailscale + VPN-Torrent + DNS ----------
    story.append(Paragraph("Tailscale Tailnet, VPN Torrent &amp; DNS", H1))

    story.append(Paragraph("Tailscale Tailnet", H2))
    story.append(Paragraph(
        "OPNsense runs the <b>Tailscale subnet router + exit node</b>, advertising <b>10.10.0.0/16</b>. "
        "Native clients run on MHV, the Media Server, NAS, WGR, plus phones and laptops. ACLs use tag-based policy: "
        "<b>tag:admin</b> reaches MGMT v10, <b>tag:user</b> is restricted to LAN v20. "
        "MagicDNS aliases are mapped to <b>*.d2.lol</b> hostnames via AdGuard Home split-horizon so the same DNS name "
        "resolves to the LAN IP at home and the 100.x address remotely.",
        BODYS))

    story.append(Paragraph("VPN Torrent Path (VLAN 60)", H2))
    story.append(Paragraph(
        "<b>Gluetun</b> runs as a privileged LXC on MHV with its own NIC pinned to VLAN 60 "
        "(<b>10.10.60.60</b>). qBittorrent and Prowlarr are bound exclusively to <b>tun0</b>. "
        "OPNsense enforces a policy route: any traffic sourced from <b>10.10.60.0/24</b> that misses the "
        "WireGuard tunnel is dropped — true kill-switch. Sonarr/Radarr live on v20 and pull completed media from the NAS "
        "via SMB, then trigger Plex library refresh. The torrent client itself never has a path to v20 servers.",
        BODYS))

    story.append(Paragraph("DNS &amp; d2.lol", H2))
    story.append(Paragraph(
        "<b>Cloudflare</b> hosts the public <b>d2.lol</b> zone. Public records resolve to the WAN IP "
        "(or a Cloudflare Tunnel for selected services). Internally, <b>AdGuard Home</b> on OPNsense runs split-horizon: "
        "<b>*.d2.lol</b> resolves to LAN IPs, with <b>plex.d2.lol</b>, "
        "<b>nas.d2.lol</b>, <b>mhv.d2.lol</b>, etc. wired to their VLAN 20 addresses. "
        "TLS is provided by Caddy (or HAProxy + acme.sh) using a Cloudflare DNS-01 wildcard cert for <b>*.d2.lol</b>.",
        BODYS))

    story.append(Paragraph("Test / Sandbox VLAN (50)", H2))
    story.append(Paragraph(
        "VLAN 50 is the &ldquo;break things&rdquo; lab: routed through the hEX with strict OPNsense rules that allow "
        "internet egress but block all inbound to v10/v20. Use it for nested Proxmox, Terraform/Ansible runs, k3s "
        "experiments, and OS images you don&rsquo;t fully trust. DHCP <b>10.10.50.50–.200</b>; "
        "static reservations live in the runbook.",
        BODYS))

    # ---------- Footer on every page ----------
    def _on_page(c, doc):
        c.setFont(BODY, 8)
        c.setFillColor(MUTED)
        c.drawString(24, 12, "d2lab \u2014 Master Network Architecture  \u2022  Generated by Perplexity Computer  \u2022  d2.lol")
        c.drawRightString(pagesize[0] - 24, 12, f"Page {doc.page + 1}")

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)

    # ---------- Merge topo + rest ----------
    from pypdf import PdfWriter, PdfReader
    w = PdfWriter()
    for p in (topo_path, rest_path):
        for page in PdfReader(p).pages:
            w.add_page(page)
    w.add_metadata({"/Title": "d2lab Master Network Architecture", "/Author": "Perplexity Computer"})
    with open(PDF_PATH, "wb") as f:
        w.write(f)
    os.remove(topo_path); os.remove(rest_path)
    print(f"Wrote {PDF_PATH}")

if __name__ == "__main__":
    build()
