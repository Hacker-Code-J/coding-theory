# hamming_vis.py
# Manim Community Edition (tested style for v0.17+ / v0.18+)
from manim import *

# manim -pqh hamming_vis.py HammingSyndrome3b1b

# -----------------------------
# Small F2 helpers
# -----------------------------
def f2_add(a, b):
    return [(x ^ y) for x, y in zip(a, b)]

def mat_vec_mul_f2(M, v):
    # M: list of rows, v: list bits
    out = []
    for row in M:
        s = 0
        for rij, vj in zip(row, v):
            s ^= (rij & vj)
        out.append(s)
    return out

def col(M, j):
    return [M[i][j] for i in range(len(M))]

def bits_tex(bits):
    # column vector tex
    return r"\begin{pmatrix}" + r"\\".join(str(b) for b in bits) + r"\end{pmatrix}"

def rowbits_tex(bits):
    return "(" + ",".join(str(b) for b in bits) + ")"

def mat_tex(M):
    rows = ["&".join(str(x) for x in row) for row in M]
    return r"\begin{pmatrix}" + r"\\".join(rows) + r"\end{pmatrix}"

def venn_subset(
    universe_label=r"\Sigma^n",
    subset_label=r"C",
    title_tex=r"A block code is a subset $C\subseteq \Sigma^n$",
    font_size=40,
):
    """
    Returns a VGroup: (title, universe_rect, subset_blob, labels)
    You can animate it as one object.
    """
    title = Tex(title_tex, font_size=font_size)

    # Universe (Sigma^n)
    U = RoundedRectangle(corner_radius=0.25, width=6.5, height=3.2)
    U.set_stroke(width=4, opacity=0.5)
    U.set_fill(opacity=0.04)

    U_lab = MathTex(universe_label, font_size=36).to_corner(UR).shift(0.2*LEFT + 0.2*DOWN)
    U_lab.move_to(U.get_corner(UR) + 0.35*LEFT + 0.35*DOWN)

    # Subset blob (C)
    blob = VMobject()
    blob.set_points_smoothly([
        [-1.8, -0.2, 0],
        [-1.2,  1.0, 0],
        [ 0.3,  0.9, 0],
        [ 1.2,  0.1, 0],
        [ 0.6, -1.0, 0],
        [-0.8, -0.9, 0],
        [-1.8, -0.2, 0],
    ])
    blob.scale(1.15)
    blob.set_stroke(width=0)               # 3b1b style: soft fill, minimal outline
    blob.set_fill(opacity=0.18)            # no explicit color; use default theme
    blob.move_to(U.get_center() + 0.2*LEFT)

    C_lab = MathTex(subset_label, font_size=44).move_to(blob.get_center() + 0.1*UP)

    diagram = VGroup(U, blob, U_lab, C_lab)
    diagram.next_to(title, DOWN, buff=0.45)

    return VGroup(title, diagram)

# -----------------------------
# Main Scene
# -----------------------------
class HammingSyndrome3b1b(Scene):
    def construct(self):
        # Your matrices (as Python bit-lists)
        H = [
            [0,1,1,1,1,0,0],
            [1,0,1,1,0,1,0],
            [1,1,0,1,0,0,1],
        ]
        G = [
            [1,0,0,0,0,1,1],
            [0,1,0,0,1,0,1],
            [0,0,1,0,1,1,0],
            [0,0,0,1,1,1,1],
        ]

#        # ------------------------------------------------------------
#        # 0) Title + “code as subset”
#        # ------------------------------------------------------------
#        title = Tex(r"Linear code as subset / image / kernel", font_size=56)
#        title.to_edge(UP)
#        self.play(Write(title), run_time=1.2)
#
#        subset = Tex(
#            r"A block code is a subset $C\subseteq \Sigma^n$",
#            font_size=40
#        ).next_to(title, DOWN, buff=0.5)
#
#        self.play(FadeIn(subset, shift=0.2*UP))
#        self.wait(0.5)
#
#        bullets = VGroup(
#            Tex(r"$\Sigma=\mathbb{F}_q$ and $C$ a linear subspace of $\mathbb{F}_q^n$", font_size=34),
#            Tex(r"$C=\mathrm{im}(c)\ :\ \mathrm{c}:\Sigma^k\to\Sigma^n$", font_size=34),
#            Tex(r"$C=\ker(H)\ :\ H:\mathbb{F}_q^n\to\mathbb{F}_q^{n-k}$", font_size=34),
#        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(subset, DOWN, buff=0.45)
#
#        for b in bullets:
#            b.set_opacity(0.25)
#
#        self.play(FadeIn(bullets, lag_ratio=0.15), run_time=1.2)
#        self.wait(0.2)

        # ------------------------------------------------------------
        # Style knobs (tweak once, affects everything)
        # ------------------------------------------------------------
        FS_TITLE = 56
        FS_MAIN  = 40
        FS_LAB   = 34

        # ------------------------------------------------------------
        # 0) Title
        # ------------------------------------------------------------
        title = Tex(r"One code, three equivalent views", font_size=FS_TITLE).to_edge(UP)
        underline = Line(LEFT, RIGHT).match_width(title).next_to(title, DOWN, buff=0.12)
        underline.set_stroke(width=6, opacity=0.45)
        self.play(Write(title), run_time=0.9)
        self.play(Create(underline), run_time=0.45)

        # ------------------------------------------------------------
        # 1) Universe Sigma^n + subset blob C
        # ------------------------------------------------------------
        statement = Tex(r"$C\subseteq \Sigma^n$", font_size=FS_MAIN).next_to(title, DOWN, buff=0.55)
        self.play(Write(statement), run_time=0.6)

        # Universe box
        U = RoundedRectangle(corner_radius=0.25, width=7.0, height=3.4)
        U.set_stroke(width=4, opacity=0.45)
        U.set_fill(opacity=0.04)
        U.next_to(statement, DOWN, buff=0.35)

        U_lab = MathTex(r"\Sigma^n", font_size=FS_LAB)
        U_lab.move_to(U.get_corner(UR) + 0.35*LEFT + 0.35*DOWN)

        # Smooth blob for C
        blob = VMobject()
        blob.set_points_smoothly([
            [-2.1, -0.1, 0],
            [-1.4,  1.1, 0],
            [ 0.1,  1.0, 0],
            [ 1.2,  0.2, 0],
            [ 0.7, -1.1, 0],
            [-0.9, -1.0, 0],
            [-2.1, -0.1, 0],
        ])
        blob.scale(1.10)
        blob.set_stroke(width=0)
        blob.set_fill(opacity=0.18)
        blob.move_to(U.get_center() + 0.3*LEFT)

        C_lab = MathTex(r"C", font_size=44).move_to(blob.get_center() + 0.1*UP)

        self.play(Create(U), FadeIn(U_lab, shift=0.15*DOWN), run_time=0.7)
        self.play(GrowFromCenter(blob), FadeIn(C_lab), run_time=0.7)

        # A few "ambient points" in Sigma^n
        ambient = VGroup(*[
            Dot(point=U.point_from_proportion(p), radius=0.03).set_opacity(0.22)
            for p in [0.08,0.16,0.23,0.31,0.39,0.47,0.56,0.64,0.72,0.81,0.90]
        ])
        self.play(FadeIn(ambient), run_time=0.4)

        # ------------------------------------------------------------
        # 2) Image view: c: Sigma^k -> Sigma^n with im(c)=C
        # ------------------------------------------------------------
        img_stmt = Tex(r"$C=\mathrm{im}(c)$", font_size=FS_MAIN)
        img_stmt.to_corner(LEFT).shift(0.6*DOWN)
        img_stmt.set_opacity(0.25)

        # Domain box Sigma^k on the left of U
        Dom = RoundedRectangle(corner_radius=0.25, width=3.0, height=1.9)
        Dom.set_stroke(width=4, opacity=0.45)
        Dom.set_fill(opacity=0.04)
        Dom.next_to(U, LEFT, buff=1.1).shift(0.15*UP)

        Dom_lab = MathTex(r"\Sigma^k", font_size=FS_LAB).move_to(Dom.get_corner(UR) + 0.3*LEFT + 0.3*DOWN)

        # Arrow lands inside blob (image)
        arrow_c = Arrow(Dom.get_right(), blob.get_left(), buff=0.2, stroke_width=6)
        c_lab = MathTex(r"c", font_size=FS_LAB).next_to(arrow_c, UP, buff=0.12)

        # A few sample messages u in Sigma^k and their images in C
        msgs = VGroup(*[
            Dot(Dom.get_center() + np.array([(-0.7+0.7*i), 0.2*((-1)**i), 0]), radius=0.04)
            for i in range(3)
        ]).set_opacity(0.75)

        codepts = VGroup(*[
            Dot(blob.get_center() + np.array([(-0.6+0.6*i), 0.25*((-1)**(i+1)), 0]), radius=0.04)
            for i in range(3)
        ]).set_opacity(0.75)

        self.play(FadeIn(img_stmt), run_time=0.3)
        self.play(Create(Dom), FadeIn(Dom_lab), run_time=0.6)
        self.play(GrowArrow(arrow_c), FadeIn(c_lab), run_time=0.6)
        self.play(FadeIn(msgs), FadeIn(codepts), run_time=0.4)

        # Animate “mapping” of points u -> c(u) into the blob
        map_anims = []
        for m, cp in zip(msgs, codepts):
            ghost = m.copy()
            map_anims.append(Transform(ghost, cp))
        self.play(LaggedStart(*map_anims, lag_ratio=0.12), run_time=1.0)
        self.wait(0.2)

        # Spotlight image statement
        img_high = SurroundingRectangle(img_stmt, buff=0.15)
        img_high.set_stroke(width=5, opacity=0.55)
        self.play(img_stmt.animate.set_opacity(1.0), Create(img_high), run_time=0.6)
        self.wait(0.2)

        # ------------------------------------------------------------
        # 3) Kernel view: H: Sigma^n -> Sigma^{n-k} with ker(H)=C
        # ------------------------------------------------------------
        ker_stmt = Tex(r"$C=\ker(H)$", font_size=FS_MAIN)
        ker_stmt.to_corner(RIGHT).shift(0.6*DOWN)
        ker_stmt.set_opacity(0.25)

        Cod = RoundedRectangle(corner_radius=0.25, width=3.3, height=1.9)
        Cod.set_stroke(width=4, opacity=0.45)
        Cod.set_fill(opacity=0.04)
        Cod.next_to(U, RIGHT, buff=1.1).shift(0.15*UP)

        Cod_lab = MathTex(r"\Sigma^{n-k}", font_size=FS_LAB).move_to(Cod.get_corner(UR) + 0.3*LEFT + 0.3*DOWN)

        arrow_H = Arrow(U.get_right(), Cod.get_left(), buff=0.2, stroke_width=6)
        H_lab = MathTex(r"H", font_size=FS_LAB).next_to(arrow_H, UP, buff=0.12)

        # Zero element in codomain highlighted
        zero = MathTex(r"0", font_size=44).move_to(Cod.get_center())
        zero_ring = Circle(radius=0.35).move_to(zero).set_stroke(width=6, opacity=0.55)

        # Show some points in Sigma^n mapping:
        outside_pts = VGroup(
            Dot(U.get_center() + 2.2*LEFT + 0.9*UP, radius=0.04),
            Dot(U.get_center() + 2.4*RIGHT + 0.6*DOWN, radius=0.04),
            Dot(U.get_center() + 0.2*RIGHT + 1.3*UP, radius=0.04),
        ).set_opacity(0.65)

        # Targets in codomain (nonzero syndromes) for outside points
        synd_pts = VGroup(
            Dot(Cod.get_center() + 0.9*LEFT + 0.5*UP, radius=0.04),
            Dot(Cod.get_center() + 0.8*RIGHT + 0.2*UP, radius=0.04),
            Dot(Cod.get_center() + 0.2*RIGHT + 0.7*DOWN, radius=0.04),
        ).set_opacity(0.65)

        self.play(FadeIn(ker_stmt), run_time=0.3)
        self.play(Create(Cod), FadeIn(Cod_lab), run_time=0.6)
        self.play(GrowArrow(arrow_H), FadeIn(H_lab), run_time=0.6)
        self.play(FadeIn(zero), Create(zero_ring), run_time=0.6)

        # Put a few points outside C, then show they map to nonzero syndromes
        self.play(FadeIn(outside_pts), run_time=0.4)
        map2 = []
        for p, sp in zip(outside_pts, synd_pts):
            ghost = p.copy()
            map2.append(Transform(ghost, sp))
        self.play(FadeIn(synd_pts), LaggedStart(*map2, lag_ratio=0.12), run_time=0.9)

        # Now show points inside C map to 0 (kernel)
        inside_pts = VGroup(
            Dot(blob.get_center() + 0.6*LEFT + 0.2*UP, radius=0.04),
            Dot(blob.get_center() + 0.2*RIGHT + 0.5*DOWN, radius=0.04),
            Dot(blob.get_center() + 0.7*RIGHT + 0.35*UP, radius=0.04),
        ).set_opacity(0.85)

        self.play(FadeIn(inside_pts), run_time=0.4)

        map3 = []
        for p in inside_pts:
            ghost = p.copy()
            map3.append(Transform(ghost, zero.copy().set_opacity(0.95)))
        self.play(LaggedStart(*map3, lag_ratio=0.12), run_time=0.9)

        # Spotlight kernel statement
        ker_high = SurroundingRectangle(ker_stmt, buff=0.15)
        ker_high.set_stroke(width=5, opacity=0.55)
        self.play(ker_stmt.animate.set_opacity(1.0), Create(ker_high), run_time=0.6)
        self.wait(0.2)

        # ------------------------------------------------------------
        # 4) Unify: fade in equivalences between the three labels
        # ------------------------------------------------------------
        eq = Tex(r"$C\subseteq \Sigma^n \quad=\quad \mathrm{im}(c) \quad=\quad \ker(H)$", font_size=42)
        eq.next_to(U, DOWN, buff=0.35)

        self.play(FadeIn(eq, shift=0.15*UP), run_time=0.7)

        # Dim the scene slightly so you can transition into G/H algebra next
        self.play(
            FadeOut(img_high),
            FadeOut(ker_high),
            img_stmt.animate.set_opacity(0.5),
            ker_stmt.animate.set_opacity(0.5),
            run_time=0.5
        )
        self.wait(0.6)

#        # Emphasize we are in F2, n=7, k=4
#        params = Tex(r"Here: $\mathbb{F}_2$,  $n=7$, $k=4$,  $(7,4,3)_2$ Hamming code", font_size=36)
#        params.next_to(bullets, DOWN, buff=0.45)
#        self.play(Write(params), run_time=1.2)
#        self.wait(0.6)

#        # ------------------------------------------------------------
#        # 1) Show G as encoding morphism (image)
#        # ------------------------------------------------------------
#        self.play(bullets[1].animate.set_opacity(1.0), run_time=0.6)
#        enc_box = SurroundingRectangle(bullets[1], buff=0.15, color=YELLOW)
#        self.play(Create(enc_box), run_time=0.6)
#
#        G_tex = MathTex("G=", mat_tex(G), font_size=40)
#        G_tex.to_corner(LEFT+DOWN)
#        G_label = Tex(r"Encoding: $c = uG$", font_size=34).next_to(G_tex, UP, buff=0.35).align_to(G_tex, LEFT)
#
#        self.play(FadeIn(G_tex, shift=0.3*LEFT), FadeIn(G_label, shift=0.3*LEFT), run_time=1.0)
#
#        # Pick a message u and compute c = uG
#        u = [1,0,1,1]  # message bits
#        # compute c = uG over F2 (u row vector)
#        # c_j = sum_i u_i * G_i,j
#        # implement by transposing logic:
#        c = []
#        for j in range(7):
#            s = 0
#            for i in range(4):
#                s ^= (u[i] & G[i][j])
#            c.append(s)
#
#        u_tex = MathTex(r"u=", bits_tex(u), font_size=40).next_to(G_label, RIGHT, buff=0.7).shift(0.05*DOWN)
#        c_tex = MathTex(r"c=uG=", bits_tex(c), font_size=40).next_to(u_tex, RIGHT, buff=0.7)
#
#        self.play(Write(u_tex), run_time=0.8)
#        self.play(Write(c_tex), run_time=1.0)
#        self.wait(0.5)
#
#        # ------------------------------------------------------------
#        # 2) Show H as parity-check (kernel)
#        # ------------------------------------------------------------
#        self.play(bullets[2].animate.set_opacity(1.0), run_time=0.6)
#        ker_box = SurroundingRectangle(bullets[2], buff=0.15, color=BLUE)
#        self.play(Create(ker_box), run_time=0.6)
#
#        H_tex = MathTex("H=", mat_tex(H), font_size=40).to_corner(RIGHT+DOWN)
#        H_label = Tex(r"Parity-check: $s(x)=Hx^\top$", font_size=34).next_to(H_tex, UP, buff=0.35).align_to(H_tex, LEFT)
#
#        self.play(FadeIn(H_tex, shift=0.3*RIGHT), FadeIn(H_label, shift=0.3*RIGHT), run_time=1.0)
#
#        # Verify c is in kernel: H c^T = 0
#        s_c = mat_vec_mul_f2(H, c)
#        sc_tex = MathTex(r"Hc^\top=", bits_tex(s_c), font_size=40).next_to(H_label, LEFT, buff=0.8)
#        zero_tex = MathTex(r"=", bits_tex([0,0,0]), font_size=40).next_to(sc_tex, RIGHT, buff=0.25)
#        sc_group = VGroup(sc_tex, zero_tex).shift(0.2*UP)
#
#        self.play(Write(sc_tex), run_time=1.0)
#        self.play(Write(zero_tex), run_time=0.8)
#        self.wait(0.6)
#
#        # Also show HG^T = 0 briefly (conceptual)
#        hg_tex = MathTex(r"HG^\top=0", font_size=44).next_to(params, DOWN, buff=0.5)
#        self.play(FadeIn(hg_tex, shift=0.2*DOWN), run_time=0.8)
#        self.wait(0.4)
#        self.play(FadeOut(hg_tex), run_time=0.4)
#
#        # ------------------------------------------------------------
#        # 3) Visualize columns of H as points in F2^3 (cube)
#        # ------------------------------------------------------------
#        self.play(FadeOut(enc_box), FadeOut(ker_box), run_time=0.5)
#        self.play(bullets[0].animate.set_opacity(1.0), run_time=0.5)
#
#        cube_title = Tex(r"Columns of $H$ live in $\mathbb{F}_2^3$", font_size=40)
#        cube_title.to_edge(UP).shift(0.2*DOWN)
#        self.play(Transform(title, cube_title), run_time=0.8)
#
#        # Build a small "cube" of F2^3 points in 2D with isometric-ish projection
#        # Map (x,y,z) in {0,1}^3 to a point in the plane
#        def proj(p):
#            x, y, z = p
#            return np.array([1.3*x + 0.8*y, 0.9*y + 1.1*z, 0.0])
#
#        points = {}
#        dots = VGroup()
#        labels = VGroup()
#        for x in [0,1]:
#            for y in [0,1]:
#                for z in [0,1]:
#                    pos = proj((x,y,z)) + 2.2*LEFT + 0.4*UP
#                    d = Dot(pos, radius=0.06)
#                    if (x,y,z) == (0,0,0):
#                        d.set_opacity(0.25)
#                    else:
#                        d.set_opacity(0.9)
#                    t = Tex(rowbits_tex([x,y,z]), font_size=26).next_to(d, RIGHT, buff=0.12)
#                    points[(x,y,z)] = d
#                    dots.add(d)
#                    labels.add(t)
#
#        cube_frame = VGroup(dots, labels)
#        self.play(FadeIn(cube_frame, lag_ratio=0.05), run_time=1.0)
#
#        # Create 7 column-vectors and place them on the cube points
#        col_group = VGroup()
#        col_tags = VGroup()
#        for j in range(7):
#            hj = col(H, j)  # 3-bit column
#            v = MathTex(bits_tex(hj), font_size=34)
#            v.move_to(2.9*RIGHT + (1.6 - 0.45*j)*UP)
#            tag = Tex(fr"col {j+1}", font_size=24).next_to(v, LEFT, buff=0.25)
#            col_group.add(v)
#            col_tags.add(tag)
#
#        self.play(FadeIn(col_group, shift=0.2*RIGHT), FadeIn(col_tags, shift=0.2*RIGHT), run_time=1.0)
#
#        # Animate: send each column-vector to its dot (stylized “matching”)
#        movers = []
#        for j in range(7):
#            hj = col(H, j)
#            key = (hj[0], hj[1], hj[2])
#            target_dot = points[key]
#            movers.append(TransformFromCopy(col_group[j], target_dot.copy().set_opacity(1.0)))
#
#        self.play(LaggedStart(*movers, lag_ratio=0.08), run_time=1.4)
#        self.wait(0.3)
#
#        # ------------------------------------------------------------
#        # 4) Syndrome decoding: y = c + e_j, s(y)=H e_j^T = column j
#        # ------------------------------------------------------------
#        # Choose an error position j (1..7)
#        j_err = 4  # 5th bit flips (0-indexed)
#        e = [0]*7
#        e[j_err] = 1
#        y = f2_add(c, e)
#        s_y = mat_vec_mul_f2(H, y)   # = H(c+e)^T = Hc^T + He^T = He^T
#
#        # Clean some previous algebra displays
#        self.play(FadeOut(sc_group), run_time=0.4)
#
#        # Put the decoding equations center stage
#        eq1 = MathTex(r"y=c+e_j", font_size=44).to_edge(UP).shift(1.0*DOWN)
#        eq2 = MathTex(r"s(y)=Hy^\top", font_size=44).next_to(eq1, DOWN, buff=0.35)
#        eq3 = MathTex(r"=H(c+e_j)^\top = Hc^\top + He_j^\top", font_size=42).next_to(eq2, DOWN, buff=0.25)
#        eq4 = MathTex(r"=0+He_j^\top = He_j^\top", font_size=44).next_to(eq3, DOWN, buff=0.25)
#
#        eqs = VGroup(eq1, eq2, eq3, eq4).shift(0.3*RIGHT)
#        eqs.set_z_index(5)
#
#        self.play(Write(eq1), run_time=0.8)
#        self.play(Write(eq2), run_time=0.8)
#        self.play(Write(eq3), run_time=1.1)
#        self.play(Write(eq4), run_time=0.9)
#        self.wait(0.4)
#
#        # Show concrete vectors (u, c, e, y, syndrome)
#        concrete = VGroup(
#            MathTex(r"u=", bits_tex(u), font_size=36),
#            MathTex(r"c=", bits_tex(c), font_size=36),
#            MathTex(r"e_j=", bits_tex(e), font_size=36),
#            MathTex(r"y=", bits_tex(y), font_size=36),
#            MathTex(r"s(y)=", bits_tex(s_y), font_size=36),
#        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
#        concrete.to_edge(LEFT).shift(0.4*DOWN)
#
#        panel = RoundedRectangle(corner_radius=0.2, height=3.3, width=4.4)
#        panel.set_stroke(opacity=0.35)
#        panel.set_fill(opacity=0.06)
#        panel.move_to(concrete.get_center()).shift(0.05*RIGHT)
#
#        self.play(FadeIn(panel), FadeIn(concrete, shift=0.2*LEFT), run_time=1.0)
#
#        # Highlight: syndrome equals column j
#        synd = s_y
#        hj = col(H, j_err)
#
#        match_tex = MathTex(
#            r"s(y)=He_j^\top = \text{col }" + str(j_err+1),
#            r"=",
#            bits_tex(hj),
#            font_size=44
#        ).to_edge(RIGHT).shift(0.2*UP)
#
#        self.play(FadeIn(match_tex, shift=0.2*RIGHT), run_time=0.9)
#
#        # Visual match on cube: highlight the dot corresponding to syndrome/column
#        key = (hj[0], hj[1], hj[2])
#        target_dot = points[key]
#        ring = Circle(radius=0.16).move_to(target_dot.get_center())
#        ring.set_stroke(width=6)
#        ring.set_color(YELLOW)
#
#        self.play(Create(ring), target_dot.animate.scale(1.4).set_opacity(1.0), run_time=0.7)
#
#        # Also highlight the actual column object in the list
#        self.play(
#            col_group[j_err].animate.set_color(YELLOW),
#            col_tags[j_err].animate.set_color(YELLOW),
#            run_time=0.5
#        )
#        self.wait(0.4)
#
#        # ------------------------------------------------------------
#        # 5) Show the “lookup table” idea (syndrome -> position)
#        # ------------------------------------------------------------
#        # Build a small table: columns of H labeled 1..7
#        rows = []
#        for j in range(7):
#            # Make BOTH columns valid MathTex strings
#            rows.append([rf"\text{{{j+1}}}", bits_tex(col(H, j))])
#
#        table = Table(
#            rows,
#            col_labels=[Tex("bit"), Tex("syndrome (= column)")],
#            include_outer_lines=True,
#            line_config={"stroke_opacity": 0.35},
#            element_to_mobject=MathTex,   # <-- IMPORTANT: MathTex, not Tex
#        ).scale(0.45)
#        table.to_edge(DOWN).shift(0.1*UP)
#
#        self.play(FadeIn(table, shift=0.25*UP), run_time=1.0)
#
#        # Highlight row for j_err+1
#        # (Manim Table indexing: (row, col), with row 1 being first data row)
#        cell_bit = table.get_cell((j_err+2, 1))  # +1 for header row, +1 because table rows start at 1
#        cell_syn = table.get_cell((j_err+2, 2))
#        hl1 = SurroundingRectangle(cell_bit, buff=0.05, color=YELLOW)
#        hl2 = SurroundingRectangle(cell_syn, buff=0.05, color=YELLOW)
#
#        self.play(Create(hl1), Create(hl2), run_time=0.7)
#
#        closing = Tex(
#            r"Single-bit error correction: identify $j$ from $s(y)$, then flip bit $j$",
#            font_size=36
#        ).to_edge(DOWN).shift(0.6*UP)
#
#        self.play(Write(closing), run_time=1.0)
#        self.wait(1.2)
#
#        # Gentle outro fade
#        self.play(
#            FadeOut(VGroup(panel, concrete, match_tex, ring, hl1, hl2, closing)),
#            run_time=1.0
#        )
#        self.play(FadeOut(table), run_time=0.6)
#        self.wait(0.2)
