#!/usr/bin/env python3
"""Generate all 8 UML diagrams for the NepTube final report."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(OUT, exist_ok=True)

# ── Colour palette ──────────────────────────────────────────────────
C_START = "#2E7D32"  # green  (start/end)
C_PROC = "#1565C0"  # blue   (process)
C_DEC = "#F57F17"  # amber  (decision)
C_IO = "#6A1B9A"  # purple (IO)
C_BG = "#FFFFFF"
C_EDGE = "#37474F"
C_ACTOR = "#0D47A1"
C_UC = "#E3F2FD"
C_UC_BD = "#1565C0"
C_SYS = "#E8EAF6"
C_LIFE = "#90CAF9"
C_MSG = "#37474F"
C_ACT = "#FFF9C4"
C_SELF = "#FFECB3"
FONT = "DejaVu Sans"

# ════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════════


def _box(
    ax, x, y, text, color, w=2.2, h=0.55, fontsize=8, textcolor="white", shape="round"
):
    """Draw a rounded rectangle with centered text."""
    if shape == "round":
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.08",
            facecolor=color,
            edgecolor=C_EDGE,
            linewidth=1.2,
            zorder=3,
        )
        ax.add_patch(box)
    elif shape == "diamond":
        pts = np.array(
            [
                [x, y + h / 2],
                [x + w / 2, y],
                [x, y - h / 2],
                [x - w / 2, y],
                [x, y + h / 2],
            ]
        )
        ax.fill(
            pts[:, 0], pts[:, 1], color=color, edgecolor=C_EDGE, linewidth=1.2, zorder=3
        )
    elif shape == "stadium":
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.15",
            facecolor=color,
            edgecolor=C_EDGE,
            linewidth=1.5,
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
        color=textcolor,
        zorder=4,
        fontfamily=FONT,
    )


def _arrow(ax, x1, y1, x2, y2, label="", color=C_EDGE, lw=1.2, style="->", fontsize=7):
    """Draw an arrow between two points, optionally with a label."""
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle=style, color=color, lw=lw),
        zorder=2,
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(
            mx + 0.1,
            my,
            label,
            fontsize=fontsize,
            color=C_EDGE,
            fontfamily=FONT,
            ha="left",
            va="center",
            style="italic",
        )


def _decision(ax, x, y, text, w=2.4, h=0.75, fontsize=7):
    """Draw a diamond decision box."""
    pts = np.array(
        [[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y], [x, y + h / 2]]
    )
    ax.fill(
        pts[:, 0], pts[:, 1], color=C_DEC, edgecolor=C_EDGE, linewidth=1.2, zorder=3
    )
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color="black",
        zorder=4,
        fontfamily=FONT,
        wrap=True,
    )


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


# ════════════════════════════════════════════════════════════════════
#  1. USER FLOWCHART
# ════════════════════════════════════════════════════════════════════
def gen_user_flowchart():
    fig, ax = plt.subplots(figsize=(8, 14))
    ax.set_xlim(-3, 7)
    ax.set_ylim(-16, 1.5)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    nodes = [
        (2, 0.5, "Start", C_START, "stadium"),
        (2, -0.7, "Register / Login", C_PROC, "round"),
        (2, -1.9, "Browse & Search Videos", C_PROC, "round"),
        (2, -3.1, "Select & Watch Video", C_PROC, "round"),
    ]
    for x, y, t, c, s in nodes:
        _box(ax, x, y, t, c, shape=s)

    # arrows between nodes
    _arrow(ax, 2, 0.22, 2, -0.42)
    _arrow(ax, 2, -0.98, 2, -1.62)
    _arrow(ax, 2, -2.18, 2, -2.82)
    _arrow(ax, 2, -3.38, 2, -3.9)

    # Decision: Add to playlist?
    _decision(ax, 2, -4.3, "Add to\nPlaylist?")
    _arrow(ax, 2, -4.68, 2, -5.2)  # No → down
    ax.text(2.15, -4.95, "No", fontsize=7, color="red", fontfamily=FONT)
    _arrow(ax, 3.2, -4.3, 5, -4.3, style="->")  # Yes → right
    ax.text(3.5, -4.1, "Yes", fontsize=7, color=C_START, fontfamily=FONT)
    _box(ax, 5, -4.3, "Save to Playlist", C_IO, w=2.0, textcolor="white")
    _arrow(ax, 5, -4.58, 5, -5.5, style="->")
    _arrow(ax, 5, -5.5, 2, -5.5, style="->")

    # Decision: Like the video?
    _decision(ax, 2, -5.6, "Like the\nVideo?")
    _arrow(ax, 2, -5.98, 2, -6.5)  # Yes
    ax.text(2.15, -6.25, "Yes", fontsize=7, color=C_START, fontfamily=FONT)
    _arrow(ax, 0.8, -5.6, -0.5, -5.6, style="->")  # No → left
    ax.text(-0.1, -5.4, "No", fontsize=7, color="red", fontfamily=FONT)
    _box(ax, -0.5, -6.5, "Dislike Video", "#E53935", w=1.8, textcolor="white")
    _arrow(ax, -0.5, -5.88, -0.5, -6.22)

    # Like
    _box(ax, 2, -6.8, "Like Video", C_START, w=1.8)
    _arrow(ax, 2, -7.08, 2, -7.5)

    # Decision: Leave comment?
    _decision(ax, 2, -7.9, "Leave a\nComment?")
    _arrow(ax, 2, -8.28, 2, -8.8)
    ax.text(2.15, -8.55, "Yes", fontsize=7, color=C_START, fontfamily=FONT)
    _box(ax, 2, -9.1, "Post Comment", C_PROC, w=1.8)
    _arrow(ax, 2, -9.38, 2, -9.8)

    # Decision: Subscribe?
    _decision(ax, 2, -10.2, "Subscribe to\nCreator?")
    _arrow(ax, 3.2, -10.2, 5, -10.2, style="->")
    ax.text(3.5, -10.0, "Yes", fontsize=7, color=C_START, fontfamily=FONT)
    _box(ax, 5, -10.2, "Subscribe", C_PROC, w=1.8)

    _arrow(ax, 2, -10.58, 2, -11.1)
    ax.text(2.15, -10.85, "No", fontsize=7, color="red", fontfamily=FONT)

    # Continue watching / recommendations
    _box(ax, 2, -11.4, "Continue Watching", C_PROC, w=2.2)
    _arrow(ax, 2, -11.68, 2, -12.2)
    _box(ax, 2, -12.5, "Get Recommendations", C_IO, w=2.2, textcolor="white")
    _arrow(ax, 2, -12.78, 2, -13.3)

    # End
    _box(ax, 2, -13.6, "End", C_START, w=1.4, shape="stadium")

    # "No" path from comment goes around
    _arrow(ax, 3.2, -7.9, 4.2, -7.9, style="->")
    ax.text(3.5, -7.7, "No", fontsize=7, color="red", fontfamily=FONT)
    ax.plot([4.2, 4.2], [-7.9, -9.8], color=C_EDGE, lw=1.2, zorder=2)
    ax.annotate(
        "",
        xy=(2, -9.8),
        xytext=(4.2, -9.8),
        arrowprops=dict(arrowstyle="->", color=C_EDGE, lw=1.2),
    )

    # Watch later from dislike
    _arrow(ax, -0.5, -6.78, -0.5, -7.2)
    _box(ax, -0.5, -7.5, "Watch Later", C_IO, w=1.8, textcolor="white")

    ax.set_title(
        "User's Flowchart", fontsize=14, fontweight="bold", fontfamily=FONT, pad=10
    )
    _save(fig, "user-flowchart.png")


# ════════════════════════════════════════════════════════════════════
#  2. CREATOR FLOWCHART
# ════════════════════════════════════════════════════════════════════
def gen_creator_flowchart():
    fig, ax = plt.subplots(figsize=(8, 14))
    ax.set_xlim(-3, 8)
    ax.set_ylim(-15, 1.5)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    _box(ax, 2.5, 0.5, "Start", C_START, w=1.5, shape="stadium")
    _arrow(ax, 2.5, 0.22, 2.5, -0.3)
    _box(ax, 2.5, -0.6, "Register / Login", C_PROC)
    _arrow(ax, 2.5, -0.88, 2.5, -1.4)

    # Decision: Edit or Upload?
    _decision(ax, 2.5, -1.8, "Edit Existing\nor Upload New?", w=2.8, h=0.8)

    # Edit → left
    _arrow(ax, 1.1, -1.8, -0.5, -1.8, style="->")
    ax.text(0.0, -1.6, "Edit", fontsize=7, color=C_PROC, fontfamily=FONT)
    _box(ax, -0.5, -2.8, "Open Dashboard", C_PROC, w=2.0)
    _arrow(ax, -0.5, -2.1, -0.5, -2.52)
    _box(ax, -0.5, -3.8, "Edit Video Details", C_PROC, w=2.0)
    _arrow(ax, -0.5, -3.08, -0.5, -3.52)
    _arrow(ax, -0.5, -4.08, -0.5, -5.0)
    ax.plot([-0.5, 2.5], [-5.0, -5.0], color=C_EDGE, lw=1.2)

    # Upload → right / down
    _arrow(ax, 2.5, -2.2, 2.5, -2.8)
    ax.text(2.65, -2.5, "Upload", fontsize=7, color=C_PROC, fontfamily=FONT)
    _box(ax, 2.5, -3.1, "Upload Video File", C_PROC)
    _arrow(ax, 2.5, -3.38, 2.5, -3.9)

    # Decision: Use AI?
    _decision(ax, 2.5, -4.3, "Use AI for\nThumbnail & Title?", w=2.8, h=0.8)
    # Yes
    _arrow(ax, 3.9, -4.3, 5.5, -4.3, style="->")
    ax.text(4.2, -4.1, "Yes", fontsize=7, color=C_START, fontfamily=FONT)
    _box(
        ax,
        5.5,
        -4.3,
        "AI Generates\nThumbnail & Title",
        C_IO,
        w=2.2,
        h=0.65,
        textcolor="white",
    )
    _arrow(ax, 5.5, -4.63, 5.5, -5.5)
    ax.plot([5.5, 2.5], [-5.5, -5.5], color=C_EDGE, lw=1.2)

    # No
    _arrow(ax, 1.1, -4.3, -0.8, -4.3, style="->")
    ax.text(0.5, -4.1, "No", fontsize=7, color="red", fontfamily=FONT)
    _box(ax, -0.8, -4.7, "Enter Manually", C_PROC, w=2.0)
    _arrow(ax, -0.8, -4.42, -0.8, -4.42)
    # route manual back
    _arrow(ax, -0.8, -4.98, -0.8, -5.5)
    ax.plot([-0.8, 2.5], [-5.5, -5.5], color=C_EDGE, lw=1.2)

    # Publish
    _arrow(ax, 2.5, -5.5, 2.5, -5.9)
    _box(ax, 2.5, -6.2, "Publish Video", C_START, w=2.0)
    _arrow(ax, 2.5, -6.48, 2.5, -7.0)

    # View stats
    _box(
        ax,
        2.5,
        -7.3,
        "View Statistics\n& Reports",
        C_IO,
        w=2.2,
        h=0.65,
        textcolor="white",
    )
    _arrow(ax, 2.5, -7.63, 2.5, -8.2)

    # Reply to comments
    _box(ax, 2.5, -8.5, "Reply to Comments", C_PROC)
    _arrow(ax, 2.5, -8.78, 2.5, -9.3)

    # End
    _box(ax, 2.5, -9.6, "End", C_START, w=1.5, shape="stadium")

    ax.set_title(
        "Creator's Flowchart", fontsize=14, fontweight="bold", fontfamily=FONT, pad=10
    )
    _save(fig, "creator-flowchart.png")


# ════════════════════════════════════════════════════════════════════
#  USE CASE DIAGRAM HELPERS
# ════════════════════════════════════════════════════════════════════
def _actor(ax, x, y, label, color=C_ACTOR):
    """Draw a stick-figure actor."""
    # head
    head = plt.Circle(
        (x, y + 0.35), 0.15, fill=False, edgecolor=color, lw=1.5, zorder=5
    )
    ax.add_patch(head)
    # body
    ax.plot([x, x], [y + 0.2, y - 0.15], color=color, lw=1.5, zorder=5)
    # arms
    ax.plot([x - 0.2, x + 0.2], [y + 0.08, y + 0.08], color=color, lw=1.5, zorder=5)
    # legs
    ax.plot([x, x - 0.2], [y - 0.15, y - 0.4], color=color, lw=1.5, zorder=5)
    ax.plot([x, x + 0.2], [y - 0.15, y - 0.4], color=color, lw=1.5, zorder=5)
    # label
    ax.text(
        x,
        y - 0.6,
        label,
        ha="center",
        va="top",
        fontsize=9,
        fontweight="bold",
        color=color,
        fontfamily=FONT,
        zorder=5,
    )


def _usecase(ax, x, y, text, w=2.2, h=0.52, fontsize=8):
    """Draw a use-case ellipse."""
    e = Ellipse(
        (x, y), w, h, facecolor=C_UC, edgecolor=C_UC_BD, linewidth=1.3, zorder=3
    )
    ax.add_patch(e)
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#0D47A1",
        fontfamily=FONT,
        fontweight="bold",
        zorder=4,
    )


def _uc_line(ax, x1, y1, x2, y2):
    """Line from actor to use-case."""
    ax.plot([x1, x2], [y1, y2], color=C_UC_BD, lw=1.0, zorder=2)


# ════════════════════════════════════════════════════════════════════
#  3. USER USE CASE DIAGRAM
# ════════════════════════════════════════════════════════════════════
def gen_user_usecase():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-2, 10)
    ax.set_ylim(-5, 3)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    # System boundary
    rect = FancyBboxPatch(
        (2, -4.5),
        6.5,
        7,
        boxstyle="round,pad=0.2",
        facecolor=C_SYS,
        edgecolor=C_UC_BD,
        linewidth=1.5,
        zorder=1,
        alpha=0.4,
    )
    ax.add_patch(rect)
    ax.text(
        5.25,
        2.2,
        "NepTube Platform",
        ha="center",
        fontsize=11,
        fontweight="bold",
        color=C_UC_BD,
        fontfamily=FONT,
    )

    # Actor
    _actor(ax, 0.5, 0, "Viewer")

    # Use cases
    cases = [
        (5, 2.0, "Login / Logout"),
        (5, 1.2, "Search & Browse Videos"),
        (5, 0.4, "Watch Video"),
        (5, -0.4, "Like / Dislike Video"),
        (5, -1.2, "Comment on Video"),
        (5, -2.0, "Subscribe to Channel"),
        (5, -2.8, "Add/Remove from Playlist"),
        (5, -3.6, "View Recommendations"),
    ]
    for x, y, t in cases:
        _usecase(ax, x, y, t, w=2.8)
        _uc_line(ax, 0.7, 0, x - 1.4, y)

    ax.set_title(
        "User's Use Case Diagram",
        fontsize=14,
        fontweight="bold",
        fontfamily=FONT,
        pad=10,
    )
    _save(fig, "user-usecase.png")


# ════════════════════════════════════════════════════════════════════
#  4. CREATOR USE CASE DIAGRAM
# ════════════════════════════════════════════════════════════════════
def gen_creator_usecase():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-2, 10)
    ax.set_ylim(-5, 3)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    rect = FancyBboxPatch(
        (2, -4.5),
        6.5,
        7,
        boxstyle="round,pad=0.2",
        facecolor=C_SYS,
        edgecolor=C_UC_BD,
        linewidth=1.5,
        zorder=1,
        alpha=0.4,
    )
    ax.add_patch(rect)
    ax.text(
        5.25,
        2.2,
        "NepTube Platform",
        ha="center",
        fontsize=11,
        fontweight="bold",
        color=C_UC_BD,
        fontfamily=FONT,
    )

    _actor(ax, 0.5, 0, "Creator")

    cases = [
        (5, 2.0, "Login / Logout"),
        (5, 1.2, "Upload Video"),
        (5, 0.4, "Remove Video"),
        (5, -0.4, "Edit Video Metadata"),
        (5, -1.2, "Change Thumbnail"),
        (5, -2.0, "View Analytics"),
        (5, -2.8, "Delete Comments"),
        (5, -3.6, "Respond to Comments"),
    ]
    for x, y, t in cases:
        _usecase(ax, x, y, t, w=2.8)
        _uc_line(ax, 0.7, 0, x - 1.4, y)

    ax.set_title(
        "Creator's Use Case Diagram",
        fontsize=14,
        fontweight="bold",
        fontfamily=FONT,
        pad=10,
    )
    _save(fig, "creator-usecase.png")


# ════════════════════════════════════════════════════════════════════
#  5. ADMIN USE CASE DIAGRAM
# ════════════════════════════════════════════════════════════════════
def gen_admin_usecase():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-2, 10)
    ax.set_ylim(-5.5, 3)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    rect = FancyBboxPatch(
        (2, -5),
        6.5,
        7.5,
        boxstyle="round,pad=0.2",
        facecolor=C_SYS,
        edgecolor=C_UC_BD,
        linewidth=1.5,
        zorder=1,
        alpha=0.4,
    )
    ax.add_patch(rect)
    ax.text(
        5.25,
        2.2,
        "NepTube Platform",
        ha="center",
        fontsize=11,
        fontweight="bold",
        color=C_UC_BD,
        fontfamily=FONT,
    )

    _actor(ax, 0.5, -0.5, "Admin")

    cases = [
        (5, 2.0, "Login / Logout"),
        (5, 1.2, "View Admin Dashboard"),
        (5, 0.4, "Manage Users\n(Ban/Unban/Roles)"),
        (5, -0.5, "Moderate Content\n(Approve/Reject)"),
        (5, -1.5, "Manage Comments\n(Hide Toxic)"),
        (5, -2.5, "Review Reports"),
        (5, -3.4, "Manage Premium\nSubscriptions"),
        (5, -4.3, "Monitor Analytics"),
    ]
    for x, y, t in cases:
        _usecase(ax, x, y, t, w=3.0, h=0.6, fontsize=7.5)
        _uc_line(ax, 0.7, -0.5, x - 1.5, y)

    ax.set_title(
        "Admin's Use Case Diagram",
        fontsize=14,
        fontweight="bold",
        fontfamily=FONT,
        pad=10,
    )
    _save(fig, "admin-usecase.png")


# ════════════════════════════════════════════════════════════════════
#  SEQUENCE DIAGRAM HELPERS
# ════════════════════════════════════════════════════════════════════
def _seq_participant(ax, x, label, y_top, y_bot, color=C_PROC):
    """Draw a participant box at top and its lifeline."""
    _box(ax, x, y_top, label, color, w=2.0, h=0.5, fontsize=8)
    ax.plot(
        [x, x], [y_top - 0.25, y_bot], color="#BDBDBD", lw=1.0, linestyle="--", zorder=1
    )


def _seq_msg(ax, x1, x2, y, label, fontsize=6.5, dashed=False, self_msg=False):
    """Draw a message arrow in a sequence diagram."""
    style = "->" if not dashed else "->"
    ls = "--" if dashed else "-"
    if self_msg:
        # self-referencing arrow
        offset = 0.6
        ax.annotate(
            "",
            xy=(x1 + 0.05, y - 0.25),
            xytext=(x1 + offset, y - 0.25),
            arrowprops=dict(arrowstyle="->", color=C_MSG, lw=1.0),
        )
        ax.plot([x1, x1 + offset], [y, y], color=C_MSG, lw=1.0, ls=ls)
        ax.plot([x1 + offset, x1 + offset], [y, y - 0.25], color=C_MSG, lw=1.0, ls=ls)
        ax.text(
            x1 + offset + 0.1,
            y - 0.13,
            label,
            fontsize=fontsize,
            color=C_MSG,
            fontfamily=FONT,
            va="center",
        )
    else:
        ax.annotate(
            "",
            xy=(x2, y),
            xytext=(x1, y),
            arrowprops=dict(arrowstyle=style, color=C_MSG, lw=1.0, linestyle=ls),
            zorder=2,
        )
        mid = (x1 + x2) / 2
        ax.text(
            mid,
            y + 0.08,
            label,
            fontsize=fontsize,
            color=C_MSG,
            fontfamily=FONT,
            ha="center",
            va="bottom",
        )


# ════════════════════════════════════════════════════════════════════
#  6. USER SEQUENCE DIAGRAM
# ════════════════════════════════════════════════════════════════════
def gen_user_sequence():
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-13, 1.5)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    # Participants
    px = {"User": 1, "NepTube": 4, "Database": 7.5}
    for name, x in px.items():
        _seq_participant(ax, x, name, 1, -12.5)

    y = 0.3
    msgs = [
        ("User", "NepTube", "Login / Register", False),
        ("NepTube", "Database", "Validate credentials", False),
        ("Database", "NepTube", "Return result", True),
        ("NepTube", "User", "Show homepage", True),
        ("User", "NepTube", "Browse videos", False),
        ("NepTube", "Database", "Fetch video list", False),
        ("Database", "NepTube", "Return videos", True),
        ("NepTube", "User", "Display videos", True),
        ("User", "NepTube", "Select & watch video", False),
        ("NepTube", "Database", "Get video data", False),
        ("Database", "NepTube", "Return video", True),
        ("NepTube", "User", "Play video", True),
        ("User", "NepTube", "Add to playlist", False),
        ("NepTube", "Database", "Save to playlist", False),
        ("Database", "NepTube", "Confirm saved", True),
        ("NepTube", "User", "Show success", True),
        ("User", "NepTube", "Subscribe to creator", False),
        ("NepTube", "Database", "Update subscription", False),
        ("Database", "NepTube", "Confirm", True),
        ("NepTube", "User", "Show subscribed", True),
        ("User", "NepTube", "Like / Dislike video", False),
        ("NepTube", "Database", "Update reaction", False),
        ("Database", "NepTube", "Confirm", True),
        ("User", "NepTube", "Post comment", False),
        ("NepTube", "Database", "Save comment", False),
        ("Database", "NepTube", "Confirm", True),
        ("NepTube", "User", "Show updated comments", True),
    ]

    step = 0.45
    for frm, to, label, dashed in msgs:
        _seq_msg(ax, px[frm], px[to], y, label, dashed=dashed)
        y -= step

    ax.set_title(
        "User's Sequence Diagram",
        fontsize=14,
        fontweight="bold",
        fontfamily=FONT,
        pad=10,
    )
    _save(fig, "user-sequence.png")


# ════════════════════════════════════════════════════════════════════
#  7. ADMIN SEQUENCE DIAGRAM
# ════════════════════════════════════════════════════════════════════
def gen_admin_sequence():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(-1, 14)
    ax.set_ylim(-7, 1.5)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    px = {"Admin": 1.5, "AdminService": 4.5, "Database": 8, "AI Moderation": 11.5}
    for name, x in px.items():
        _seq_participant(
            ax,
            x,
            name,
            1,
            -6.5,
            color=(
                "#C62828"
                if name == "Admin"
                else (
                    "#1565C0"
                    if name == "AdminService"
                    else "#2E7D32" if name == "Database" else "#6A1B9A"
                )
            ),
        )

    msgs = [
        ("Admin", "AdminService", "Initiate content moderation", False),
        ("AdminService", "Database", "Retrieve flagged content", False),
        ("Database", "AdminService", "Return flagged items", True),
        ("AdminService", "AI Moderation", "Send content for analysis", False),
        ("AI Moderation", "AdminService", "Return verdict (toxicity, category)", True),
        ("AdminService", "Database", "Update content status", False),
        ("Database", "AdminService", "Confirm update", True),
        ("AdminService", "Admin", "Notify moderation complete", True),
    ]

    y = 0.2
    step = 0.6
    for frm, to, label, dashed in msgs:
        _seq_msg(ax, px[frm], px[to], y, label, fontsize=7, dashed=dashed)
        y -= step

    ax.set_title(
        "Admin's Sequence Diagram",
        fontsize=14,
        fontweight="bold",
        fontfamily=FONT,
        pad=10,
    )
    _save(fig, "admin-sequence.png")


# ════════════════════════════════════════════════════════════════════
#  8. CREATOR SEQUENCE DIAGRAM
# ════════════════════════════════════════════════════════════════════
def gen_creator_sequence():
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-15, 1.5)
    ax.axis("off")
    ax.set_aspect("equal")
    fig.patch.set_facecolor("white")

    px = {"Creator": 1, "NepTube": 4, "Database": 7.5}
    for name, x in px.items():
        _seq_participant(
            ax, x, name, 1, -14.5, color="#E65100" if name == "Creator" else C_PROC
        )

    msgs = [
        ("Creator", "NepTube", "Login / Register", False),
        ("NepTube", "Database", "Validate credentials", False),
        ("Database", "NepTube", "Return result", True),
        ("NepTube", "Creator", "Show creator dashboard", True),
        ("Creator", "NepTube", "Upload new video", False),
        ("NepTube", "Database", "Store video metadata", False),
        ("Database", "NepTube", "Confirm stored", True),
        ("NepTube", "Creator", "Show upload success", True),
        ("Creator", "NepTube", "Edit video details", False),
        ("NepTube", "Database", "Update video metadata", False),
        ("Database", "NepTube", "Confirm updated", True),
        ("NepTube", "Creator", "Show updated details", True),
        ("Creator", "NepTube", "Reply to comment", False),
        ("NepTube", "Database", "Save reply", False),
        ("Database", "NepTube", "Confirm saved", True),
        ("NepTube", "Creator", "Show updated comments", True),
        ("Creator", "NepTube", "Request analytics", False),
        ("NepTube", "Database", "Fetch analytics data", False),
        ("Database", "NepTube", "Return stats", True),
        ("NepTube", "Creator", "Display analytics dashboard", True),
    ]

    y = 0.3
    step = 0.55
    # Add group labels
    groups = [
        (0, 3, "Authentication"),
        (4, 7, "Video Upload"),
        (8, 11, "Edit Video"),
        (12, 15, "Comment Reply"),
        (16, 19, "View Analytics"),
    ]

    for frm, to, label, dashed in msgs:
        _seq_msg(ax, px[frm], px[to], y, label, dashed=dashed)
        y -= step

    ax.set_title(
        "Creator's Sequence Diagram",
        fontsize=14,
        fontweight="bold",
        fontfamily=FONT,
        pad=10,
    )
    _save(fig, "creator-sequence.png")


# ════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Generating NepTube report diagrams ...")
    gen_user_flowchart()
    gen_creator_flowchart()
    gen_user_usecase()
    gen_creator_usecase()
    gen_admin_usecase()
    gen_user_sequence()
    gen_admin_sequence()
    gen_creator_sequence()
    print("Done – all 8 diagrams saved to", OUT)
