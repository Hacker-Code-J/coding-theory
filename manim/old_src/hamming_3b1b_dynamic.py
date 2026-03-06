from manim import *
import numpy as np

# manim -pqh hamming_3b1b_dynamic.py Hamming3b1bDynamic

def col_to_tex(c):
    a,b,d = [int(x) for x in c]
    return rf"\begin{{pmatrix}}{a}\\{b}\\{d}\end{{pmatrix}}"

def bit_row(n=7, size=0.35, buff=0.12):
    # Returns (group_of_squares, group_of_labels)
    squares = VGroup(*[
        RoundedRectangle(corner_radius=0.08, height=size, width=size,
                         stroke_width=2)
        for _ in range(n)
    ]).arrange(RIGHT, buff=buff)
    labels = VGroup(*[
        MathTex("0", font_size=26)
        for _ in range(n)
    ])
    for sq, lb in zip(squares, labels):
        lb.move_to(sq)
    return squares, labels

class Hamming3b1bDynamic(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"

        # --------------------------
        # 0) Title + "three lenses"
        # --------------------------
        title = Tex(r"Hamming $(7,4,3)_2$ as subset / image / kernel",
                    font_size=52, color=WHITE).to_edge(UP)
        lenses = VGroup(
            Tex(r"Subset: $C\subseteq \mathbb{F}_2^7$", font_size=34, color=GREY_A),
            Tex(r"Image: $C=\mathrm{Im}(Enc)$, $Enc:\mathbb{F}_2^4\to\mathbb{F}_2^7$", font_size=34, color=GREY_A),
            Tex(r"Kernel: $C=\ker(H)$, $H:\mathbb{F}_2^7\to\mathbb{F}_2^3$", font_size=34, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT).shift(0.35*DOWN)

        self.play(FadeIn(title, shift=DOWN))
        self.play(LaggedStart(*[Write(x) for x in lenses], lag_ratio=0.15))
        self.wait(0.4)

        kbox = SurroundingRectangle(lenses[2], color=YELLOW, buff=0.12)
        self.play(Create(kbox))
        self.wait(0.25)

        # --------------------------
        # 1) Show H and its columns
        # --------------------------
        H_tex = MathTex(
            r"H=\begin{pmatrix}"
            r"1&0&1&0&1&0&1\\"
            r"0&1&1&0&0&1&1\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}",
            font_size=40, color=WHITE
        ).next_to(title, DOWN, buff=0.55)

        claim = Tex(r"Columns are all nonzero vectors in $\mathbb{F}_2^3$",
                    font_size=34, color=GREY_B).next_to(H_tex, DOWN, buff=0.35)

        self.play(FadeOut(lenses[0:2], shift=LEFT), FadeOut(kbox, shift=LEFT))
        self.play(lenses[2].animate.to_edge(LEFT).shift(0.95*UP))
        self.play(Write(H_tex))
        self.play(FadeIn(claim, shift=DOWN))
        self.wait(0.3)

        cols = [
            (1,0,0),
            (0,1,0),
            (1,1,0),
            (0,0,1),
            (1,0,1),
            (0,1,1),
            (1,1,1),
        ]

        # panel for syndrome vectors
        panel = RoundedRectangle(corner_radius=0.25, height=3.7, width=6.2,
                                 color=BLUE_E, stroke_width=2).to_edge(RIGHT).shift(0.1*DOWN)
        panel_label = Tex(r"$\mathbb{F}_2^3$ (syndromes)", font_size=34, color=BLUE_A)\
            .next_to(panel, UP, buff=0.2)

        self.play(Create(panel), FadeIn(panel_label))

        col_mobs = VGroup(*[
            MathTex(col_to_tex(c), font_size=34, color=WHITE)
            for c in cols
        ])
        col_mobs.arrange_in_grid(rows=2, cols=4, buff=0.42)
        col_mobs.move_to(panel.get_center()).shift(0.05*UP + 0.12*LEFT)

        # index labels 1..7
        idx = VGroup(*[
            Tex(rf"$j={j+1}$", font_size=26, color=GREY_B).next_to(col_mobs[j], DOWN, buff=0.08)
            for j in range(7)
        ])

        self.play(LaggedStart(*[FadeIn(m) for m in col_mobs], lag_ratio=0.07))
        self.play(LaggedStart(*[FadeIn(t) for t in idx], lag_ratio=0.05))
        self.wait(0.35)

        # --------------------------
        # 2) Kernel definition + parameters
        # --------------------------
        ker = MathTex(r"C=\ker(H)=\{x\in\mathbb{F}_2^7:\;Hx^\top=0\}",
                      font_size=42, color=YELLOW).next_to(claim, DOWN, buff=0.42)
        params = Tex(r"$(7,4,3)_2$  $\Rightarrow$  corrects $1$ error",
                     font_size=34, color=GREY_A).next_to(ker, DOWN, buff=0.18)

        self.play(Write(ker))
        self.play(FadeIn(params, shift=DOWN))
        self.wait(0.35)

        # --------------------------
        # 3) The "wire" visualization of H : F2^7 -> F2^3
        # --------------------------
        # 7-bit word row
        squares, bits = bit_row(n=7, size=0.38, buff=0.12)
        word = VGroup(squares, bits).move_to(2.6*LEFT + 1.4*DOWN)
        word_label = Tex(r"word $y\in\mathbb{F}_2^7$", font_size=30, color=GREY_B)\
            .next_to(word, UP, buff=0.22).align_to(word, LEFT)

        self.play(FadeIn(word_label, shift=UP), FadeIn(word, shift=UP))

        # 3-bit syndrome register on right-bottom
        syn_sq, syn_bits = bit_row(n=3, size=0.42, buff=0.18)
        syndrome = VGroup(syn_sq, syn_bits).move_to(4.2*RIGHT + 1.55*DOWN)
        syn_label = Tex(r"syndrome $s(y)=Hy^\top\in\mathbb{F}_2^3$",
                        font_size=30, color=BLUE_A).next_to(syndrome, UP, buff=0.22)

        for sq in syn_sq:
            sq.set_stroke(width=2)
        self.play(FadeIn(syn_label, shift=UP), FadeIn(syndrome, shift=UP))
        self.wait(0.2)

        # "H" map label with arrow
        map_arrow = Arrow(word.get_right(), syndrome.get_left(),
                          buff=0.35, color=WHITE)
        H_map = MathTex(r"H", font_size=42, color=WHITE).next_to(map_arrow, UP, buff=0.1)
        self.play(GrowArrow(map_arrow), FadeIn(H_map))
        self.wait(0.15)

        # 7 wires to each syndrome bit (stylized)
        wires = VGroup()
        for j in range(7):
            start = squares[j].get_bottom() + 0.06*DOWN
            # split endpoints to 3 syndrome squares
            for r in range(3):
                end = syn_sq[r].get_top() + 0.06*UP
                # only draw wire if H[r,j] = 1
                Hij = [
                    [1,0,1,0,1,0,1],
                    [0,1,1,0,0,1,1],
                    [0,0,0,1,1,1,1],
                ][r][j]
                if Hij == 1:
                    path = CubicBezier(
                        start,
                        start + 0.8*DOWN + 0.2*(j-3)*RIGHT,
                        end + 0.8*UP + 0.3*(j-3)*RIGHT,
                        end
                    )
                    path.set_stroke(color=GREY_C, width=2, opacity=0.7)
                    wires.add(path)

        self.play(LaggedStart(*[Create(w) for w in wires], lag_ratio=0.01), run_time=1.0)
        self.wait(0.25)

        # --------------------------
        # 4) Single-bit error pulse travels + syndrome becomes a column
        # --------------------------
        story = VGroup(
            MathTex(r"y=c+e", font_size=42, color=WHITE),
            MathTex(r"s(y)=Hy^\top=H(c+e)^\top=He^\top", font_size=38, color=YELLOW),
            MathTex(r"e=e_j\ \Rightarrow\ He_j^\top=\text{$j$-th column of }H", font_size=38, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT).shift(0.15*DOWN)

        self.play(FadeIn(story, shift=RIGHT))
        self.wait(0.25)

        # pick which bit flips (change this)
        j_demo = 6  # 1..7
        j = j_demo - 1

        # highlight the chosen bit square and change label to 1
        pulse_color = YELLOW
        self.play(
            squares[j].animate.set_stroke(color=pulse_color, width=4).set_fill(opacity=0.15),
            bits[j].animate.set_color(pulse_color),
            Transform(bits[j], MathTex("1", font_size=26, color=pulse_color).move_to(bits[j])),
            run_time=0.6
        )
        self.wait(0.15)

        # Make a traveling dot that goes to the syndrome register via a representative route:
        # We compute the column vector visually by highlighting the corresponding column in the panel.
        target_col = col_mobs[j]
        target_idx = idx[j]
        col_highlight = SurroundingRectangle(target_col, color=pulse_color, buff=0.12)
        self.play(Create(col_highlight),
                  target_col.animate.set_color(pulse_color),
                  target_idx.animate.set_color(pulse_color),
                  run_time=0.5)
        self.wait(0.15)

        # Update syndrome bits to match that column (hard-coded from cols list)
        a,b,c = cols[j]
        new_syn = [a,b,c]
        syn_targets = VGroup(*[
            MathTex(str(new_syn[r]), font_size=28, color=pulse_color).move_to(syn_bits[r])
            for r in range(3)
        ])

        # Animate "energy" pulses along the active wires for that column
        active_rows = [r for r in range(3) if new_syn[r] == 1]
        pulses = VGroup()
        for r in active_rows:
            # find a wire from this bit to this syndrome component
            # (the wire exists because that entry is 1 in this column)
            # search in wires by proximity: pick a wire whose start is near squares[j] bottom and end near syn_sq[r] top
            start_ref = squares[j].get_bottom()
            end_ref = syn_sq[r].get_top()
            best = None
            best_score = 1e9
            for w in wires:
                # w is a CubicBezier; approximate endpoints via get_start/end
                s = w.get_start()
                e = w.get_end()
                score = np.linalg.norm(s-start_ref) + np.linalg.norm(e-end_ref)
                if score < best_score:
                    best_score = score
                    best = w
            if best is not None:
                dot = Dot(best.get_start(), radius=0.055, color=pulse_color)
                pulses.add(dot)
                self.add(dot)
                self.play(MoveAlongPath(dot, best), run_time=0.6, rate_func=linear)
                self.remove(dot)

        # Set syndrome register labels
        self.play(*[
            Transform(syn_bits[r], syn_targets[r])
            for r in range(3)
        ], *[
            syn_sq[r].animate.set_stroke(color=pulse_color if new_syn[r]==1 else GREY_C,
                                         width=4 if new_syn[r]==1 else 2)
            for r in range(3)
        ], run_time=0.6)

        self.wait(0.2)

        # Show "match -> j"
        conclusion = Tex(r"Match the syndrome with a column $\Rightarrow$ identify error position $j$",
                         font_size=36, color=WHITE)\
            .next_to(syn_label, DOWN, buff=0.28).align_to(syn_label, LEFT)
        self.play(Write(conclusion))
        self.wait(0.6)

        # --------------------------
        # 5) Finale: cube visualization of F2^3 (optional but very 3b1b)
        # --------------------------
        cube_title = Tex(r"Think of $\mathbb{F}_2^3$ as cube vertices (binary coordinates)",
                         font_size=32, color=GREY_B).to_edge(DOWN).shift(0.1*UP)
        self.play(FadeIn(cube_title, shift=UP))

        # Cube points in a 2D projection
        # Map (x,y,z) in {0,1}^3 to plane coordinates
        def proj(p):
            x,y,z = p
            return np.array([2.2 + 0.9*x + 0.45*z, -2.1 + 0.9*y + 0.45*z, 0])

        vertices = [(x,y,z) for x in [0,1] for y in [0,1] for z in [0,1]]
        dots = VGroup()
        labels = VGroup()
        for v in vertices:
            d = Dot(proj(v), radius=0.06, color=GREY_C)
            t = MathTex(rf"{v[0]}{v[1]}{v[2]}", font_size=26, color=GREY_B).next_to(d, RIGHT, buff=0.08)
            dots.add(d); labels.add(t)

        # edges of cube: differ by one coordinate
        edges = VGroup()
        for v in vertices:
            for w in vertices:
                if sum(abs(v[i]-w[i]) for i in range(3)) == 1:
                    if vertices.index(v) < vertices.index(w):
                        e = Line(proj(v), proj(w), stroke_width=2, color=GREY_E)
                        e.set_stroke(opacity=0.7)  # <-- compatible with Manim CE
                        edges.add(e)

        self.play(FadeIn(edges), FadeIn(dots), FadeIn(labels), run_time=0.8)

        # Highlight the syndrome vertex (a,b,c)
        synd_vertex = (a,b,c)
        s_dot = dots[vertices.index(synd_vertex)]
        s_box = SurroundingRectangle(s_dot, color=pulse_color, buff=0.12)
        self.play(Create(s_box), s_dot.animate.set_color(pulse_color))
        self.wait(0.7)

        # Soft fade-out
        self.play(*[FadeOut(m) for m in [
            title, lenses[2], H_tex, claim, panel, panel_label, col_mobs, idx,
            ker, params, word_label, word, syndrome, syn_label, map_arrow, H_map,
            wires, story, col_highlight, conclusion, cube_title, edges, dots, labels, s_box
        ]], run_time=1.0)
