"""
Manim CE (robust) full script: 3blue1brown-style “Goppa code as a machine”.

Key fix vs prior draft:
- Avoid nested VGroups that can break .to_corner() boundary computations on some Manim CE versions.
  We "flatten" submobjects: add circle, dots, labels directly to the parent VGroup.

USAGE:
  manim -pqh goppa_vis.py GoppaStoryboard
  manim -pql goppa_vis.py GoppaStoryboard
"""

from manim import *
import numpy as np


# ----------------------------
# Styling helpers (3B1B-ish)
# ----------------------------

def glow(obj, scale=1.15, opacity=0.25):
    halo = obj.copy().set_style(fill_opacity=opacity, stroke_opacity=0)
    halo.scale(scale)
    return halo


# ----------------------------
# Reusable visual components
# ----------------------------

class BitCell(VGroup):
    def __init__(self, value=0, size=0.5):
        super().__init__()
        self.value = int(value)

        self.box = RoundedRectangle(
            corner_radius=0.08,
            width=size,
            height=size,
            stroke_width=2,
        )
        self.txt = MathTex(str(self.value)).scale(0.7)
        self.txt.move_to(self.box.get_center())
        self.add(self.box, self.txt)

    def set_value_anim(self, new_value: int):
        """Return an animation to change the displayed bit."""
        self.value = int(new_value)
        new_txt = MathTex(str(self.value)).scale(0.7).move_to(self.box.get_center())
        return Transform(self.txt, new_txt)

    def emphasize(self):
        return Indicate(self.box, scale_factor=1.1)


class BitStrip(VGroup):
    """
    A row of bit cells. Implemented with FLATTENED submobjects (no nested VGroup containers)
    to avoid boundary-point issues in some Manim versions.
    """
    def __init__(self, n=7, values=None, cell_size=0.5, buff=0.12):
        super().__init__()
        self.n = n
        if values is None:
            values = [0] * n

        self._cells = [BitCell(values[i], size=cell_size) for i in range(n)]
        for c in self._cells:
            self.add(c)
        self.arrange(RIGHT, buff=buff)

    def cell(self, i: int) -> BitCell:
        return self._cells[i]

    def values(self):
        return [c.value for c in self._cells]


class SupportCircle(VGroup):
    """
    Support points alpha_i ∈ F_{2^m}, drawn as dots on a circle.
    Robust: FLATTENED submobjects (no nested VGroups).
    """
    def __init__(self, n=7, radius=1.4):
        super().__init__()
        self.n = n

        self.circle = Circle(radius=radius, stroke_width=2)

        self._points = []
        self._labels = []

        angles = np.linspace(PI / 8, 2 * PI + PI / 8, n, endpoint=False)
        for i, th in enumerate(angles):
            p = Dot(self.circle.point_at_angle(th), radius=0.055)
            lab = MathTex(rf"\alpha_{{{i+1}}}").scale(0.45)
            lab.next_to(p, OUT, buff=0.12)
            self._points.append(p)
            self._labels.append(lab)

        # FLATTEN: add all primitives directly
        self.add(self.circle, *self._points, *self._labels)

    def point(self, i: int) -> Mobject:
        return self._points[i]

    def flash_point(self, i: int):
        return Flash(self._points[i], flash_radius=0.25, line_length=0.18)


class ModGMachine(VGroup):
    """A “reduce mod g(x)” box: input -> remainder/syndrome."""
    def __init__(self, width=2.8, height=1.2):
        super().__init__()
        self.box = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            stroke_width=2,
        )
        self.title = MathTex(r"\bmod\ g(x)").scale(0.7)
        self.title.move_to(self.box.get_center())

        self.in_port = Dot(self.box.get_left(), radius=0.04)
        self.out_port = Dot(self.box.get_right(), radius=0.04)

        self.add(self.box, self.title, self.in_port, self.out_port)


class SyndromeLamps(VGroup):
    """
    Lamps represent syndrome coordinates in F_2^{mt}.
    Robust: FLATTENED submobjects.
    """
    def __init__(self, count=6, lamp_r=0.08, buff=0.18):
        super().__init__()
        self.count = count
        self._lamps = [
            Circle(radius=lamp_r, stroke_width=2).set_fill(opacity=0)
            for _ in range(count)
        ]
        for L in self._lamps:
            self.add(L)
        self.arrange(RIGHT, buff=buff)

    def set_on_anims(self, indices):
        """Return a list of animations turning selected lamps on."""
        indices = set(indices)
        anims = []
        for j, lamp in enumerate(self._lamps):
            if j in indices:
                anims.append(lamp.animate.set_fill(opacity=1).set_stroke(width=2))
            else:
                anims.append(lamp.animate.set_fill(opacity=0).set_stroke(width=2))
        return anims


# ----------------------------
# Main storyboard scene
# ----------------------------

class GoppaStoryboard(Scene):
    def construct(self):
        # If your terminal/video looks too dark, comment this out.
        self.camera.background_color = "#0f111a"

        # ===== Title
        title = Tex("Binary Goppa Code", font_size=54)
        subtitle = Tex(
            r"as a machine: residues $\to$ rational function $\to$ mod $g(x)$",
            font_size=30,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(Write(title), FadeIn(subtitle, shift=DOWN))
        self.wait(0.6)

        self.play(title.animate.to_edge(UP), subtitle.animate.to_edge(UP).shift(DOWN * 0.6))

        # ===== Layout anchors
        support = SupportCircle(n=7, radius=1.35).to_corner(UL).shift(DOWN * 0.4)
        support_lbl = Tex(
            r"Support $L=\{\alpha_1,\dots,\alpha_n\}\subset \mathbb{F}_{2^m}$",
            font_size=28,
        )
        support_lbl.next_to(support, DOWN, buff=0.2).align_to(support, LEFT)

        bits = BitStrip(n=7, values=[0, 1, 0, 1, 0, 0, 1], cell_size=0.5).to_corner(DL).shift(UP * 0.55)
        bits_lbl = Tex(r"Word $c\in\mathbb{F}_2^n$", font_size=28)
        bits_lbl.next_to(bits, UP, buff=0.18).align_to(bits, LEFT)

        machine = ModGMachine().move_to(ORIGIN).shift(RIGHT * 0.6)

        lamps = SyndromeLamps(count=6).to_edge(RIGHT).shift(UP * 0.25)
        lamps_lbl = Tex(r"Syndrome lamps $s(c)\in\mathbb{F}_2^{mt}$", font_size=28)
        lamps_lbl.next_to(lamps, DOWN, buff=0.18)

        self.play(
            FadeIn(support, shift=UP * 0.2),
            FadeIn(support_lbl, shift=UP * 0.2),
            FadeIn(bits, shift=DOWN * 0.2),
            FadeIn(bits_lbl, shift=DOWN * 0.2),
            FadeIn(machine, scale=0.95),
            FadeIn(lamps, shift=RIGHT * 0.2),
            FadeIn(lamps_lbl, shift=RIGHT * 0.2),
        )
        self.wait(0.4)

        # ===== Arrows from bit i to alpha_i
        arrows = VGroup()
        for i in range(7):
            arr = always_redraw(
                lambda i=i: Arrow(
                    start=bits.cell(i).get_top(),
                    end=support.point(i).get_bottom(),
                    buff=0.12,
                    max_tip_length_to_length_ratio=0.12,
                    stroke_width=2,
                )
            )
            arrows.add(arr)

        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.06, run_time=1.2))
        self.wait(0.2)

        # Highlight active bits/poles
        active = [i for i, v in enumerate(bits.values()) if v == 1]
        self.play(*[bits.cell(i).emphasize() for i in active], run_time=0.8)
        self.play(*[support.flash_point(i) for i in active], run_time=0.8)

        # ===== Assemble rational function R_c(x)
        terms = VGroup()
        for i in active:
            t = MathTex(rf"\frac{{1}}{{x-\alpha_{{{i+1}}}}}").scale(0.55)
            t.move_to(support.point(i).get_center()).shift(RIGHT * 0.15)
            terms.add(t)

        funnel = Arrow(start=support.get_right(), end=machine.in_port.get_left(), buff=0.2, stroke_width=3)
        self.play(Create(funnel))
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in terms], lag_ratio=0.08, run_time=1.0))
        self.wait(0.2)

        sum_spot = machine.get_left() + RIGHT * 0.2
        self.play(
            LaggedStart(
                *[
                    t.animate.move_to(sum_spot + UP * (0.25 - 0.18 * j)).scale(1.05)
                    for j, t in enumerate(terms)
                ],
                lag_ratio=0.08,
                run_time=1.1,
            )
        )

        Rc = MathTex(r"R_c(x)=\sum_{i=1}^n \frac{c_i}{x-\alpha_i}").scale(0.72)
        Rc.next_to(machine, UP, buff=0.35).align_to(machine, LEFT)

        # Compress: many small terms -> clean sum formula
        self.play(TransformMatchingTex(terms, Rc))
        self.wait(0.4)

        # ===== Mod g(x) constraint
        congr = MathTex(r"R_c(x)\equiv 0 \pmod{g(x)}").scale(0.75)
        congr.next_to(machine, DOWN, buff=0.35).align_to(machine, LEFT)
        self.play(Write(congr))
        self.wait(0.3)

        out_arrow = Arrow(start=machine.out_port.get_right(), end=lamps.get_left(), buff=0.2, stroke_width=3)
        self.play(Create(out_arrow))

        # Show a nonzero syndrome (some lamps on)
        self.play(*lamps.set_on_anims({0, 2, 5}), run_time=0.7)
        self.wait(0.3)

        # Kernel condition: lamps all off
        kernel_tex = MathTex(r"C=\{c:\ s(c)=0\}=\ker(H)").scale(0.78)
        kernel_tex.to_edge(RIGHT).shift(DOWN * 1.0)
        self.play(Write(kernel_tex))
        self.wait(0.3)

        self.play(*lamps.set_on_anims(set()), run_time=0.8)
        self.play(Indicate(kernel_tex, scale_factor=1.05), run_time=0.8)
        self.wait(0.4)

        # ===== Parity-check matrix view: s(c)=Hc^T
        H_eq = MathTex(r"s(c)=Hc^\top").scale(0.82)
        H_eq.next_to(kernel_tex, DOWN, buff=0.25).align_to(kernel_tex, LEFT)

        # Abstract block-matrix icon (6 x 7) with tiny squares
        rows = []
        for _ in range(6):
            row = VGroup(*[Square(0.18, stroke_width=1) for __ in range(7)]).arrange(RIGHT, buff=0.03)
            rows.append(row)
        H_icon = VGroup(*rows).arrange(DOWN, buff=0.05)
        H_icon.next_to(H_eq, DOWN, buff=0.2).align_to(H_eq, LEFT)

        H_brace = Brace(H_icon, LEFT)
        H_dim = MathTex(r"mt\times n").scale(0.6).next_to(H_brace, LEFT, buff=0.15)

        self.play(Write(H_eq), FadeIn(H_icon, shift=DOWN * 0.2), GrowFromCenter(H_brace), FadeIn(H_dim))
        self.wait(0.4)

        meas = Tex("Each row is a linear test (dot product).", font_size=26)
        meas.next_to(H_icon, DOWN, buff=0.25).align_to(H_icon, LEFT)
        self.play(FadeIn(meas, shift=DOWN * 0.1))
        self.wait(0.4)

        # ===== Image view: Enc(u)=uG (basis-of-kernel idea)
        self.play(FadeOut(arrows), FadeOut(funnel), FadeOut(out_arrow), run_time=0.7)

        enc_tex = MathTex(r"Enc:\mathbb{F}_2^k\to\mathbb{F}_2^n,\quad Enc(u)=uG").scale(0.78)
        enc_tex.to_edge(LEFT).shift(UP * 0.1)

        u = BitStrip(n=4, values=[1, 0, 1, 1], cell_size=0.45)
        u.next_to(enc_tex, DOWN, buff=0.25).align_to(enc_tex, LEFT)
        u_lbl = Tex(r"Message $u\in\mathbb{F}_2^k$", font_size=26)
        u_lbl.next_to(u, DOWN, buff=0.15).align_to(u, LEFT)

        basis = VGroup()
        for j in range(4):
            b = BitStrip(
                n=7,
                values=[(i + j) % 2 for i in range(7)],
                cell_size=0.24,
                buff=0.07,
            )
            b.set_opacity(0.55)
            basis.add(b)
        basis.arrange(DOWN, buff=0.12)
        basis.next_to(u, RIGHT, buff=0.6).shift(UP * 0.15)

        basis_lbl = Tex(r"Pick a basis of $\ker(H)$", font_size=26)
        basis_lbl.next_to(basis, UP, buff=0.18).align_to(basis, LEFT)

        plus = MathTex(r"+").scale(1.2)
        plus.next_to(basis, RIGHT, buff=0.3).shift(UP * 0.2)

        out_c = BitStrip(n=7, values=bits.values(), cell_size=0.45)
        out_c.next_to(plus, RIGHT, buff=0.35).shift(UP * 0.2)
        out_lbl = Tex(r"Output codeword $c\in C$", font_size=26)
        out_lbl.next_to(out_c, DOWN, buff=0.15).align_to(out_c, LEFT)

        self.play(FadeIn(enc_tex, shift=UP * 0.2))
        self.play(FadeIn(u, shift=UP * 0.1), FadeIn(u_lbl, shift=UP * 0.1))
        self.play(FadeIn(basis_lbl, shift=UP * 0.1), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in basis], lag_ratio=0.1))
        self.play(FadeIn(plus), FadeIn(out_c), FadeIn(out_lbl))
        self.wait(0.5)

        tri = VGroup(
            MathTex(r"C\subseteq\mathbb{F}_2^n"),
            MathTex(r"C=\ker(H)"),
            MathTex(r"C=\operatorname{im}(Enc)"),
        ).arrange(DOWN, buff=0.25).to_edge(RIGHT).shift(DOWN * 1.2)

        self.play(FadeIn(tri, shift=LEFT * 0.2))
        self.wait(1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.2)
