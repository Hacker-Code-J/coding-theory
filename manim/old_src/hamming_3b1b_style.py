# manim -pqh hamming_3b1b_style.py Hamming3B1B
#
# A more “3blue1brown-ish” scene:
# - clean layout, big arrows, subtle highlights, motion cues
# - emphasizes: subset -> linear subspace -> image(Enc) -> kernel(H)
# - then zooms into Hamming(7,4,3): columns = nonzero vectors in F2^3
# - demonstrates: single-bit error e_j => syndrome s = H e^T equals j-th column => identify j
#
# Manim Community Edition >= 0.17 recommended.

from manim import *
import numpy as np

# ---------- style knobs ----------
BG = "#0b0f1a"          # deep navy
ACCENT = "#4cc9f0"      # cyan
ACCENT2 = "#f72585"     # magenta
SOFT = "#a7c5eb"        # pale blue
WARN = "#fca311"        # orange-ish
TEXT = "#e9ecef"        # off-white

def tex_matrix(m):
    rows = [" & ".join(str(int(x)) for x in r) for r in m]
    body = r"\\ ".join(rows)
    return rf"\begin{{pmatrix}} {body} \end{{pmatrix}}"

def col_tex(v):
    return rf"\begin{{pmatrix}} {int(v[0])}\\ {int(v[1])}\\ {int(v[2])} \end{{pmatrix}}"

def hamming_H():
    return np.array([
        [1,0,1,0,1,0,1],
        [0,1,1,0,0,1,1],
        [0,0,0,1,1,1,1],
    ], dtype=int)

class Hamming3B1B(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ============================================================
        # 0) Header: "block code" + three mathematical structures
        # ============================================================
        header = Tex(r"Block code", color=TEXT).scale(0.95)
        defn = MathTex(r"C\subseteq \Sigma^n", color=TEXT).scale(1.3)
        header_group = VGroup(header, defn).arrange(RIGHT, buff=0.35)
        header_group.to_edge(UP, buff=0.55)

        self.play(FadeIn(header_group, shift=DOWN), run_time=0.9)

        # three “structure cards” (subspace / image / kernel)
        card_w, card_h = 4.25, 1.35

        def card(title_tex, body_tex, color=ACCENT):
            box = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.18,
                                   stroke_color=color, stroke_width=2.5,
                                   fill_color=BLACK, fill_opacity=0.25)
            title = Tex(title_tex, color=color).scale(0.7).to_edge(UP)
            body = MathTex(body_tex, color=TEXT).scale(0.75)
            title.next_to(box.get_top(), DOWN, buff=0.12)
            body.move_to(box.get_center()).shift(0.05*DOWN)
            return VGroup(box, title, body)

        c1 = card(r"Linear subspace",
                  r"\Sigma=\mathbb{F}_q,\ \ C\le \mathbb{F}_q^n",
                  color=ACCENT)
        c2 = card(r"Image of encoding",
                  r"Enc:\Sigma^k\to\Sigma^n,\ \ \mathrm{im}(Enc)=C",
                  color=ACCENT2)
        c3 = card(r"Kernel of checks",
                  r"H:\mathbb{F}_q^n\to\mathbb{F}_q^{n-k},\ \ \ker(H)=C",
                  color=WARN)

        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.55).scale(0.92)
        cards.next_to(header_group, DOWN, buff=0.55)

        self.play(LaggedStart(
            FadeIn(c1, shift=UP*0.2),
            FadeIn(c2, shift=UP*0.2),
            FadeIn(c3, shift=UP*0.2),
            lag_ratio=0.18
        ), run_time=1.2)
        self.wait(0.35)

        # connective arrows between cards
        arr12 = Arrow(c1.get_right(), c2.get_left(), buff=0.18, stroke_width=5, color=SOFT)
        arr23 = Arrow(c2.get_right(), c3.get_left(), buff=0.18, stroke_width=5, color=SOFT)
        self.play(GrowArrow(arr12), GrowArrow(arr23), run_time=0.6)
        self.wait(0.25)

        # spotlight: "kernel(H)" is what we’ll use for Hamming
        spot = SurroundingRectangle(c3[0], color=WARN, buff=0.12, corner_radius=0.16)
        self.play(Create(spot), run_time=0.5)
        self.wait(0.3)

        # slide cards upward to make room for the Hamming demo “stage”
        everything = VGroup(header_group, cards, arr12, arr23, spot)
        self.play(everything.animate.scale(0.92).to_edge(UP, buff=0.2), run_time=0.8)

        # ============================================================
        # 1) Hamming setup: show H and “columns are all nonzero vectors”
        # ============================================================
        H = hamming_H()
        H_tex = MathTex(r"H=", tex_matrix(H), color=TEXT).scale(0.92)

        stage = RoundedRectangle(width=12.8, height=5.4, corner_radius=0.25,
                                 stroke_color=SOFT, stroke_width=2,
                                 fill_color=BLACK, fill_opacity=0.18)
        stage.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(stage), run_time=0.6)

        h_title = Tex(r"Hamming $(7,4,3)_2$", color=ACCENT).scale(0.9)
        h_sub = Tex(r"Columns of $H\in\mathbb{F}_2^{3\times 7}$ are all nonzero vectors in $\mathbb{F}_2^3$",
                    color=TEXT).scale(0.62)
        h_header = VGroup(h_title, h_sub).arrange(DOWN, buff=0.12).move_to(stage.get_top()).shift(0.65*DOWN)

        H_tex.move_to(stage.get_left()).shift(3.3*RIGHT + 0.3*DOWN)

        self.play(Write(h_header), run_time=0.9)
        self.play(FadeIn(H_tex, shift=LEFT*0.3), run_time=0.8)
        self.wait(0.25)

        # column indices under H (1..7)
        mat = H_tex[1]
        left_x = mat.get_left()[0]
        right_x = mat.get_right()[0]
        xs = np.linspace(left_x + 0.28, right_x - 0.28, 7)

        col_labels = VGroup()
        for j in range(7):
            t = Tex(str(j+1), color=SOFT).scale(0.48)
            t.move_to(np.array([xs[j], mat.get_bottom()[1]-0.35, 0]))
            col_labels.add(t)
        self.play(LaggedStart(*[FadeIn(l) for l in col_labels], lag_ratio=0.06), run_time=0.6)

        # ============================================================
        # 2) Make "nonzero vectors in F2^3" feel geometric
        #    We'll draw a cube-like 3D-ish grid of 8 points (but 2D)
        #    and highlight the 7 nonzero points with labels matching columns.
        # ============================================================
        cube_origin = stage.get_right() + LEFT*4.15 + UP*1.05
        # positions for 3-bit points: (b1,b2,b3) -> affine 2D embedding
        dx = 0.62
        dy = 0.55
        dz = 0.42
        # basis for a pseudo-3D look
        e1 = np.array([dx, 0, 0])       # x
        e2 = np.array([0, dy, 0])       # y
        e3 = np.array([dz, dz*0.9, 0])  # diagonal "z"

        pts = {}
        dots = VGroup()
        labels = VGroup()

        for a in [0,1]:
            for b in [0,1]:
                for c in [0,1]:
                    p = cube_origin + a*e1 + b*e2 + c*e3
                    key = (a,b,c)
                    pts[key] = p
                    dot = Dot(p, radius=0.055, color=SOFT if key!=(0,0,0) else "#444a57")
                    dots.add(dot)

        # edges of the cube (optional)
        edges = VGroup()
        def add_edge(u,v, opacity=0.35):
            edges.add(Line(pts[u], pts[v], stroke_width=2, color=SOFT).set_opacity(opacity))

        for b in [0,1]:
            for c in [0,1]:
                add_edge((0,b,c),(1,b,c))
        for a in [0,1]:
            for c in [0,1]:
                add_edge((a,0,c),(a,1,c))
        for a in [0,1]:
            for b in [0,1]:
                add_edge((a,b,0),(a,b,1))

        basis_label = Tex(r"$\mathbb{F}_2^3$", color=TEXT).scale(0.7)
        basis_label.next_to(dots, UP, buff=0.25).align_to(dots, LEFT)

        self.play(FadeIn(edges), FadeIn(dots), FadeIn(basis_label), run_time=0.9)

        # Now label the 7 nonzero points by the corresponding column index.
        # H columns in order:
        # 1:(1,0,0) 2:(0,1,0) 3:(1,1,0) 4:(0,0,1) 5:(1,0,1) 6:(0,1,1) 7:(1,1,1)
        cols = [H[:,j] for j in range(7)]
        key_map = []
        for j in range(7):
            v = tuple(int(x) for x in cols[j])
            key_map.append((j+1, v))

        for (idx, v) in key_map:
            p = pts[v]
            # glow ring
            ring = Circle(radius=0.12, color=ACCENT).move_to(p).set_stroke(width=3)
            ring.set_opacity(0.7)
            lab = Tex(str(idx), color=ACCENT).scale(0.48).next_to(p, RIGHT, buff=0.08)
            labels.add(VGroup(ring, lab))

        self.play(LaggedStart(*[FadeIn(g, shift=UP*0.05) for g in labels], lag_ratio=0.06),
                  run_time=0.9)
        self.wait(0.25)

        # subtle link: highlight column j in H and the matching point in F2^3
        # We'll do a quick “scan” across columns.
        scan_rect = Rectangle(width=(xs[1]-xs[0])*0.95,
                              height=(mat.get_top()[1]-mat.get_bottom()[1])*0.95,
                              stroke_color=ACCENT, stroke_width=4)
        scan_rect.move_to([xs[0], mat.get_center()[1], 0])
        self.play(Create(scan_rect), run_time=0.4)

        for j in range(7):
            # highlight cube label group for index j+1
            g = labels[j]
            self.play(
                scan_rect.animate.move_to([xs[j], mat.get_center()[1], 0]),
                g.animate.scale(1.12),
                run_time=0.25
            )
            self.play(g.animate.scale(1/1.12), run_time=0.18)

        self.play(FadeOut(scan_rect), run_time=0.25)

        # ============================================================
        # 3) Core decoding idea: one-bit error -> syndrome = column
        # ============================================================
        # Create a "received vector y = c + e" strip with 7 bits; flip one bit.
        strip_y = VGroup()
        bit_boxes = VGroup()
        bits = [0,1,1,0,1,0,0]  # arbitrary "received" bits for visualization
        # We'll say there is a 1-bit error at position j0
        j0 = 5  # 0-index; position 6 in 1-index
        pos = j0 + 1

        # build bit boxes
        start = stage.get_bottom() + UP*1.25 + LEFT*4.9
        for i in range(7):
            sq = RoundedRectangle(width=0.62, height=0.62, corner_radius=0.12,
                                  stroke_color=SOFT, stroke_width=2,
                                  fill_color=BLACK, fill_opacity=0.25)
            sq.move_to(start + RIGHT*i*0.72)
            t = Tex(str(bits[i]), color=TEXT).scale(0.65).move_to(sq.get_center())
            bit_boxes.add(VGroup(sq, t))
        strip_y = bit_boxes

        y_label = MathTex(r"y\in\mathbb{F}_2^7", color=TEXT).scale(0.75)
        y_label.next_to(strip_y, UP, buff=0.18).align_to(strip_y, LEFT)

        self.play(FadeIn(strip_y, shift=UP*0.15), FadeIn(y_label, shift=UP*0.15), run_time=0.8)

        # show "e_j" as a single red pulse on one box
        err_box = strip_y[j0][0]
        err_pulse = Circle(radius=0.36, color=ACCENT2).move_to(err_box.get_center()).set_stroke(width=6)
        err_text = MathTex(r"e_{%d}" % pos, color=ACCENT2).scale(0.75)
        err_text.next_to(err_box, DOWN, buff=0.25)

        self.play(Create(err_pulse), FadeIn(err_text, shift=DOWN*0.1), run_time=0.5)
        self.play(err_pulse.animate.set_opacity(0.2), run_time=0.3)

        # "syndrome map" arrow from y to s = H y^T (but for c+e, Hc^T=0 so s=He^T)
        map_group = VGroup()

        s_target = MathTex(r"s(y)=Hy^\top", color=TEXT).scale(0.85)
        s_target.next_to(strip_y, RIGHT, buff=1.0).shift(0.05*UP)

        map_arrow = Arrow(strip_y.get_right(), s_target.get_left(), buff=0.18,
                          stroke_width=6, color=ACCENT)
        map_label = Tex(r"parity checks", color=ACCENT).scale(0.55).next_to(map_arrow, UP, buff=0.08)

        self.play(GrowArrow(map_arrow), FadeIn(map_label), Write(s_target), run_time=0.9)

        # Now reveal the key simplification: since c in ker(H), Hc^T=0, so s=He^T
        simpl = MathTex(r"\text{If }c\in C=\ker(H),\ \ Hc^\top=0\ \Rightarrow\ s(y)=He^\top",
                        color=TEXT).scale(0.65)
        simpl.next_to(map_arrow, DOWN, buff=0.25).align_to(map_arrow, LEFT)
        box_simpl = SurroundingRectangle(simpl, color=SOFT, buff=0.15, corner_radius=0.12).set_opacity(0.85)

        self.play(FadeIn(box_simpl), Write(simpl), run_time=0.9)
        self.wait(0.25)

        # compute the syndrome (it's exactly the j0-th column)
        e = np.zeros(7, dtype=int)
        e[j0] = 1
        s = (H @ e) % 2
        colj = H[:, j0]

        syn_vec = MathTex(r"s = ", col_tex(s), color=TEXT).scale(0.95)
        syn_vec.next_to(s_target, DOWN, buff=0.35).align_to(s_target, LEFT)

        # highlight j0-th column in H and show equality
        col_rect = Rectangle(
            width=(xs[1]-xs[0])*0.95,
            height=(mat.get_top()[1]-mat.get_bottom()[1])*0.95,
            stroke_width=5,
            stroke_color=ACCENT2
        ).move_to([xs[j0], mat.get_center()[1], 0])

        claim = MathTex(r"= H_{(:,%d)}" % pos, color=ACCENT2).scale(0.95)
        claim.next_to(syn_vec, RIGHT, buff=0.25)

        self.play(Write(syn_vec), Create(col_rect), FadeIn(claim, shift=LEFT*0.1), run_time=0.8)

        # link syndrome to the cube point / label
        # find which cube label corresponds to this column (it is labels[j0])
        glow = labels[j0][0].copy().set_color(ACCENT2).set_opacity(0.95).set_stroke(width=5)
        self.play(Transform(labels[j0][0], glow), run_time=0.35)
        self.play(labels[j0][0].animate.set_opacity(0.75).set_color(ACCENT), run_time=0.35)

        # conclusion: identify position j
        concl = Tex(r"Syndrome $\;s\;$ uniquely identifies the error position $\;j$.", color=TEXT).scale(0.75)
        concl.to_edge(DOWN, buff=0.5)

        # Also show parameters quickly: (7,4,3)_2 and "corrects 1 error"
        params = MathTex(r"(n,k,d)=(7,4,3),\ \ t=\left\lfloor\frac{d-1}{2}\right\rfloor=1",
                         color=TEXT).scale(0.75)
        params.next_to(concl, UP, buff=0.18)

        params_box = SurroundingRectangle(params, color=WARN, buff=0.18, corner_radius=0.14).set_opacity(0.85)

        self.play(FadeIn(params_box), Write(params), run_time=0.8)
        self.play(Write(concl), run_time=0.7)

        # final emphasis pulse around the identified bit position
        pulse2 = Circle(radius=0.38, color=ACCENT2).move_to(err_box.get_center()).set_stroke(width=6)
        self.play(Create(pulse2), run_time=0.25)
        self.play(pulse2.animate.scale(1.25).set_opacity(0), run_time=0.45)

        self.wait(1.2)

        # tidy end: fade some stuff, keep the essence
        self.play(
            FadeOut(err_pulse),
            FadeOut(err_text),
            FadeOut(map_label),
            FadeOut(map_arrow),
            run_time=0.6
        )
        self.wait(0.4)
