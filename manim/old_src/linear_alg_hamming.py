from manim import *
import numpy as np

# manim -pqh linear_alg_hamming.py LinearAlgebraCoding

# ---------- Your example matrices ----------
H = np.array([
    [0, 1, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 1],
], dtype=int)

G = np.array([
    [1, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1],
], dtype=int)

def f2(bits):  # string -> np
    return np.array([int(b) for b in bits], dtype=int)

def bits(v):   # np -> string
    return "".join(str(int(x)%2) for x in v.tolist())

def enc(m_bits: str) -> str:
    m = f2(m_bits)
    c = (m @ G) % 2
    return bits(c)

def colH(j1: int):
    return tuple(H[:, j1-1].tolist())

def proj_cube(v, origin=np.array([4.1, -0.5, 0.0]), sx=1.2, sy=1.2, sz=0.65):
    x,y,z = v
    return origin + np.array([sx*x + sz*z, sy*y + 0.55*sz*z, 0])

class LinearAlgebraCoding(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"

        # --- Space boxes ---
        V = MathTex(r"\mathbb{F}_2^4", font_size=56).move_to(LEFT*5 + UP*1.2)
        W = MathTex(r"\mathbb{F}_2^7", font_size=56).move_to(LEFT*1 + UP*1.2)
        U = MathTex(r"\mathbb{F}_2^3", font_size=56).move_to(RIGHT*3.4 + UP*1.2)

        a1 = Arrow(V.get_right(), W.get_left(), buff=0.25)
        a2 = Arrow(W.get_right(), U.get_left(), buff=0.25)
        labG = MathTex(r"G", font_size=46).next_to(a1, UP, buff=0.12)
        labH = MathTex(r"H", font_size=46).next_to(a2, UP, buff=0.12)

        self.play(FadeIn(V), FadeIn(W), FadeIn(U))
        self.play(GrowArrow(a1), FadeIn(labG), GrowArrow(a2), FadeIn(labH))
        self.wait(0.2)

        # --- Subspace sheet in W: C = Im(Enc) ---
        sheet = RoundedRectangle(corner_radius=0.25, height=1.3, width=4.5,
                                 stroke_width=2, color=YELLOW)
        sheet.move_to(W.get_center() + DOWN*1.8)
        sheet.set_stroke(opacity=0.9)
        sheet_label = Tex(r"$C=\mathrm{Im}(Enc)$", font_size=34, color=YELLOW)\
            .next_to(sheet, UP, buff=0.12).align_to(sheet, LEFT)

        self.play(Create(sheet), FadeIn(sheet_label, shift=UP))
        self.wait(0.2)

        # --- Show G matrix briefly (flash) then shrink away ---
        G_tex = MathTex(
            r"G=\begin{pmatrix}"
            r"1&0&0&0&0&1&1\\"
            r"0&1&0&0&1&0&1\\"
            r"0&0&1&0&1&1&0\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}",
            font_size=32
        ).to_edge(LEFT).shift(DOWN*2.2)

        self.play(FadeIn(G_tex, shift=RIGHT), run_time=0.6)
        self.wait(0.4)
        self.play(FadeOut(G_tex, shift=LEFT), run_time=0.5)

        # --- Animate encoding m -> c = mG ---
        m_bits = "1011"
        c_bits = enc(m_bits)

        m_dot = Dot(V.get_center() + DOWN*0.9, radius=0.08, color=WHITE)
        m_lab = MathTex(r"m", font_size=34).next_to(m_dot, UP, buff=0.12)
        self.play(FadeIn(m_dot), FadeIn(m_lab))
        self.wait(0.1)

        c_dot = Dot(sheet.get_center(), radius=0.09, color=YELLOW)
        c_lab = MathTex(r"c=mG", font_size=34, color=YELLOW).next_to(c_dot, UP, buff=0.12)

        self.play(MoveAlongPath(m_dot, a1), run_time=0.8, rate_func=smooth)
        self.play(Transform(m_dot, c_dot), Transform(m_lab, c_lab), run_time=0.5)
        self.wait(0.2)

        # --- Show H matrix briefly (flash) then shrink away ---
        H_tex = MathTex(
            r"H=\begin{pmatrix}"
            r"0&1&1&1&1&0&0\\"
            r"1&0&1&1&0&1&0\\"
            r"1&1&0&1&0&0&1"
            r"\end{pmatrix}",
            font_size=32
        ).to_edge(RIGHT).shift(DOWN*2.2)

        self.play(FadeIn(H_tex, shift=LEFT), run_time=0.6)
        self.wait(0.4)
        self.play(FadeOut(H_tex, shift=RIGHT), run_time=0.5)

        # --- Kernel view: Hc = 0 (show dot goes to origin in U) ---
        zeroU = Dot(U.get_center() + DOWN*0.9, radius=0.08, color=BLUE_A)
        zeroLab = MathTex(r"0", font_size=34, color=BLUE_A).next_to(zeroU, UP, buff=0.12)

        self.play(FadeIn(zeroU), FadeIn(zeroLab), run_time=0.4)
        self.play(MoveAlongPath(m_dot, a2), run_time=0.8, rate_func=smooth)
        self.play(Transform(m_dot, zeroU), run_time=0.4)
        self.wait(0.2)

        comp = Tex(r"$H\circ Enc=0$  (equivalently $HG^\top=0$)", font_size=32, color=GREY_B)\
            .to_edge(UP).shift(DOWN*0.2)
        self.play(FadeIn(comp, shift=DOWN), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(comp, shift=UP), run_time=0.4)

        # --- Build syndrome cube in U: F2^3 ---
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

        cube = VGroup(edges, dots, labels)
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.01), run_time=0.9)
        self.play(FadeIn(dots), FadeIn(labels), run_time=0.5)
        self.wait(0.2)

        # --- Error: pick a j and show syndrome = column j ---
        j_demo = 4  # (in your H, column 4 = 111 gives a nice 3-step walk)
        s = colH(j_demo)
        s_bits = f"{s[0]}{s[1]}{s[2]}"

        err = Dot(W.get_center() + DOWN*1.8 + RIGHT*1.8, radius=0.08, color=RED)
        errLab = MathTex(r"e_j", font_size=34, color=RED).next_to(err, UP, buff=0.12)
        self.play(FadeIn(err), FadeIn(errLab), run_time=0.5)

        sy = Tex(rf"$s(y)=He_{{{j_demo}}}^\top$ is the {j_demo}-th column of $H$", font_size=30, color=WHITE)\
            .to_edge(DOWN)
        self.play(FadeIn(sy, shift=UP), run_time=0.6)

        # send error through H to land on syndrome vertex
        e_through = Dot(err.get_center(), radius=0.08, color=RED)
        self.add(e_through)
        self.play(MoveAlongPath(e_through, a2), run_time=0.8, rate_func=smooth)
        self.remove(e_through)

        target = dots[vertices.index(s)]
        ring = SurroundingRectangle(target, color=YELLOW, buff=0.12)
        self.play(Create(ring), target.animate.set_color(YELLOW), run_time=0.4)

        # edge-walk from 000 to s (x then y then z) to make it “3b1b geometric”
        start = (0,0,0)
        traveler = Dot(proj_cube(start), radius=0.07, color=YELLOW)
        self.add(traveler)

        path = [start]
        cur = [0,0,0]
        if s[0]==1: cur[0]=1; path.append(tuple(cur))
        if s[1]==1: cur[1]=1; path.append(tuple(cur))
        if s[2]==1: cur[2]=1; path.append(tuple(cur))

        for a,b in zip(path[:-1], path[1:]):
            pulse_edge = edge_map[(a,b)].copy().set_stroke(color=YELLOW, width=6)
            pulse_edge.set_stroke(opacity=0.95)
            self.play(Create(pulse_edge), run_time=0.15)
            self.play(traveler.animate.move_to(proj_cube(b)), run_time=0.55, rate_func=smooth)
            self.play(FadeOut(pulse_edge), run_time=0.15)

        self.remove(traveler)

        decode = Tex(rf"Match the syndrome vertex $\Rightarrow$ flipped position $j={j_demo}$",
                     font_size=30, color=YELLOW).next_to(sy, UP, buff=0.2)
        self.play(FadeIn(decode, shift=UP), run_time=0.6)
        self.wait(1.0)
