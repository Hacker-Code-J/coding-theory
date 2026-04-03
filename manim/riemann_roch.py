"""
Riemann-Roch Theorem — Professional 3B1B-style Manim Animation
===============================================================
Render commands:
  manim -pql riemann_roch.py RiemannRochFull        # low-quality preview
  manim -pqm riemann_roch.py RiemannRochFull        # medium quality
  manim -pqh riemann_roch.py RiemannRochFull        # high quality (HD)
  manim -pql riemann_roch.py <SceneName>            # individual scene

Scenes (standalone):
  S1_Title            Title card + formula
  S2_Surfaces         Compact Riemann surfaces, genus
  S3_Divisors         Divisors: formal sums of points
  S4_SpaceLD          The space L(D) and dimension ℓ(D)
  S5_Canonical        Canonical divisor K_X, deg(K) = 2g−2
  S6_Examples         Riemann-Roch on ℙ¹ and the elliptic curve
  S7_Theorem          Full theorem statement + Serre duality
  S8_Consequences     Corollaries and closing
"""

from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────────────
BG      = "#0d1117"
SURF_C  = "#58a6ff"   # curve / Riemann surface
DIV_C   = "#3fb950"   # divisor — positive coefficient
POLE_C  = "#f85149"   # divisor — negative coefficient / poles
CANON_C = "#d2a8ff"   # canonical divisor / holomorphic differentials
FUNC_C  = "#ffa657"   # meromorphic functions / L(D)
DIM_C   = "#8b949e"   # background / inactive
GOLD    = "#e6b450"   # theorem highlight


# ── Geometry helpers ─────────────────────────────────────────────────────────

def make_surface(genus: int, scale: float = 1.0, color=SURF_C) -> VGroup:
    """
    2D schematic of a genus-g compact surface:
      g=0  →  filled circle (sphere)
      g=1  →  circle + inner oval (torus cross-section)
      g≥2  →  elongated ellipse + g inner ovals (multi-torus)
    """
    fill_op = 0.10
    sw = 2.6
    if genus == 0:
        return VGroup(Circle(radius=0.9 * scale, color=color,
                             fill_opacity=fill_op, stroke_width=sw))
    if genus == 1:
        outer = Circle(radius=0.95 * scale, color=color,
                       fill_opacity=fill_op, stroke_width=sw)
        inner = Ellipse(width=0.72 * scale, height=0.38 * scale,
                        color=color, fill_opacity=0, stroke_width=sw - 0.6)
        return VGroup(outer, inner)
    # genus >= 2
    w = (1.9 + 1.25 * (genus - 1)) * scale
    h = 1.45 * scale
    outer = Ellipse(width=w, height=h, color=color,
                    fill_opacity=fill_op, stroke_width=sw)
    holes = VGroup()
    sp = w / (genus + 1)
    for i in range(genus):
        hole = Ellipse(width=0.60 * scale, height=0.32 * scale,
                       color=color, fill_opacity=0, stroke_width=sw - 0.6)
        hole.move_to([(-w / 2 + sp * (i + 1)), 0, 0])
        holes.add(hole)
    return VGroup(outer, holes)


def oval_pt(t: float) -> np.ndarray:
    """A point on the standard schematic curve X (2.4 × 1.2 ellipse)."""
    return np.array([2.4 * np.cos(t), 1.2 * np.sin(t), 0.0])


def make_curve(color=SURF_C, sw=2.6) -> ParametricFunction:
    return ParametricFunction(oval_pt, t_range=[0, TAU],
                              color=color, stroke_width=sw)


# ── Act functions — each takes a `scene` (Scene) as first argument ────────────

def act1_title(sc: Scene):
    title = Text("Riemann-Roch Theorem", font_size=66, weight=BOLD, color=WHITE)
    sub   = Text("A bridge between geometry and analysis on curves",
                 font_size=28, color=DIM_C)
    VGroup(title, sub).arrange(DOWN, buff=0.48).move_to(UP * 0.9)

    formula = MathTex(
        r"\ell(D) - \ell(K_X - D) = \deg(D) - g + 1",
        font_size=44, color=GOLD,
    ).next_to(sub, DOWN, buff=0.65)

    sc.play(Write(title, run_time=1.2))
    sc.play(FadeIn(sub, shift=UP * 0.2), run_time=0.7)
    sc.wait(0.4)
    sc.play(Write(formula, run_time=1.1))
    sc.wait(1.3)
    sc.play(FadeOut(VGroup(title, sub, formula)), run_time=0.7)


def act2_surfaces(sc: Scene):
    hdr = Text("Compact Riemann Surfaces", font_size=40, color=WHITE)\
        .to_edge(UP, buff=0.40)
    sc.play(FadeIn(hdr, shift=DOWN * 0.2), run_time=0.5)

    # ── Three surface schematics ──────────────────────────────────────────────
    def labeled(g, name, chi_str):
        surf = make_surface(g, scale=1.0)
        g_lbl   = MathTex(rf"g = {g}", font_size=26, color=SURF_C)
        nm_lbl  = Text(name, font_size=18, color=DIM_C)
        chi_lbl = MathTex(rf"\chi = {chi_str}", font_size=20, color=DIM_C)
        g_lbl .next_to(surf, DOWN, buff=0.14)
        nm_lbl.next_to(g_lbl,  DOWN, buff=0.08)
        chi_lbl.next_to(nm_lbl, DOWN, buff=0.08)
        return VGroup(surf, g_lbl, nm_lbl, chi_lbl)

    grp0 = labeled(0, "Sphere  ℙ¹",       "+2").move_to(LEFT  * 4.5 + DOWN * 0.2)
    grp1 = labeled(1, "Torus / Elliptic",  " 0").move_to(ORIGIN      + DOWN * 0.2)
    grp2 = labeled(2, "Double torus",      "-2").move_to(RIGHT * 4.5 + DOWN * 0.2)

    sc.play(
        LaggedStart(FadeIn(grp0), FadeIn(grp1), FadeIn(grp2), lag_ratio=0.35),
        run_time=1.0,
    )
    sc.wait(0.3)

    # ── Euler characteristic ──────────────────────────────────────────────────
    chi_eq = MathTex(r"\chi(X) = 2 - 2g", font_size=36, color=WHITE)\
        .to_edge(DOWN, buff=0.95)
    sc.play(Write(chi_eq, run_time=0.7))
    sc.wait(0.3)

    holo = Tex(
        r"Genus $g$ = number of independent holomorphic 1-forms on $X$",
        font_size=26, color=DIM_C,
    ).next_to(chi_eq, DOWN, buff=0.28)
    sc.play(FadeIn(holo, shift=UP * 0.2), run_time=0.5)
    sc.wait(1.1)

    sc.play(FadeOut(VGroup(hdr, grp0, grp1, grp2, chi_eq, holo)), run_time=0.7)


def act3_divisors(sc: Scene):
    hdr = Text("Divisors  —  Keeping Track of Zeros and Poles",
               font_size=36, color=WHITE).to_edge(UP, buff=0.40)
    sc.play(FadeIn(hdr, shift=DOWN * 0.2), run_time=0.5)

    # ── Curve X ───────────────────────────────────────────────────────────────
    curve = make_curve().move_to(DOWN * 0.15)
    X_lbl = MathTex(r"X", font_size=32, color=SURF_C)\
        .next_to(curve, RIGHT, buff=0.18)
    sc.play(Create(curve, run_time=0.9), FadeIn(X_lbl), run_time=0.9)

    # ── Four marked points ────────────────────────────────────────────────────
    t_vals  = [0.45, 1.55, 2.80, 4.50]
    names   = [r"P_1", r"P_2", r"P_3", r"P_4"]
    coefs   = [3, -1, 2, -2]
    colors  = [DIV_C, POLE_C, DIV_C, POLE_C]

    dots, p_lbls, c_lbls = VGroup(), VGroup(), VGroup()
    for t, nm, c, col in zip(t_vals, names, coefs, colors):
        pos = oval_pt(t) + DOWN * 0.15
        d  = Dot(pos, radius=0.090, color=col)
        pl = MathTex(nm, font_size=22, color=col).next_to(d, UP,   buff=0.12)
        cl = MathTex(("+" if c > 0 else "") + str(c), font_size=20, color=col)\
            .next_to(d, DOWN, buff=0.12)
        dots.add(d); p_lbls.add(pl); c_lbls.add(cl)

    sc.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.25), run_time=0.7)
    sc.play(LaggedStart(*[FadeIn(l) for l in p_lbls], lag_ratio=0.15), run_time=0.5)
    sc.play(LaggedStart(*[FadeIn(l) for l in c_lbls], lag_ratio=0.15), run_time=0.5)
    sc.wait(0.2)

    # ── Divisor expression and degree ─────────────────────────────────────────
    div_eq = MathTex(
        r"D \;=\; 3P_1 - P_2 + 2P_3 - 2P_4",
        font_size=34, color=WHITE,
    ).to_edge(DOWN, buff=1.30)
    sc.play(Write(div_eq, run_time=0.9))

    deg_eq = MathTex(
        r"\deg(D) \;=\; 3 + (-1) + 2 + (-2) \;=\; 2",
        font_size=28, color=DIM_C,
    ).next_to(div_eq, DOWN, buff=0.25)
    sc.play(Write(deg_eq, run_time=0.7))
    sc.wait(0.3)

    # ── Annotation ────────────────────────────────────────────────────────────
    notes = VGroup(
        Tex(r"$n_P > 0$: pole of order $\leq n_P$ \emph{allowed}",
            font_size=23, color=DIV_C),
        Tex(r"$n_P < 0$: zero of order $\geq |n_P|$ \emph{required}",
            font_size=23, color=POLE_C),
    ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)\
     .to_edge(LEFT, buff=0.55).shift(DOWN * 0.2)
    sc.play(FadeIn(notes, shift=RIGHT * 0.2), run_time=0.5)
    sc.wait(1.1)

    sc.play(FadeOut(VGroup(hdr, curve, X_lbl, dots, p_lbls, c_lbls,
                            div_eq, deg_eq, notes)), run_time=0.7)


def act4_space_ld(sc: Scene):
    hdr = Text("The Space  L(D)  and its Dimension  ℓ(D)",
               font_size=38, color=WHITE).to_edge(UP, buff=0.40)
    sc.play(FadeIn(hdr, shift=DOWN * 0.2), run_time=0.5)

    # ── Definition ────────────────────────────────────────────────────────────
    defn = MathTex(
        r"L(D) \;=\; \bigl\{\,f \text{ meromorphic on } X"
        r"\;\bigm|\; \operatorname{div}(f) + D \geq 0\,\bigr\} \;\cup\; \{0\}",
        font_size=30,
    ).move_to(UP * 2.05)
    sc.play(Write(defn, run_time=1.2))
    sc.wait(0.3)

    unpack = Tex(
        r"Concretely: at each point $P$, the function $f$ has a pole"
        r" of order $\leq n_P$, \; where $D = \sum n_P \cdot P$",
        font_size=25, color=DIM_C,
    ).next_to(defn, DOWN, buff=0.30)
    sc.play(FadeIn(unpack, shift=UP * 0.15), run_time=0.6)
    sc.wait(0.3)

    dim_eq = MathTex(
        r"\ell(D) \;=\; \dim_{\mathbb{C}} L(D)",
        font_size=38, color=FUNC_C,
    ).next_to(unpack, DOWN, buff=0.42)
    sc.play(Write(dim_eq, run_time=0.7))
    sc.wait(0.3)

    # ── Boxed example: D = n·P on ℙ¹ ─────────────────────────────────────────
    eg_body = VGroup(
        Tex(r"$X = \mathbb{P}^1$, \quad $D = n \cdot P_0$",
            font_size=26, color=SURF_C),
        MathTex(
            r"L(nP_0) \;=\; \operatorname{span}\{1,\, z,\, z^2,\, \ldots,\, z^n\}",
            font_size=26, color=FUNC_C),
        MathTex(r"\Rightarrow \quad \ell(nP_0) \;=\; n + 1",
                font_size=28, color=FUNC_C),
    ).arrange(DOWN, buff=0.20).next_to(dim_eq, DOWN, buff=0.42)
    eg_box = SurroundingRectangle(eg_body, color=FUNC_C, buff=0.22,
                                   corner_radius=0.12, stroke_width=2.0)
    sc.play(FadeIn(eg_body), Create(eg_box), run_time=0.7)
    sc.wait(0.3)

    # ── Key fact ──────────────────────────────────────────────────────────────
    neg_fact = Tex(
        r"\textbf{Key fact}: $\deg(D) < 0 \;\Rightarrow\; \ell(D) = 0$",
        font_size=25, color=DIM_C,
    ).to_edge(DOWN, buff=0.60)
    sc.play(FadeIn(neg_fact, shift=UP * 0.2), run_time=0.5)
    sc.wait(1.1)

    sc.play(FadeOut(VGroup(hdr, defn, unpack, dim_eq, eg_body, eg_box, neg_fact)),
            run_time=0.7)


def act5_canonical(sc: Scene):
    hdr = Text("The Canonical Divisor  K\u2093", font_size=40, color=WHITE)\
        .to_edge(UP, buff=0.40)
    sc.play(FadeIn(hdr, shift=DOWN * 0.2), run_time=0.5)

    # ── Definition ────────────────────────────────────────────────────────────
    intro = Tex(
        r"Choose any non-zero meromorphic 1-form $\omega$ on $X$.",
        font_size=27, color=DIM_C,
    ).move_to(UP * 2.0)
    sc.play(FadeIn(intro, shift=DOWN * 0.1), run_time=0.5)

    k_def = MathTex(
        r"K_X \;=\; \operatorname{div}(\omega)"
        r"\;=\; \sum_{P \in X} \operatorname{ord}_P(\omega) \cdot P",
        font_size=32, color=CANON_C,
    ).next_to(intro, DOWN, buff=0.35)
    sc.play(Write(k_def, run_time=0.9))
    sc.wait(0.3)

    indep = Tex(
        r"(The linear equivalence class $[K_X]$ is independent of the choice of $\omega$.)",
        font_size=22, color=DIM_C,
    ).next_to(k_def, DOWN, buff=0.22)
    sc.play(FadeIn(indep, shift=UP * 0.1), run_time=0.5)

    # ── deg(K) = 2g-2 ────────────────────────────────────────────────────────
    deg_k = MathTex(r"\deg(K_X) \;=\; 2g - 2", font_size=40, color=CANON_C)\
        .next_to(indep, DOWN, buff=0.40)
    sc.play(Write(deg_k, run_time=0.8))
    sc.wait(0.3)

    # ── Table: one row per genus ──────────────────────────────────────────────
    rows_data = [
        (0, "-2", r"K_{\mathbb{P}^1} \sim -2P_\infty"),
        (1,  "0", r"K_X \sim 0 \text{ (nowhere-zero holomorphic form)}"),
        (2, "+2", r"\deg(K_X) = 2"),
    ]
    table_rows = VGroup()
    for g_val, deg_str, note_str in rows_data:
        surf  = make_surface(g_val, scale=0.38)
        g_tex = MathTex(rf"g={g_val}", font_size=20, color=SURF_C)
        d_tex = MathTex(rf"\deg K={deg_str}", font_size=22, color=CANON_C)
        n_tex = MathTex(note_str, font_size=18, color=DIM_C)
        row   = VGroup(surf, g_tex, d_tex, n_tex).arrange(RIGHT, buff=0.45)
        table_rows.add(row)

    table_rows.arrange(DOWN, buff=0.30, aligned_edge=LEFT)\
        .to_edge(DOWN, buff=0.45).shift(RIGHT * 0.4)

    sc.play(
        LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in table_rows],
                    lag_ratio=0.35),
        run_time=0.9,
    )
    sc.wait(1.2)

    sc.play(FadeOut(VGroup(hdr, intro, k_def, indep, deg_k, table_rows)), run_time=0.7)


def act6_examples(sc: Scene):
    hdr = Text("Riemann-Roch in Action", font_size=40, color=WHITE)\
        .to_edge(UP, buff=0.40)
    rr_bar = MathTex(
        r"\ell(D) - \ell(K-D) = \deg(D) - g + 1",
        font_size=26, color=GOLD,
    ).next_to(hdr, DOWN, buff=0.26)
    sc.play(FadeIn(hdr, shift=DOWN * 0.2), FadeIn(rr_bar), run_time=0.55)

    # ──────────────────────────────────────────────────────────────────────────
    # Example 1 — g=0, D = n·P on ℙ¹
    # ──────────────────────────────────────────────────────────────────────────
    ex1_title = Text("Example 1  —  Genus 0  (Riemann sphere  ℙ¹)",
                     font_size=27, color=SURF_C).move_to(UP * 1.55)
    sc.play(FadeIn(ex1_title, shift=DOWN * 0.12), run_time=0.4)

    ex1 = VGroup(
        MathTex(r"g=0,\quad K \sim -2P_\infty,\quad \deg(K)=-2",
                font_size=26),
        MathTex(r"D = n \cdot P_0,\quad \deg(D)=n\geq 0",
                font_size=26),
        MathTex(
            r"\deg(K-D) = -2-n < 0 \;\Rightarrow\; \ell(K-D) = 0",
            font_size=25, color=CANON_C,
        ),
        MathTex(r"\therefore\quad \ell(D) = n - 0 + 1 = n+1",
                font_size=28, color=FUNC_C),
        Tex(r"Basis: $\{1,\, z,\, z^2,\, \ldots,\, z^n\}$ \checkmark",
            font_size=24, color=DIV_C),
    ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)\
     .next_to(ex1_title, DOWN, buff=0.28).to_edge(LEFT, buff=1.1)

    for line in ex1:
        sc.play(FadeIn(line, shift=RIGHT * 0.1), run_time=0.38)
        sc.wait(0.12)
    sc.wait(0.65)
    sc.play(FadeOut(VGroup(ex1_title, ex1)), run_time=0.5)

    # ──────────────────────────────────────────────────────────────────────────
    # Example 2 — g=1 (elliptic curve), ℓ(nP) table
    # ──────────────────────────────────────────────────────────────────────────
    ex2_title = Text("Example 2  —  Genus 1  (Elliptic curve / complex torus)",
                     font_size=26, color=SURF_C).move_to(UP * 1.55)
    sc.play(FadeIn(ex2_title, shift=DOWN * 0.12), run_time=0.4)

    # Manual table: n | ℓ(nP) | basis
    col_x = [-4.0, -2.5, -0.4]  # x-positions of three columns
    headers = [
        MathTex(r"n",           font_size=24, color=GOLD),
        MathTex(r"\ell(nP)",    font_size=24, color=GOLD),
        MathTex(r"\text{basis of } L(nP)", font_size=22, color=GOLD),
    ]
    rows = [
        ["0", "1",  r"\{1\}"],
        ["1", "1",  r"\{1\}"],
        ["2", "2",  r"\{1,\,\wp\}"],
        ["3", "3",  r"\{1,\,\wp,\,\wp'\}"],
    ]

    # Position headers
    for hd, x in zip(headers, col_x):
        hd.move_to([x, 0.85, 0])
    header_grp = VGroup(*headers)
    uline = Line(
        [col_x[0] - 0.4, 0.60, 0],
        [col_x[2] + 2.2, 0.60, 0],
        stroke_width=1.4, color=DIM_C,
    )

    row_mobjs = VGroup()
    for r_i, row_data in enumerate(rows):
        y = 0.30 - r_i * 0.52
        cell_col = FUNC_C if r_i >= 0 else WHITE
        row_grp = VGroup()
        for c_i, (val, x) in enumerate(zip(row_data, col_x)):
            cell = MathTex(val, font_size=24,
                           color=(FUNC_C if c_i == 1 else
                                  DIV_C  if c_i == 2 else WHITE))
            cell.move_to([x, y, 0])
            row_grp.add(cell)
        row_mobjs.add(row_grp)

    sc.play(FadeIn(header_grp), Create(uline), run_time=0.45)
    for row in row_mobjs:
        sc.play(FadeIn(row, shift=RIGHT * 0.08), run_time=0.32)
        sc.wait(0.08)
    sc.wait(0.35)

    # Verification
    verify = MathTex(
        r"K_X \sim 0 \;\Rightarrow\; \ell(K-nP) = 0 \text{ for } n\geq 1",
        font_size=24, color=CANON_C,
    ).to_edge(RIGHT, buff=0.6).shift(UP * 0.5)
    rr_check = MathTex(
        r"\ell(nP) \;=\; n - 1 + 1 \;=\; n \quad \checkmark",
        font_size=26, color=FUNC_C,
    ).next_to(verify, DOWN, buff=0.25)
    sc.play(FadeIn(verify, shift=LEFT * 0.15), run_time=0.5)
    sc.play(Write(rr_check, run_time=0.6))
    sc.wait(0.9)

    sc.play(FadeOut(VGroup(hdr, rr_bar, ex2_title,
                            header_grp, uline, row_mobjs,
                            verify, rr_check)), run_time=0.7)


def act7_theorem(sc: Scene):
    hdr = Text("The Riemann-Roch Theorem", font_size=40, color=WHITE)\
        .to_edge(UP, buff=0.40)
    sc.play(FadeIn(hdr, shift=DOWN * 0.2), run_time=0.5)

    # ── Build formula term by term ────────────────────────────────────────────
    f1 = MathTex(r"\ell(D)", font_size=52, color=FUNC_C).move_to(UP * 1.6)
    sc.play(Write(f1, run_time=0.7))
    n1 = Tex(r"$\ell(D)$: \# independent meromorphic functions allowed by $D$",
             font_size=22, color=DIM_C).next_to(f1, DOWN, buff=0.25)
    sc.play(FadeIn(n1, shift=UP * 0.1), run_time=0.4)
    sc.wait(0.35)

    f2 = MathTex(r"\ell(D) \;-\; \ell(K_X - D)",
                 font_size=48, color=WHITE).move_to(UP * 1.6)
    f2.set_color_by_tex(r"\ell(D)", FUNC_C)
    sc.play(TransformMatchingTex(f1, f2), FadeOut(n1), run_time=0.8)
    n2 = Tex(
        r"$\ell(K_X-D)$: holomorphic 1-forms obstructing $L(D)$ \; (correction term)",
        font_size=22, color=CANON_C,
    ).next_to(f2, DOWN, buff=0.25)
    sc.play(FadeIn(n2, shift=UP * 0.1), run_time=0.4)
    sc.wait(0.35)

    f3 = MathTex(
        r"\ell(D) - \ell(K_X - D) \;=\; \deg(D) - g + 1",
        font_size=44, color=WHITE,
    ).move_to(UP * 1.6)
    sc.play(TransformMatchingTex(f2, f3), FadeOut(n2), run_time=0.9)
    sc.wait(0.3)

    # Theorem box
    thm_box = SurroundingRectangle(
        f3, color=GOLD, buff=0.32, corner_radius=0.14, stroke_width=2.8,
    )
    thm_lbl = Text("Riemann-Roch", font_size=20, color=GOLD)\
        .next_to(thm_box, UP, buff=0.10)
    sc.play(Create(thm_box), FadeIn(thm_lbl), run_time=0.55)
    sc.wait(0.4)

    # ── Colour-coded annotations ──────────────────────────────────────────────
    anns = VGroup(
        Tex(r"$\ell(D)$\;: algebraic data  (vector space dimension)",
            font_size=23, color=FUNC_C),
        Tex(r"$\ell(K_X-D)$\;: correction via holomorphic differentials",
            font_size=23, color=CANON_C),
        Tex(r"$\deg(D)$\;: total ``pole budget'' of the divisor $D$",
            font_size=23, color=DIV_C),
        Tex(r"$g$\;: genus of the Riemann surface $X$",
            font_size=23, color=SURF_C),
    ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)\
     .to_edge(DOWN, buff=0.42).to_edge(LEFT, buff=0.55)

    sc.play(
        LaggedStart(*[FadeIn(a, shift=RIGHT * 0.15) for a in anns], lag_ratio=0.30),
        run_time=1.0,
    )
    sc.wait(0.4)

    # ── Serre duality (right side) ────────────────────────────────────────────
    serre = VGroup(
        MathTex(
            r"H^1\!\bigl(X,\mathcal{O}(D)\bigr) \;\cong\; H^0\!\bigl(X,\mathcal{O}(K_X-D)\bigr)^\vee",
            font_size=24, color=CANON_C,
        ),
        Tex(r"Serre duality $\;\Rightarrow\; h^1(D) = \ell(K_X-D)$",
            font_size=21, color=DIM_C),
    ).arrange(DOWN, buff=0.18)\
     .to_edge(RIGHT, buff=0.45).shift(UP * 0.3)

    serre_box = SurroundingRectangle(serre, color=CANON_C, buff=0.18,
                                      corner_radius=0.10, stroke_width=1.6)
    sc.play(FadeIn(serre), Create(serre_box), run_time=0.6)
    sc.wait(1.2)

    sc.play(FadeOut(VGroup(hdr, f3, thm_box, thm_lbl, anns, serre, serre_box)),
            run_time=0.8)


def act8_consequences(sc: Scene):
    hdr = Text("Consequences", font_size=40, color=WHITE).to_edge(UP, buff=0.40)
    rr_bar = MathTex(
        r"\ell(D) - \ell(K-D) = \deg(D) - g + 1",
        font_size=26, color=GOLD,
    ).next_to(hdr, DOWN, buff=0.26)
    sc.play(FadeIn(hdr, shift=DOWN * 0.2), FadeIn(rr_bar), run_time=0.55)

    # ── Four corollaries ──────────────────────────────────────────────────────
    corollaries = [
        (FUNC_C,
         r"\textbf{Riemann's inequality}: if $\deg(D)\geq 2g-1$ then "
         r"$\ell(K-D)=0$, so $\ell(D)=\deg(D)-g+1$",
         r"(the correction term vanishes for large enough $D$)"),
        (CANON_C,
         r"\textbf{Holomorphic forms}: setting $D=0$ gives $\ell(K_X)=g$",
         r"The genus = the dimension of the space of holomorphic 1-forms"),
        (SURF_C,
         r"\textbf{Genus 0}: any curve with $g=0$ is isomorphic to $\mathbb{P}^1$",
         r"(take $D=P$: $\ell(P)=2$, so a degree-1 meromorphic function exists)"),
        (DIV_C,
         r"\textbf{Elliptic embedding}: $g=1$, $D=3P$ gives $\ell(3P)=3$",
         r"Basis $\{1,\wp,\wp'\}$ embeds the torus into $\mathbb{P}^2$ as a cubic curve"),
    ]

    items = VGroup()
    for col, main_s, note_s in corollaries:
        main = Tex(main_s, font_size=24, color=col)
        note = Tex(note_s, font_size=19, color=DIM_C)\
            .next_to(main, DOWN, buff=0.08).shift(RIGHT * 0.25)
        items.add(VGroup(main, note))

    items.arrange(DOWN, buff=0.30, aligned_edge=LEFT)\
        .next_to(rr_bar, DOWN, buff=0.32).to_edge(LEFT, buff=0.65)

    for item in items:
        sc.play(FadeIn(item[0], shift=RIGHT * 0.1), run_time=0.38)
        sc.play(FadeIn(item[1], shift=RIGHT * 0.1), run_time=0.32)
        sc.wait(0.20)
    sc.wait(0.7)

    # ── Closing frame ─────────────────────────────────────────────────────────
    sc.play(FadeOut(VGroup(hdr, rr_bar, items)), run_time=0.75)

    final = MathTex(
        r"\ell(D) \;-\; \ell(K_X-D) \;=\; \deg(D) \;-\; g \;+\; 1",
        font_size=46, color=GOLD,
    ).move_to(UP * 0.6)
    closing = Text(
        "Algebra on curves, governed by topology.",
        font_size=30, color=DIM_C,
    ).next_to(final, DOWN, buff=0.55)

    sc.play(Write(final, run_time=1.2))
    sc.play(FadeIn(closing, shift=UP * 0.2), run_time=0.7)
    sc.wait(1.6)
    sc.play(FadeOut(VGroup(final, closing)), run_time=0.9)


# ── Standalone scene wrappers ─────────────────────────────────────────────────

class S1_Title(Scene):
    def construct(self):
        self.camera.background_color = BG
        act1_title(self)

class S2_Surfaces(Scene):
    def construct(self):
        self.camera.background_color = BG
        act2_surfaces(self)

class S3_Divisors(Scene):
    def construct(self):
        self.camera.background_color = BG
        act3_divisors(self)

class S4_SpaceLD(Scene):
    def construct(self):
        self.camera.background_color = BG
        act4_space_ld(self)

class S5_Canonical(Scene):
    def construct(self):
        self.camera.background_color = BG
        act5_canonical(self)

class S6_Examples(Scene):
    def construct(self):
        self.camera.background_color = BG
        act6_examples(self)

class S7_Theorem(Scene):
    def construct(self):
        self.camera.background_color = BG
        act7_theorem(self)

class S8_Consequences(Scene):
    def construct(self):
        self.camera.background_color = BG
        act8_consequences(self)


# ── Full video — all eight acts in one Scene ──────────────────────────────────

class RiemannRochFull(Scene):
    """Renders the complete Riemann-Roch story in one video file."""

    def construct(self):
        self.camera.background_color = BG
        act1_title(self)
        act2_surfaces(self)
        act3_divisors(self)
        act4_space_ld(self)
        act5_canonical(self)
        act6_examples(self)
        act7_theorem(self)
        act8_consequences(self)
        self.wait(0.5)
