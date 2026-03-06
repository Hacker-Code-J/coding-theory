from manim import *
import numpy as np

# manim -pql hamming_syndrome_coset.py SyndromeCosetHamming
# manim -pqh hamming_syndrome_coset.py SyndromeCosetHamming
# manim -p -r 1920,1080 hamming_syndrome_coset.py SyndromeCosetHamming

# -----------------------------
# Canonical Hamming (7,4,3) parity-check matrix
# -----------------------------
H = np.array([
    [1,0,1,0,1,0,1],
    [0,1,1,0,0,1,1],
    [0,0,0,1,1,1,1],
], dtype=int)

H_COLS = [tuple(H[:, j].tolist()) for j in range(7)]  # syndromes of 1-bit errors

def proj_cube(v, origin=np.array([4.1, -0.6, 0.0]), sx=1.25, sy=1.25, sz=0.68):
    """2D projection of {0,1}^3 as a cube."""
    x, y, z = v
    return origin + np.array([sx*x + sz*z, sy*y + 0.55*sz*z, 0])

def bit_cell(size=0.42):
    return RoundedRectangle(corner_radius=0.08, height=size, width=size, stroke_width=2)

def make_register(bits, size=0.42, buff=0.06, font_size=22, color=WHITE):
    bits = list(bits)
    cells = VGroup(*[bit_cell(size) for _ in bits]).arrange(RIGHT, buff=buff)
    labels = VGroup(*[
        MathTex(bits[i], font_size=font_size, color=color).move_to(cells[i])
        for i in range(len(bits))
    ])
    return VGroup(cells, labels)

def set_register(scene, reg, bits, color=YELLOW, run_time=0.4):
    cells, labels = reg[0], reg[1]
    bits = list(bits)
    targets = VGroup(*[
        MathTex(bits[i], font_size=labels[i].font_size, color=color).move_to(labels[i])
        for i in range(len(bits))
    ])
    scene.play(
        *[Transform(labels[i], targets[i]) for i in range(len(bits))],
        *[cells[i].animate.set_stroke(color=color, width=3).set_fill(opacity=0.12) for i in range(len(bits))],
        run_time=run_time
    )

class SyndromeCosetHamming(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"

        # ------------------------------------------------------------
        # 0) Title
        # ------------------------------------------------------------
        title = Tex(r"Syndrome = coset label = error identifier (Hamming $[7,4,3]_2$)",
                    font_size=44, color=GREY_A).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN), run_time=0.8)

        # ------------------------------------------------------------
        # 1) Build cube = F2^3 (syndrome space)
        # ------------------------------------------------------------
        vertices = [(x,y,z) for x in [0,1] for y in [0,1] for z in [0,1]]

        dots = VGroup()
        labels = VGroup()
        for v in vertices:
            d = Dot(proj_cube(v), radius=0.055, color=GREY_C)
            t = MathTex(f"{v[0]}{v[1]}{v[2]}", font_size=22, color=GREY_B).next_to(d, RIGHT, buff=0.06)
            dots.add(d); labels.add(t)

        edges = VGroup()
        edge_map = {}
        for i, v in enumerate(vertices):
            for j, w in enumerate(vertices):
                if j <= i:
                    continue
                if sum(abs(v[k]-w[k]) for k in range(3)) == 1:
                    L = Line(proj_cube(v), proj_cube(w), stroke_width=2, color=GREY_E)
                    L.set_stroke(opacity=0.75)
                    edges.add(L)
                    edge_map[(v,w)] = L
                    edge_map[(w,v)] = L

        cube_caption = Tex(r"$\mathbb{F}_2^3$ (syndromes)", font_size=28, color=BLUE_A)\
            .next_to(VGroup(edges, dots), UP, buff=0.2).align_to(dots, LEFT)

        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.01), run_time=0.9)
        self.play(FadeIn(dots), FadeIn(labels), FadeIn(cube_caption, shift=UP), run_time=0.6)

        # ------------------------------------------------------------
        # 2) Left: F2^7 and the map H
        # ------------------------------------------------------------
        space7 = MathTex(r"\mathbb{F}_2^7", font_size=52, color=WHITE).move_to(np.array([-4.2, 1.3, 0]))
        space3 = MathTex(r"\mathbb{F}_2^3", font_size=52, color=WHITE).move_to(np.array([2.7, 1.3, 0]))

        # A visible arrow from left space to the cube region
        arrowH = Arrow(np.array([-2.9, 1.2, 0]), np.array([2.0, 1.2, 0]), buff=0.2, color=WHITE)
        labH = MathTex(r"H", font_size=44, color=WHITE).next_to(arrowH, UP, buff=0.08)

        self.play(FadeIn(space7), FadeIn(space3), run_time=0.5)
        self.play(GrowArrow(arrowH), FadeIn(labH, shift=UP), run_time=0.7)

        # A 7-bit word bar y in F2^7
        ybar = make_register("0000000", size=0.44, buff=0.06, font_size=22, color=WHITE)
        ybar.move_to(np.array([-4.2, -0.9, 0]))
        ylab = MathTex(r"y", font_size=34, color=WHITE).next_to(ybar, UP, buff=0.12).align_to(ybar, LEFT)
        self.play(FadeIn(ybar, shift=UP), FadeIn(ylab, shift=UP), run_time=0.6)

        # ------------------------------------------------------------
        # 3) Kernel + SES (short, then fade)
        # ------------------------------------------------------------
        ker_cap = Tex(r"$T_H:y\mapsto Hy^\top$, \quad $C=\ker(T_H)$",
                      font_size=32, color=YELLOW).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(ker_cap, shift=DOWN), run_time=0.6)

        # show "codeword" c maps to 000: pulse from ybar through H to vertex 000
        c_dot = Dot(ybar.get_right() + 0.15*RIGHT, radius=0.06, color=YELLOW)
        self.add(c_dot)
        self.play(c_dot.animate.move_to(arrowH.get_start()), run_time=0.3)
        self.play(MoveAlongPath(c_dot, arrowH), run_time=0.8, rate_func=smooth)
        self.remove(c_dot)

        dot000 = dots[vertices.index((0,0,0))]
        ring000 = SurroundingRectangle(dot000, color=BLUE_A, buff=0.14)
        self.play(Create(ring000), run_time=0.25)
        self.play(FadeOut(ring000), run_time=0.25)

        ses = MathTex(r"0\to C\to \mathbb{F}_2^7 \xrightarrow{H} \mathbb{F}_2^3\to 0",
                      font_size=40, color=GREY_A).to_edge(UP).shift(DOWN*0.9)
        cos = Tex(r"$\mathbb{F}_2^7/C \cong \mathbb{F}_2^3$  (8 cosets $\leftrightarrow$ 8 syndromes)",
                  font_size=28, color=GREY_B).next_to(ses, DOWN, buff=0.18)

        self.play(FadeIn(ses, shift=DOWN), FadeIn(cos, shift=DOWN), run_time=0.8)
        # glow all vertices briefly = "all syndromes exist"
        halo_all = VGroup(*[SurroundingRectangle(d, color=BLUE_A, buff=0.12) for d in dots])
        self.play(LaggedStart(*[Create(h) for h in halo_all], lag_ratio=0.03), run_time=0.7)
        self.play(FadeOut(halo_all), run_time=0.4)

        self.play(FadeOut(ses), FadeOut(cos), FadeOut(ker_cap), run_time=0.6)

        # ------------------------------------------------------------
        # 4) Cosets: visualize as stacks above each syndrome vertex
        # ------------------------------------------------------------
        cap_cosets = Tex(r"Cosets: all words with the same syndrome form one bucket",
                         font_size=30, color=GREY_A).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(cap_cosets, shift=DOWN), run_time=0.6)

        stacks = VGroup()
        for v in vertices:
            base = proj_cube(v)
            # three faint dots "stacked" to suggest many elements in that coset
            st = VGroup(*[
                Dot(base + np.array([0.0, 0.22*k, 0.0]), radius=0.03, color=GREY_E)
                for k in range(1, 4)
            ])
            stacks.add(st)

        self.play(FadeIn(stacks), run_time=0.6)
        self.wait(0.3)
        self.play(FadeOut(stacks), FadeOut(cap_cosets), run_time=0.6)

        # ------------------------------------------------------------
        # 5) Weight-1 coset leaders e_j and the lookup rule
        # ------------------------------------------------------------
        cap_ej = Tex(r"Weight-1 coset leaders: $e_j$ (one flipped bit)",
                     font_size=30, color=GREY_A).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(cap_ej, shift=DOWN), run_time=0.6)

        # Show seven basis vectors as arrows (just indices, not full vectors)
        idx_row = VGroup(*[
            Tex(rf"$j={j}$", font_size=24, color=GREY_B)
            for j in range(1, 8)
        ]).arrange(RIGHT, buff=0.35).move_to(np.array([-4.2, -2.7, 0]))

        ej_marks = VGroup(*[
            Dot(idx_row[j-1].get_center() + 0.28*UP, radius=0.04, color=RED)
            for j in range(1, 8)
        ])

        self.play(FadeIn(idx_row, shift=UP), FadeIn(ej_marks, shift=UP), run_time=0.6)

        # Map each e_j to its syndrome vertex (= column j of H)
        # We animate only a couple, then do a fast “all seven” highlight.
        def highlight_mapping(j, run_time=0.55):
            v = H_COLS[j-1]
            target_dot = dots[vertices.index(v)]
            ring = SurroundingRectangle(target_dot, color=YELLOW, buff=0.12)
            self.play(ej_marks[j-1].animate.set_color(YELLOW), run_time=0.15)
            self.play(Create(ring), target_dot.animate.set_color(YELLOW), run_time=run_time)
            self.play(FadeOut(ring), ej_marks[j-1].animate.set_color(RED), run_time=0.25)

        highlight_mapping(1)
        highlight_mapping(4)

        # Now: flash all nonzero syndrome vertices = all columns of H
        nonzero = [v for v in vertices if v != (0,0,0)]
        halos = VGroup(*[
            SurroundingRectangle(dots[vertices.index(v)], color=YELLOW, buff=0.12)
            for v in nonzero
        ])
        self.play(LaggedStart(*[Create(h) for h in halos], lag_ratio=0.03), run_time=0.7)
        self.play(FadeOut(halos), run_time=0.4)

        self.play(FadeOut(cap_ej), run_time=0.4)

        # ------------------------------------------------------------
        # 6) Full decoding demo: y = c + e_j, syndrome identifies j
        # ------------------------------------------------------------
        cap_dec = Tex(r"Decoding: compute $s(y)=Hy^\top$ and match it to a column of $H$",
                      font_size=30, color=WHITE).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(cap_dec, shift=DOWN), run_time=0.6)

        # Put a codeword c in the bar (we keep it abstract, just show "a valid word")
        set_register(self, ybar, "1011010", color=YELLOW, run_time=0.6)

        # Inject a 1-bit error at j=7 (most dynamic syndrome)
        j_demo = 7
        j0 = j_demo - 1
        flip_box = SurroundingRectangle(ybar[0][j0], color=RED, buff=0.08)
        self.play(Create(flip_box), run_time=0.2)
        # toggle last bit visually
        current = list("1011010")
        current[j0] = "0" if current[j0] == "1" else "1"
        self.play(
            Transform(ybar[1][j0], MathTex(current[j0], font_size=22, color=RED).move_to(ybar[1][j0])),
            ybar[0][j0].animate.set_stroke(color=RED, width=4).set_fill(opacity=0.18),
            run_time=0.45
        )

        # syndrome = column j
        s = H_COLS[j0]
        # pulse through H arrow to the cube vertex
        pulse = Dot(ybar.get_right() + 0.15*RIGHT, radius=0.06, color=RED)
        self.add(pulse)
        self.play(pulse.animate.move_to(arrowH.get_start()), run_time=0.3)
        self.play(MoveAlongPath(pulse, arrowH), run_time=0.8, rate_func=smooth)
        self.remove(pulse)

        target = dots[vertices.index(s)]
        ringS = SurroundingRectangle(target, color=YELLOW, buff=0.12)
        self.play(Create(ringS), target.animate.set_color(YELLOW), run_time=0.4)

        # Edge-walk 000 -> s to make it feel geometric
        start = (0,0,0)
        traveler = Dot(proj_cube(start), radius=0.07, color=YELLOW)
        self.add(traveler)

        # walk in x,y,z order
        path = [start]
        cur = [0,0,0]
        if s[0]==1: cur[0]=1; path.append(tuple(cur))
        if s[1]==1: cur[1]=1; path.append(tuple(cur))
        if s[2]==1: cur[2]=1; path.append(tuple(cur))

        for a,b in zip(path[:-1], path[1:]):
            # find an edge line to pulse
            # build a line on the fly; we can pulse a temporary line for robustness
            L = Line(proj_cube(a), proj_cube(b), stroke_width=6, color=YELLOW)
            L.set_stroke(opacity=0.95)
            self.play(Create(L), run_time=0.15)
            self.play(traveler.animate.move_to(proj_cube(b)), run_time=0.55, rate_func=smooth)
            self.play(FadeOut(L), run_time=0.15)

        self.remove(traveler)

        # identify j
        identify = Tex(rf"Syndrome $={s[0]}{s[1]}{s[2]}$ matches column $j={j_demo}$",
                       font_size=30, color=YELLOW).to_edge(DOWN)
        flash = SurroundingRectangle(ybar[0][j0], color=YELLOW, buff=0.08)

        self.play(FadeIn(identify, shift=UP), Create(flash), run_time=0.6)
        self.wait(0.8)

        # Correction: flip back
        self.play(
            Transform(ybar[1][j0], MathTex("0", font_size=22, color=YELLOW).move_to(ybar[1][j0])),
            run_time=0.35
        )
        # send back to 000 (visual “back to kernel”)
        ring000 = SurroundingRectangle(dot000, color=BLUE_A, buff=0.14)
        self.play(Create(ring000), run_time=0.25)
        self.play(FadeOut(ring000), run_time=0.25)

        # cleanup
        self.play(FadeOut(cap_dec), FadeOut(identify), FadeOut(flip_box), FadeOut(flash), FadeOut(ringS),
                  FadeOut(idx_row), FadeOut(ej_marks),
                  run_time=0.9)
