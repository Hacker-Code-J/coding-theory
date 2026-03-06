from manim import *
import numpy as np

# Manim Community Edition (CE).
# Run:
#   manim -pqh hamming731.py Hamming731KernelImage
# or higher quality:
#   manim -p -r 1920,1080 hamming731.py Hamming731KernelImage

def vec_str(bits):
    return "".join(str(int(b)) for b in bits)

def col_to_tex(col_bits):
    # col_bits length 3 over F2
    a,b,c = [int(x) for x in col_bits]
    return r"\begin{pmatrix}%d\\%d\\%d\end{pmatrix}" % (a,b,c)

class Hamming731KernelImage(Scene):
    def construct(self):
        self.camera.background_color = "#0b0f19"  # dark, 3b1b-ish

        # --- Title / thesis ---
        title = Tex(r"Hamming $(7,4,3)_2$ via $\ker(H)$ and $s(y)=Hy^\top$",
                    font_size=52, color=WHITE)
        subtitle = Tex(r"Three viewpoints: subset, image, kernel",
                       font_size=34, color=GREY_B)
        VGroup(title, subtitle).arrange(DOWN, buff=0.35).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN))
        self.wait(0.6)

        # --- Viewpoint bullets (mathematician lens) ---
        bullets = VGroup(
            Tex(r"$C\subseteq \mathbb{F}_2^7$ (subset)", font_size=36),
            Tex(r"$C=\mathrm{Im}(Enc)$ with $Enc:\mathbb{F}_2^4\to \mathbb{F}_2^7$", font_size=36),
            Tex(r"$C=\ker(H)$ with $H:\mathbb{F}_2^7\to \mathbb{F}_2^3$", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(0.2*DOWN)

        for b in bullets:
            b.set_color(WHITE)

        self.play(LaggedStart(*[Write(b) for b in bullets], lag_ratio=0.2))
        self.wait(0.7)

        # Highlight "kernel" bullet
        kernel_box = SurroundingRectangle(bullets[2], color=YELLOW, buff=0.15)
        self.play(Create(kernel_box))
        self.wait(0.5)

        # --- Define H explicitly ---
        H_tex = MathTex(
            r"H=\begin{pmatrix}"
            r"1&0&1&0&1&0&1\\"
            r"0&1&1&0&0&1&1\\"
            r"0&0&0&1&1&1&1"
            r"\end{pmatrix}\in \mathbb{F}_2^{3\times 7}",
            font_size=40,
            color=WHITE
        )
        H_tex.next_to(subtitle, DOWN, buff=0.7)

        self.play(FadeOut(bullets[0:2], shift=LEFT), FadeOut(kernel_box, shift=LEFT))
        self.play(bullets[2].animate.to_edge(LEFT).shift(0.8*UP))
        self.play(Write(H_tex))
        self.wait(0.7)

        # --- Visualize columns: all nonzero vectors in F2^3 ---
        col_title = Tex(r"Columns of $H$ are all nonzero vectors in $\mathbb{F}_2^3$",
                        font_size=34, color=GREY_A)
        col_title.next_to(H_tex, DOWN, buff=0.5)
        self.play(FadeIn(col_title, shift=DOWN))
        self.wait(0.4)

        # List the 7 nonzero vectors of F2^3 in the exact column order of H:
        cols = [
            (1,0,0),
            (0,1,0),
            (1,1,0),
            (0,0,1),
            (1,0,1),
            (0,1,1),
            (1,1,1),
        ]

        # draw a "syndrome space" panel
        panel = RoundedRectangle(corner_radius=0.25, height=3.6, width=6.2,
                                 color=BLUE_E, stroke_width=2)
        panel.to_edge(RIGHT).shift(0.2*DOWN)
        panel_label = Tex(r"Syndrome space $\mathbb{F}_2^3$", font_size=34, color=BLUE_A)
        panel_label.next_to(panel, UP, buff=0.2)

        self.play(Create(panel), FadeIn(panel_label))
        self.wait(0.3)

        # Arrange column vectors inside panel in a neat grid
        col_mobs = VGroup()
        for i, c in enumerate(cols):
            mt = MathTex(col_to_tex(c), font_size=34, color=WHITE)
            col_mobs.add(mt)

        col_mobs.arrange_in_grid(rows=2, cols=4, buff=0.45)
        # remove the last empty spot visually by shifting
        col_mobs.move_to(panel.get_center()).shift(0.05*UP + 0.1*LEFT)
        col_mobs[3].shift(0.25*DOWN)  # minor aesthetic tweak

        # index labels 1..7
        idx = VGroup()
        for j in range(7):
            t = Tex(rf"$j={j+1}$", font_size=26, color=GREY_B)
            t.next_to(col_mobs[j], DOWN, buff=0.08)
            idx.add(t)

        self.play(LaggedStart(*[FadeIn(m) for m in col_mobs], lag_ratio=0.08))
        self.play(LaggedStart(*[FadeIn(t) for t in idx], lag_ratio=0.06))
        self.wait(0.6)

        # --- Kernel statement: C = ker(H) ---
        ker_statement = MathTex(
            r"C=\ker(H)=\{x\in\mathbb{F}_2^7:\;Hx^\top=0\}",
            font_size=42, color=YELLOW
        )
        ker_statement.next_to(col_title, DOWN, buff=0.5)
        self.play(Write(ker_statement))
        self.wait(0.6)

        params = Tex(r"Parameters: $(n,k,d)=(7,4,3)$, corrects $t=\lfloor (d-1)/2\rfloor=1$ error",
                     font_size=34, color=GREY_A)
        params.next_to(ker_statement, DOWN, buff=0.25)
        self.play(FadeIn(params, shift=DOWN))
        self.wait(0.8)

        # --- Map diagram: F2^7 --H--> F2^3 ; kernel highlighted ---
        # Create a small commutative-ish diagram
        left_space = MathTex(r"\mathbb{F}_2^7", font_size=44, color=WHITE)
        right_space = MathTex(r"\mathbb{F}_2^3", font_size=44, color=WHITE)
        arrow = Arrow(LEFT, RIGHT, buff=0.25, color=WHITE)
        H_label = MathTex(r"H", font_size=40, color=WHITE).next_to(arrow, UP, buff=0.1)

        diagram = VGroup(left_space, arrow, right_space, H_label).arrange(RIGHT, buff=0.4)
        diagram.to_edge(LEFT).shift(1.3*DOWN)

        self.play(FadeIn(diagram, shift=UP))
        self.wait(0.4)

        ker_glow = SurroundingRectangle(left_space, color=YELLOW, buff=0.18)
        ker_text = Tex(r"$C$ lives inside here as the kernel", font_size=30, color=YELLOW)
        ker_text.next_to(diagram, DOWN, buff=0.25).align_to(diagram, LEFT)

        self.play(Create(ker_glow), FadeIn(ker_text))
        self.wait(0.8)

        # --- Introduce received word: y = c + e ---
        eq1 = MathTex(r"y=c+e", font_size=44, color=WHITE)
        eq2 = MathTex(r"s(y)=Hy^\top", font_size=44, color=WHITE)
        eq3 = MathTex(r"=H(c+e)^\top=Hc^\top+He^\top", font_size=40, color=GREY_A)
        eq4 = MathTex(r"=0+He^\top=He^\top", font_size=44, color=YELLOW)

        eq_group = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        eq_group.next_to(diagram, RIGHT, buff=0.8).shift(0.3*DOWN)

        self.play(Write(eq1))
        self.wait(0.3)
        self.play(Write(eq2))
        self.wait(0.3)
        self.play(Write(eq3))
        self.wait(0.4)
        self.play(Write(eq4))
        self.wait(0.8)

        # --- Single-bit error case: e = e_j (standard basis) ---
        ej = MathTex(r"e=e_j\in\mathbb{F}_2^7\quad(\text{1 at position }j,\text{ else }0)",
                    font_size=36, color=WHITE)
        ej.next_to(eq_group, DOWN, buff=0.35).align_to(eq_group, LEFT)
        self.play(FadeIn(ej, shift=DOWN))
        self.wait(0.5)

        # Show: He_j^T = j-th column of H
        col_fact = MathTex(r"He_j^\top=\text{the $j$-th column of }H", font_size=42, color=YELLOW)
        col_fact.next_to(ej, DOWN, buff=0.2).align_to(ej, LEFT)
        self.play(Write(col_fact))
        self.wait(0.7)

        # --- Animated decoding: pick a j, highlight column, show syndrome equals it ---
        # We'll demonstrate with j=6 (arbitrary, but visually nice)
        j_demo = 6
        target = col_mobs[j_demo-1]
        target_idx = idx[j_demo-1]

        # pulse highlight
        highlight = SurroundingRectangle(target, color=YELLOW, buff=0.12)
        self.play(Create(highlight), target.animate.set_color(YELLOW), target_idx.animate.set_color(YELLOW))
        self.wait(0.4)

        # show syndrome vector equals that highlighted column
        synd = MathTex(r"s(y)=\begin{pmatrix}0\\1\\1\end{pmatrix}", font_size=48, color=YELLOW)
        synd.move_to(panel.get_center()).shift(1.25*DOWN)  # below the grid
        synd_label = Tex(r"Computed syndrome", font_size=28, color=GREY_B)
        synd_label.next_to(synd, LEFT, buff=0.25)

        self.play(FadeIn(synd_label, shift=RIGHT), FadeIn(synd, shift=RIGHT))
        self.wait(0.3)

        match_text = Tex(r"Match $\Rightarrow$ error position $j=6$", font_size=36, color=WHITE)
        match_text.next_to(synd, DOWN, buff=0.25).align_to(synd, LEFT)
        self.play(Write(match_text))
        self.wait(0.8)

        # --- Wrap: tie back to "subset / image / kernel" ---
        wrap = VGroup(
            Tex(r"Subset: $C\subseteq\mathbb{F}_2^7$", font_size=32, color=GREY_A),
            Tex(r"Image: $C=\mathrm{Im}(Enc)$", font_size=32, color=GREY_A),
            Tex(r"Kernel: $C=\ker(H)$, decode via $s(y)=Hy^\top$", font_size=32, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        wrap.to_edge(DOWN).shift(0.1*UP)
        self.play(FadeIn(wrap, shift=UP))
        self.wait(1.2)

        # final fade
        self.play(
            FadeOut(VGroup(
                title, subtitle, H_tex, col_title, ker_statement, params,
                diagram, ker_glow, ker_text, eq_group, ej, col_fact,
                panel, panel_label, col_mobs, idx, highlight, synd, synd_label, match_text, wrap
            )),
            run_time=1.0
        )
