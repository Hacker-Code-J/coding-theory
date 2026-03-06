from manim import *
import numpy as np

# Run examples:
#   manim -pqh hamming731_film.py KernelSyndrome
#   manim -pqh hamming731_film.py ImageEncoding
#
# Notes:
# - All arithmetic is conceptual over F2 (we don't numerically compute in manim).
# - Visual pacing is "3b1b-ish": headline -> structure -> zoom-in computation.

def col_to_tex(col_bits):
    a, b, c = [int(x) for x in col_bits]
    return r"\begin{pmatrix}%d\\%d\\%d\end{pmatrix}" % (a, b, c)

class KernelSyndrome(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"

        # --- Opening ---
        title = Tex(r"Hamming $(7,4,3)_2$ as a \textbf{kernel} + syndrome decoding",
                    font_size=52, color=WHITE)
        subtitle = Tex(r"Parity checks are linear equations: $H:\mathbb{F}_2^7\to\mathbb{F}_2^3$",
                       font_size=34, color=GREY_B)
        VGroup(title, subtitle).arrange(DOWN, buff=0.35).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN))
        self.wait(0.6)

        # --- Mathematician viewpoint bullets ---
        bullets = VGroup(
            Tex(r"$C\subseteq \mathbb{F}_2^7$ (subset)", font_size=36, color=WHITE),
            Tex(r"$C=\mathrm{Im}(Enc)$ (image of an encoding morphism)", font_size=36, color=WHITE),
            Tex(r"$C=\ker(H)$ (solutions to parity-check equations)", font_size=36, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(0.15*DOWN)

        self.play(LaggedStart(*[Write(b) for b in bullets], lag_ratio=0.18))
        self.wait(0.5)

        kernel_box = SurroundingRectangle(bullets[2], color=YELLOW, buff=0.15)
        self.play(Create(kernel_box))
        self.wait(0.4)

        # --- Show H ---
        H_tex = MathTex(
            r"H=\begin{pmatrix}"
            r"1&0&1&0&1&0&1\\"
            r"0&1&1&0&0&1&1\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}\in \mathbb{F}_2^{3\times 7}",
            font_size=40, color=WHITE
        ).next_to(subtitle, DOWN, buff=0.75)

        self.play(FadeOut(bullets[0:2], shift=LEFT), FadeOut(kernel_box, shift=LEFT))
        self.play(bullets[2].animate.to_edge(LEFT).shift(0.85*UP))
        self.play(Write(H_tex))
        self.wait(0.6)

        # --- Columns are all nonzero vectors of F2^3 ---
        col_title = Tex(r"Columns of $H$ are \emph{all nonzero} vectors in $\mathbb{F}_2^3$",
                        font_size=34, color=GREY_A).next_to(H_tex, DOWN, buff=0.55)
        self.play(FadeIn(col_title, shift=DOWN))
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

        panel = RoundedRectangle(corner_radius=0.25, height=3.75, width=6.35,
                                 color=BLUE_E, stroke_width=2).to_edge(RIGHT).shift(0.15*DOWN)
        panel_label = Tex(r"Syndrome space $\mathbb{F}_2^3$", font_size=34, color=BLUE_A)\
            .next_to(panel, UP, buff=0.2)

        self.play(Create(panel), FadeIn(panel_label))
        self.wait(0.2)

        col_mobs = VGroup(*[
            MathTex(col_to_tex(c), font_size=34, color=WHITE)
            for c in cols
        ])
        col_mobs.arrange_in_grid(rows=2, cols=4, buff=0.45)
        col_mobs.move_to(panel.get_center()).shift(0.05*UP + 0.12*LEFT)
        col_mobs[3].shift(0.25*DOWN)  # tiny aesthetic tweak

        idx = VGroup(*[
            Tex(rf"$j={j+1}$", font_size=26, color=GREY_B).next_to(col_mobs[j], DOWN, buff=0.08)
            for j in range(7)
        ])

        self.play(LaggedStart(*[FadeIn(m) for m in col_mobs], lag_ratio=0.07))
        self.play(LaggedStart(*[FadeIn(t) for t in idx], lag_ratio=0.05))
        self.wait(0.5)

        # --- Kernel definition ---
        ker_statement = MathTex(
            r"C=\ker(H)=\{x\in\mathbb{F}_2^7:\;Hx^\top=0\}",
            font_size=42, color=YELLOW
        ).next_to(col_title, DOWN, buff=0.55)
        self.play(Write(ker_statement))
        self.wait(0.5)

        params = Tex(r"Parameters: $(7,4,3)_2$  $\Rightarrow$  corrects $t=\lfloor(d-1)/2\rfloor=1$ error",
                     font_size=34, color=GREY_A)\
            .next_to(ker_statement, DOWN, buff=0.22)
        self.play(FadeIn(params, shift=DOWN))
        self.wait(0.55)

        # --- Diagram: F2^7 --H--> F2^3 ---
        left_space = MathTex(r"\mathbb{F}_2^7", font_size=44, color=WHITE)
        right_space = MathTex(r"\mathbb{F}_2^3", font_size=44, color=WHITE)
        arrow = Arrow(LEFT, RIGHT, buff=0.25, color=WHITE)
        H_label = MathTex(r"H", font_size=40, color=WHITE).next_to(arrow, UP, buff=0.1)

        diagram = VGroup(left_space, arrow, right_space, H_label).arrange(RIGHT, buff=0.4)
        diagram.to_edge(LEFT).shift(1.35*DOWN)
        self.play(FadeIn(diagram, shift=UP))
        self.wait(0.25)

        ker_glow = SurroundingRectangle(left_space, color=YELLOW, buff=0.18)
        ker_text = Tex(r"Kernel = all vectors sent to $0$",
                       font_size=30, color=YELLOW)\
            .next_to(diagram, DOWN, buff=0.22).align_to(diagram, LEFT)
        self.play(Create(ker_glow), FadeIn(ker_text))
        self.wait(0.55)

        # --- Received word and syndrome ---
        eq1 = MathTex(r"y=c+e", font_size=44, color=WHITE)
        eq2 = MathTex(r"s(y)=Hy^\top", font_size=44, color=WHITE)
        eq3 = MathTex(r"=H(c+e)^\top=Hc^\top+He^\top", font_size=40, color=GREY_A)
        eq4 = MathTex(r"=0+He^\top=He^\top", font_size=44, color=YELLOW)

        eq_group = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        eq_group.next_to(diagram, RIGHT, buff=0.75).shift(0.25*DOWN)

        self.play(Write(eq1)); self.wait(0.25)
        self.play(Write(eq2)); self.wait(0.25)
        self.play(Write(eq3)); self.wait(0.35)
        self.play(Write(eq4)); self.wait(0.6)

        # --- Single-bit error e = e_j ---
        ej = MathTex(r"e=e_j\in\mathbb{F}_2^7\quad(\text{1 at position }j,\ 0\text{ elsewhere})",
                    font_size=36, color=WHITE)\
            .next_to(eq_group, DOWN, buff=0.35).align_to(eq_group, LEFT)
        self.play(FadeIn(ej, shift=DOWN))
        self.wait(0.35)

        col_fact = MathTex(r"He_j^\top=\text{the $j$-th column of }H",
                           font_size=42, color=YELLOW)\
            .next_to(ej, DOWN, buff=0.18).align_to(ej, LEFT)
        self.play(Write(col_fact))
        self.wait(0.5)

        # --- Demo decode: choose a position ---
        j_demo = 6
        target = col_mobs[j_demo-1]
        target_idx = idx[j_demo-1]

        highlight = SurroundingRectangle(target, color=YELLOW, buff=0.12)
        self.play(Create(highlight),
                  target.animate.set_color(YELLOW),
                  target_idx.animate.set_color(YELLOW))
        self.wait(0.25)

        synd = MathTex(r"s(y)=\begin{pmatrix}0\\1\\1\end{pmatrix}",
                       font_size=48, color=YELLOW)
        synd.move_to(panel.get_center()).shift(1.27*DOWN)

        synd_label = Tex(r"computed syndrome", font_size=28, color=GREY_B)\
            .next_to(synd, LEFT, buff=0.25)

        self.play(FadeIn(synd_label, shift=RIGHT), FadeIn(synd, shift=RIGHT))
        self.wait(0.2)

        match_text = Tex(r"Match $\Rightarrow$ error position $j=6$",
                         font_size=36, color=WHITE)\
            .next_to(synd, DOWN, buff=0.25).align_to(synd, LEFT)
        self.play(Write(match_text))
        self.wait(0.8)

        # --- Close with the three viewpoints ---
        wrap = VGroup(
            Tex(r"Subset: $C\subseteq\mathbb{F}_2^7$", font_size=32, color=GREY_A),
            Tex(r"Kernel: $C=\ker(H)$", font_size=32, color=GREY_A),
            Tex(r"Decoding: $s(y)=Hy^\top$ identifies a 1-bit error", font_size=32, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN).shift(0.12*UP)

        self.play(FadeIn(wrap, shift=UP))
        self.wait(1.0)


class ImageEncoding(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"

        # --- Opening: Image viewpoint ---
        title = Tex(r"Same code as an \textbf{image}: $C=\mathrm{Im}(Enc)$",
                    font_size=54, color=WHITE).to_edge(UP)
        subtitle = Tex(r"Pick a linear encoding morphism $Enc:\mathbb{F}_2^4\to\mathbb{F}_2^7$",
                       font_size=34, color=GREY_B).next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN))
        self.wait(0.6)

        # --- Show H in systematic form ---
        H_tex = MathTex(
            r"H=\left[\;P^\top\mid I_3\;\right]",
            font_size=44, color=WHITE
        ).next_to(subtitle, DOWN, buff=0.75).to_edge(LEFT)

        H_full = MathTex(
            r"H=\begin{pmatrix}"
            r"1&0&1&0&1&0&1\\"
            r"0&1&1&0&0&1&1\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}",
            font_size=40, color=WHITE
        ).next_to(H_tex, DOWN, buff=0.35).align_to(H_tex, LEFT)

        self.play(Write(H_tex))
        self.play(Write(H_full))
        self.wait(0.4)

        # Visual partition marker between first 4 and last 3 columns
        # We'll draw a vertical line over the matrix to indicate [P^T | I]
        partition = Line(UP, DOWN, color=GREY_B, stroke_width=3)
        partition.set_height(H_full.height * 1.05)
        partition.move_to(H_full.get_center())
        # approximate x shift: push to after 4 columns
        partition.shift(1.35 * RIGHT)
        self.play(Create(partition))
        self.wait(0.35)

        note = Tex(r"With $H=[P^\top\mid I_3]$, a natural choice is $G=[I_4\mid P]$.",
                   font_size=34, color=GREY_A)\
            .next_to(H_full, DOWN, buff=0.45).align_to(H_full, LEFT)
        self.play(FadeIn(note, shift=DOWN))
        self.wait(0.5)

        # --- Define P and G explicitly (matching your H) ---
        P_tex = MathTex(
            r"P=\begin{pmatrix}"
            r"0&1&1\\"
            r"1&0&1\\"
            r"1&1&0\\"
            r"1&1&1"
            r"\end{pmatrix}",
            font_size=40, color=WHITE
        )
        G_tex = MathTex(
            r"G=\left[\;I_4\mid P\;\right]=\begin{pmatrix}"
            r"1&0&0&0&0&1&1\\"
            r"0&1&0&0&1&0&1\\"
            r"0&0&1&0&1&1&0\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}",
            font_size=40, color=YELLOW
        )

        mats = VGroup(P_tex, G_tex).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        mats.to_edge(RIGHT).shift(0.25*DOWN)

        self.play(FadeIn(P_tex, shift=LEFT))
        self.wait(0.25)
        self.play(FadeIn(G_tex, shift=LEFT))
        self.wait(0.6)

        # --- Encoding morphism Enc(m)=mG ---
        enc1 = MathTex(r"Enc:\mathbb{F}_2^4\to\mathbb{F}_2^7", font_size=44, color=WHITE)
        enc2 = MathTex(r"m\longmapsto c=mG", font_size=44, color=WHITE)
        enc_group = VGroup(enc1, enc2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        enc_group.next_to(note, DOWN, buff=0.65).align_to(note, LEFT)

        self.play(Write(enc1))
        self.play(Write(enc2))
        self.wait(0.5)

        # --- Show a concrete message -> codeword animation ---
        msg = MathTex(r"m=(1,0,1,1)", font_size=46, color=WHITE)
        code = MathTex(r"c=mG\in\mathbb{F}_2^7", font_size=46, color=YELLOW)
        msg_code = VGroup(msg, code).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        msg_code.next_to(enc_group, DOWN, buff=0.55).align_to(enc_group, LEFT)

        self.play(FadeIn(msg_code, shift=DOWN))
        self.wait(0.35)

        # Not computing c explicitly (keeps things clean, 3b1b style),
        # but we show the idea: linear combination of rows of G.
        lincomb = Tex(r"Interpretation: $c$ is a $\mathbb{F}_2$-linear combination of the rows of $G$",
                      font_size=34, color=GREY_A)\
            .next_to(msg_code, DOWN, buff=0.25).align_to(msg_code, LEFT)
        self.play(FadeIn(lincomb, shift=DOWN))
        self.wait(0.5)

        # --- Compatibility: HG^T = 0 hence Im(Enc) subset ker(H) ---
        compat1 = MathTex(r"HG^\top=0", font_size=54, color=YELLOW)
        compat2 = MathTex(r"\Rightarrow\ H(Enc(m))^\top = H(mG)^\top = 0",
                          font_size=40, color=WHITE)
        compat3 = MathTex(r"\Rightarrow\ \mathrm{Im}(Enc)\subseteq \ker(H)",
                          font_size=46, color=YELLOW)

        compat = VGroup(compat1, compat2, compat3).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        compat.to_edge(DOWN).shift(0.2*UP)

        self.play(Write(compat1))
        self.wait(0.25)
        self.play(Write(compat2))
        self.wait(0.35)
        self.play(Write(compat3))
        self.wait(0.8)

        # --- Close: all three viewpoints unified ---
        wrap = VGroup(
            Tex(r"Subset: $C\subseteq\mathbb{F}_2^7$", font_size=32, color=GREY_A),
            Tex(r"Image: $C=\mathrm{Im}(Enc)$ with $Enc(m)=mG$", font_size=32, color=GREY_A),
            Tex(r"Kernel: $C=\ker(H)$ and $HG^\top=0$ links the two", font_size=32, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        wrap.next_to(compat, UP, buff=0.35).align_to(compat, LEFT)
        self.play(FadeIn(wrap, shift=UP))
        self.wait(1.0)
