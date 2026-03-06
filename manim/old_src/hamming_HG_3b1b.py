from manim import *
import numpy as np

# manim -pqh hamming_HG_3b1b.py HammingHG3B1B

# ------------------------------------------------------------
# Your matrices (over F2)
# ------------------------------------------------------------
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

# Columns of H as tuples (these are the syndromes of single-bit errors)
H_COLS = [tuple(H[:, j].tolist()) for j in range(H.shape[1])]  # length 7, each length 3

# ------------------------------------------------------------
# Small F2 helpers
# ------------------------------------------------------------
def f2_vec_from_bits(bits: str) -> np.ndarray:
    return np.array([int(b) for b in bits], dtype=int)

def f2_bits_from_vec(v: np.ndarray) -> str:
    return "".join(str(int(x) % 2) for x in v.tolist())

def encode(m_bits: str) -> str:
    """Enc(m)=mG with m a 1x4 row over F2."""
    m = f2_vec_from_bits(m_bits)  # length 4
    c = (m @ G) % 2
    return f2_bits_from_vec(c)

def flip_bit(bits: str, j1: int) -> str:
    b = list(bits)
    j0 = j1 - 1
    b[j0] = "0" if b[j0] == "1" else "1"
    return "".join(b)

# ------------------------------------------------------------
# Visual primitives
# ------------------------------------------------------------
def bit_cell(size=0.48):
    return RoundedRectangle(corner_radius=0.10, height=size, width=size, stroke_width=2)

def make_register(bitstring, size=0.48, buff=0.09, font_size=30, color=WHITE):
    bits = list(bitstring)
    cells = VGroup(*[bit_cell(size) for _ in bits]).arrange(RIGHT, buff=buff)
    labels = VGroup(*[
        MathTex(bits[i], font_size=font_size, color=color).move_to(cells[i])
        for i in range(len(bits))
    ])
    return VGroup(cells, labels)

def set_register_bits(scene, reg, bitstring, color=YELLOW, run_time=0.5):
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

def proj_cube(v, origin=np.array([3.9, -0.15, 0.0]), sx=1.35, sy=1.35, sz=0.72):
    """Clean 2D projection for cube {0,1}^3."""
    x, y, z = v
    return origin + np.array([sx*x + sz*z, sy*y + 0.55*sz*z, 0])

class HammingHG3B1B(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"

        # ------------------------------------------------------------
        # Protagonist choices
        # ------------------------------------------------------------
        m_bits = "1011"              # message (data)
        x_bits = encode(m_bits)      # codeword (image viewpoint)
        # choose an error with "most geometric motion": syndrome 111 occurs at the column equal to 111
        # In your H, column 4 is (1,1,1)^T, so pick j=4 to get s=111 and a 3-step cube walk.
        j_demo = 4
        y_bits = flip_bit(x_bits, j_demo)
        s = H_COLS[j_demo - 1]       # syndrome = column j
        s_bits = f"{s[0]}{s[1]}{s[2]}"

        # ------------------------------------------------------------
        # 0) Title / SES (animated)
        # ------------------------------------------------------------
        title = Tex(
            r"$0\to C\hookrightarrow\mathbb{F}_2^7 \xrightarrow{H} \mathbb{F}_2^3\to 0$",
            font_size=40, color=GREY_A
        ).to_edge(UP)
        underline = Underline(title, buff=0.1).set_stroke(width=3)

        self.play(Write(title), Create(underline), run_time=0.9)
        self.play(FadeOut(underline), run_time=0.3)

        # ------------------------------------------------------------
        # 1) Build omniscient world (animated reveal)
        # ------------------------------------------------------------

        # LEFT: RAM page context
        page_origin = np.array([-4.1, 0.8, 0.0])
        d_list = ["0000","0001","0011","0101","1010","1111"]
        page_rows = []
        for i, dd in enumerate(d_list):
            cw = encode(dd)
            rr = make_register(cw, size=0.34, buff=0.05, font_size=18, color=GREY_B)
            rr.move_to(page_origin + np.array([0.0, -0.45*i, 0.0]))
            for c in rr[0]:
                c.set_stroke(color=GREY_E, width=2)
            for t in rr[1]:
                t.set_color(GREY_B)
            page_rows.append(rr)

        ram_page = VGroup(*page_rows)
        valid_box = RoundedRectangle(
            corner_radius=0.20,
            height=ram_page.height + 0.5,
            width=ram_page.width + 0.7,
            stroke_width=2, color=YELLOW
        )
        valid_box.move_to(ram_page.get_center())
        valid_box.set_stroke(opacity=0.85)
        valid_tag = Tex(r"$C=\ker(H)$", font_size=26, color=YELLOW)\
            .next_to(valid_box, UP, buff=0.12).align_to(valid_box, LEFT)

        # protagonist word x (7-bit)
        row = make_register("0000000", size=0.52, buff=0.10, font_size=34, color=WHITE)
        row.move_to(np.array([-3.9, -0.6, 0]))
        row_lab = Tex(r"$x\in\mathbb{F}_2^7$ (memory word)", font_size=26, color=GREY_A)\
            .next_to(row, UP, buff=0.20).align_to(row, LEFT)

        # data|parity braces (systematic by G)
        cells = row[0]
        data_brace = Brace(VGroup(*cells[:4]), DOWN, color=GREY_B)
        par_brace  = Brace(VGroup(*cells[4:]), DOWN, color=GREY_B)
        data_tag = Tex("data", font_size=22, color=GREY_B).next_to(data_brace, DOWN, buff=0.08)
        par_tag  = Tex("parity", font_size=22, color=GREY_B).next_to(par_brace, DOWN, buff=0.08)

        # TOP-LEFT: data register + encoder box
        data_reg = make_register(m_bits, size=0.50, buff=0.12, font_size=34, color=WHITE)
        data_reg.move_to(np.array([-4.3, 2.0, 0]))
        data_lab = Tex(r"$m\in\mathbb{F}_2^4$", font_size=26, color=GREY_B)\
            .next_to(data_reg, UP, buff=0.18).align_to(data_reg, LEFT)

        enc_box = RoundedRectangle(corner_radius=0.18, height=0.95, width=1.65,
                                   stroke_width=2, color=GREY_B)
        enc_box.move_to(np.array([-2.2, 2.0, 0]))
        enc_text = Tex(r"$Enc(m)=mG$", font_size=26, color=WHITE).move_to(enc_box)

        # RIGHT: cube = F2^3
        vertices = [(x,y,z) for x in [0,1] for y in [0,1] for z in [0,1]]
        dots = VGroup()
        labels = VGroup()
        for v in vertices:
            d = Dot(proj_cube(v), radius=0.06, color=GREY_C)
            t = MathTex(f"{v[0]}{v[1]}{v[2]}", font_size=24, color=GREY_B).next_to(d, RIGHT, buff=0.06)
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
        cube_caption = Tex(r"$\mathbb{F}_2^3$ (syndromes)", font_size=26, color=BLUE_A)\
            .next_to(cube, UP, buff=0.18).align_to(cube, LEFT)

        # CENTER: H arrow
        H_arrow = Arrow(ram_page.get_right() + 0.4*RIGHT, cube.get_left() + 0.4*LEFT,
                        buff=0.25, color=WHITE)
        H_tag = MathTex(r"H", font_size=42, color=WHITE).next_to(H_arrow, UP, buff=0.10)

        # Syndrome register
        syn_reg = make_register("000", size=0.50, buff=0.12, font_size=34, color=WHITE)
        syn_reg.next_to(cube, DOWN, buff=0.35).align_to(cube, LEFT)
        syn_lab = Tex(r"$s(y)=Hy^\top$", font_size=24, color=BLUE_A).next_to(syn_reg, UP, buff=0.12)

        # --- Animated reveal (left -> center -> right) ---
        self.play(
            LaggedStart(
                FadeIn(ram_page, shift=0.2*UP),
                Create(valid_box),
                FadeIn(valid_tag, shift=0.2*UP),
                lag_ratio=0.2
            ),
            run_time=1.1
        )
        self.play(valid_box.animate.set_stroke(width=4), run_time=0.18)
        self.play(valid_box.animate.set_stroke(width=2), run_time=0.18)

        self.play(FadeIn(row, shift=0.2*UP), FadeIn(row_lab, shift=0.2*UP), run_time=0.7)
        self.play(GrowFromCenter(data_brace), GrowFromCenter(par_brace),
                  FadeIn(data_tag, shift=0.1*DOWN), FadeIn(par_tag, shift=0.1*DOWN),
                  run_time=0.7)

        self.play(FadeIn(data_reg, shift=0.2*DOWN), FadeIn(data_lab, shift=0.2*DOWN), run_time=0.6)
        self.play(Create(enc_box), FadeIn(enc_text, shift=0.1*UP), run_time=0.6)

        self.play(GrowArrow(H_arrow), FadeIn(H_tag, shift=0.1*UP), run_time=0.7)

        # cube: edges then vertices then labels
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.01), run_time=0.9)
        self.play(FadeIn(dots, shift=0.1*UP), run_time=0.4)
        self.play(FadeIn(labels, shift=0.1*UP), FadeIn(cube_caption, shift=0.1*UP), run_time=0.5)

        self.play(FadeIn(syn_reg, shift=0.2*UP), FadeIn(syn_lab, shift=0.2*UP), run_time=0.6)
        self.wait(0.2)

        # ------------------------------------------------------------
        # 2) Image lens: build x = mG (show digits fill)
        # ------------------------------------------------------------
        cap1 = Tex(r"Image: $C=\mathrm{Im}(Enc)$ with $Enc(m)=mG$",
                   font_size=30, color=GREY_A).to_edge(UP).shift(0.55*DOWN)
        self.play(FadeIn(cap1, shift=DOWN), run_time=0.6)

        # animate "m enters encoder"
        m_dot = Dot(data_reg.get_right() + 0.1*RIGHT, radius=0.06, color=WHITE)
        self.add(m_dot)
        self.play(m_dot.animate.move_to(enc_box.get_left() + 0.1*RIGHT), run_time=0.6, rate_func=smooth)
        self.remove(m_dot)

        # fill row as [data|000] then full codeword x
        set_register_bits(self, row, m_bits + "000", color=GREY_B, run_time=0.6)
        set_register_bits(self, row, x_bits, color=YELLOW, run_time=0.6)

        glow = SurroundingRectangle(row, color=YELLOW, buff=0.10)
        self.play(Create(glow), run_time=0.25)
        self.play(FadeOut(cap1), run_time=0.5)

        # ------------------------------------------------------------
        # 3) Kernel lens: Hx^T = 000 (and HG^T = 0 implicitly)
        # ------------------------------------------------------------
        cap2 = Tex(r"Kernel: $C=\ker(H)$, and $H(Enc(m))^\top=0$",
                   font_size=30, color=YELLOW).to_edge(UP).shift(0.55*DOWN)
        self.play(FadeIn(cap2, shift=DOWN), run_time=0.6)

        pulse_x = Dot(row.get_right() + 0.1*RIGHT, radius=0.07, color=YELLOW)
        self.add(pulse_x)
        self.play(MoveAlongPath(pulse_x, H_arrow), run_time=0.8, rate_func=smooth)
        self.remove(pulse_x)

        set_register_bits(self, syn_reg, "000", color=BLUE_A, run_time=0.4)
        dot000 = dots[vertices.index((0,0,0))]
        ring000 = SurroundingRectangle(dot000, color=BLUE_A, buff=0.14)
        self.play(Create(ring000), run_time=0.25)
        self.play(FadeOut(ring000), run_time=0.25)
        self.play(FadeOut(cap2), run_time=0.5)

        # ------------------------------------------------------------
        # 4) Columns of H = nonzero cube vertices
        # ------------------------------------------------------------
        cap3 = Tex(r"Columns of $H$ are all nonzero vectors in $\mathbb{F}_2^3$",
                   font_size=30, color=GREY_A).to_edge(UP).shift(0.55*DOWN)
        self.play(FadeIn(cap3, shift=DOWN), run_time=0.6)

        nonzero = [v for v in vertices if v != (0,0,0)]
        halos = VGroup(*[SurroundingRectangle(dots[vertices.index(v)], color=YELLOW, buff=0.12) for v in nonzero])
        self.play(LaggedStart(*[Create(h) for h in halos], lag_ratio=0.03), run_time=0.7)
        self.play(FadeOut(halos), run_time=0.4)
        self.play(FadeOut(cap3), run_time=0.5)

        # ------------------------------------------------------------
        # 5) Single-bit error e_j and syndrome lookup as cube walk
        # ------------------------------------------------------------
        cap4 = Tex(rf"Single-bit error: $y=x+e_{{{j_demo}}}$ (flip bit {j_demo})",
                   font_size=30, color=RED).to_edge(UP).shift(0.55*DOWN)
        self.play(FadeIn(cap4, shift=DOWN), run_time=0.6)

        j0 = j_demo - 1
        flip_box = SurroundingRectangle(row[0][j0], color=RED, buff=0.10)
        self.play(Create(flip_box), run_time=0.25)
        self.play(
            Transform(row[1][j0], MathTex(y_bits[j0], font_size=34, color=RED).move_to(row[1][j0])),
            row[0][j0].animate.set_stroke(color=RED, width=4).set_fill(opacity=0.18),
            run_time=0.45
        )
        self.play(FadeOut(cap4), run_time=0.4)

        cap5 = Tex(rf"$s(y)=Hy^\top=He_{{{j_demo}}}^\top$ equals the $j$-th column of $H$",
                   font_size=28, color=WHITE).to_edge(UP).shift(0.55*DOWN)
        self.play(FadeIn(cap5, shift=DOWN), run_time=0.6)

        # cancellation picture: x maps to 000 (fade), error defines syndrome
        # yellow pulse (x) -> 000
        pulse_x2 = Dot(row.get_right() + 0.1*RIGHT, radius=0.07, color=YELLOW)
        self.add(pulse_x2)
        self.play(MoveAlongPath(pulse_x2, H_arrow), run_time=0.8, rate_func=smooth)
        self.remove(pulse_x2)
        ring000 = SurroundingRectangle(dot000, color=YELLOW, buff=0.14)
        self.play(Create(ring000), run_time=0.2)
        self.play(FadeOut(ring000), run_time=0.2)

        # red pulse (error) -> syndrome register
        pulse_e = Dot(row[0][j0].get_center(), radius=0.07, color=RED)
        self.add(pulse_e)
        self.play(pulse_e.animate.move_to(row.get_right() + 0.1*RIGHT), run_time=0.25)
        self.play(MoveAlongPath(pulse_e, H_arrow), run_time=0.9, rate_func=smooth)
        self.remove(pulse_e)

        set_register_bits(self, syn_reg, s_bits, color=BLUE_A, run_time=0.5)
        self.play(FadeOut(cap5), run_time=0.5)

        # Edge-guided navigation: 000 -> s_bits (x then y then z)
        cap6 = Tex(r"Edge-walk on the cube: start at $000$, step for each 1-bit of $s(y)$",
                   font_size=28, color=BLUE_A).to_edge(UP).shift(0.55*DOWN)
        self.play(FadeIn(cap6, shift=DOWN), run_time=0.6)

        start = (0,0,0)
        target = (s[0], s[1], s[2])

        ring_start = SurroundingRectangle(dots[vertices.index(start)], color=WHITE, buff=0.14)
        ring_target = SurroundingRectangle(dots[vertices.index(target)], color=YELLOW, buff=0.14)
        self.play(Create(ring_start), run_time=0.25)

        traveler = Dot(proj_cube(start), radius=0.08, color=YELLOW)
        self.add(traveler)

        path = [start]
        cur = [0,0,0]
        if target[0] == 1:
            cur[0] = 1; path.append(tuple(cur))
        if target[1] == 1:
            cur[1] = 1; path.append(tuple(cur))
        if target[2] == 1:
            cur[2] = 1; path.append(tuple(cur))

        for a, b in zip(path[:-1], path[1:]):
            edge = edge_map[(a, b)]
            pulse_edge = edge.copy()
            pulse_edge.set_stroke(color=YELLOW, width=6)
            pulse_edge.set_stroke(opacity=0.95)
            self.play(Create(pulse_edge), run_time=0.15)
            self.play(traveler.animate.move_to(proj_cube(b)), run_time=0.55, rate_func=smooth)
            self.play(FadeOut(pulse_edge), run_time=0.15)

        self.remove(traveler)
        self.play(Create(ring_target), dots[vertices.index(target)].animate.set_color(YELLOW), run_time=0.3)
        self.play(FadeOut(cap6), run_time=0.5)

        # Decode punchline: identify j
        cap7 = Tex(rf"Decode: $s(y)=h_j$  $\Rightarrow$  $j={j_demo}$",
                   font_size=34, color=YELLOW).to_edge(DOWN)
        self.play(FadeIn(cap7, shift=UP), run_time=0.6)

        tag = Tex(rf"$h_{{{j_demo}}}$", font_size=28, color=YELLOW)\
            .next_to(dots[vertices.index(target)], UP, buff=0.10)
        flash = SurroundingRectangle(row[0][j0], color=YELLOW, buff=0.10)

        self.play(FadeIn(tag, shift=UP), Create(flash), run_time=0.5)
        self.wait(1.0)

        # Clean end
        self.play(FadeOut(cap7), FadeOut(tag), FadeOut(flash),
                  FadeOut(ring_start), FadeOut(ring_target),
                  FadeOut(flip_box), FadeOut(glow),
                  run_time=0.9)
