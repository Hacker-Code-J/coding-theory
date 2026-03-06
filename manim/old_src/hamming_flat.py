from manim import *
import numpy as np

# ============================================================
# Hamming (7,4,3) over F2 — flat, dynamic linear-algebra viz
# Run:
#   pip install manim
#   manim -pqh hamming_flat.py HammingFlat
#   manim -pql hamming_flat.py HammingFlat
# ============================================================

# ----------------------------
# Helpers: F2 linear algebra
# ----------------------------
def mod2(A):
    return np.array(A, dtype=int) % 2

def f2_matmul(A, B):
    # A @ B over F2
    return (A @ B) % 2

def f2_vecmul_row(v_row, M):
    # v_row: (n,), M: (n x m) -> (m,)
    return (v_row @ M) % 2

def bits_tex(v, sep="\\,"):
    return "\\begin{pmatrix}" + sep.join(str(int(x)) for x in v) + "\\end{pmatrix}"

def make_bit_string(v, one_color=GREEN, zero_color=GRAY_B):
    squares = VGroup()
    for b in v:
        sq = Square(side_length=0.35)
        sq.set_stroke(WHITE, 2)
        if int(b) == 1:
            sq.set_fill(one_color, opacity=0.9)
        else:
            sq.set_fill(zero_color, opacity=0.5)
        squares.add(sq)
    squares.arrange(RIGHT, buff=0.08)
    return squares

def label_bits_under(squares, v, font_size=22):
    labs = VGroup(*[
        MathTex(str(int(b)), font_size=font_size).next_to(sq, DOWN, buff=0.08)
        for sq, b in zip(squares, v)
    ])
    return labs

def highlight_column(matrix_mob, j, color=YELLOW):
    # rectangle around the j-th column
    entries = matrix_mob.get_entries()
    rows = matrix_mob.get_rows()
    cols = len(rows[0])
    rcount = len(rows)
    col_entries = []
    for r in range(rcount):
        idx = r * cols + j
        col_entries.append(entries[idx])
    col_group = VGroup(*col_entries)
    rect = SurroundingRectangle(col_group, buff=0.12, color=color)
    return rect, col_group

def syndrome_panel(vectors, header="Syndromes (nonzero in $\\mathbb{F}_2^3$)"):
    title = Tex(header, font_size=30)
    rows = VGroup()
    for i, v in enumerate(vectors, start=1):
        left = Tex(f"column vector {i}", font_size=26).set_opacity(0.9)
        bits = make_bit_string(v, one_color=BLUE, zero_color=GRAY_D)
        labs = label_bits_under(bits, v, font_size=18).set_opacity(0.9)
        row = VGroup(left, VGroup(bits, labs)).arrange(RIGHT, buff=0.25)
        rows.add(row)

    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    panel = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)

    bg = RoundedRectangle(corner_radius=0.18, width=panel.width + 0.55, height=panel.height + 0.45)
    bg.set_fill(GRAY_E, opacity=0.35).set_stroke(WHITE, opacity=0.15)
    group = VGroup(bg, panel)
    panel.move_to(bg.get_center())
    return group, rows

def flash_cell(mobj, color=YELLOW, buff=0.05, **kwargs):
    r = SurroundingRectangle(mobj, buff=buff, color=color, **kwargs)
    return r

BUFF_H = 0.55          # horizontal spacing between blocks
LEFT_MARGIN = 0.6
TOP_SHIFT = UP * 0.6
FIT_MARGIN = 1.4       # total width margin vs frame width

HILITE_COL = YELLOW
HILITE_ACTIVE = BLUE

def bin_entry(x, font_size=34, **_):
    return MathTex(str(int(x)), font_size=font_size)

def entry_at(entries, ncols, i, j):
    return entries[i*ncols + j]


# ----------------------------
# Main Scene
# ----------------------------
class HammingFlat(Scene):
    def construct(self):
        # Your matrices
        H = mod2([
            [0, 1, 1, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1],
        ])
        G = mod2([
            [1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1],
        ])

        # ----------------------------------------------------
        # Title + pipeline: F2^4 --G--> F2^7 --H--> F2^3
        # ----------------------------------------------------
        title = Tex("Hamming $[7,4,3]_2$", font_size=40).to_edge(UP, buff=0.15)

        pipe = MathTex(
            r"\mathbb{F}_2^4", r"\xrightarrow{\;\;G\;\;}", r"\mathbb{F}_2^7",
            r"\xrightarrow{\;\;H\;\;}", r"\mathbb{F}_2^3",
            font_size=44
        )

        pipe_box = RoundedRectangle(
            corner_radius=0.22,
            width=pipe.width + 0.6,
            height=pipe.height + 0.35
        ).set_fill(BLACK, opacity=0.35).set_stroke(WHITE, opacity=0.18)

        pipe_group = VGroup(pipe_box, pipe)
        pipe.move_to(pipe_box.get_center())

        # this is the key line
        pipe_group.next_to(title, DOWN, buff=0.05)

        self.play(FadeIn(title))
        self.play(FadeIn(pipe_group, shift=DOWN * 0.2))

#        banner = MathTex(r"C=\ker(H)=\mathrm{im}(G)\subseteq \mathbb{F}_2^7", font_size=40)
#        banner_bg = RoundedRectangle(corner_radius=0.2, width=banner.width + 0.55, height=banner.height + 0.35)
#        banner_bg.set_fill(GRAY_E, opacity=0.28).set_stroke(WHITE, opacity=0.15)
#        banner_group = VGroup(banner_bg, banner)
#        banner.move_to(banner_bg.get_center())
#        banner_group.to_edge(LEFT).shift(DOWN * 0.2)
#
#        self.play(FadeIn(banner_group, shift=RIGHT * 0.2))
#        self.wait(0.2)

        # ----------------------------------------------------
        # Left: show H and G as objects
        # ----------------------------------------------------
        G_tex = MathTex(
            r"G=",
            r"\begin{pmatrix}"
            r"1&0&0&0&0&1&1\\"
            r"0&1&0&0&1&0&1\\"
            r"0&0&1&0&1&1&0\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}",
            font_size=40
        ).to_edge(LEFT).shift(UP*0.9)   # choose a nice starting height

        H_tex = MathTex(
            r"H=",
            r"\begin{pmatrix}"
            r"0&1&1&1&1&0&0\\"
            r"1&0&1&1&0&1&0\\"
            r"1&1&0&1&0&0&1"
            r"\end{pmatrix}",
            font_size=40
        ).align_to(G_tex, LEFT)

        # KEY: control the gap here
        gap_GH = 1
        H_tex.next_to(G_tex, DOWN, buff=gap_GH, aligned_edge=LEFT)

        H_lab = Tex(r"Parity-check map $H:\mathbb{F}_2^7\to\mathbb{F}_2^3$", font_size=28)\
            .next_to(H_tex, DOWN, buff=0.18)
        H_lab.move_to([H_tex.get_center()[0], H_lab.get_center()[1], 0])

        G_lab = Tex(r"Generator map $G:\mathbb{F}_2^4\to\mathbb{F}_2^7$", font_size=28)\
            .next_to(G_tex, DOWN, buff=0.18)
        G_lab.move_to([G_tex.get_center()[0], G_lab.get_center()[1], 0])

        self.play(Write(G_tex), FadeIn(G_lab, shift=DOWN*0.15))
        self.play(Write(H_tex), FadeIn(H_lab, shift=DOWN*0.15))


        # ----------------------------------------------------
        # Right: flat syndrome lookup panel (columns of H)
        # ----------------------------------------------------
        # 1) Build the panel
        syndromes = [H[:, j] for j in range(7)]
        panel, synd_rows = syndrome_panel(syndromes)

        # 2) Put it to the right of the (G,H) block (controls x)
        left_block = VGroup(G_tex, G_lab, H_tex, H_lab)
        panel.next_to(left_block, RIGHT, buff=2)

        # 3) Move it to the vertical middle of the gap between G and H (controls y)
        gap_mid_y = 0.5 * (G_tex.get_bottom()[1] + H_tex.get_top()[1])
        panel.move_to([panel.get_center()[0], gap_mid_y, 0])

        self.play(FadeIn(panel, shift=LEFT * 0.2), run_time=1.5)
        self.wait(0.25)
        self.play(FadeOut(panel, shift=RIGHT * 0.2), run_time=1.5)
        self.wait(0.25)
        self.play(FadeOut(H_tex), FadeOut(H_lab, shift=UP*0.15))
        self.wait(0.25)
        self.play(FadeOut(G_tex), FadeOut(G_lab, shift=UP*0.15))

        # ----------------------------------------------------
        # Encoding: pick m, compute c=mG, show as bit strip
        # ----------------------------------------------------
#        enc_glow = SurroundingRectangle(pipe[0:3], buff=0.12, color=GREEN)
#
#        m = mod2([1, 0, 1, 1])
#        c = f2_vecmul_row(m, G)
#
#        m_tex = MathTex(r"m=", bits_tex(m), font_size=40).move_to(RIGHT * 0.5 + UP * 0.8)
#        c_tex = MathTex(r"c=mG=", bits_tex(c), font_size=40).next_to(m_tex, DOWN, buff=0.18).align_to(m_tex, LEFT)
#
#        c_bits = make_bit_string(c, one_color=GREEN, zero_color=GRAY_B).next_to(c_tex, DOWN, buff=0.25).align_to(c_tex, LEFT)
#        c_labs = label_bits_under(c_bits, c, font_size=20)
#
#        self.play(Create(enc_glow))
#        self.play(Write(m_tex))
#        self.play(Write(c_tex))
#        self.play(FadeIn(c_bits, shift=UP * 0.15), FadeIn(c_labs, shift=UP * 0.15))
#
#        # Show H c^T = 0 (kernel condition)
#        syn0 = f2_matmul(H, c.reshape(-1, 1)).reshape(-1)
#        ker_tex = MathTex(r"Hc^\top=", bits_tex(syn0), r"=0", font_size=40).next_to(c_bits, DOWN, buff=0.25).align_to(c_bits, LEFT)
#        self.play(Write(ker_tex))
#        self.wait(0.25)
#        self.play(FadeOut(ker_tex, shift=DOWN * 0.1), FadeOut(enc_glow))

        # ----------------------------------------------------
        # Encoding: pick m, compute c=mG, show as bit strip
        # ----------------------------------------------------
        enc_glow = SurroundingRectangle(pipe[0:3], buff=0.12, color=GREEN)

        # -----------------------------
        # Build "linear algebra" layout
        # -----------------------------
        m = mod2([1, 0, 1, 1])
        c = f2_vecmul_row(m, G)

        # Matrix versions FIRST (stable cell addressing)
        m_label = MathTex(r"m=", font_size=40)
        m_row = Matrix([list(map(int, m))], element_to_mobject=lambda x, **kw: bin_entry(x, 34, **kw),
               v_buff=0.35, h_buff=0.55).scale(0.7)

        m_group = VGroup(m_label, m_row).arrange(RIGHT, buff=0.18)

        G_label = MathTex(r"G=", font_size=40)
        G_mat = Matrix(G.tolist(), element_to_mobject=lambda x, **kw: bin_entry(x, 34, **kw),
               v_buff=0.35, h_buff=0.45).scale(0.7)
        G_group = VGroup(G_label, G_mat).arrange(RIGHT, buff=0.18)

        times = MathTex(r"\cdot", font_size=52)
        eq = MathTex(r"=", font_size=52)

        # Output bit strip (placeholder -> target)
        c_bits = make_bit_string([0]*7, one_color=GREEN, zero_color=GRAY_B)
        c_bits_target = make_bit_string(c, one_color=GREEN, zero_color=GRAY_B)

        # Arrange everything as ONE line, then fit + anchor (prevents clipping)
        la_group = VGroup(m_group, times, G_group, eq, c_bits).arrange(
            RIGHT, buff=BUFF_H, aligned_edge=ORIGIN
        )

        target_w = config.frame_width - FIT_MARGIN
        if la_group.width > target_w:
            la_group.scale_to_fit_width(target_w)

        la_group.to_edge(LEFT, buff=LEFT_MARGIN).shift(TOP_SHIFT)

        # Keep target exactly on top of placeholder positions
        c_bits_target.move_to(c_bits)

        # Animate entrance cleanly
        self.play(FadeIn(m_group, shift=RIGHT*0.15), run_time=0.6)
        self.play(FadeIn(times, shift=RIGHT*0.10), FadeIn(G_group, shift=RIGHT*0.10), run_time=0.6)
        self.play(FadeIn(eq, shift=RIGHT*0.10), FadeIn(c_bits, shift=UP*0.10), run_time=0.6)

        # -----------------------------
        # Convenience: stable indexing
        # -----------------------------
        m_entries = m_row.get_entries()     # 4 entries
        G_entries = G_mat.get_entries()     # 4*7 entries (row-major)

        def G_entry(i, j):
            return G_entries[i*7 + j]

        active = [i for i, mi in enumerate(m) if int(mi) == 1]

        # -----------------------------
        # Scratch area for XOR text (fixed location)
        # -----------------------------
        xor_anchor = VGroup(G_group, eq).get_right() + RIGHT*0.65 + UP*0.55
        xor_tex = MathTex("", font_size=30).move_to(xor_anchor)
        self.add(xor_tex)  # keep one object, update its content

        # Optional: a subtle background panel for XOR scratch (helps readability)
        xor_bg = RoundedRectangle(corner_radius=0.12,
                                 width=2.2, height=0.65).move_to(xor_anchor)
        xor_bg.set_fill(BLACK, opacity=0.25).set_stroke(WHITE, opacity=0.12)
        self.add(xor_bg)
        self.bring_to_front(xor_tex)

        # -----------------------------
        # Animate each output bit c_j = <m, col_j>
        # -----------------------------
        for j in range(7):
            # Column highlight (all 4 entries)
            col_rects = VGroup(*[
                flash_cell(G_entry(i, j), color=HILITE_COL, buff=0.06)
                for i in range(4)
            ])

            # Active m entries (where m_i = 1)
            m_rects = VGroup(*[
                flash_cell(m_entries[i], color=HILITE_ACTIVE, buff=0.08)
                for i in active
            ])

            # Selected G entries in that column (where m_i = 1)
            picks = VGroup(*[
                flash_cell(G_entry(i, j), color=HILITE_ACTIVE, buff=0.06)
                for i in active
            ])

            self.play(FadeIn(col_rects), run_time=0.18)
            self.play(FadeIn(m_rects), run_time=0.18)
            self.play(Transform(col_rects, picks), run_time=0.18)

            # XOR computation text (update one persistent MathTex)
            picked_vals = [int(G[i, j]) for i in active]
            xor_val = 0
            for v in picked_vals:
                xor_val ^= v

            new_xor = MathTex(
                r"\oplus".join(str(v) for v in picked_vals) + rf"={xor_val}",
                font_size=30
            ).move_to(xor_anchor)

            self.play(Transform(xor_tex, new_xor), run_time=0.50)

            # Update output bit in place (transform placeholder -> target)
            self.play(ReplacementTransform(c_bits[j], c_bits_target[j]), run_time=0.20)
            c_bits[j] = c_bits_target[j]  # keep reference consistent
            self.add(c_bits[j])

            # Cleanup highlights (keep XOR panel)
            self.play(FadeOut(m_rects), FadeOut(col_rects), run_time=0.15)

        # Finish: clear XOR scratch, indicate result
        self.play(FadeOut(xor_tex), FadeOut(xor_bg), run_time=0.3)
        self.play(Indicate(c_bits, scale_factor=1.05), run_time=0.6)

        # Final result label (appears once at the end)
        final_tex = MathTex(r"c = ", bits_tex(c), font_size=38).next_to(c_bits, DOWN, buff=0.25)
#        final_tex.align_to(c_bits, LEFT)  # or center it: 
        final_tex.move_to([c_bits.get_center()[0], final_tex.get_center()[1], 0])

        final_bg = RoundedRectangle(
            corner_radius=0.15,
            width=final_tex.width + 0.5,
            height=final_tex.height + 0.3
        ).set_fill(BLACK, opacity=0.25).set_stroke(WHITE, opacity=0.12)

        final_group = VGroup(final_bg, final_tex)
        final_tex.move_to(final_bg.get_center())
        final_group.next_to(c_bits, DOWN, buff=0.22).align_to(c_bits, LEFT)

        self.play(FadeIn(final_group, shift=UP*0.1), run_time=0.6)

        syn0 = f2_matmul(H, c.reshape(-1, 1)).reshape(-1)  # expect [0,0,0]

        check_tex = MathTex(
            r"Hc^\top =",
            bits_tex(syn0),
            r"= 0",
            font_size=38
        )

        check_bg = RoundedRectangle(
            corner_radius=0.15,
            width=check_tex.width + 0.5,
            height=check_tex.height + 0.3
        ).set_fill(BLACK, opacity=0.25).set_stroke(WHITE, opacity=0.12)

        check_group = VGroup(check_bg, check_tex)
        check_tex.move_to(check_bg.get_center())

        # ----------------------------------------------------
        # Verification: build H · c^T = s, then show s = 0
        # ----------------------------------------------------
        # syn0 should be length-3 vector
        syn0 = f2_matmul(H, c.reshape(-1, 1)).reshape(-1)

        H_label = MathTex(r"H", font_size=40)
        H_mat = Matrix(
            H.tolist() if hasattr(H, "tolist") else H,
            element_to_mobject=lambda x, *a, **k: bin_entry(x, 34, *a, **k),
            v_buff=0.35, h_buff=0.45
        ).scale(0.72)
        H_group = VGroup(H_label, H_mat).arrange(RIGHT, buff=0.18)

        dot = MathTex(r"\cdot", font_size=52)
        cT = Matrix(
            [[int(x)] for x in (c.tolist() if hasattr(c, "tolist") else c)],
            element_to_mobject=lambda x, *a, **k: bin_entry(x, 34, *a, **k),
            v_buff=0.35, h_buff=0.55
        ).scale(0.72)

        eq = MathTex(r"=", font_size=52)

        # syndrome column: start as [0,0,0]^T, then transform each entry to computed syn0
        s_col = Matrix(
            [[0],[0],[0]],
            element_to_mobject=lambda x, *a, **k: bin_entry(x, 34, *a, **k),
            v_buff=0.35, h_buff=0.55
        ).scale(0.72)

        check_group = VGroup(H_group, dot, cT, eq, s_col).arrange(RIGHT, buff=0.55, aligned_edge=ORIGIN)

        # place BELOW the whole mG line and CENTER it horizontally
        check_group.next_to(la_group, DOWN, buff=0.55)
        check_group.set_x(la_group.get_center()[0])

        # Fit-to-frame if needed, then re-place
        target_w = config.frame_width - 1.4
        if check_group.width > target_w:
            check_group.scale_to_fit_width(target_w)
            check_group.next_to(la_group, DOWN, buff=0.55)
            check_group.set_x(la_group.get_center()[0])

        self.play(FadeIn(check_group, shift=UP*0.10), run_time=0.6)

        # Optional: visually connect the strip to the column vector
        # (copy c_bits into cT entries, so it feels like transpose/vectorization)
        cT_entries = cT.get_entries()  # 7 entries (top to bottom)
        # c_bits is a VGroup of 7 bit mobjects (left to right)
        self.play(
            LaggedStart(*[
                TransformFromCopy(c_bits[j], cT_entries[j])
                for j in range(7)
            ], lag_ratio=0.06),
            run_time=0.8
        )

        # Now do row-by-row dot products: s_i = <row_i(H), c>
        H_entries = H_mat.get_entries()   # 3*7 entries
        s_entries = s_col.get_entries()   # 3 entries

        def H_entry(i, j):  # i=0..2, j=0..6
            return entry_at(H_entries, 7, i, j)

        active_c = [j for j, cj in enumerate(c) if int(cj) == 1]  # positions where c_j=1

        # A fixed scratch position for XOR text
        xor_anchor = check_group.get_right() + RIGHT*0.65 + UP*0.35
        xor_bg = RoundedRectangle(corner_radius=0.12, width=2.4, height=0.65).move_to(xor_anchor)
        xor_bg.set_fill(BLACK, opacity=0.25).set_stroke(WHITE, opacity=0.12)
        xor_tex = MathTex("", font_size=30).move_to(xor_anchor)
        self.add(xor_bg, xor_tex)

        for i in range(3):
            # highlight the i-th row of H
            row_rects = VGroup(*[
                SurroundingRectangle(H_entry(i, j), buff=0.05, color=YELLOW)
                for j in range(7)
            ])
            # highlight active entries of c (where c_j=1)
            c_rects = VGroup(*[
                SurroundingRectangle(cT_entries[j], buff=0.07, color=BLUE)
                for j in active_c
            ])
            # highlight the selected H entries in that row (where c_j=1)
            picks = VGroup(*[
                SurroundingRectangle(H_entry(i, j), buff=0.05, color=BLUE)
                for j in active_c
            ])

            self.play(FadeIn(row_rects), run_time=0.18)
            self.play(FadeIn(c_rects), run_time=0.18)
            self.play(Transform(row_rects, picks), run_time=0.18)

            # XOR of the picked H values (since c_j=1 selects those columns)
            picked_vals = [int(H[i, j]) for j in active_c]
            xor_val = 0
            for v in picked_vals:
                xor_val ^= v

            new_xor = MathTex(
                r"\oplus".join(str(v) for v in picked_vals) + rf"={xor_val}",
                font_size=30
            ).move_to(xor_anchor)
            self.play(Transform(xor_tex, new_xor), run_time=0.20)

            # Write syndrome entry i (transform current displayed entry -> computed syn0[i])
            target_entry = bin_entry(int(syn0[i]), 34)
            target_entry.move_to(s_entries[i])

            self.play(ReplacementTransform(s_entries[i], target_entry), run_time=0.20)
            s_entries[i] = target_entry
            self.add(s_entries[i])

            self.play(FadeOut(c_rects), FadeOut(row_rects), run_time=0.15)

        self.play(FadeOut(xor_tex), FadeOut(xor_bg), run_time=0.3)

        # Final statement "= 0" (clean)
        zero_tex = MathTex(r"=0", font_size=38).next_to(s_col, RIGHT, buff=0.25).align_to(s_col, ORIGIN)
        self.play(Write(zero_tex), run_time=0.4)

        
        # Place it under the final c=... box (or under c_bits if you prefer)
        check_group.next_to(s_col, DOWN, buff=0.18).align_to(s_col, LEFT)

        self.play(FadeIn(check_group, shift=UP*0.08), run_time=0.6)

            
        
#        # ----------------------------------------------------
#        # Inject a single-bit error: y = c + e_j
#        # ----------------------------------------------------
#        syn_glow = SurroundingRectangle(pipe[2:5], buff=0.12, color=BLUE)
#
#        j = 4  # 0-indexed (bit 5)
#        e = np.zeros(7, dtype=int); e[j] = 1
#        y = (c + e) % 2
#
#        flip_rect = SurroundingRectangle(c_bits[j], buff=0.06, color=RED)
#        flip_txt = Tex(f"flip bit {j+1}", font_size=26, color=RED).next_to(flip_rect, UP, buff=0.1)
#
#        y_tex = MathTex(r"y=c+e_{%d}=" % (j + 1), bits_tex(y), font_size=40).next_to(c_tex, DOWN, buff=0.25).align_to(c_tex, LEFT)
#        y_bits = make_bit_string(y, one_color=GREEN, zero_color=GRAY_B).next_to(y_tex, DOWN, buff=0.25).align_to(y_tex, LEFT)
#        y_labs = label_bits_under(y_bits, y, font_size=20)
#
#        self.play(Create(flip_rect), FadeIn(flip_txt, shift=UP * 0.1))
#        self.wait(0.15)
#        self.play(
#            Transform(c_tex, y_tex),
#            Transform(c_bits, y_bits),
#            Transform(c_labs, y_labs),
#        )
#        self.play(FadeOut(flip_rect), FadeOut(flip_txt))
#        self.play(Create(syn_glow))
#        self.wait(0.2)
#
#        # ----------------------------------------------------
#        # Syndrome: s(y) = Hy^T = He_j^T = (j-th column of H)
#        # ----------------------------------------------------
#        s = f2_matmul(H, y.reshape(-1, 1)).reshape(-1)
#
#        s_tex = MathTex(r"s(y)=Hy^\top=", bits_tex(s), font_size=40).next_to(c_bits, DOWN, buff=0.25).align_to(c_bits, LEFT)
#        self.play(Write(s_tex))
#
#        # Overlay an actual Matrix object on top of the rendered H for column highlighting
#        H_mob = Matrix(H.tolist(), left_bracket="(", right_bracket=")",
#                       element_to_mobject=lambda x: MathTex(str(x), font_size=32))
#        H_mob.scale(0.72).move_to(H_tex[1].get_center())
#        self.add(H_mob)
#
#        col_rect, _ = highlight_column(H_mob, j, color=YELLOW)
#
#        # Find matching row in lookup panel
#        synd_idx = next(i for i, v in enumerate(syndromes) if np.all(v == s))  # 0..6
#        row_target = synd_rows[synd_idx]
#        row_rect = SurroundingRectangle(row_target, buff=0.10, color=YELLOW)
#
#        # Move s(y) next to the matched row (flat "pattern match")
#        target_point = row_target.get_right() + RIGHT * 1.05
#        self.play(s_tex.animate.move_to(target_point).set_opacity(0.95), run_time=0.6)
#
#        # Show "column equals syndrome"
#        col_eq = MathTex(r"He_{%d}^\top=" % (j + 1), bits_tex(H[:, j]), font_size=38)
#        col_eq.next_to(H_mob, RIGHT, buff=0.5).shift(UP * 0.4)
#        arrow_col = Arrow(col_rect.get_right(), col_eq.get_left(), buff=0.15, stroke_width=6)
#
#        arrow_match = Arrow(col_eq.get_right(), row_rect.get_left(), buff=0.2, stroke_width=6)
#
#        self.play(Create(col_rect), Create(row_rect))
#        self.play(Write(col_eq), GrowArrow(arrow_col))
#        self.play(GrowArrow(arrow_match))
#        self.wait(0.25)
#
#        concl = Tex(r"Syndrome matches the $j$-th column $\Rightarrow$ error position identified", font_size=30)
#        concl.to_edge(DOWN)
#        self.play(Write(concl))
#        self.wait(0.4)
#
#        # ----------------------------------------------------
#        # Correct the error: y -> c by flipping bit j back
#        # ----------------------------------------------------
#        corr = (y + e) % 2
#        corr_bits = make_bit_string(corr, one_color=GREEN, zero_color=GRAY_B).move_to(c_bits.get_center())
#        corr_labs = label_bits_under(corr_bits, corr, font_size=20).move_to(c_labs.get_center())
#
#        fix_rect = SurroundingRectangle(c_bits[j], buff=0.06, color=GREEN)
#        fix_txt = Tex("correct", font_size=26, color=GREEN).next_to(fix_rect, UP, buff=0.1)
#
#        self.play(Create(fix_rect), FadeIn(fix_txt, shift=UP * 0.1))
#        self.play(Transform(c_bits, corr_bits), Transform(c_labs, corr_labs), run_time=0.7)
#        self.play(FadeOut(fix_rect), FadeOut(fix_txt))
#        self.wait(0.2)
#
#        # cleanup and final statement
#        self.play(
#            FadeOut(VGroup(col_rect, row_rect, col_eq, arrow_col, arrow_match), shift=DOWN * 0.15),
#            FadeOut(concl, shift=DOWN * 0.15),
#            FadeOut(syn_glow),
#        )
#        final = Tex(r"$C=\ker(H)=\mathrm{im}(G)$ and single-bit errors are corrected via $s(y)$", font_size=34)
#        final.to_edge(DOWN)
#        self.play(Write(final))
#        self.wait(1.0)
#
#
# Optional: quick loop showing "each column is a syndrome"
#class SyndromeOnlyFlat(Scene):
#    def construct(self):
#        H = mod2([
#            [0, 1, 1, 1, 1, 0, 0],
#            [1, 0, 1, 1, 0, 1, 0],
#            [1, 1, 0, 1, 0, 0, 1],
#        ])
#
#        title = Tex("Single-bit error syndromes are columns of $H$", font_size=46).to_edge(UP)
#        self.play(Write(title))
#
#        H_mob = Matrix(H.tolist(), left_bracket="(", right_bracket=")",
#                       element_to_mobject=lambda x: MathTex(str(x), font_size=36))
#        H_mob.scale(0.9).shift(LEFT * 3.0)
#        self.play(Create(H_mob))
#
#        syndromes = [H[:, j] for j in range(7)]
#        panel, synd_rows = syndrome_panel(syndromes, header="Columns of $H$ (each is a nonzero syndrome)")
#        panel.to_edge(RIGHT).shift(DOWN * 0.2)
#        self.play(FadeIn(panel, shift=LEFT * 0.2))
#
#        for j in range(7):
#            rect, _ = highlight_column(H_mob, j, color=YELLOW)
#            row_rect = SurroundingRectangle(synd_rows[j], buff=0.10, color=YELLOW)
#            self.play(Create(rect), Create(row_rect))
#            self.wait(0.25)
#            self.play(FadeOut(rect), FadeOut(row_rect))
#
#        self.wait(0.4)
