"""
Hamming [7,4,3]_2 — Professional 3B1B-style animation
======================================================
Render commands:
  manim -pql hamming_animation.py HammingFull        # low-quality preview
  manim -pqm hamming_animation.py HammingFull        # medium
  manim -pqh hamming_animation.py HammingFull        # high quality
  manim -pql hamming_animation.py <SceneName>        # individual scene
"""

from manim import *
import numpy as np

# ─── Palette ────────────────────────────────────────────────────────────────
BG       = "#0d1117"
DATA_C   = "#58a6ff"   # blue  – data bits
PAR_C    = "#3fb950"   # green – parity bits
ERR_C    = "#f85149"   # red   – error
SYN_C    = "#d2a8ff"   # purple – syndrome
CORR_C   = "#ffa657"   # orange – correction / codeword
DIM_C    = "#8b949e"   # grey  – background elements

# ─── Hamming [7,4,3] constants ───────────────────────────────────────────────
H = np.array([
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
], dtype=int)

PARITY_IDX = [0, 1, 3]      # 0-indexed positions of p1, p2, p4
DATA_IDX   = [2, 4, 5, 6]   # 0-indexed positions of d3, d5, d6, d7

# position j (1-indexed) → syndrome vertex (column j-1 of H as tuple)
J_TO_VERTEX = {j: tuple(H[:, j-1].tolist()) for j in range(1, 8)}
VERTEX_TO_J = {v: j for j, v in J_TO_VERTEX.items()}

CUBE_VERTS = [(x, y, z) for x in [0, 1] for y in [0, 1] for z in [0, 1]]


def hamming_encode(d: list) -> np.ndarray:
    c = np.zeros(7, dtype=int)
    c[2], c[4], c[5], c[6] = d
    c[0] = (c[2] ^ c[4] ^ c[6]) % 2
    c[1] = (c[2] ^ c[5] ^ c[6]) % 2
    c[3] = (c[4] ^ c[5] ^ c[6]) % 2
    return c


def syndrome(y: np.ndarray) -> np.ndarray:
    return (H @ y) % 2


# ─── Reusable helpers ────────────────────────────────────────────────────────

def bit_rect(size=0.52, stroke_color=WHITE, fill_color=BLACK, fill_opacity=0.0):
    return RoundedRectangle(
        corner_radius=0.07, height=size, width=size,
        stroke_width=2.2, stroke_color=stroke_color,
        fill_color=fill_color, fill_opacity=fill_opacity,
    )


class BitRow(VGroup):
    """A horizontal row of labelled bit cells."""

    def __init__(self, bits, size=0.52, buff=0.09,
                 bit_color=WHITE, stroke_color=DIM_C, fs=28):
        super().__init__()
        self.n = len(bits)
        self._fs = fs
        self.cells  = VGroup()
        self.labels = VGroup()
        for b in bits:
            r = bit_rect(size, stroke_color)
            l = MathTex(str(b), font_size=fs, color=bit_color).move_to(r)
            self.cells.add(r)
            self.labels.add(l)
        self.cells.arrange(RIGHT, buff=buff)
        for i in range(self.n):
            self.labels[i].move_to(self.cells[i])
        self.add(self.cells, self.labels)

    # ---- convenience ----
    def cell(self, i):  return self.cells[i]
    def label(self, i): return self.labels[i]

    def color_cell(self, i, color, opacity=0.18):
        self.cells[i].set_stroke(color=color, width=2.8)
        self.cells[i].set_fill(color=color, opacity=opacity)
        self.labels[i].set_color(color)

    def anim_set_bit(self, scene, i, val, color=YELLOW, rt=0.35):
        new = MathTex(str(val), font_size=self._fs, color=color).move_to(self.labels[i])
        scene.play(
            Transform(self.labels[i], new),
            self.cells[i].animate.set_stroke(color=color, width=3).set_fill(color=color, opacity=0.2),
            run_time=rt,
        )


def cube_proj(v, origin=ORIGIN, sx=1.5, sy=1.5, sz=0.72):
    x, y, z = v
    return origin + np.array([sx*x + sz*z, sy*y + 0.55*sz*z, 0.0])


def build_cube(origin=ORIGIN, sx=1.5, sy=1.5, sz=0.72, dot_r=0.075):
    def p(v): return cube_proj(v, origin, sx, sy, sz)

    dot_map = {}
    dots = VGroup()
    for v in CUBE_VERTS:
        col = DIM_C if v == (0,0,0) else WHITE
        d = Dot(p(v), radius=dot_r, color=col)
        dots.add(d)
        dot_map[v] = d

    edges = VGroup()
    for i, v in enumerate(CUBE_VERTS):
        for j, w in enumerate(CUBE_VERTS):
            if j <= i: continue
            if sum(abs(v[k]-w[k]) for k in range(3)) == 1:
                e = Line(p(v), p(w), stroke_width=1.6, color=DIM_C, stroke_opacity=0.55)
                edges.add(e)

    lbl_map = {}
    lbls = VGroup()
    for v in CUBE_VERTS:
        l = MathTex(f"{v[0]}{v[1]}{v[2]}", font_size=19, color=DIM_C)
        l.next_to(dot_map[v], RIGHT, buff=0.07)
        lbls.add(l)
        lbl_map[v] = l

    return VGroup(edges, dots, lbls), dot_map, lbl_map


# ────────────────────────────────────────────────────────────────────────────
# SCENE 1 – Title
# ────────────────────────────────────────────────────────────────────────────
class S1_Title(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Hamming Codes", font_size=76, weight=BOLD, color=WHITE)
        code  = MathTex(r"[7,\,4,\,3]_2", font_size=52, color=DATA_C)
        sub   = Text("How to find and fix a corrupted bit", font_size=30, color=DIM_C)

        VGroup(title, code, sub).arrange(DOWN, buff=0.45).move_to(ORIGIN)

        self.play(Write(title, run_time=1.1))
        self.play(FadeIn(code, shift=UP*0.25), run_time=0.65)
        self.play(FadeIn(sub,  shift=UP*0.25), run_time=0.65)
        self.wait(1.1)
        self.play(FadeOut(VGroup(title, code, sub)), run_time=0.7)


# ────────────────────────────────────────────────────────────────────────────
# SCENE 2 – The problem: a noisy channel flips a bit
# ────────────────────────────────────────────────────────────────────────────
class S2_NoisyChannel(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── header ──
        hdr = Text("The Problem", font_size=40, color=WHITE).to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        # ── Alice & Bob nodes ──
        def node(label, color):
            circle = Circle(radius=0.55, color=color,
                            fill_opacity=0.12, stroke_width=2.8)
            text = Text(label, font_size=25, color=color)
            return VGroup(circle, text.move_to(circle))

        alice = node("Alice", DATA_C).move_to(LEFT*5.2 + UP*0.3)
        bob   = node("Bob",   PAR_C ).move_to(RIGHT*5.2 + UP*0.3)

        channel_line = DashedLine(
            alice[0].get_right(), bob[0].get_left(),
            dash_length=0.18, dashed_ratio=0.5,
            stroke_width=1.8, color=DIM_C,
        )
        channel_lbl = Text("noisy channel", font_size=20, color=DIM_C)\
            .next_to(channel_line, UP, buff=0.14)

        self.play(
            FadeIn(alice), FadeIn(bob),
            Create(channel_line), FadeIn(channel_lbl),
            run_time=0.75,
        )

        # ── 4-bit message travelling right ──
        msg = [1, 0, 1, 1]
        bits = VGroup(*[
            MathTex(str(b), font_size=38, color=DATA_C) for b in msg
        ]).arrange(RIGHT, buff=0.28).move_to(alice[0].get_right() + RIGHT*0.7 + UP*0.3)

        self.play(FadeIn(bits, shift=RIGHT*0.2), run_time=0.5)
        self.play(bits.animate.move_to(ORIGIN + UP*0.3), run_time=0.65, rate_func=smooth)

        # ── noise flash on bit index 2 ──
        noise_pos = bits[2].get_center()
        self.play(Flash(noise_pos, color=ERR_C, flash_radius=0.55), run_time=0.4)
        err_bit = MathTex("0", font_size=38, color=ERR_C).move_to(noise_pos)
        self.play(Transform(bits[2], err_bit), run_time=0.3)

        # ── continue to Bob ──
        self.play(bits.animate.move_to(bob[0].get_left() + LEFT*0.7 + UP*0.3),
                  run_time=0.65, rate_func=smooth)
        self.wait(0.3)

        # ── question ──
        q = Text("Which bit was flipped?", font_size=32, color=YELLOW)\
            .to_edge(DOWN, buff=0.9)
        self.play(FadeIn(q, shift=UP*0.25), run_time=0.5)
        self.wait(0.7)

        answer = Text("Hamming's insight: add redundancy cleverly.",
                      font_size=26, color=DIM_C)\
            .next_to(q, DOWN, buff=0.25)
        self.play(FadeIn(answer, shift=UP*0.2), run_time=0.5)
        self.wait(1.0)

        self.play(
            FadeOut(VGroup(hdr, alice, bob, channel_line, channel_lbl,
                           bits, q, answer)),
            run_time=0.7,
        )


# ────────────────────────────────────────────────────────────────────────────
# SCENE 3 – Bit positions: powers-of-2 are parity, rest are data
# ────────────────────────────────────────────────────────────────────────────
class S3_Positions(Scene):
    def construct(self):
        self.camera.background_color = BG

        hdr = Text("Bit Positions: The Key Idea", font_size=40, color=WHITE)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        # ── 7 slots ──
        cells = VGroup(*[bit_rect(0.64, DIM_C) for _ in range(7)])\
            .arrange(RIGHT, buff=0.22).move_to(UP*0.8)
        pos_nums = VGroup(*[
            MathTex(str(i+1), font_size=22, color=DIM_C).next_to(cells[i], DOWN, buff=0.12)
            for i in range(7)
        ])
        pos_lbl = Text("position:", font_size=22, color=DIM_C)\
            .next_to(pos_nums, LEFT, buff=0.3).align_to(pos_nums[0], DOWN)

        self.play(FadeIn(cells), FadeIn(pos_nums), FadeIn(pos_lbl), run_time=0.6)
        self.wait(0.2)

        # ── mark parity positions (1, 2, 4) ──
        parity_note = Text("Parity positions = powers of 2", font_size=26, color=PAR_C)\
            .to_edge(DOWN, buff=1.1)
        self.play(FadeIn(parity_note, shift=UP*0.2), run_time=0.4)

        p_labels = ["p_1", "p_2", "p_4"]
        for k, i in enumerate(PARITY_IDX):
            cells[i].set_stroke(color=PAR_C, width=3).set_fill(color=PAR_C, opacity=0.18)
            lbl = MathTex(p_labels[k], font_size=24, color=PAR_C).move_to(cells[i])
            self.play(FadeIn(lbl), run_time=0.25)

        self.wait(0.35)

        # ── mark data positions (3, 5, 6, 7) ──
        data_note = Text("Data positions = everything else", font_size=26, color=DATA_C)\
            .next_to(parity_note, DOWN, buff=0.2)
        self.play(FadeIn(data_note, shift=UP*0.2), run_time=0.4)

        demo_data = [1, 0, 1, 1]
        for k, i in enumerate(DATA_IDX):
            cells[i].set_stroke(color=DATA_C, width=3).set_fill(color=DATA_C, opacity=0.18)
            lbl = MathTex(str(demo_data[k]), font_size=28, color=DATA_C).move_to(cells[i])
            self.play(FadeIn(lbl), run_time=0.25)

        self.wait(0.4)

        # ── binary addresses of each position ──
        bin_note = Tex(
            r"Each position $j$ has a 3-bit binary address:",
            font_size=26, color=GREY_A,
        ).next_to(cells, DOWN, buff=0.8)
        self.play(FadeOut(parity_note), FadeOut(data_note),
                  FadeIn(bin_note, shift=UP*0.2), run_time=0.5)

        bin_lbls = VGroup(*[
            MathTex(format(i+1, "03b"), font_size=19, color=SYN_C)\
                .next_to(pos_nums[i], DOWN, buff=0.1)
            for i in range(7)
        ])
        self.play(
            LaggedStart(*[FadeIn(b, shift=UP*0.1) for b in bin_lbls], lag_ratio=0.1),
            run_time=0.8,
        )

        insight = Tex(
            r"Parity bit $p_k$ = XOR of all bits whose position has a \textbf{1} in bit $k$",
            font_size=26, color=YELLOW,
        ).next_to(bin_note, DOWN, buff=0.3)
        self.play(FadeIn(insight, shift=UP*0.2), run_time=0.6)
        self.wait(1.1)

        self.play(FadeOut(VGroup(hdr, cells, pos_nums, pos_lbl, bin_lbls,
                                  bin_note, insight)), run_time=0.7)


# ────────────────────────────────────────────────────────────────────────────
# SCENE 4 – Parity-check matrix H
# ────────────────────────────────────────────────────────────────────────────
class S4_Matrix(Scene):
    def construct(self):
        self.camera.background_color = BG

        hdr = Text("The Parity-Check Matrix  H", font_size=40, color=WHITE)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        # ── H matrix ──
        H_tex = MathTex(
            r"H = \begin{pmatrix}"
            r"1 & 0 & 1 & 0 & 1 & 0 & 1 \\"
            r"0 & 1 & 1 & 0 & 0 & 1 & 1 \\"
            r"0 & 0 & 0 & 1 & 1 & 1 & 1"
            r"\end{pmatrix}",
            font_size=38,
        ).move_to(UP*1.3)
        self.play(Write(H_tex, run_time=1.4))

        # ── column annotations: binary numbers 1..7 ──
        col_note = Tex(
            r"Column $j$ of $H$ is the binary representation of $j$",
            font_size=26, color=SYN_C,
        ).next_to(H_tex, DOWN, buff=0.35)
        self.play(FadeIn(col_note, shift=UP*0.2), run_time=0.6)

        # ── syndrome definition ──
        syn_def = MathTex(
            r"\text{syndrome:}\quad s(y) = H y^\top \pmod{2}",
            font_size=34, color=SYN_C,
        ).next_to(col_note, DOWN, buff=0.4)
        self.play(Write(syn_def, run_time=0.9))

        # ── key property ──
        key = Tex(
            r"If $y = c + e_j$ \;(codeword $c$ \,+\, single-bit error at position $j$):\\[4pt]"
            r"$s(y) = Hc^\top + He_j^\top = \mathbf{0} + \text{col}_j(H)$",
            font_size=27, color=CORR_C,
        ).next_to(syn_def, DOWN, buff=0.4)
        self.play(FadeIn(key, shift=UP*0.2), run_time=0.7)
        self.wait(0.4)

        big_idea = Text(
            "The syndrome is exactly the binary address of the bad bit!",
            font_size=26, color=YELLOW, weight=BOLD,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(big_idea, shift=UP*0.25), run_time=0.55)
        self.wait(1.2)

        self.play(FadeOut(VGroup(hdr, H_tex, col_note, syn_def, key, big_idea)),
                  run_time=0.7)


# ────────────────────────────────────────────────────────────────────────────
# SCENE 5 – Full decode pipeline (encode → corrupt → syndrome → correct)
# ────────────────────────────────────────────────────────────────────────────
class S5_DecodePipeline(Scene):
    def construct(self):
        self.camera.background_color = BG

        hdr = Text("Decoding in Action", font_size=40, color=WHITE)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        # ─── 1. Show the codeword ───────────────────────────────────────────
        data    = [1, 0, 1, 1]
        cw      = hamming_encode(data)
        j_err   = 4          # 0-indexed → position 5 (1-indexed)
        cw_copy = cw.copy()
        cw_copy[j_err] ^= 1  # received/corrupted word

        row_y = UP * 1.5
        cw_label = Text("codeword  c :", font_size=24, color=DIM_C)\
            .to_edge(LEFT, buff=0.45).align_to(row_y, UP).shift(DOWN*0.04)
        reg_c = BitRow(cw, size=0.52, buff=0.10, fs=28).next_to(cw_label, RIGHT, buff=0.28)
        reg_c.move_to(row_y + reg_c.get_center() * RIGHT)  # keep vertical

        # colour data vs parity
        for i in PARITY_IDX: reg_c.color_cell(i, PAR_C)
        for i in DATA_IDX:   reg_c.color_cell(i, DATA_C)

        pos_nums_c = VGroup(*[
            MathTex(str(i+1), font_size=17, color=DIM_C)\
                .next_to(reg_c.cell(i), DOWN, buff=0.07)
            for i in range(7)
        ])
        self.play(FadeIn(cw_label), FadeIn(reg_c), FadeIn(pos_nums_c), run_time=0.6)
        self.wait(0.3)

        # ─── 2. Inject error ────────────────────────────────────────────────
        err_lbl = Text(f"error injected at position {j_err+1}  →", font_size=24, color=ERR_C)\
            .to_edge(LEFT, buff=0.45).shift(UP*0.45)
        self.play(FadeIn(err_lbl, shift=RIGHT*0.2), run_time=0.4)

        # copy row for received word
        rec_label = Text("received  y :", font_size=24, color=DIM_C)\
            .move_to(cw_label).shift(DOWN*1.15)
        reg_y = BitRow(cw_copy, size=0.52, buff=0.10, fs=28)\
            .move_to(reg_c).shift(DOWN*1.15)
        for i in PARITY_IDX: reg_y.color_cell(i, PAR_C)
        for i in DATA_IDX:   reg_y.color_cell(i, DATA_C)
        reg_y.color_cell(j_err, ERR_C)

        pos_nums_y = VGroup(*[
            MathTex(str(i+1), font_size=17, color=DIM_C)\
                .next_to(reg_y.cell(i), DOWN, buff=0.07)
            for i in range(7)
        ])
        self.play(
            Flash(reg_c.cell(j_err).get_center(), color=ERR_C, flash_radius=0.48),
            FadeIn(reg_y), FadeIn(rec_label), FadeIn(pos_nums_y),
            run_time=0.65,
        )
        self.wait(0.3)

        # ─── 3. Compute syndrome ────────────────────────────────────────────
        s     = syndrome(cw_copy)
        s_str = "".join(map(str, s))
        s_val = int(s_str, 2)   # should equal j_err+1

        syn_label = Text("syndrome  s :", font_size=24, color=SYN_C)\
            .move_to(rec_label).shift(DOWN*1.15)
        reg_s = BitRow(s, size=0.52, buff=0.10, fs=28, bit_color=SYN_C,
                       stroke_color=SYN_C)\
            .move_to(reg_y).shift(DOWN*1.15)
        for i in range(3):
            reg_s.cell(i).set_stroke(color=SYN_C, width=2.5)\
                         .set_fill(color=SYN_C, opacity=0.14)

        arrow_syn = Arrow(
            reg_y.get_bottom() + DOWN*0.08,
            reg_s.get_top()    + UP*0.08,
            buff=0.04, stroke_width=2.5, color=SYN_C,
            max_tip_length_to_length_ratio=0.2,
        )
        syn_eq = MathTex(
            rf"s = H y^\top = {s_str}_2 = {s_val}",
            font_size=26, color=SYN_C,
        ).next_to(reg_s, RIGHT, buff=0.35)

        self.play(GrowArrow(arrow_syn), run_time=0.35)
        self.play(FadeIn(syn_label), FadeIn(reg_s), Write(syn_eq), run_time=0.65)
        self.wait(0.3)

        # ─── 4. Identify & correct ──────────────────────────────────────────
        identify = Text(
            f"syndrome {s_str}₂ = {s_val}  →  error at bit {s_val}",
            font_size=24, color=CORR_C,
        ).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(identify, shift=UP*0.2), run_time=0.5)

        ring = SurroundingRectangle(reg_y.cell(j_err), color=CORR_C, buff=0.07,
                                    corner_radius=0.07, stroke_width=2.5)
        self.play(Create(ring), run_time=0.35)
        self.wait(0.3)

        # flip it back
        fixed_lbl = MathTex(str(cw[j_err]), font_size=28, color=CORR_C)\
            .move_to(reg_y.label(j_err))
        self.play(
            Transform(reg_y.labels[j_err], fixed_lbl),
            reg_y.cell(j_err).animate
                .set_stroke(color=CORR_C, width=3)
                .set_fill(color=CORR_C, opacity=0.2),
            run_time=0.45,
        )
        self.wait(0.3)

        done = Text("Corrected!", font_size=26, color=YELLOW, weight=BOLD)\
            .next_to(identify, DOWN, buff=0.2)
        self.play(FadeIn(done, shift=UP*0.2), run_time=0.4)
        self.wait(1.0)

        self.play(FadeOut(VGroup(
            hdr, cw_label, reg_c, pos_nums_c, err_lbl,
            rec_label, reg_y, pos_nums_y, arrow_syn,
            syn_label, reg_s, syn_eq,
            identify, ring, done,
        )), run_time=0.75)


# ────────────────────────────────────────────────────────────────────────────
# SCENE 6 – The syndrome cube: F_2^3 visualized
# ────────────────────────────────────────────────────────────────────────────
class S6_CubeFinale(Scene):
    def construct(self):
        self.camera.background_color = BG

        hdr = Text("Syndrome Space  \u2014  the Cube", font_size=40, color=WHITE)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        # ── build cube ──────────────────────────────────────────────────────
        cube_grp, dot_map, lbl_map = build_cube(
            origin=RIGHT*2.2, sx=1.55, sy=1.55, sz=0.75, dot_r=0.08,
        )
        edges, dots, cube_lbls = cube_grp[0], cube_grp[1], cube_grp[2]

        f2_3 = MathTex(r"\mathbb{F}_2^3", font_size=46, color=WHITE)\
            .next_to(cube_grp, UP, buff=0.2)

        self.play(
            LaggedStart(*[Create(e) for e in edges], lag_ratio=0.02),
            run_time=0.8,
        )
        self.play(FadeIn(dots), FadeIn(cube_lbls), FadeIn(f2_3), run_time=0.5)

        # ── origin = kernel ─────────────────────────────────────────────────
        ker_ring = Circle(radius=0.2, color=SYN_C, stroke_width=2.2)\
            .move_to(dot_map[(0,0,0)])
        ker_lbl = MathTex(r"\ker H = C", font_size=22, color=SYN_C)\
            .next_to(dot_map[(0,0,0)], LEFT, buff=0.22)
        dot_map[(0,0,0)].set_color(SYN_C)

        self.play(Create(ker_ring), FadeIn(ker_lbl, shift=RIGHT*0.15), run_time=0.5)
        self.wait(0.2)

        # ── label 7 nonzero vertices with e_j ───────────────────────────────
        j_tags = VGroup()
        for v, j in VERTEX_TO_J.items():
            tag = MathTex(rf"e_{j}", font_size=20, color=ERR_C)\
                .next_to(dot_map[v], RIGHT, buff=0.06)
            j_tags.add(tag)
            dot_map[v].set_color(ERR_C)

        self.play(
            LaggedStart(*[FadeIn(t, shift=LEFT*0.1) for t in j_tags], lag_ratio=0.08),
            run_time=0.8,
        )
        self.play(
            *[Indicate(dot_map[v], color=YELLOW, scale_factor=1.9)
              for v in VERTEX_TO_J],
            run_time=0.7,
        )
        self.wait(0.3)

        # ── left-side explanation ────────────────────────────────────────────
        expl = VGroup(
            Tex(r"7 nonzero vertices", font_size=26, color=ERR_C),
            MathTex(r"\updownarrow", font_size=28, color=DIM_C),
            Tex(r"7 correctable bit positions", font_size=26, color=DATA_C),
            MathTex(r"\updownarrow", font_size=28, color=DIM_C),
            Tex(r"7 distinct single-bit error patterns", font_size=26, color=CORR_C),
        ).arrange(DOWN, buff=0.22).move_to(LEFT*3.2)

        self.play(FadeIn(expl, shift=RIGHT*0.3), run_time=0.8)
        self.wait(0.5)

        # ── coset structure ──────────────────────────────────────────────────
        coset_note = Tex(
            r"$\mathbb{F}_2^7 / C \;\cong\; \mathbb{F}_2^3$"
            r"\quad $\Rightarrow$ \quad 8 cosets $\leftrightarrow$ 8 syndromes",
            font_size=26, color=GREY_A,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(coset_note, shift=UP*0.2), run_time=0.5)
        self.wait(0.8)

        # ── flash a demo: error at j=7 lands on (1,1,1) ─────────────────────
        demo_v = (1, 1, 1)
        demo_j = VERTEX_TO_J[demo_v]
        demo_ring = SurroundingRectangle(dot_map[demo_v], color=YELLOW,
                                          buff=0.12, stroke_width=2.5,
                                          corner_radius=0.12)
        demo_txt = Tex(
            rf"syndrome $111_2 = 7$ $\Rightarrow$ flip bit 7",
            font_size=25, color=YELLOW,
        ).next_to(coset_note, DOWN, buff=0.18)
        self.play(Create(demo_ring), FadeIn(demo_txt, shift=UP*0.15), run_time=0.5)
        self.wait(1.0)

        # ── final summary ────────────────────────────────────────────────────
        summary = Text(
            "[7, 4, 3]₂  —  4 data bits, 3 parity bits, corrects every 1-bit error",
            font_size=24, color=YELLOW, weight=BOLD,
        ).to_edge(DOWN, buff=0.25)
        self.play(
            FadeOut(coset_note), FadeOut(demo_txt), FadeOut(demo_ring),
            FadeIn(summary, shift=UP*0.2),
            run_time=0.7,
        )
        self.wait(1.4)

        self.play(FadeOut(VGroup(
            hdr, cube_grp, f2_3, ker_ring, ker_lbl,
            j_tags, expl, summary,
        )), run_time=0.9)


# ────────────────────────────────────────────────────────────────────────────
# FULL VIDEO — single Scene that inlines every act
# ────────────────────────────────────────────────────────────────────────────
class HammingFull(Scene):
    """Renders the complete Hamming Code story in one video file.

    Each act_* method mirrors the construct() of the matching S*_ class,
    but operates on `self` so Manim's renderer stays consistent.
    """

    def construct(self):
        self.camera.background_color = BG
        self.act1_title()
        self.act2_noisy_channel()
        self.act3_positions()
        self.act4_matrix()
        self.act5_decode()
        self.act6_cube()
        self.wait(0.5)

    # ── Act 1 ────────────────────────────────────────────────────────────────
    def act1_title(self):
        title = Text("Hamming Codes", font_size=76, weight=BOLD, color=WHITE)
        code  = MathTex(r"[7,\,4,\,3]_2", font_size=52, color=DATA_C)
        sub   = Text("How to find and fix a corrupted bit", font_size=30, color=DIM_C)
        VGroup(title, code, sub).arrange(DOWN, buff=0.45).move_to(ORIGIN)

        self.play(Write(title, run_time=1.1))
        self.play(FadeIn(code, shift=UP*0.25), run_time=0.65)
        self.play(FadeIn(sub,  shift=UP*0.25), run_time=0.65)
        self.wait(1.1)
        self.play(FadeOut(VGroup(title, code, sub)), run_time=0.7)

    # ── Act 2 ────────────────────────────────────────────────────────────────
    def act2_noisy_channel(self):
        hdr = Text("The Problem", font_size=40, color=WHITE).to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        def node(label, color):
            c = Circle(radius=0.55, color=color, fill_opacity=0.12, stroke_width=2.8)
            t = Text(label, font_size=25, color=color).move_to(c)
            return VGroup(c, t)

        alice = node("Alice", DATA_C).move_to(LEFT*5.2 + UP*0.3)
        bob   = node("Bob",   PAR_C ).move_to(RIGHT*5.2 + UP*0.3)
        line  = DashedLine(alice[0].get_right(), bob[0].get_left(),
                           dash_length=0.18, dashed_ratio=0.5,
                           stroke_width=1.8, color=DIM_C)
        ch_lbl = Text("noisy channel", font_size=20, color=DIM_C)\
            .next_to(line, UP, buff=0.14)

        self.play(FadeIn(alice), FadeIn(bob), Create(line), FadeIn(ch_lbl), run_time=0.75)

        bits = VGroup(*[MathTex(str(b), font_size=38, color=DATA_C)
                        for b in [1, 0, 1, 1]])\
            .arrange(RIGHT, buff=0.28)\
            .move_to(alice[0].get_right() + RIGHT*0.7 + UP*0.3)

        self.play(FadeIn(bits, shift=RIGHT*0.2), run_time=0.5)
        self.play(bits.animate.move_to(ORIGIN + UP*0.3), run_time=0.65, rate_func=smooth)

        self.play(Flash(bits[2].get_center(), color=ERR_C, flash_radius=0.55), run_time=0.4)
        self.play(Transform(bits[2], MathTex("0", font_size=38, color=ERR_C)
                            .move_to(bits[2])), run_time=0.3)
        self.play(bits.animate.move_to(bob[0].get_left() + LEFT*0.7 + UP*0.3),
                  run_time=0.65, rate_func=smooth)

        q = Text("Which bit was flipped?", font_size=32, color=YELLOW).to_edge(DOWN, buff=0.9)
        ans = Text("Hamming's insight: add redundancy cleverly.", font_size=26, color=DIM_C)\
            .next_to(q, DOWN, buff=0.25)
        self.play(FadeIn(q, shift=UP*0.25), run_time=0.5)
        self.wait(0.5)
        self.play(FadeIn(ans, shift=UP*0.2), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(VGroup(hdr, alice, bob, line, ch_lbl, bits, q, ans)), run_time=0.7)

    # ── Act 3 ────────────────────────────────────────────────────────────────
    def act3_positions(self):
        hdr = Text("Bit Positions: The Key Idea", font_size=40, color=WHITE)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        cells = VGroup(*[bit_rect(0.64, DIM_C) for _ in range(7)])\
            .arrange(RIGHT, buff=0.22).move_to(UP*0.8)
        pos_nums = VGroup(*[
            MathTex(str(i+1), font_size=22, color=DIM_C).next_to(cells[i], DOWN, buff=0.12)
            for i in range(7)
        ])
        pos_lbl = Text("position:", font_size=22, color=DIM_C)\
            .next_to(pos_nums, LEFT, buff=0.3).align_to(pos_nums[0], DOWN)

        self.play(FadeIn(cells), FadeIn(pos_nums), FadeIn(pos_lbl), run_time=0.6)

        parity_note = Text("Parity positions = powers of 2", font_size=26, color=PAR_C)\
            .to_edge(DOWN, buff=1.1)
        self.play(FadeIn(parity_note, shift=UP*0.2), run_time=0.4)

        p_mobjs = VGroup()
        for k, i in enumerate(PARITY_IDX):
            cells[i].set_stroke(color=PAR_C, width=3).set_fill(color=PAR_C, opacity=0.18)
            lbl = MathTex(["p_1","p_2","p_4"][k], font_size=24, color=PAR_C).move_to(cells[i])
            p_mobjs.add(lbl)
            self.play(FadeIn(lbl), run_time=0.25)

        data_note = Text("Data positions = everything else", font_size=26, color=DATA_C)\
            .next_to(parity_note, DOWN, buff=0.2)
        self.play(FadeIn(data_note, shift=UP*0.2), run_time=0.4)

        d_mobjs = VGroup()
        for k, i in enumerate(DATA_IDX):
            cells[i].set_stroke(color=DATA_C, width=3).set_fill(color=DATA_C, opacity=0.18)
            lbl = MathTex(str([1,0,1,1][k]), font_size=28, color=DATA_C).move_to(cells[i])
            d_mobjs.add(lbl)
            self.play(FadeIn(lbl), run_time=0.25)

        bin_note = Tex(r"Each position $j$ has a 3-bit binary address:",
                       font_size=26, color=GREY_A).next_to(cells, DOWN, buff=0.8)
        self.play(FadeOut(parity_note), FadeOut(data_note),
                  FadeIn(bin_note, shift=UP*0.2), run_time=0.5)

        bin_lbls = VGroup(*[
            MathTex(format(i+1, "03b"), font_size=19, color=SYN_C)
            .next_to(pos_nums[i], DOWN, buff=0.1) for i in range(7)
        ])
        self.play(LaggedStart(*[FadeIn(b, shift=UP*0.1) for b in bin_lbls],
                              lag_ratio=0.1), run_time=0.8)

        insight = Tex(
            r"Parity bit $p_k$ = XOR of all bits whose position has a \textbf{1} in bit $k$",
            font_size=26, color=YELLOW,
        ).next_to(bin_note, DOWN, buff=0.3)
        self.play(FadeIn(insight, shift=UP*0.2), run_time=0.6)
        self.wait(1.1)

        self.play(FadeOut(VGroup(hdr, cells, pos_nums, pos_lbl, p_mobjs, d_mobjs,
                                  bin_lbls, bin_note, insight)), run_time=0.7)

    # ── Act 4 ────────────────────────────────────────────────────────────────
    def act4_matrix(self):
        hdr = Text("The Parity-Check Matrix  H", font_size=40, color=WHITE)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        H_tex = MathTex(
            r"H = \begin{pmatrix}"
            r"1 & 0 & 1 & 0 & 1 & 0 & 1 \\"
            r"0 & 1 & 1 & 0 & 0 & 1 & 1 \\"
            r"0 & 0 & 0 & 1 & 1 & 1 & 1"
            r"\end{pmatrix}",
            font_size=38,
        ).move_to(UP*1.3)
        self.play(Write(H_tex, run_time=1.4))

        col_note = Tex(r"Column $j$ of $H$ is the binary representation of $j$",
                       font_size=26, color=SYN_C).next_to(H_tex, DOWN, buff=0.35)
        self.play(FadeIn(col_note, shift=UP*0.2), run_time=0.6)

        syn_def = MathTex(r"\text{syndrome:}\quad s(y) = H y^\top \pmod{2}",
                          font_size=34, color=SYN_C).next_to(col_note, DOWN, buff=0.4)
        self.play(Write(syn_def, run_time=0.9))

        key = Tex(
            r"If $y = c + e_j$: \quad"
            r"$s(y) = Hc^\top + He_j^\top = \mathbf{0} + \text{col}_j(H)$",
            font_size=27, color=CORR_C,
        ).next_to(syn_def, DOWN, buff=0.4)
        self.play(FadeIn(key, shift=UP*0.2), run_time=0.7)

        big = Text("The syndrome is the binary address of the bad bit!",
                   font_size=26, color=YELLOW, weight=BOLD).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(big, shift=UP*0.25), run_time=0.55)
        self.wait(1.2)
        self.play(FadeOut(VGroup(hdr, H_tex, col_note, syn_def, key, big)), run_time=0.7)

    # ── Act 5 ────────────────────────────────────────────────────────────────
    def act5_decode(self):
        hdr = Text("Decoding in Action", font_size=40, color=WHITE)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        data = [1, 0, 1, 1]
        cw   = hamming_encode(data)
        j_err = 4
        cw_rx = cw.copy(); cw_rx[j_err] ^= 1

        # codeword row
        cw_lbl = Text("codeword  c :", font_size=24, color=DIM_C)\
            .to_edge(LEFT, buff=0.45).shift(UP*1.5)
        reg_c = BitRow(cw, size=0.52, buff=0.10, fs=28).next_to(cw_lbl, RIGHT, buff=0.28)
        for i in PARITY_IDX: reg_c.color_cell(i, PAR_C)
        for i in DATA_IDX:   reg_c.color_cell(i, DATA_C)
        pos_c = VGroup(*[MathTex(str(i+1), font_size=17, color=DIM_C)
                          .next_to(reg_c.cell(i), DOWN, buff=0.07) for i in range(7)])
        self.play(FadeIn(cw_lbl), FadeIn(reg_c), FadeIn(pos_c), run_time=0.6)

        # received row
        err_lbl = Text(f"error at position {j_err+1}  →", font_size=24, color=ERR_C)\
            .to_edge(LEFT, buff=0.45).shift(UP*0.45)
        self.play(FadeIn(err_lbl, shift=RIGHT*0.2), run_time=0.4)

        rx_lbl = Text("received  y :", font_size=24, color=DIM_C)\
            .move_to(cw_lbl).shift(DOWN*1.15)
        reg_y = BitRow(cw_rx, size=0.52, buff=0.10, fs=28).move_to(reg_c).shift(DOWN*1.15)
        for i in PARITY_IDX: reg_y.color_cell(i, PAR_C)
        for i in DATA_IDX:   reg_y.color_cell(i, DATA_C)
        reg_y.color_cell(j_err, ERR_C)
        pos_y = VGroup(*[MathTex(str(i+1), font_size=17, color=DIM_C)
                          .next_to(reg_y.cell(i), DOWN, buff=0.07) for i in range(7)])
        self.play(Flash(reg_c.cell(j_err).get_center(), color=ERR_C, flash_radius=0.48),
                  FadeIn(reg_y), FadeIn(rx_lbl), FadeIn(pos_y), run_time=0.65)

        # syndrome row
        s     = syndrome(cw_rx)
        s_str = "".join(map(str, s))
        s_val = int(s_str, 2)

        syn_lbl = Text("syndrome  s :", font_size=24, color=SYN_C)\
            .move_to(rx_lbl).shift(DOWN*1.15)
        reg_s = BitRow(s, size=0.52, buff=0.10, fs=28, bit_color=SYN_C,
                       stroke_color=SYN_C).move_to(reg_y).shift(DOWN*1.15)
        for i in range(3):
            reg_s.cell(i).set_stroke(color=SYN_C, width=2.5).set_fill(color=SYN_C, opacity=0.14)
        arr = Arrow(reg_y.get_bottom()+DOWN*0.08, reg_s.get_top()+UP*0.08,
                    buff=0.04, stroke_width=2.5, color=SYN_C,
                    max_tip_length_to_length_ratio=0.2)
        syn_eq = MathTex(rf"s = Hy^\top = {s_str}_2 = {s_val}",
                         font_size=26, color=SYN_C).next_to(reg_s, RIGHT, buff=0.35)
        self.play(GrowArrow(arr), run_time=0.35)
        self.play(FadeIn(syn_lbl), FadeIn(reg_s), Write(syn_eq), run_time=0.65)

        # identify
        identify = Text(f"syndrome {s_str}₂ = {s_val}  →  flip bit {s_val}",
                        font_size=24, color=CORR_C).to_edge(DOWN, buff=1.0)
        ring = SurroundingRectangle(reg_y.cell(j_err), color=CORR_C, buff=0.07,
                                    corner_radius=0.07, stroke_width=2.5)
        self.play(FadeIn(identify, shift=UP*0.2), Create(ring), run_time=0.5)
        self.wait(0.3)

        # correct
        fixed = MathTex(str(cw[j_err]), font_size=28, color=CORR_C).move_to(reg_y.label(j_err))
        self.play(Transform(reg_y.labels[j_err], fixed),
                  reg_y.cell(j_err).animate.set_stroke(color=CORR_C, width=3)
                                           .set_fill(color=CORR_C, opacity=0.2),
                  run_time=0.45)
        done = Text("Corrected!", font_size=26, color=YELLOW, weight=BOLD)\
            .next_to(identify, DOWN, buff=0.2)
        self.play(FadeIn(done, shift=UP*0.2), run_time=0.4)
        self.wait(1.0)

        self.play(FadeOut(VGroup(hdr, cw_lbl, reg_c, pos_c, err_lbl,
                                  rx_lbl, reg_y, pos_y, arr,
                                  syn_lbl, reg_s, syn_eq,
                                  identify, ring, done)), run_time=0.75)

    # ── Act 6 ────────────────────────────────────────────────────────────────
    def act6_cube(self):
        hdr = Text("Syndrome Space  —  the Cube", font_size=40, color=WHITE)\
            .to_edge(UP, buff=0.4)
        self.play(FadeIn(hdr, shift=DOWN*0.2), run_time=0.5)

        cube_grp, dot_map, lbl_map = build_cube(
            origin=RIGHT*2.2, sx=1.55, sy=1.55, sz=0.75, dot_r=0.08)
        edges, dots, cube_lbls = cube_grp[0], cube_grp[1], cube_grp[2]

        f2_3 = MathTex(r"\mathbb{F}_2^3", font_size=46, color=WHITE)\
            .next_to(cube_grp, UP, buff=0.2)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.02), run_time=0.8)
        self.play(FadeIn(dots), FadeIn(cube_lbls), FadeIn(f2_3), run_time=0.5)

        # kernel
        dot_map[(0,0,0)].set_color(SYN_C)
        ker_ring = Circle(radius=0.2, color=SYN_C, stroke_width=2.2)\
            .move_to(dot_map[(0,0,0)])
        ker_lbl = MathTex(r"\ker H = C", font_size=22, color=SYN_C)\
            .next_to(dot_map[(0,0,0)], LEFT, buff=0.22)
        self.play(Create(ker_ring), FadeIn(ker_lbl, shift=RIGHT*0.15), run_time=0.5)

        # error labels on 7 nonzero vertices
        j_tags = VGroup()
        for v, j in VERTEX_TO_J.items():
            dot_map[v].set_color(ERR_C)
            t = MathTex(rf"e_{j}", font_size=20, color=ERR_C)\
                .next_to(dot_map[v], RIGHT, buff=0.06)
            j_tags.add(t)
        self.play(LaggedStart(*[FadeIn(t, shift=LEFT*0.1) for t in j_tags],
                              lag_ratio=0.08), run_time=0.8)
        self.play(*[Indicate(dot_map[v], color=YELLOW, scale_factor=1.9)
                    for v in VERTEX_TO_J], run_time=0.7)

        # explanation
        expl = VGroup(
            Tex(r"7 nonzero vertices",               font_size=26, color=ERR_C),
            MathTex(r"\updownarrow",                 font_size=28, color=DIM_C),
            Tex(r"7 correctable bit positions",      font_size=26, color=DATA_C),
            MathTex(r"\updownarrow",                 font_size=28, color=DIM_C),
            Tex(r"7 single-bit error patterns",      font_size=26, color=CORR_C),
        ).arrange(DOWN, buff=0.22).move_to(LEFT*3.2)
        self.play(FadeIn(expl, shift=RIGHT*0.3), run_time=0.8)
        self.wait(0.5)

        coset = Tex(
            r"$\mathbb{F}_2^7 / C \;\cong\; \mathbb{F}_2^3$"
            r"\quad $\Rightarrow$\quad 8 cosets $\leftrightarrow$ 8 syndromes",
            font_size=26, color=GREY_A,
        ).to_edge(DOWN, buff=0.55)
        self.play(FadeIn(coset, shift=UP*0.2), run_time=0.5)
        self.wait(0.8)

        demo_ring = SurroundingRectangle(dot_map[(1,1,1)], color=YELLOW,
                                          buff=0.12, stroke_width=2.5, corner_radius=0.12)
        demo_txt = Tex(r"syndrome $111_2 = 7 \;\Rightarrow\;$ flip bit 7",
                       font_size=25, color=YELLOW).next_to(coset, DOWN, buff=0.18)
        self.play(Create(demo_ring), FadeIn(demo_txt, shift=UP*0.15), run_time=0.5)
        self.wait(1.0)

        summary = Text(
            "[7, 4, 3]₂  —  4 data bits · 3 parity bits · corrects every 1-bit error",
            font_size=24, color=YELLOW, weight=BOLD,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(coset), FadeOut(demo_txt), FadeOut(demo_ring),
                  FadeIn(summary, shift=UP*0.2), run_time=0.7)
        self.wait(1.4)
        self.play(FadeOut(VGroup(hdr, cube_grp, f2_3, ker_ring, ker_lbl,
                                  j_tags, expl, summary)), run_time=0.9)
