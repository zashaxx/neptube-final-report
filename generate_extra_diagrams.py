#!/usr/bin/env python3
"""Generate additional diagrams for the NepTube final report:
- System Architecture Diagram
- ER Diagram
- DFD Level-0 (Context Diagram)
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT, exist_ok=True)

FONT = "DejaVu Sans"
C_EDGE = "#37474F"


def _save(fig, name):
    fig.savefig(
        os.path.join(OUT, name),
        dpi=200,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
    )
    plt.close(fig)
    print(f"  ✓ {name}")


def _rbox(
    ax, x, y, w, h, text, fc, ec="#37474F", fontsize=9, tc="white", lw=1.5, radius=0.08
):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle=f"round,pad={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=3,
    )
    ax.add_patch(box)
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color=tc,
        fontfamily=FONT,
        zorder=4,
    )


def _arrow(
    ax,
    x1,
    y1,
    x2,
    y2,
    label="",
    color="#37474F",
    lw=1.2,
    fontsize=7,
    ha="center",
    va="bottom",
    offset=(0, 0.08),
):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=color, lw=lw),
        zorder=2,
    )
    if label:
        mx, my = (x1 + x2) / 2 + offset[0], (y1 + y2) / 2 + offset[1]
        ax.text(
            mx,
            my,
            label,
            fontsize=fontsize,
            color=color,
            fontfamily=FONT,
            ha=ha,
            va=va,
            style="italic",
        )


def _darrow(ax, x1, y1, x2, y2, label="", color="#37474F", lw=1.2, fontsize=7):
    """Double-headed arrow."""
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="<->", color=color, lw=lw),
        zorder=2,
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + 0.12
        ax.text(
            mx,
            my,
            label,
            fontsize=fontsize,
            color=color,
            fontfamily=FONT,
            ha="center",
            va="bottom",
            style="italic",
        )


# ════════════════════════════════════════════════════════════════════
#  1. SYSTEM ARCHITECTURE DIAGRAM
# ════════════════════════════════════════════════════════════════════
def gen_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(-1, 15)
    ax.set_ylim(-7.5, 3)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    # ── Presentation Layer (Top) ──
    layer_y = 2.0
    bg = FancyBboxPatch(
        (-0.5, 1.2),
        15,
        1.6,
        boxstyle="round,pad=0.15",
        facecolor="#E3F2FD",
        edgecolor="#1565C0",
        lw=1.5,
        alpha=0.4,
        zorder=1,
    )
    ax.add_patch(bg)
    ax.text(
        0.0,
        2.5,
        "Presentation Layer",
        fontsize=10,
        fontweight="bold",
        color="#1565C0",
        fontfamily=FONT,
        va="center",
    )

    _rbox(ax, 3, layer_y, 2.2, 0.7, "Next.js\nFrontend", "#1565C0")
    _rbox(ax, 6, layer_y, 2.2, 0.7, "React 19\nComponents", "#1E88E5")
    _rbox(ax, 9, layer_y, 2.2, 0.7, "Tailwind CSS\nStyling", "#42A5F5")
    _rbox(ax, 12, layer_y, 2.2, 0.7, "Radix UI\nPrimitives", "#64B5F6")

    # ── Application Layer (Middle) ──
    layer_y2 = -0.2
    bg2 = FancyBboxPatch(
        (-0.5, -1.0),
        15,
        1.6,
        boxstyle="round,pad=0.15",
        facecolor="#FFF3E0",
        edgecolor="#E65100",
        lw=1.5,
        alpha=0.4,
        zorder=1,
    )
    ax.add_patch(bg2)
    ax.text(
        0.0,
        0.3,
        "Application Layer",
        fontsize=10,
        fontweight="bold",
        color="#E65100",
        fontfamily=FONT,
        va="center",
    )

    _rbox(ax, 3, layer_y2, 2.2, 0.7, "tRPC\nAPI Routes", "#E65100")
    _rbox(ax, 6, layer_y2, 2.2, 0.7, "Clerk\nAuthentication", "#F4511E")
    _rbox(ax, 9, layer_y2, 2.2, 0.7, "UploadThing\nFile Uploads", "#FF7043")
    _rbox(ax, 12, layer_y2, 2.2, 0.7, "Bun\nRuntime", "#FF8A65")

    # ── Data Layer (Bottom Left) ──
    layer_y3 = -2.8
    bg3 = FancyBboxPatch(
        (-0.5, -3.6),
        7.5,
        1.6,
        boxstyle="round,pad=0.15",
        facecolor="#E8F5E9",
        edgecolor="#2E7D32",
        lw=1.5,
        alpha=0.4,
        zorder=1,
    )
    ax.add_patch(bg3)
    ax.text(
        0.0,
        -2.3,
        "Data Layer",
        fontsize=10,
        fontweight="bold",
        color="#2E7D32",
        fontfamily=FONT,
        va="center",
    )

    _rbox(ax, 3, layer_y3, 2.2, 0.7, "PostgreSQL\n(Neon)", "#2E7D32")
    _rbox(ax, 6, layer_y3, 2.2, 0.7, "Drizzle ORM\nType-safe", "#43A047")

    # ── AI/ML Services (Bottom Right) ──
    bg4 = FancyBboxPatch(
        (7.5, -3.6),
        7,
        1.6,
        boxstyle="round,pad=0.15",
        facecolor="#F3E5F5",
        edgecolor="#6A1B9A",
        lw=1.5,
        alpha=0.4,
        zorder=1,
    )
    ax.add_patch(bg4)
    ax.text(
        8.0,
        -2.3,
        "AI/ML Services",
        fontsize=10,
        fontweight="bold",
        color="#6A1B9A",
        fontfamily=FONT,
        va="center",
    )

    _rbox(ax, 10, layer_y3, 2.0, 0.7, "Pollinations\nAI NLP", "#6A1B9A")
    _rbox(ax, 12.5, layer_y3, 2.0, 0.7, "Replicate\nWhisper v3", "#8E24AA")

    # ── External Services ──
    layer_y4 = -5.3
    bg5 = FancyBboxPatch(
        (-0.5, -6.1),
        15,
        1.6,
        boxstyle="round,pad=0.15",
        facecolor="#FBE9E7",
        edgecolor="#BF360C",
        lw=1.5,
        alpha=0.4,
        zorder=1,
    )
    ax.add_patch(bg5)
    ax.text(
        0.0,
        -4.8,
        "External Services",
        fontsize=10,
        fontweight="bold",
        color="#BF360C",
        fontfamily=FONT,
        va="center",
    )

    _rbox(ax, 3, layer_y4, 2.2, 0.7, "Vercel\nDeployment", "#BF360C")
    _rbox(ax, 6, layer_y4, 2.2, 0.7, "eSewa / Khalti\nPayments", "#D84315")
    _rbox(ax, 9, layer_y4, 2.2, 0.7, "HuggingFace\nModeration", "#E64A19")
    _rbox(ax, 12, layer_y4, 2.2, 0.7, "CDN\nVideo Delivery", "#F4511E")

    # ── Arrows between layers ──
    for x in [3, 6, 9, 12]:
        _arrow(ax, x, 1.55, x, 0.15)
    for x in [3, 6]:
        _arrow(ax, x, -0.55, x, -2.45)
    for x in [10, 12.5]:
        _arrow(ax, x if x == 10 else 12, -0.55, x, -2.45)
    _arrow(ax, 3, -3.15, 3, -4.95)
    _arrow(ax, 6, -3.15, 6, -4.95)
    _arrow(ax, 9, -0.55, 9, -4.95)
    _arrow(ax, 12, -3.15, 12, -4.95)

    ax.set_title(
        "System Architecture Diagram",
        fontsize=16,
        fontweight="bold",
        fontfamily=FONT,
        pad=15,
    )
    _save(fig, "system-architecture.png")


# ════════════════════════════════════════════════════════════════════
#  2. ER DIAGRAM
# ════════════════════════════════════════════════════════════════════
def gen_er_diagram():
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(-1, 17)
    ax.set_ylim(-10, 3)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    def entity(x, y, name, attrs, pk=None, color="#1565C0"):
        w, h_header = 3.2, 0.55
        row_h = 0.38
        total_h = h_header + row_h * len(attrs)
        # Header
        header = FancyBboxPatch(
            (x - w / 2, y - h_header / 2),
            w,
            h_header,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor="#37474F",
            lw=1.5,
            zorder=3,
        )
        ax.add_patch(header)
        ax.text(
            x,
            y,
            name,
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
            color="white",
            fontfamily=FONT,
            zorder=4,
        )
        # Attribute rows
        for i, attr in enumerate(attrs):
            ry = y - h_header / 2 - row_h * (i + 0.5)
            bg_c = "#FAFAFA" if i % 2 == 0 else "#F5F5F5"
            rect = plt.Rectangle(
                (x - w / 2, ry - row_h / 2),
                w,
                row_h,
                facecolor=bg_c,
                edgecolor="#BDBDBD",
                lw=0.5,
                zorder=3,
            )
            ax.add_patch(rect)
            is_pk = attr == pk
            prefix = "PK " if is_pk else "   "
            fc = "#C62828" if is_pk else "#212121"
            fw = "bold" if is_pk else "normal"
            ax.text(
                x - w / 2 + 0.15,
                ry,
                f"{prefix}{attr}",
                fontsize=7,
                va="center",
                fontfamily=FONT,
                color=fc,
                fontweight=fw,
                zorder=4,
            )
        # Border
        border = plt.Rectangle(
            (x - w / 2, y - h_header / 2 - row_h * len(attrs)),
            w,
            total_h,
            fill=False,
            edgecolor="#37474F",
            lw=1.5,
            zorder=5,
        )
        ax.add_patch(border)
        return (x, y - h_header / 2 - row_h * len(attrs) / 2)  # center of body

    def rel_line(ax, x1, y1, x2, y2, label="", card1="", card2=""):
        ax.plot([x1, x2], [y1, y2], color="#546E7A", lw=1.2, zorder=2)
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(
                mx,
                my + 0.15,
                label,
                fontsize=6,
                color="#546E7A",
                fontfamily=FONT,
                ha="center",
                va="bottom",
                style="italic",
                bbox=dict(fc="white", ec="none", pad=1),
            )
        if card1:
            ax.text(
                x1 + (x2 - x1) * 0.12,
                y1 + (y2 - y1) * 0.12 + 0.12,
                card1,
                fontsize=6,
                color="#C62828",
                fontfamily=FONT,
                ha="center",
            )
        if card2:
            ax.text(
                x2 + (x1 - x2) * 0.12,
                y2 + (y1 - y2) * 0.12 + 0.12,
                card2,
                fontsize=6,
                color="#C62828",
                fontfamily=FONT,
                ha="center",
            )

    # ── Entities ──
    users_pos = entity(
        2,
        2,
        "Users",
        [
            "id (PK)",
            "clerk_id",
            "name",
            "image_url",
            "role",
            "subscription_tier",
            "is_banned",
        ],
        pk="id (PK)",
        color="#1565C0",
    )

    videos_pos = entity(
        8,
        2,
        "Videos",
        [
            "id (PK)",
            "title",
            "video_url",
            "thumbnail_url",
            "status",
            "view_count",
            "user_id (FK)",
            "ai_summary",
        ],
        pk="id (PK)",
        color="#2E7D32",
    )

    comments_pos = entity(
        14,
        2,
        "Comments",
        [
            "id (PK)",
            "content",
            "user_id (FK)",
            "video_id (FK)",
            "parent_id",
            "is_toxic",
            "sentiment",
        ],
        pk="id (PK)",
        color="#E65100",
    )

    subs_pos = entity(
        2,
        -3.5,
        "Subscriptions",
        ["id (PK)", "subscriber_id (FK)", "channel_id (FK)", "created_at"],
        pk="id (PK)",
        color="#6A1B9A",
    )

    playlists_pos = entity(
        8,
        -3.5,
        "Playlists",
        ["id (PK)", "name", "visibility", "user_id (FK)", "created_at"],
        pk="id (PK)",
        color="#00838F",
    )

    likes_pos = entity(
        14,
        -3.5,
        "VideoLikes",
        ["id (PK)", "user_id (FK)", "video_id (FK)", "is_like"],
        pk="id (PK)",
        color="#C62828",
    )

    watch_pos = entity(
        2,
        -7.5,
        "WatchHistory",
        ["id (PK)", "user_id (FK)", "video_id (FK)", "watch_duration"],
        pk="id (PK)",
        color="#4E342E",
    )

    notifs_pos = entity(
        8,
        -7.5,
        "Notifications",
        ["id (PK)", "user_id (FK)", "type", "title", "is_read"],
        pk="id (PK)",
        color="#37474F",
    )

    reports_pos = entity(
        14,
        -7.5,
        "Reports",
        ["id (PK)", "reporter_id (FK)", "target_type", "reason", "status"],
        pk="id (PK)",
        color="#880E4F",
    )

    # ── Relationships ──
    # Users → Videos (1:N)
    rel_line(ax, 3.6, 1.5, 6.4, 1.5, "uploads", "1", "N")
    # Users → Comments (1:N)
    ax.plot([3.6, 5, 5, 12.4], [0.5, 0.5, 0.0, 0.0], color="#546E7A", lw=1.0, zorder=2)
    ax.text(
        5.3, 0.15, "posts", fontsize=6, color="#546E7A", fontfamily=FONT, style="italic"
    )
    # Videos → Comments (1:N)
    rel_line(ax, 9.6, 1.0, 12.4, 1.0, "has", "1", "N")
    # Users → Subscriptions (1:N)
    rel_line(ax, 2, -0.55, 2, -2.8, "subscribes", "1", "N")
    # Users → Playlists (1:N)
    ax.plot(
        [3.6, 5.5, 5.5, 6.4],
        [-0.2, -0.2, -3.5, -3.5],
        color="#546E7A",
        lw=1.0,
        zorder=2,
    )
    ax.text(
        5.7,
        -2.0,
        "creates",
        fontsize=6,
        color="#546E7A",
        fontfamily=FONT,
        style="italic",
    )
    # Videos → Likes (1:N)
    rel_line(ax, 9.6, -0.2, 12.4, -3.5, "receives", "1", "N")
    # Users → WatchHistory (1:N)
    rel_line(ax, 2, -4.9, 2, -6.8, "watches", "1", "N")
    # Users → Notifications (1:N)
    ax.plot(
        [3.6, 5.5, 5.5, 6.4],
        [-4.2, -4.2, -7.5, -7.5],
        color="#546E7A",
        lw=1.0,
        zorder=2,
    )
    ax.text(
        5.7,
        -6.0,
        "receives",
        fontsize=6,
        color="#546E7A",
        fontfamily=FONT,
        style="italic",
    )
    # Users → Reports (1:N)
    ax.plot(
        [3.6, 11, 11, 12.4], [-4.5, -4.5, -7.5, -7.5], color="#546E7A", lw=1.0, zorder=2
    )
    ax.text(
        11.2,
        -6.0,
        "files",
        fontsize=6,
        color="#546E7A",
        fontfamily=FONT,
        style="italic",
    )

    ax.set_title(
        "Entity Relationship (ER) Diagram",
        fontsize=16,
        fontweight="bold",
        fontfamily=FONT,
        pad=15,
    )
    _save(fig, "er-diagram.png")


# ════════════════════════════════════════════════════════════════════
#  3. DFD LEVEL-0 (CONTEXT DIAGRAM)
# ════════════════════════════════════════════════════════════════════
def gen_dfd_diagram():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(-2, 16)
    ax.set_ylim(-8, 4)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    # ── Central Process ──
    circle = plt.Circle(
        (7, -2), 2.0, facecolor="#E3F2FD", edgecolor="#1565C0", lw=2.5, zorder=3
    )
    ax.add_patch(circle)
    ax.text(
        7,
        -1.6,
        "NepTube",
        fontsize=14,
        fontweight="bold",
        ha="center",
        va="center",
        color="#1565C0",
        fontfamily=FONT,
        zorder=4,
    )
    ax.text(
        7,
        -2.2,
        "Video Streaming\nPlatform",
        fontsize=9,
        ha="center",
        va="center",
        color="#37474F",
        fontfamily=FONT,
        zorder=4,
    )

    # ── External Entities ──
    def ext_entity(x, y, label, color="#37474F"):
        w, h = 2.8, 0.9
        rect = FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.1",
            facecolor="#FAFAFA",
            edgecolor=color,
            lw=2,
            zorder=3,
        )
        ax.add_patch(rect)
        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=color,
            fontfamily=FONT,
            zorder=4,
        )

    # Viewer (left)
    ext_entity(0, 0, "Viewer", "#1565C0")
    _darrow(ax, 1.4, 0, 5, -1.2, "", "#1565C0", lw=1.5)
    ax.text(
        2.5,
        0.3,
        "Watch, Like,\nComment, Subscribe",
        fontsize=7,
        color="#1565C0",
        fontfamily=FONT,
        ha="center",
    )
    ax.text(
        3.5,
        -1.2,
        "Videos, Recommendations,\nNotifications",
        fontsize=7,
        color="#1565C0",
        fontfamily=FONT,
        ha="center",
    )

    # Creator (left-bottom)
    ext_entity(0, -4, "Content\nCreator", "#E65100")
    _darrow(ax, 1.4, -4, 5.3, -3, "", "#E65100", lw=1.5)
    ax.text(
        2.0,
        -2.8,
        "Upload Video,\nEdit Metadata",
        fontsize=7,
        color="#E65100",
        fontfamily=FONT,
        ha="center",
    )
    ax.text(
        3.0,
        -4.2,
        "Analytics,\nAI Thumbnails",
        fontsize=7,
        color="#E65100",
        fontfamily=FONT,
        ha="center",
    )

    # Admin (top)
    ext_entity(7, 3, "Admin", "#C62828")
    _darrow(ax, 7, 2.55, 7, 0, "", "#C62828", lw=1.5)
    ax.text(
        7.8,
        1.8,
        "Moderate,\nManage Users",
        fontsize=7,
        color="#C62828",
        fontfamily=FONT,
        ha="center",
    )
    ax.text(
        5.8,
        1.3,
        "Reports,\nAnalytics",
        fontsize=7,
        color="#C62828",
        fontfamily=FONT,
        ha="center",
    )

    # Database (right)
    ext_entity(14, -1, "PostgreSQL\nDatabase", "#2E7D32")
    _darrow(ax, 9, -1.5, 12.6, -1, "", "#2E7D32", lw=1.5)
    ax.text(
        11,
        -0.5,
        "Store/Retrieve\nData",
        fontsize=7,
        color="#2E7D32",
        fontfamily=FONT,
        ha="center",
    )

    # AI Services (right-bottom)
    ext_entity(14, -3.5, "AI/ML\nServices", "#6A1B9A")
    _darrow(ax, 9, -2.5, 12.6, -3.5, "", "#6A1B9A", lw=1.5)
    ax.text(
        11.2,
        -2.5,
        "Content Analysis,\nRecommendations",
        fontsize=7,
        color="#6A1B9A",
        fontfamily=FONT,
        ha="center",
    )

    # Payment (bottom)
    ext_entity(7, -7, "Payment\nGateway", "#4E342E")
    _darrow(ax, 7, -6.55, 7, -4, "", "#4E342E", lw=1.5)
    ax.text(
        7.8,
        -5.8,
        "Payment\nRequests",
        fontsize=7,
        color="#4E342E",
        fontfamily=FONT,
        ha="center",
    )
    ax.text(
        5.8,
        -5.2,
        "Confirmation,\nReceipts",
        fontsize=7,
        color="#4E342E",
        fontfamily=FONT,
        ha="center",
    )

    ax.set_title(
        "Data Flow Diagram — Level 0 (Context Diagram)",
        fontsize=16,
        fontweight="bold",
        fontfamily=FONT,
        pad=15,
    )
    _save(fig, "dfd-diagram.png")


# ════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating additional NepTube diagrams ...")
    gen_system_architecture()
    gen_er_diagram()
    gen_dfd_diagram()
    print("Done – additional diagrams saved to", OUT)
