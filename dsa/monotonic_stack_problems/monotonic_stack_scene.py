"""Manim remake of the hand-drawn monotonic-stack walkthrough.

Mirrors the iPad recording beat for beat: title, index row, array row,
a cursor sweeping left to right, entries pushed as (value, index) pairs,
blue arcs firing back from the popping element to each entry it resolves,
and the answer row filling in to [2, 2, 5, 5, 5, -1].

Render:
    manim -qh --format=mp4 monotonic_stack_scene.py MonotonicStack
    MS_GRID=0 manim -qh -t monotonic_stack_scene.py MonotonicStack   # alpha .mov

manim lives in pyenv 3.10.9, not the project .venv:
    /Users/orb/.pyenv/versions/3.10.9/bin/manim
"""

import os

from manim import *

# The paper-dot grid is drawn geometry, not background, so --transparent keeps
# it. Set MS_GRID=0 to drop it and let the ink float on real alpha.
SHOW_GRID = os.environ.get("MS_GRID", "1") == "1"

# --- match the recording's canvas ------------------------------------------
config.pixel_width = 1250
config.pixel_height = 900
config.frame_height = 8.0
config.frame_width = 8.0 * 1250 / 900
config.frame_rate = 30
config.background_color = "#363236"

INK_RED = "#E05356"
INK_BLUE = "#0F72E2"
INK_YELLOW = "#F1F11F"
DOT_GREY = "#69676A"
HAND = "Bradley Hand"

NUMS = [4, 1, 6, 3, 2, 7]

COLS = [-3.4 + 1.66 * i for i in range(6)]
Y_IDX = 2.66
Y_ARR = 1.15
Y_RES = -0.35
Y_STK = -1.86
DY_STK = 0.84
X_VAL = -3.55
X_TAG = -2.65


def hand(text, color, size=54):
    return Text(str(text), font=HAND, color=color, font_size=size)


class MonotonicStack(Scene):
    def construct(self):
        self.draw_grid()
        self.draw_board()

        self.stack = []        # list of (value, index, VGroup) bottom-of-list = top of stack
        self.answers = {}
        self.cursor = None

        for i, v in enumerate(NUMS):
            self.move_cursor(i)
            if self.stack and self.stack[-1][0] < v:
                self.resolve(i, v)
            self.push(i, v)

        self.finish()

    # -- static scaffolding --------------------------------------------------
    def draw_grid(self):
        if not SHOW_GRID:
            return
        dots = VGroup()
        x = -config.frame_width / 2
        while x < config.frame_width / 2:
            y = -4.0
            while y < 4.0:
                dots.add(Dot(point=[x, y, 0], radius=0.018, color=DOT_GREY))
                y += 0.62
            x += 0.62
        self.add(dots.set_opacity(0.55))

    def draw_board(self):
        title = hand("MONOTONIC STACK", INK_BLUE, 62).move_to([-0.1, 3.45, 0])
        self.play(Write(title, run_time=2.2))

        self.idx = VGroup()
        for i in range(6):
            self.idx.add(hand(i, INK_YELLOW).move_to([COLS[i], Y_IDX, 0]))
        self.play(Write(self.idx, run_time=1.8))

        self.arr = VGroup()
        for i, v in enumerate(NUMS):
            self.arr.add(hand(v, INK_RED, 62).move_to([COLS[i], Y_ARR, 0]))
        self.play(Write(self.arr, run_time=2.4))
        self.wait(0.4)

    # -- beats ---------------------------------------------------------------
    def move_cursor(self, i):
        tip = Arrow(
            start=[COLS[i], Y_RES - 0.42, 0],
            end=[COLS[i], Y_RES + 0.42, 0],
            buff=0,
            color=INK_BLUE,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.45,
        )
        if self.cursor is None:
            self.cursor = tip
            self.play(GrowArrow(self.cursor), run_time=0.7)
        else:
            self.play(self.cursor.animate.move_to(tip.get_center()), run_time=0.7)
        self.wait(0.5)

    def push(self, i, v):
        row = VGroup(
            hand(v, INK_RED).move_to([X_VAL, Y_STK - DY_STK * len(self.stack), 0]),
            hand(i, INK_YELLOW).move_to([X_TAG, Y_STK - DY_STK * len(self.stack), 0]),
        )
        self.stack.append((v, i, row))
        self.play(Write(row, run_time=1.0))
        self.wait(0.6)

    def resolve(self, i, v):
        """Everything the arriving value v at index i pops."""
        top_row = self.stack[-1][2]
        sweep = CurvedArrow(
            self.arr[i].get_bottom() + DOWN * 0.12,
            top_row.get_right() + RIGHT * 0.45,
            angle=-2.1,
            color=INK_BLUE,
            stroke_width=6,
            tip_length=0.22,
        )
        self.play(Create(sweep), run_time=1.4)

        cmp = hand(f"{v} > {self.stack[-1][0]}", INK_BLUE, 46)
        cmp.next_to(top_row, RIGHT, buff=1.55)
        rule = Underline(cmp, color=INK_BLUE, stroke_width=5)
        self.play(Write(cmp, run_time=1.0))
        self.play(Create(rule), run_time=0.5)

        pop = hand("POP!", INK_BLUE, 46).next_to(cmp, UP, buff=0.45).shift(RIGHT * 0.85)
        self.play(FadeIn(pop, shift=UP * 0.2), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(cmp), FadeOut(rule), FadeOut(pop), FadeOut(sweep), run_time=0.5)

        while self.stack and self.stack[-1][0] < v:
            _, tag, row = self.stack.pop()
            arc = CurvedArrow(
                self.idx[i].get_bottom() + DOWN * 0.1,
                self.arr[tag].get_bottom() + DOWN * 0.15,
                angle=1.5,
                color=INK_BLUE,
                stroke_width=6,
                tip_length=0.2,
            )
            ans = hand(i, INK_BLUE).move_to([COLS[tag], Y_RES, 0])
            self.answers[tag] = ans
            self.play(Create(arc), run_time=0.9)
            self.play(Write(ans), FadeOut(row), run_time=0.8)
            self.wait(0.45)
            self.play(FadeOut(arc), run_time=0.4)

        # entries left behind slide down to close the gap
        if self.stack:
            self.play(
                *[
                    row.animate.move_to([row.get_center()[0], Y_STK - DY_STK * k, 0])
                    for k, (_, _, row) in enumerate(self.stack)
                ],
                run_time=0.5,
            )

    def finish(self):
        """Whatever survives the sweep never finds a greater element."""
        leftovers = []
        for _, tag, row in self.stack:
            ans = hand("-1", INK_BLUE).move_to([COLS[tag], Y_RES, 0])
            self.answers[tag] = ans
            leftovers.append((ans, row))

        for ans, row in leftovers:
            self.play(Write(ans), FadeOut(row), run_time=0.8)

        self.play(FadeOut(self.cursor), run_time=0.6)
        self.wait(2.5)
