from manim import *
import numpy as np

# manim -pql hamming_story_skeleton.py HammingSyndromeStory
# manim -pqh hamming_story_skeleton.py HammingSyndromeStory

from manim import *
import numpy as np

# ============================================================
# Hamming [7,4,3]_2: syndrome = coset label = error identifier
# ============================================================

# Canonical Hamming parity-check matrix: columns are all 7 nonzero vectors in F2^3
H = np.array([
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
], dtype=int)

# Syndromes of single-bit errors: s(e_j) = H e_j^T = column j of H
H_COLS = [tuple(H[:, j].tolist()) for j in range(7)]


# -----------------------------
# Geometry helpers (cube F2^3)
# -----------------------------
def proj_cube(v, origin=np.array([4.2, -0.6, 0.0]), sx=1.25, sy=1.25, sz=0.68):
    """2D projection of the cube {0,1}^3."""
    x, y, z = v
    return origin + np.array([sx * x + sz * z, sy * y + 0.55 * sz * z, 0])


def cube_vertices():
    return [(x, y, z) for x in [0, 1] for y in [0, 1] for z in [0, 1]]


def hamming_vertex_to_j():
    """
    For the canonical H above, the nonzero vertices correspond to columns:
      j=1:100, j=2:010, j=3:110, j=4:001, j=5:101, j=6:011, j=7:111
    """
    return {
        (1, 0, 0): 1,
        (0, 1, 0): 2,
        (1, 1, 0): 3,
        (0, 0, 1): 4,
        (1, 0, 1): 5,
        (0, 1, 1): 6,
        (1, 1, 1): 7,
    }


# -----------------------------
# Bit-bar helper (for F2^7 words)
# -----------------------------
def bit_cell(size=0.44):
    return RoundedRectangle(corner_radius=0.08, height=size, width=size, stroke_width=2)


def make_register(bitstring, size=0.44, buff=0.06, font_size=22, color=WHITE):
    bits = list(bitstring)
    cells = VGroup(*[bit_cell(size) for _ in bits]).arrange(RIGHT, buff=buff)
    labels = VGroup(*[
        MathTex(bits[i], font_size=font_size, color=color).move_to(cells[i])
        for i in range(len(bits))
    ])
    return VGroup(cells, labels)


def set_register(scene, reg, bitstring, color=YELLOW, run_time=0.4):
    cells, labels = reg[0], reg[1]
    bits = list(bitstring)
    targets = VGroup(*[
        MathTex(bits[i], font_size=labels[i].font_size, color=color).move_to(labels[i])
        for i in range(len(bits))
    ])
    scene.play(
        *[Transform(labels[i], targets[i]) for i in range(len(bits))],
        *[cells[i].animate.set_stroke(color=color, width=3).set_fill(opacity=0.12) for i in range(len(bits))],
        run_time=run_time
    )


def toggle_bit_char(ch: str) -> str:
    return "0" if ch == "1" else "1"


# ============================================================
# Main story scene
# ============================================================
class HammingSyndromeStory(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"

        # Build persistent objects (omniscient wide shot)
        st = self.build_stage()

        # Add base stage (minimal animation)
        self.play(FadeIn(st["title"], shift=DOWN), run_time=0.7)
        self.play(FadeIn(st["space7"]), FadeIn(st["space3"]), run_time=0.4)
        self.play(GrowArrow(st["arrowH"]), FadeIn(st["labH"], shift=UP), run_time=0.6)
        self.play(LaggedStart(*[Create(e) for e in st["edges"]], lag_ratio=0.01), run_time=0.8)
        self.play(FadeIn(st["dots"]), FadeIn(st["labels"]), FadeIn(st["cube_caption"], shift=UP), run_time=0.6)
        self.play(FadeIn(st["ybar"], shift=UP), FadeIn(st["ylab"], shift=UP), run_time=0.6)

        # ACT I: Map + kernel (codewords go to 000)
        self.act_map_and_kernel(st)

        # ACT II: Exactness + cosets as fibers
        self.act_exactness_and_cosets(st)

        # ACT III: Unit errors as fingerprints (columns of H)
        self.act_unit_errors_as_fingerprints(st)

        # ACT IV: Decode demo with VISIBLE CANCELLATION
        self.act_decode_demo(st)

        self.wait(0.6)

    # ------------------------------------------------------------
    # Stage construction
    # ------------------------------------------------------------
    def build_stage(self):
        title = Tex(
            r"Syndrome = coset label = error identifier (Hamming $[7,4,3]_2$)",
            font_size=44, color=GREY_A
        ).to_edge(UP)

        space7 = MathTex(r"\mathbb{F}_2^7", font_size=52, color=WHITE).move_to(np.array([-4.3, 1.3, 0]))
        space3 = MathTex(r"\mathbb{F}_2^3", font_size=52, color=WHITE).move_to(np.array([2.5, 1.3, 0]))

        arrowH = Arrow(np.array([-2.9, 1.2, 0]), np.array([2.0, 1.2, 0]), buff=0.2, color=WHITE)
        labH = MathTex(r"H", font_size=44, color=WHITE).next_to(arrowH, UP, buff=0.08)

        # Cube for syndrome space
        verts = cube_vertices()
        dots = VGroup()
        labels = VGroup()
        vertex_to_dot = {}
        vertex_to_label = {}

        for v in verts:
            d = Dot(proj_cube(v), radius=0.055, color=GREY_C)
            t = MathTex(f"{v[0]}{v[1]}{v[2]}", font_size=22, color=GREY_B).next_to(d, RIGHT, buff=0.06)
            dots.add(d)
            labels.add(t)
            vertex_to_dot[v] = d
            vertex_to_label[v] = t

        edges = VGroup()
        for i, v in enumerate(verts):
            for j, w in enumerate(verts):
                if j <= i:
                    continue
                if sum(abs(v[k] - w[k]) for k in range(3)) == 1:
                    L = Line(proj_cube(v), proj_cube(w), stroke_width=2, color=GREY_E)
                    L.set_stroke(opacity=0.75)
                    edges.add(L)

        cube_caption = Tex(r"$\mathbb{F}_2^3$ (syndromes)", font_size=28, color=BLUE_A) \
            .next_to(VGroup(edges, dots), UP, buff=0.2).align_to(dots, LEFT)

        # Word bar y in F2^7
        ybar = make_register("0000000", size=0.44, buff=0.06, font_size=22, color=WHITE)
        ybar.move_to(np.array([-4.2, -0.9, 0]))
        ylab = MathTex(r"y", font_size=34, color=WHITE).next_to(ybar, UP, buff=0.12).align_to(ybar, LEFT)

        return {
            "title": title,
            "space7": space7,
            "space3": space3,
            "arrowH": arrowH,
            "labH": labH,
            "edges": edges,
            "dots": dots,
            "labels": labels,
            "cube_caption": cube_caption,
            "vertex_to_dot": vertex_to_dot,
            "vertex_to_label": vertex_to_label,
            "ybar": ybar,
            "ylab": ylab,
        }

    # ------------------------------------------------------------
    # Helper: pulse through H
    # ------------------------------------------------------------
    def pulse_through_H(self, arrowH, start_point, end_point, color=YELLOW,
                       travel_time=0.8, radius=0.06):
        dot = Dot(start_point, radius=radius, color=color)
        self.add(dot)
        self.play(dot.animate.move_to(arrowH.get_start()), run_time=0.20)
        self.play(MoveAlongPath(dot, arrowH), run_time=travel_time, rate_func=smooth)
        self.play(dot.animate.move_to(end_point), run_time=0.25)
        self.remove(dot)

    # ------------------------------------------------------------
    # ACT I: Map + kernel
    # ------------------------------------------------------------
    def act_map_and_kernel(self, st):
        arrowH = st["arrowH"]
        v2d = st["vertex_to_dot"]

        cap = Tex(r"$T_H:y\mapsto Hy^\top$, \quad $C=\ker(T_H)$",
                  font_size=32, color=YELLOW).next_to(st["title"], DOWN, buff=0.25)
        self.play(FadeIn(cap, shift=DOWN), run_time=0.5)

        # Pulse a "codeword" through H -> lands at 000
        start = st["ybar"].get_right() + 0.15 * RIGHT
        self.pulse_through_H(arrowH, start, v2d[(0, 0, 0)].get_center(), color=YELLOW, travel_time=0.75)

        dot000 = v2d[(0, 0, 0)]
        ring000 = SurroundingRectangle(dot000, color=BLUE_A, buff=0.14)
        self.play(Create(ring000), run_time=0.25)
        self.play(FadeOut(ring000), run_time=0.25)

        ker_lab = Tex(r"fiber over $000$ is $C$", font_size=28, color=YELLOW) \
            .next_to(dot000, DOWN, buff=0.25).shift(0.3 * RIGHT)
        self.play(FadeIn(ker_lab, shift=UP), run_time=0.4)
        self.wait(0.3)

        self.play(FadeOut(ker_lab), FadeOut(cap), run_time=0.6)

    # ------------------------------------------------------------
    # ACT II: Exactness + cosets as fibers
    # ------------------------------------------------------------
    def act_exactness_and_cosets(self, st):
        dots = st["dots"]
        v2d = st["vertex_to_dot"]

        ses = MathTex(r"0\to C\to \mathbb{F}_2^7 \xrightarrow{H} \mathbb{F}_2^3\to 0",
                      font_size=40, color=GREY_A).to_edge(UP).shift(DOWN * 0.9)
        cos = Tex(r"$\mathbb{F}_2^7/C \cong \mathbb{F}_2^3$  (8 cosets $\leftrightarrow$ 8 syndromes)",
                  font_size=28, color=GREY_B).next_to(ses, DOWN, buff=0.18)

        self.play(FadeIn(ses, shift=DOWN), FadeIn(cos, shift=DOWN), run_time=0.8)

        halo_all = VGroup(*[SurroundingRectangle(d, color=BLUE_A, buff=0.12) for d in dots])
        self.play(LaggedStart(*[Create(h) for h in halo_all], lag_ratio=0.03), run_time=0.7)
        self.play(FadeOut(halo_all), run_time=0.4)

        self.play(FadeOut(ses), FadeOut(cos), run_time=0.6)

        cap = Tex(r"Cosets are fibers: $H^{-1}(s)$ is one bucket (one coset)",
                  font_size=30, color=GREY_A).next_to(st["title"], DOWN, buff=0.25)
        self.play(FadeIn(cap, shift=DOWN), run_time=0.5)

        stacks = VGroup()
        verts = cube_vertices()
        for v in verts:
            base = v2d[v].get_center()
            stck = VGroup(*[
                Dot(base + np.array([0.0, 0.22 * k, 0.0]), radius=0.03, color=GREY_E)
                for k in range(1, 4)
            ])
            stacks.add(stck)

        # Highlight 000 fiber as the code C
        fiber000 = stacks[verts.index((0, 0, 0))]
        for d in fiber000:
            d.set_color(YELLOW)

        self.play(FadeIn(stacks), run_time=0.6)
        self.wait(0.4)
        self.play(FadeOut(stacks), FadeOut(cap), run_time=0.7)

    # ------------------------------------------------------------
    # ACT III: Unit errors as fingerprints (columns of H)
    # ------------------------------------------------------------
    def act_unit_errors_as_fingerprints(self, st):
        v2d = st["vertex_to_dot"]

        cap = Tex(r"Unit errors $e_j$ map to distinct nonzero syndromes: $s(e_j)=He_j^\top$",
                  font_size=30, color=GREY_A).next_to(st["title"], DOWN, buff=0.25)
        self.play(FadeIn(cap, shift=DOWN), run_time=0.6)

        v2j = hamming_vertex_to_j()
        j_tags = VGroup()
        for v, j in v2j.items():
            tag = Tex(rf"$j={j}$", font_size=22, color=YELLOW).next_to(v2d[v], UP, buff=0.08)
            j_tags.add(tag)

        self.play(FadeIn(j_tags, shift=UP), run_time=0.6)

        # Demonstrate a few mappings explicitly
        for j in [1, 4, 7]:
            v = H_COLS[j - 1]
            d = v2d[v]
            ring = SurroundingRectangle(d, color=YELLOW, buff=0.12)
            self.play(Create(ring), d.animate.set_color(YELLOW), run_time=0.35)
            self.play(FadeOut(ring), run_time=0.2)

        # Flash all nonzero vertices
        nonzero = [v for v in cube_vertices() if v != (0, 0, 0)]
        halos = VGroup(*[
            SurroundingRectangle(v2d[v], color=YELLOW, buff=0.12)
            for v in nonzero
        ])
        self.play(LaggedStart(*[Create(h) for h in halos], lag_ratio=0.03), run_time=0.7)
        self.play(FadeOut(halos), run_time=0.4)

        self.play(FadeOut(cap), run_time=0.5)

        # keep for later if you want
        st["j_tags"] = j_tags

    # ------------------------------------------------------------
    # ACT IV: Decode demo with visible cancellation
    # ------------------------------------------------------------
    def act_decode_demo(self, st):
        arrowH = st["arrowH"]
        ybar = st["ybar"]
        v2d = st["vertex_to_dot"]

        cap = Tex(r"Decode: compute $s(y)=Hy^\top$; match the cube vertex; flip that bit",
                  font_size=30, color=WHITE).next_to(st["title"], DOWN, buff=0.25)
        self.play(FadeIn(cap, shift=DOWN), run_time=0.6)

        # Choose a visible codeword c in C (any kernel example for the story)
        c_bits = "1011010"
        set_register(self, ybar, c_bits, color=YELLOW, run_time=0.6)

        # Inject 1-bit error at j=7 (syndrome 111)
        j_demo = 7
        j0 = j_demo - 1
        flip_box = SurroundingRectangle(ybar[0][j0], color=RED, buff=0.08)
        self.play(Create(flip_box), run_time=0.2)

        corrupted = list(c_bits)
        corrupted[j0] = toggle_bit_char(corrupted[j0])
        self.play(
            Transform(ybar[1][j0], MathTex(corrupted[j0], font_size=22, color=RED).move_to(ybar[1][j0])),
            ybar[0][j0].animate.set_stroke(color=RED, width=4).set_fill(opacity=0.18),
            run_time=0.45
        )

        # --- Cancellation visual: Hy = H(c + e_j) = Hc + He_j = 0 + He_j ---
        s = H_COLS[j0]  # syndrome vertex = column j
        dot000 = v2d[(0, 0, 0)]
        target_dot = v2d[s]

        cap_cancel = MathTex(
            r"Hy^\top = H(c+e_j)^\top = Hc^\top + He_j^\top = 0 + He_j^\top",
            font_size=30, color=GREY_A
        ).to_edge(UP).shift(0.55 * DOWN)
        self.play(FadeIn(cap_cancel, shift=DOWN), run_time=0.5)

        # Tiny split cue (optional but very 3b1b)
        plus = MathTex(r"+", font_size=44, color=GREY_B).move_to(ybar.get_right() + 0.35 * RIGHT)
        c_tag = MathTex(r"c", font_size=30, color=YELLOW).next_to(plus, UP, buff=0.12)
        e_tag = MathTex(r"e_j", font_size=30, color=RED).next_to(plus, DOWN, buff=0.12)
        self.play(FadeIn(plus), FadeIn(c_tag), FadeIn(e_tag), run_time=0.25)
        self.play(FadeOut(plus), FadeOut(c_tag), FadeOut(e_tag), run_time=0.25)

        # 1) Yellow pulse: codeword component -> 000 and annihilates
        c_start = ybar.get_right() + 0.15 * RIGHT + 0.18 * UP
        self.pulse_through_H(arrowH, c_start, dot000.get_center(), color=YELLOW, travel_time=0.75)

        ring0 = SurroundingRectangle(dot000, color=YELLOW, buff=0.14)
        self.play(Create(ring0), run_time=0.18)
        self.play(FadeOut(ring0), run_time=0.22)

        # 2) Red pulse: error component -> syndrome vertex
        e_start = ybar.get_right() + 0.15 * RIGHT + 0.18 * DOWN
        self.pulse_through_H(arrowH, e_start, target_dot.get_center(), color=RED, travel_time=0.85)

        ringS = SurroundingRectangle(target_dot, color=YELLOW, buff=0.12)
        self.play(Create(ringS), target_dot.animate.set_color(YELLOW), run_time=0.35)

        self.play(FadeOut(cap_cancel, shift=UP), run_time=0.45)

        # Identify j and correct
        s_bits = f"{s[0]}{s[1]}{s[2]}"
        identify = Tex(rf"Syndrome $={s_bits}$ means $j={j_demo}$",
                       font_size=30, color=YELLOW).to_edge(DOWN)
        flash = SurroundingRectangle(ybar[0][j0], color=YELLOW, buff=0.08)

        self.play(FadeIn(identify, shift=UP), Create(flash), run_time=0.6)
        self.wait(0.6)

        # Correction = flip back
        self.play(
            Transform(ybar[1][j0], MathTex(c_bits[j0], font_size=22, color=YELLOW).move_to(ybar[1][j0])),
            run_time=0.35
        )

        # Return-to-kernel visual: highlight 000 vertex
        ring000 = SurroundingRectangle(dot000, color=BLUE_A, buff=0.14)
        self.play(Create(ring000), run_time=0.25)
        self.play(FadeOut(ring000), run_time=0.25)

        # Cleanup overlays
        self.play(
            FadeOut(cap),
            FadeOut(identify),
            FadeOut(flip_box),
            FadeOut(flash),
            FadeOut(ringS),
            run_time=0.9
        )
