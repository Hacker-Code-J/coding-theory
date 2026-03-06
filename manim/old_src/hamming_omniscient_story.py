from manim import *
import numpy as np

# manim -pqh hamming_omniscient_story.py OmniscientHammingStory

# -----------------------------
# Math for your specific H (systematic x = [d | p])
# -----------------------------
def encode_systematic_for_given_H(d_bits: str) -> str:
    """
    For H = [[1 0 1 0 1 0 1],
             [0 1 1 0 0 1 1],
             [0 0 0 1 1 1 1]]
    with x = [d1 d2 d3 d4 p1 p2 p3], enforce Hx^T = 0:

    row1: d1 + d3 + p1 + p3 = 0
    row2: d2 + d3 + p2 + p3 = 0
    row3: d4 + p1 + p2 + p3 = 0

    Solve:
      p3 = d1 + d2 + d4
      p1 = d1 + d3 + p3
      p2 = d2 + d3 + p3
    """
    d = [int(b) for b in d_bits]  # length 4
    p3 = d[0] ^ d[1] ^ d[3]
    p1 = d[0] ^ d[2] ^ p3
    p2 = d[1] ^ d[2] ^ p3
    x = d + [p1, p2, p3]
    return "".join(str(b) for b in x)

def flip_bit(bits: str, j1: int) -> str:
    b = list(bits)
    j0 = j1 - 1
    b[j0] = "0" if b[j0] == "1" else "1"
    return "".join(b)

# columns of H in your order (syndrome for 1-bit error at position j)
H_COLS = [
    (1,0,0),  # j=1
    (0,1,0),  # j=2
    (1,1,0),  # j=3
    (0,0,1),  # j=4
    (1,0,1),  # j=5
    (0,1,1),  # j=6
    (1,1,1),  # j=7
]

# -----------------------------
# Visual primitives
# -----------------------------
def bit_cell(size=0.48):
    r = RoundedRectangle(corner_radius=0.10, height=size, width=size, stroke_width=2)
    return r

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
    x,y,z = v
    return origin + np.array([sx*x + sz*z, sy*y + 0.55*sz*z, 0])

class OmniscientHammingStory(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"

        # -----------------------------
        # Locked narrative choices
        # -----------------------------
        d_bits = "1011"
        x_bits = encode_systematic_for_given_H(d_bits)   # -> 1011010
        j_demo = 7
        y_bits = flip_bit(x_bits, j_demo)
        s = H_COLS[j_demo - 1]
        s_bits = f"{s[0]}{s[1]}{s[2]}"  # -> 111

        # -----------------------------
        # Global omniscient layout
        # -----------------------------
        title = Tex(
            r"$0\to C\hookrightarrow\mathbb{F}_2^7 \xrightarrow{H} \mathbb{F}_2^3\to 0$",
            font_size=40, color=GREY_A
        ).to_edge(UP)
#        self.add(title)
        underline = Underline(title, buff=0.1).set_stroke(width=3)
        self.play(Write(title), Create(underline), run_time=0.9)
        self.play(FadeOut(underline), run_time=0.3)

        # LEFT: data register and encoder
        data_reg = make_register(d_bits, size=0.50, buff=0.12, font_size=34, color=WHITE)
        data_reg.move_to(np.array([-4.3, 2.0, 0]))

        data_lab = Tex(r"data $d\in\mathbb{F}_2^4$", font_size=26, color=GREY_B)\
            .next_to(data_reg, UP, buff=0.18).align_to(data_reg, LEFT)

        enc_box = RoundedRectangle(corner_radius=0.18, height=0.95, width=1.65,
                                   stroke_width=2, color=GREY_B)
        enc_box.move_to(np.array([-2.2, 2.0, 0]))
        enc_text = Tex(r"$Enc$", font_size=30, color=WHITE).move_to(enc_box)

        # Output row (protagonist) sits in RAM area
        row = make_register("0000000", size=0.52, buff=0.10, font_size=34, color=WHITE)
        row.move_to(np.array([-3.9, -0.6, 0]))

        # data|parity braces
        cells = row[0]
        data_brace = Brace(VGroup(*cells[:4]), DOWN, color=GREY_B)
        par_brace  = Brace(VGroup(*cells[4:]), DOWN, color=GREY_B)
        data_tag = Tex("data", font_size=22, color=GREY_B).next_to(data_brace, DOWN, buff=0.08)
        par_tag  = Tex("parity", font_size=22, color=GREY_B).next_to(par_brace, DOWN, buff=0.08)

        row_lab = Tex(r"word in $\mathbb{F}_2^7$:  $x=[d\mid p]$", font_size=26, color=GREY_A)\
            .next_to(row, UP, buff=0.20).align_to(row, LEFT)

        # RAM page context (a few dim rows)
        page_origin = np.array([-4.1, 0.8, 0.0])
        d_list = ["0000","0001","0011","0101","1010","1111"]
        page_rows = []
        for i, dd in enumerate(d_list):
            cw = encode_systematic_for_given_H(dd)
            rr = make_register(cw, size=0.34, buff=0.05, font_size=18, color=GREY_B)
            rr.move_to(page_origin + np.array([0.0, -0.45*i, 0.0]))
            # dim visuals
            for c in rr[0]:
                c.set_stroke(color=GREY_E, width=2)
            for t in rr[1]:
                t.set_color(GREY_B)
            page_rows.append(rr)

        ram_page = VGroup(*page_rows)

        valid_box = RoundedRectangle(corner_radius=0.20,
                                     height=ram_page.height + 0.5,
                                     width=ram_page.width + 0.7,
                                     stroke_width=2, color=YELLOW)
        valid_box.move_to(ram_page.get_center())
        valid_box.set_stroke(opacity=0.85)
        valid_tag = Tex(r"valid slice $C=\ker(H)$", font_size=26, color=YELLOW)\
            .next_to(valid_box, UP, buff=0.12).align_to(valid_box, LEFT)

        # Center: H arrow
        # Place cube first to compute positions
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
        cube_caption = Tex(r"syndrome space $\mathbb{F}_2^3$ (cube)", font_size=26, color=BLUE_A)\
            .next_to(cube, UP, buff=0.18).align_to(cube, LEFT)

        H_arrow = Arrow(ram_page.get_right() + 0.4*RIGHT, cube.get_left() + 0.4*LEFT,
                        buff=0.25, color=WHITE)
        H_tag = MathTex(r"H", font_size=42, color=WHITE).next_to(H_arrow, UP, buff=0.10)

        # Syndrome register
        syn_reg = make_register("000", size=0.50, buff=0.12, font_size=34, color=WHITE)
        syn_reg.next_to(cube, DOWN, buff=0.35).align_to(cube, LEFT)
        syn_lab = Tex(r"$s(y)=Hy^\top$", font_size=24, color=BLUE_A).next_to(syn_reg, UP, buff=0.12)

#        # Add base objects (omniscient view)
#        self.add(ram_page, valid_box, valid_tag)
#        self.add(row, row_lab, data_brace, par_brace, data_tag, par_tag)
#        self.add(data_reg, data_lab, enc_box, enc_text)
#        self.add(H_arrow, H_tag)
#        self.add(cube, cube_caption)
#        self.add(syn_reg, syn_lab)

        # -----------------------------
        # Omniscient layout reveal (animated)
        # -----------------------------

        # 1) RAM page appears first (context)
        self.play(
            LaggedStart(
                FadeIn(ram_page, shift=0.2*UP),
                Create(valid_box),
                FadeIn(valid_tag, shift=0.2*UP),
                lag_ratio=0.2
            ),
            run_time=1.1
        )

        # Optional: give the valid slice a gentle “attention pulse”
        self.play(valid_box.animate.set_stroke(width=4), run_time=0.2)
        self.play(valid_box.animate.set_stroke(width=2), run_time=0.2)

        # 2) Protagonist row + data/parity braces
        self.play(
            FadeIn(row, shift=0.2*UP),
            FadeIn(row_lab, shift=0.2*UP),
            run_time=0.7
        )
        self.play(
            GrowFromCenter(data_brace),
            GrowFromCenter(par_brace),
            FadeIn(data_tag, shift=0.1*DOWN),
            FadeIn(par_tag, shift=0.1*DOWN),
            run_time=0.7
        )

        # 3) Data register + encoder box (top-left)
        self.play(
            FadeIn(data_reg, shift=0.2*DOWN),
            FadeIn(data_lab, shift=0.2*DOWN),
            run_time=0.6
        )
        self.play(
            Create(enc_box),
            FadeIn(enc_text, shift=0.1*UP),
            run_time=0.6
        )

        # 4) Map arrow H (bridge between worlds)
        self.play(GrowArrow(H_arrow), FadeIn(H_tag, shift=0.1*UP), run_time=0.7)

        # 5) Cube geometry (edges then vertices then labels)
        # If cube is VGroup(edges, dots, labels), reveal in that order:
        edges, dots, labels = cube[0], cube[1], cube[2]
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.01), run_time=0.9)
        self.play(FadeIn(dots, shift=0.1*UP), run_time=0.4)
        self.play(FadeIn(labels, shift=0.1*UP), FadeIn(cube_caption, shift=0.1*UP), run_time=0.5)

        # 6) Syndrome register under cube
        self.play(
            FadeIn(syn_reg, shift=0.2*UP),
            FadeIn(syn_lab, shift=0.2*UP),
            run_time=0.6
        )

        self.wait(0.2)

#        # -----------------------------
#        # Beat 1: "Type" data word + encode into codeword
#        # -----------------------------
#        cap1 = Tex(r"Image view: $Enc:\mathbb{F}_2^4\to\mathbb{F}_2^7$,  $C=\mathrm{Im}(Enc)$",
#                   font_size=30, color=GREY_A).to_edge(UP).shift(0.55*DOWN)
#        self.play(FadeIn(cap1, shift=DOWN), run_time=0.6)
#
#        # Animate data bits arriving into encoder
#        d_dot = Dot(data_reg.get_right() + 0.1*RIGHT, radius=0.06, color=WHITE)
#        self.add(d_dot)
#        self.play(d_dot.animate.move_to(enc_box.get_left() + 0.1*RIGHT), run_time=0.6, rate_func=smooth)
#        self.remove(d_dot)
#
#        # Fill row as [data|???] then parity
#        self.play(*[row[0][i].animate.set_stroke(color=GREY_C, width=3) for i in range(7)], run_time=0.3)
#        set_register_bits(self, row, d_bits + "000", color=GREY_B, run_time=0.6)
#        set_register_bits(self, row, x_bits, color=YELLOW, run_time=0.6)
#
#        # Slide the protagonist row visually “into” valid slice (small nudge + glow)
#        glow = SurroundingRectangle(row, color=YELLOW, buff=0.10)
#        self.play(Create(glow), run_time=0.3)
#        self.play(FadeOut(cap1), run_time=0.5)
#
#        # -----------------------------
#        # Beat 2: Kernel view: send x through H -> syndrome 000
#        # -----------------------------
#        cap2 = Tex(r"Kernel view: $C=\ker(H)$, so valid words satisfy $Hx^\top=000$",
#                   font_size=30, color=YELLOW).to_edge(UP).shift(0.55*DOWN)
#        self.play(FadeIn(cap2, shift=DOWN), run_time=0.6)
#
#        pulse_x = Dot(row.get_right() + 0.1*RIGHT, radius=0.07, color=YELLOW)
#        self.add(pulse_x)
#        self.play(MoveAlongPath(pulse_x, H_arrow), run_time=0.8, rate_func=smooth)
#        self.remove(pulse_x)
#
#        # Emphasize 000 in syndrome register and vertex 000
#        set_register_bits(self, syn_reg, "000", color=BLUE_A, run_time=0.4)
#        dot000 = dots[vertices.index((0,0,0))]
#        ring000 = SurroundingRectangle(dot000, color=BLUE_A, buff=0.14)
#        self.play(Create(ring000), run_time=0.25)
#        self.play(FadeOut(ring000), run_time=0.25)
#        self.play(FadeOut(cap2), run_time=0.5)
#
#        # -----------------------------
#        # Beat 3: SES exactness visual: two valid rows map to 000
#        # -----------------------------
#        cap3 = Tex(r"Exactness at $\mathbb{F}_2^7$: $\mathrm{Im}(\iota)=\ker(H)$",
#                   font_size=30, color=YELLOW).to_edge(UP).shift(0.55*DOWN)
#        self.play(FadeIn(cap3, shift=DOWN), run_time=0.6)
#
#        def pulse_row_to_zero(rr):
#            g = SurroundingRectangle(rr, color=YELLOW, buff=0.08)
#            self.play(Create(g), run_time=0.2)
#            dot = Dot(rr.get_right() + 0.1*RIGHT, radius=0.06, color=YELLOW)
#            self.add(dot)
#            self.play(MoveAlongPath(dot, H_arrow), run_time=0.7, rate_func=smooth)
#            self.remove(dot)
#            # pulse syndrome reg (stays 000)
#            self.play(*[
#                syn_reg[0][i].animate.set_stroke(color=BLUE_A, width=3).set_fill(opacity=0.10)
#                for i in range(3)
#            ], run_time=0.25)
#            self.play(FadeOut(g), run_time=0.2)
#
#        pulse_row_to_zero(page_rows[1])
#        pulse_row_to_zero(page_rows[4])
#        self.play(FadeOut(cap3), run_time=0.5)
#
#        # -----------------------------
#        # Beat 4: Columns are all nonzero cube vertices
#        # -----------------------------
#        cap4 = Tex(r"Columns of $H$ are exactly the 7 nonzero vectors in $\mathbb{F}_2^3$",
#                   font_size=30, color=GREY_A).to_edge(UP).shift(0.55*DOWN)
#        self.play(FadeIn(cap4, shift=DOWN), run_time=0.6)
#
#        # Glow all nonzero vertices
#        nonzero = [v for v in vertices if v != (0,0,0)]
#        halos = VGroup(*[SurroundingRectangle(dots[vertices.index(v)], color=YELLOW, buff=0.12) for v in nonzero])
#        self.play(LaggedStart(*[Create(h) for h in halos], lag_ratio=0.03), run_time=0.7)
#        self.play(FadeOut(halos), run_time=0.4)
#        self.play(FadeOut(cap4), run_time=0.5)
#
#        # -----------------------------
#        # Beat 5: Inject 1-bit error at j=7
#        # -----------------------------
#        cap5 = Tex(rf"Single-bit error: $y=x+e_{{{j_demo}}}$ (flip bit {j_demo})",
#                   font_size=30, color=RED).to_edge(UP).shift(0.55*DOWN)
#        self.play(FadeIn(cap5, shift=DOWN), run_time=0.6)
#
#        j0 = j_demo - 1
#        flip_box = SurroundingRectangle(row[0][j0], color=RED, buff=0.10)
#        self.play(Create(flip_box), run_time=0.25)
#        self.play(
#            Transform(row[1][j0], MathTex(y_bits[j0], font_size=34, color=RED).move_to(row[1][j0])),
#            row[0][j0].animate.set_stroke(color=RED, width=4).set_fill(opacity=0.18),
#            run_time=0.45
#        )
#        self.play(FadeOut(cap5), run_time=0.4)
#
#        # -----------------------------
#        # Beat 6: Cancellation: Hy = Hx + He7 = 0 + He7
#        # -----------------------------
#        cap6 = Tex(r"$s(y)=Hy^\top=H(x+e_7)^\top=Hx^\top+He_7^\top=He_7^\top$",
#                   font_size=28, color=WHITE).to_edge(UP).shift(0.55*DOWN)
#        self.play(FadeIn(cap6, shift=DOWN), run_time=0.6)
#
#        # yellow pulse for x: goes to 000 and fades
#        pulse_x2 = Dot(row.get_right() + 0.1*RIGHT, radius=0.07, color=YELLOW)
#        self.add(pulse_x2)
#        self.play(MoveAlongPath(pulse_x2, H_arrow), run_time=0.8, rate_func=smooth)
#        self.remove(pulse_x2)
#        # show "cancel" at 000
#        ring000 = SurroundingRectangle(dot000, color=YELLOW, buff=0.14)
#        self.play(Create(ring000), run_time=0.2)
#        self.play(FadeOut(ring000), run_time=0.2)
#
#        # red pulse for e7: starts at the flipped bit cell, goes through H
#        pulse_e = Dot(row[0][j0].get_center(), radius=0.07, color=RED)
#        self.add(pulse_e)
#        self.play(pulse_e.animate.move_to(row.get_right() + 0.1*RIGHT), run_time=0.25)
#        self.play(MoveAlongPath(pulse_e, H_arrow), run_time=0.9, rate_func=smooth)
#        self.remove(pulse_e)
#
#        # write syndrome 111
#        set_register_bits(self, syn_reg, s_bits, color=BLUE_A, run_time=0.5)
#        self.play(FadeOut(cap6), run_time=0.5)
#
#        # -----------------------------
#        # Beat 7: Edge-walk on cube from 000 to 111 (x then y then z)
#        # -----------------------------
#        cap7 = Tex(r"Edge-guided navigation: start at $000$ and walk to $s(y)$",
#                   font_size=30, color=BLUE_A).to_edge(UP).shift(0.55*DOWN)
#        self.play(FadeIn(cap7, shift=DOWN), run_time=0.6)
#
#        start = (0,0,0)
#        target = (s[0], s[1], s[2])
#
#        ring_start = SurroundingRectangle(dots[vertices.index(start)], color=WHITE, buff=0.14)
#        ring_target = SurroundingRectangle(dots[vertices.index(target)], color=YELLOW, buff=0.14)
#        self.play(Create(ring_start), run_time=0.25)
#
#        traveler = Dot(proj_cube(start), radius=0.08, color=YELLOW)
#        self.add(traveler)
#
#        # step order x,y,z when bit is 1
#        path = [start]
#        cur = list(start)
#        if target[0] == 1:
#            cur[0] = 1; path.append(tuple(cur))
#        if target[1] == 1:
#            cur[1] = 1; path.append(tuple(cur))
#        if target[2] == 1:
#            cur[2] = 1; path.append(tuple(cur))
#
#        for a, b in zip(path[:-1], path[1:]):
#            edge = edge_map[(a, b)]
#            pulse_edge = edge.copy()
#            pulse_edge.set_stroke(color=YELLOW, width=6)
#            pulse_edge.set_stroke(opacity=0.95)
#            self.play(Create(pulse_edge), run_time=0.15)
#            self.play(traveler.animate.move_to(proj_cube(b)), run_time=0.55, rate_func=smooth)
#            self.play(FadeOut(pulse_edge), run_time=0.15)
#
#        self.remove(traveler)
#        self.play(Create(ring_target), dots[vertices.index(target)].animate.set_color(YELLOW), run_time=0.3)
#        self.play(FadeOut(cap7), run_time=0.5)
#
#        # -----------------------------
#        # Beat 8: Decode: s(y)=h_j identifies j=7
#        # -----------------------------
#        cap8 = Tex(rf"Decode: $s(y)=h_j$  $\Rightarrow$  $j={j_demo}$",
#                   font_size=34, color=YELLOW).to_edge(DOWN)
#        self.play(FadeIn(cap8, shift=UP), run_time=0.6)
#
#        # tag vertex with "h7"
#        tag = Tex(r"$h_7$", font_size=28, color=YELLOW)\
#            .next_to(dots[vertices.index(target)], UP, buff=0.10)
#
#        # flash bit position 7 on the row
#        flash = SurroundingRectangle(row[0][j0], color=YELLOW, buff=0.10)
#        self.play(FadeIn(tag, shift=UP), Create(flash), run_time=0.5)
#        self.wait(1.0)
#
#        # clean finish
#        self.play(FadeOut(cap8), FadeOut(tag), FadeOut(flash),
#                  FadeOut(ring_start), FadeOut(ring_target), FadeOut(flip_box), FadeOut(glow),
#                  run_time=0.9)
