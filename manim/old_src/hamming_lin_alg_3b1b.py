from manim import *
import numpy as np

# manim -pqh hamming_lin_alg_3b1b.py HammingLinearAlgebra3B1B
# manim -p -r 1920,1080 hamming_lin_alg_3b1b.py HammingLinearAlgebra3B1B

from manim import *
import numpy as np

# -----------------------------
# Canonical (7,4,3) Hamming code over F2
# -----------------------------
H = np.array([
    [1,0,1,0,1,0,1],
    [0,1,1,0,0,1,1],
    [0,0,0,1,1,1,1],
], dtype=int)

G = np.array([
    [1,0,0,0,0,1,1],
    [0,1,0,0,1,0,1],
    [0,0,1,0,1,1,0],
    [0,0,0,1,1,1,1],
], dtype=int)

H_COLS = [tuple(H[:, j].tolist()) for j in range(7)]  # syndromes of 1-bit errors

def f2(bits: str) -> np.ndarray:
    return np.array([int(b) for b in bits], dtype=int)

def bits(v: np.ndarray) -> str:
    return "".join(str(int(x) % 2) for x in v.tolist())

def enc(m_bits: str) -> str:
    """Enc(m)=mG (m is 1x4 over F2)"""
    m = f2(m_bits)
    c = (m @ G) % 2
    return bits(c)

def flip_bit(x_bits: str, j1: int) -> str:
    b = list(x_bits)
    j0 = j1 - 1
    b[j0] = "0" if b[j0] == "1" else "1"
    return "".join(b)

def proj_cube(v, origin=np.array([4.0, -1.2, 0.0]), sx=1.25, sy=1.25, sz=0.68):
    """Clean 2D projection of the cube {0,1}^3."""
    x, y, z = v
    return origin + np.array([sx*x + sz*z, sy*y + 0.55*sz*z, 0])

class HammingLinearAlgebra3B1B(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#0b0f19"
        frame = self.camera.frame

        # -----------------------------
        # Protagonist choices
        # -----------------------------
        m_bits = "1011"
        c_bits = enc(m_bits)       # a real codeword
        j_demo = 7                 # most dynamic: syndrome = 111
        y_bits = flip_bit(c_bits, j_demo)
        s = H_COLS[j_demo - 1]
        s_bits = f"{s[0]}{s[1]}{s[2]}"

        # -----------------------------
        # Stage layout: spaces + arrows
        # -----------------------------
        V = MathTex(r"V=\mathbb{F}_2^4", font_size=52, color=WHITE).move_to(LEFT*5 + UP*2.2)
        W = MathTex(r"W=\mathbb{F}_2^7", font_size=52, color=WHITE).move_to(LEFT*1 + UP*2.2)
        U = MathTex(r"U=\mathbb{F}_2^3", font_size=52, color=WHITE).move_to(RIGHT*3.6 + UP*2.2)

        a1 = Arrow(V.get_right(), W.get_left(), buff=0.25, color=WHITE)
        a2 = Arrow(W.get_right(), U.get_left(), buff=0.25, color=WHITE)
        labEnc = MathTex(r"Enc(m)=mG", font_size=36, color=WHITE).next_to(a1, UP, buff=0.12)
        labH   = MathTex(r"H", font_size=40, color=WHITE).next_to(a2, UP, buff=0.12)

        title = Tex(r"Hamming $(7,4,3)_2$ as image + kernel + syndrome geometry",
                    font_size=44, color=GREY_A).to_edge(UP)

        self.play(FadeIn(title, shift=DOWN), run_time=0.8)
        self.play(FadeIn(V), FadeIn(W), FadeIn(U), run_time=0.6)
        self.play(GrowArrow(a1), FadeIn(labEnc), GrowArrow(a2), FadeIn(labH), run_time=0.8)
        self.wait(0.2)

        # Zoom slightly to center the diagram (gentle 3b1b move)
        self.play(frame.animate.move_to(np.array([0.2, 1.0, 0])).set(width=13.0), run_time=0.8)

        # -----------------------------
        # Subspace visuals: C = Im(Enc) = ker(H)
        # -----------------------------
        C_sheet = RoundedRectangle(corner_radius=0.22, height=1.25, width=4.8,
                                   stroke_width=2, color=YELLOW)
        C_sheet.move_to(W.get_center() + DOWN*1.8)
        C_sheet.set_stroke(opacity=0.9)
        C_label = Tex(r"$C=\mathrm{Im}(Enc)=\ker(H)$", font_size=32, color=YELLOW)\
            .next_to(C_sheet, UP, buff=0.12).align_to(C_sheet, LEFT)

        self.play(Create(C_sheet), FadeIn(C_label, shift=UP), run_time=0.8)
        self.wait(0.2)

        # Flash G and H briefly (then disappear) — linear algebra authenticity
        G_tex = MathTex(
            r"G=\begin{pmatrix}"
            r"1&0&0&0&0&1&1\\"
            r"0&1&0&0&1&0&1\\"
            r"0&0&1&0&1&1&0\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}",
            font_size=30, color=GREY_A
        ).to_edge(LEFT).shift(DOWN*2.4)

        H_tex = MathTex(
            r"H=\begin{pmatrix}"
            r"1&0&1&0&1&0&1\\"
            r"0&1&1&0&0&1&1\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}",
            font_size=30, color=GREY_A
        ).to_edge(RIGHT).shift(DOWN*2.4)

        self.play(FadeIn(G_tex, shift=RIGHT), FadeIn(H_tex, shift=LEFT), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(G_tex, shift=LEFT), FadeOut(H_tex, shift=RIGHT), run_time=0.6)

        # -----------------------------
        # Animate a message m -> codeword c = mG (image lens)
        # -----------------------------
        m_dot = Dot(V.get_center() + DOWN*0.8, radius=0.08, color=WHITE)
        m_lbl = MathTex(r"m", font_size=34, color=WHITE).next_to(m_dot, UP, buff=0.10)

        c_dot = Dot(C_sheet.get_center() + LEFT*0.4, radius=0.09, color=YELLOW)
        c_lbl = MathTex(r"c=mG\in C", font_size=34, color=YELLOW).next_to(c_dot, UP, buff=0.10)

        cap_img = Tex(r"Image lens: $C=\mathrm{Im}(Enc)$", font_size=32, color=GREY_A)\
            .next_to(title, DOWN, buff=0.25)

        self.play(FadeIn(cap_img, shift=DOWN), run_time=0.5)
        self.play(FadeIn(m_dot), FadeIn(m_lbl), run_time=0.4)
        self.play(MoveAlongPath(m_dot, a1), run_time=0.9, rate_func=smooth)
        self.play(Transform(m_dot, c_dot), Transform(m_lbl, c_lbl), run_time=0.5)
        self.play(FadeOut(cap_img, shift=UP), run_time=0.4)
        self.wait(0.2)

        # -----------------------------
        # Kernel lens: Hc = 0 (c maps to origin in U)
        # -----------------------------
        zeroU = Dot(U.get_center() + DOWN*0.8, radius=0.08, color=BLUE_A)
        zeroLbl = MathTex(r"0", font_size=34, color=BLUE_A).next_to(zeroU, UP, buff=0.10)

        cap_ker = Tex(r"Kernel lens: $C=\ker(H)$ so $Hc=0$", font_size=32, color=YELLOW)\
            .next_to(title, DOWN, buff=0.25)

        self.play(FadeIn(zeroU), FadeIn(zeroLbl), run_time=0.4)
        self.play(FadeIn(cap_ker, shift=DOWN), run_time=0.5)
        self.play(MoveAlongPath(m_dot, a2), run_time=0.9, rate_func=smooth)
        self.play(Transform(m_dot, zeroU), run_time=0.4)
        self.play(FadeOut(cap_ker, shift=UP), run_time=0.4)

        comp = Tex(r"$H\circ Enc=0\quad(\Leftrightarrow\ HG^\top=0)$", font_size=30, color=GREY_B)\
            .next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(comp, shift=DOWN), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(comp, shift=UP), run_time=0.4)

        # -----------------------------
        # Syndrome geometry: cube for F2^3
        # -----------------------------
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

        cube_caption = Tex(r"$\mathbb{F}_2^3$ as a cube (syndromes)", font_size=26, color=BLUE_A)\
            .move_to(np.array([4.0, 0.35, 0]))

        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.01), run_time=0.9)
        self.play(FadeIn(dots), FadeIn(labels), FadeIn(cube_caption, shift=UP), run_time=0.6)
        self.wait(0.2)

        # Highlight all nonzero vertices (columns of H)
        cap_cols = Tex(r"Columns of $H$ are all nonzero vectors in $\mathbb{F}_2^3$",
                       font_size=30, color=GREY_A).next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(cap_cols, shift=DOWN), run_time=0.5)

        halos = VGroup(*[
            SurroundingRectangle(dots[vertices.index(v)], color=YELLOW, buff=0.12)
            for v in vertices if v != (0,0,0)
        ])
        self.play(LaggedStart(*[Create(h) for h in halos], lag_ratio=0.03), run_time=0.7)
        self.play(FadeOut(halos), FadeOut(cap_cols, shift=UP), run_time=0.5)

        # -----------------------------
        # 1-bit error: syndrome is column j (j=7 gives 111)
        # -----------------------------
        cap_err = Tex(
            rf"1-bit error $e_{{{j_demo}}}$: $s(y)=He_{{{j_demo}}}^\top$ is the {j_demo}-th column of $H$",
            font_size=28, color=WHITE
        ).to_edge(DOWN)

        self.play(FadeIn(cap_err, shift=UP), run_time=0.6)

        # Error dot in W, mapped through H to vertex s
        e_dot = Dot(W.get_center() + DOWN*1.8 + RIGHT*1.9, radius=0.08, color=RED)
        e_lbl = MathTex(rf"e_{{{j_demo}}}", font_size=34, color=RED).next_to(e_dot, UP, buff=0.10)
        self.play(FadeIn(e_dot), FadeIn(e_lbl), run_time=0.5)

        mapped = Dot(e_dot.get_center(), radius=0.08, color=RED)
        self.add(mapped)
        self.play(MoveAlongPath(mapped, a2), run_time=0.9, rate_func=smooth)
        self.remove(mapped)

        target = dots[vertices.index(s)]
        ring = SurroundingRectangle(target, color=YELLOW, buff=0.12)
        self.play(Create(ring), target.animate.set_color(YELLOW), run_time=0.4)

        # Edge-walk 000 -> s (x then y then z) to “feel” the bits
        start = (0,0,0)
        traveler = Dot(proj_cube(start), radius=0.07, color=YELLOW)
        self.add(traveler)

        path = [start]
        cur = [0,0,0]
        if s[0] == 1:
            cur[0] = 1; path.append(tuple(cur))
        if s[1] == 1:
            cur[1] = 1; path.append(tuple(cur))
        if s[2] == 1:
            cur[2] = 1; path.append(tuple(cur))

        for a, b in zip(path[:-1], path[1:]):
            pulse_edge = edge_map[(a,b)].copy()
            pulse_edge.set_stroke(color=YELLOW, width=6)
            pulse_edge.set_stroke(opacity=0.95)
            self.play(Create(pulse_edge), run_time=0.15)
            self.play(traveler.animate.move_to(proj_cube(b)), run_time=0.55, rate_func=smooth)
            self.play(FadeOut(pulse_edge), run_time=0.15)

        self.remove(traveler)

        decode = Tex(rf"Unique match $\Rightarrow$ error position $j={j_demo}$",
                     font_size=32, color=YELLOW).next_to(cap_err, UP, buff=0.2)
        self.play(FadeIn(decode, shift=UP), run_time=0.6)
        self.wait(1.0)

        self.play(FadeOut(cap_err), FadeOut(decode), FadeOut(ring), run_time=0.7)
