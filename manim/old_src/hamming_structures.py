# manim -pqh hamming_structures.py StructuresOverview HammingSyndromeDemo HammingKernelAndImage
#
# Notes:
# - Designed for Manim Community Edition (>=0.17).
# - This is a didactic visualization: it emphasizes the *morphisms* Enc and H,
#   and the Hamming(7,4,3) syndrome rule "s = H e^T equals the j-th column".
#
# What you get:
#   1) StructuresOverview: "subset" vs "linear subspace" vs "image(Enc)" vs "kernel(H)" vs "AG evaluation"
#   2) HammingSyndromeDemo: show H columns, pick a 1-bit error, compute syndrome = that column, locate j
#   3) HammingKernelAndImage: show C = ker(H), dim(C)=4, and (optionally) a systematic generator G with HG^T=0
#
# You can freely edit text/math to match your lecture note style.

from manim import *
import numpy as np

# ---------- small helpers ----------

def tex_matrix(m, field_tex=r"\mathbb{F}_2"):
    """
    Convert a 2D list/np-array with entries 0/1 into a LaTeX pmatrix.
    """
    rows = []
    for r in m:
        rows.append(" & ".join(str(int(x)) for x in r))
    body = r"\\ ".join(rows)
    return rf"\begin{{pmatrix}} {body} \end{{pmatrix}}"

def column_tex(v):
    return rf"\begin{{pmatrix}} {int(v[0])}\\ {int(v[1])}\\ {int(v[2])}\end{{pmatrix}}"

def binary_vec_tex(v):
    return r"\big(" + ",".join(str(int(x)) for x in v) + r"\big)"

# ---------- Scenes ----------

class StructuresOverview(Scene):
    def construct(self):
        title = Tex(r"Block codes as \emph{sets} and \emph{linear-algebraic objects}").scale(0.9)
        title.to_edge(UP)

        # Core definition
        core = MathTex(r"C \subseteq \Sigma^n").scale(1.2)
        core_box = SurroundingRectangle(core, buff=0.25, corner_radius=0.15)
        core_group = VGroup(core, core_box).next_to(title, DOWN, buff=0.7)

        self.play(Write(title))
        self.play(FadeIn(core_group, shift=DOWN))
        self.wait(0.4)

        # Bullets: linear subspace, image Enc, kernel H, AG evaluation
        bullets = VGroup(
            Tex(r"$\Sigma=\mathbb{F}_q$ and $C$ a \emph{linear subspace} of $\mathbb{F}_q^n$"),
            Tex(r"$C$ as an \emph{image} of an encoding morphism $Enc:\Sigma^k\to\Sigma^n$"),
            Tex(r"$C$ as a \emph{kernel} of parity checks $H:\mathbb{F}_q^n\to\mathbb{F}_q^{n-k}$"),
            Tex(r"(AG) $C$ as an \emph{evaluation image} of functions/sections on a curve/variety"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.8)
        bullets.next_to(core_group, DOWN, buff=0.6).to_edge(LEFT, buff=0.9)

        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT) for b in bullets], lag_ratio=0.15))
        self.wait(0.6)

        # Diagram: Enc and H
        left = MathTex(r"\Sigma^k").scale(1.1)
        mid = MathTex(r"\Sigma^n").scale(1.1)
        right = MathTex(r"\mathbb{F}_q^{n-k}").scale(1.1)

        mid.shift(2.3*RIGHT + 0.6*DOWN)
        left.next_to(mid, LEFT, buff=2.2)
        right.next_to(mid, RIGHT, buff=2.2)

        enc_arrow = Arrow(left.get_right(), mid.get_left(), buff=0.15)
        enc_label = MathTex(r"Enc").scale(0.9).next_to(enc_arrow, UP, buff=0.1)

        h_arrow = Arrow(mid.get_right(), right.get_left(), buff=0.15)
        h_label = MathTex(r"H").scale(0.9).next_to(h_arrow, UP, buff=0.1)

        img_label = Tex(r"$\mathrm{im}(Enc)=C$").scale(0.75).next_to(mid, DOWN, buff=0.25)
        ker_label = Tex(r"$\ker(H)=C$").scale(0.75).next_to(mid, UP, buff=0.25)

        diag = VGroup(left, mid, right, enc_arrow, h_arrow, enc_label, h_label, img_label, ker_label)
        diag.to_edge(RIGHT, buff=0.8)

        self.play(FadeIn(diag, shift=LEFT))
        self.wait(0.8)

        # Highlight equivalences
        highlight1 = SurroundingRectangle(bullets[1], color=YELLOW, buff=0.15, corner_radius=0.1)
        highlight2 = SurroundingRectangle(bullets[2], color=YELLOW, buff=0.15, corner_radius=0.1)

        self.play(Create(highlight1))
        self.play(Transform(highlight1, highlight2))
        self.wait(0.8)
        self.play(FadeOut(highlight1))

        # Finish
        tagline = Tex(r"Key mantra: \quad $C$ is a subset, but also \emph{image} and \emph{kernel}.").scale(0.85)
        tagline.to_edge(DOWN)
        self.play(Write(tagline))
        self.wait(1.0)


class HammingSyndromeDemo(Scene):
    """
    Visualizes the classic Hamming(7,4,3) parity-check matrix H whose columns are all nonzero vectors in F2^3,
    and demonstrates that for a single-bit error e_j, the syndrome s = H e^T equals the j-th column of H.
    """
    def construct(self):
        title = Tex(r"Hamming $(7,4,3)$: syndrome identifies a 1-bit error").scale(0.9).to_edge(UP)
        self.play(Write(title))

        H = np.array([
            [1,0,1,0,1,0,1],
            [0,1,1,0,0,1,1],
            [0,0,0,1,1,1,1],
        ], dtype=int)

        H_tex = MathTex(r"H=", tex_matrix(H)).scale(0.85)
        H_tex.to_edge(LEFT, buff=0.8).shift(0.2*DOWN)
        self.play(FadeIn(H_tex, shift=RIGHT))
        self.wait(0.4)

        # Column labels 1..7 under the matrix
        col_labels = VGroup(*[
            Tex(str(j+1)).scale(0.5)
            for j in range(7)
        ])
        # Position labels under approximate column centers (works well with this scale)
        # We'll estimate column x positions by sampling points along the matrix width.
        mat_bbox = H_tex[1].get_bounding_box()  # bounding box points
        # fallback: use H_tex.get_left/right
        left_x = H_tex[1].get_left()[0]
        right_x = H_tex[1].get_right()[0]
        xs = np.linspace(left_x + 0.25, right_x - 0.25, 7)
        for j, lab in enumerate(col_labels):
            lab.move_to(np.array([xs[j], H_tex[1].get_bottom()[1]-0.35, 0]))

        self.play(LaggedStart(*[FadeIn(l) for l in col_labels], lag_ratio=0.08))
        self.wait(0.3)

        # Explain "columns are all nonzero vectors in F2^3"
        explain = Tex(r"Columns of $H$ are all nonzero vectors in $\mathbb{F}_2^3$.").scale(0.8)
        explain.next_to(H_tex, DOWN, buff=0.35).align_to(H_tex, LEFT)
        self.play(Write(explain))
        self.wait(0.5)

        # Pick a received word y = c + e, with a 1-bit error at position j
        # We'll demonstrate just the error part; we don't need an explicit codeword.
        j = 5  # choose position 6 (1-indexed), i.e. j=6; 0-index is 5
        j1 = j + 1

        e = np.zeros(7, dtype=int)
        e[j] = 1

        # Syndrome s = H e^T equals column j
        s = (H @ e) % 2
        colj = H[:, j]

        # Right-side computation panel
        panel = VGroup().to_edge(RIGHT, buff=0.8).shift(0.1*DOWN)

        eq1 = MathTex(
            r"e = (0,\dots,0,1,0,\dots,0)",
            rf"\quad\text{{(1 at position {j1})}}"
        ).scale(0.72)

        eq2 = MathTex(r"s(y)=H e^\top").scale(0.85)
        eq3 = MathTex(r"= \text{(the }", rf"{j1}", r"\text{-th column of }H)").scale(0.85)
        eq3[1].set_color(YELLOW)

        panel_content = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        panel_content.move_to(panel.get_center())
        panel = panel_content

        self.play(FadeIn(panel, shift=LEFT))
        self.wait(0.5)

        # Highlight the chosen column in H
        # We'll draw a rectangle around the column area using the x coordinate from xs[j]
        col_rect = Rectangle(
            width=(xs[1] - xs[0]) * 0.95,
            height=(H_tex[1].get_top()[1] - H_tex[1].get_bottom()[1]) * 0.95,
            stroke_width=4,
            stroke_color=YELLOW,
        )
        col_rect.move_to(np.array([xs[j], H_tex[1].get_center()[1], 0]))

        self.play(Create(col_rect))
        self.wait(0.4)

        # Show the actual computed syndrome vector and the column vector side-by-side
        synd_tex = MathTex(r"s = ", column_tex(s)).scale(1.0)
        col_tex = MathTex(r"H_{(:,", str(j1), r")}", r" = ", column_tex(colj)).scale(1.0)
        col_tex[1].set_color(YELLOW)

        vectors = VGroup(synd_tex, col_tex).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        vectors.next_to(panel, DOWN, buff=0.6).align_to(panel, LEFT)

        self.play(Write(vectors))
        self.wait(0.6)

        check = Tex(r"Thus $s$ uniquely identifies the error position $j$.").scale(0.8)
        check.to_edge(DOWN)
        self.play(Write(check))
        self.wait(1.0)

        # Optional: show the mapping "syndrome -> position" as a lookup
        lookup_title = Tex(r"Syndrome lookup (nonzero in $\mathbb{F}_2^3$)").scale(0.65)
        lookup_title.next_to(explain, DOWN, buff=0.35).align_to(H_tex, LEFT)

        # Create a small table-like list: column index -> column vector
        pairs = VGroup()
        for t in range(7):
            vv = H[:, t]
            item = MathTex(str(t+1), r"\mapsto", column_tex(vv)).scale(0.6)
            if t == j:
                item.set_color(YELLOW)
            pairs.add(item)
        pairs.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        pairs.next_to(lookup_title, DOWN, buff=0.2).align_to(lookup_title, LEFT)

        self.play(FadeIn(lookup_title))
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT*0.2) for p in pairs], lag_ratio=0.05))
        self.wait(1.2)

        self.play(FadeOut(col_rect), FadeOut(pairs), FadeOut(lookup_title))
        self.wait(0.3)


class HammingKernelAndImage(Scene):
    """
    Shows C = ker(H) as a linear subspace of F2^7, explains dimensions, and (optionally)
    shows a systematic generator matrix G with HG^T=0, so C = im(Enc) too.
    """
    def construct(self):
        title = Tex(r"Hamming $(7,4,3)$ as $\ker(H)$ and as $\mathrm{im}(Enc)$").scale(0.9).to_edge(UP)
        self.play(Write(title))

        H = np.array([
            [1,0,1,0,1,0,1],
            [0,1,1,0,0,1,1],
            [0,0,0,1,1,1,1],
        ], dtype=int)

        H_tex = MathTex(r"H=", tex_matrix(H)).scale(0.85).to_edge(LEFT, buff=0.8).shift(0.1*DOWN)
        self.play(FadeIn(H_tex, shift=RIGHT))
        self.wait(0.3)

        # Kernel definition
        ker_def = MathTex(r"C=\ker(H)=\{x\in\mathbb{F}_2^7:\;Hx^\top=0\}").scale(0.85)
        ker_def.next_to(H_tex, RIGHT, buff=0.8).shift(0.3*UP)
        self.play(Write(ker_def))
        self.wait(0.5)

        # Dimensions: rank(H)=3 so dim ker = 7-3 = 4
        dim_line = MathTex(r"\mathrm{rank}(H)=3 \;\Rightarrow\; \dim C = 7-3=4").scale(0.85)
        dim_line.next_to(ker_def, DOWN, buff=0.35).align_to(ker_def, LEFT)
        self.play(Write(dim_line))
        self.wait(0.6)

        # Show a systematic generator matrix G for this H (standard construction).
        # One valid choice consistent with H = [P^T | I_3] ordering (as given) is:
        #   G = [I_4 | P] where P columns correspond to columns 5..7? etc.
        # For the specific H given, a consistent systematic G is:
        G = np.array([
            [1,0,0,0,1,1,0],
            [0,1,0,0,1,0,1],
            [0,0,1,0,0,1,1],
            [0,0,0,1,1,1,1],
        ], dtype=int)

        # Verify HG^T = 0 in the *animation* (purely internal check)
        prod = (H @ G.T) % 2
        ok = np.all(prod == 0)

        g_title = Tex(r"A generator matrix $G$ gives $C=\mathrm{im}(Enc)$ with $Enc(m)=mG$.").scale(0.72)
        g_title.to_edge(DOWN).shift(0.15*UP)

        G_tex = MathTex(r"G=", tex_matrix(G)).scale(0.78)
        G_tex.next_to(dim_line, DOWN, buff=0.55).align_to(ker_def, LEFT)

        hg = MathTex(r"H G^\top = 0").scale(0.85)
        hg.next_to(G_tex, RIGHT, buff=0.6).shift(0.1*UP)

        # If the internal check fails (shouldn't), display a warning in the scene.
        if not ok:
            warn = Tex(r"Warning: chosen $G$ does not satisfy $HG^\top=0$.").set_color(RED).scale(0.7)
            warn.next_to(hg, DOWN, buff=0.2)
            self.play(FadeIn(warn))
            self.wait(0.5)

        self.play(FadeIn(g_title, shift=UP*0.2))
        self.play(FadeIn(G_tex, shift=UP*0.2))
        self.play(Write(hg))
        self.wait(0.6)

        # Show Enc arrow and image
        enc_diag_left = MathTex(r"\mathbb{F}_2^4").scale(1.0)
        enc_diag_right = MathTex(r"\mathbb{F}_2^7").scale(1.0)
        enc_diag_left.next_to(G_tex, DOWN, buff=0.55).align_to(G_tex, LEFT)
        enc_diag_right.next_to(enc_diag_left, RIGHT, buff=2.2)
        enc_arrow = Arrow(enc_diag_left.get_right(), enc_diag_right.get_left(), buff=0.15)
        enc_label = MathTex(r"Enc(m)=mG").scale(0.75).next_to(enc_arrow, UP, buff=0.1)

        im_label = Tex(r"$\mathrm{im}(Enc)=C$").scale(0.7).next_to(enc_diag_right, DOWN, buff=0.15)
        ker_label = Tex(r"$C=\ker(H)$").scale(0.7).next_to(enc_diag_right, UP, buff=0.15)

        self.play(FadeIn(enc_diag_left, enc_diag_right, enc_arrow, enc_label))
        self.play(FadeIn(im_label), FadeIn(ker_label))
        self.wait(1.0)

        # Final emphasis: image = kernel
        eq = MathTex(r"\mathrm{im}(Enc)=C=\ker(H)").scale(1.05)
        eq_box = SurroundingRectangle(eq, buff=0.25, corner_radius=0.15)
        eq_group = VGroup(eq, eq_box).move_to(2.6*DOWN + 0.3*RIGHT)

        self.play(FadeIn(eq_group))
        self.wait(1.2)
