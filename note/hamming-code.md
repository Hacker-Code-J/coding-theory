 ---
    Hamming Codes via Algebraic Geometry

    1. Hamming Code as a Reed-Solomon / Algebraic Code

    The Hamming $[7,4,3]_2$ code is the simplest instance of a cyclic code over $\mathbb{F}_2$. Its generator polynomial
    divides $x^7 - 1$ over $\mathbb{F}2$, and the roots live in $\mathbb{F}{2^3}$ (the splitting field). This already puts it
    in the world of algebraic curves over finite fields — specifically the simplest one: the projective line $\mathbb{P}^1$.

    ---
    2. The Parity-Check Matrix = Points of Projective Space

    The columns of $H$ are all nonzero vectors in $\mathbb{F}_2^3$, i.e., all points of $\mathbb{P}^2(\mathbb{F}_2)$:

    $$\text{columns of } H \longleftrightarrow \mathbb{P}^2(\mathbb{F}_2) \setminus {} = 7 \text{ points}$$

    The Hamming code is the dual distance-3 code whose parity checks correspond exactly to these 7 projective points. This is
    the first non-trivial projective geometry code.

    More generally, the $r$-th order Hamming code has parity-check matrix whose columns are all points of
    $\mathbb{P}^{r-1}(\mathbb{F}_q)$.

    ---
    3. Algebraic-Geometric (AG) Codes — Goppa's Construction

    In 1981, Goppa generalized this dramatically. Given:
    - A smooth projective curve $\mathcal{X}$ over $\mathbb{F}_q$
    - A set of rational points $P_1, \ldots, P_n \in \mathcal{X}(\mathbb{F}_q)$
    - A divisor $G$ on $\mathcal{X}$

    define the AG code:
    $$C(\mathcal{X}, G, D) = { (f(P_1), \ldots, f(P_n)) \mid f \in \mathcal{L}(G) }$$

    where $\mathcal{L}(G)$ is the Riemann-Roch space of rational functions with poles bounded by $G$.

    The Riemann-Roch theorem gives:
    $$k = \deg G - g + 1, \quad d \geq n - \deg G$$

    where $g$ is the genus of the curve. Hamming codes arise from $g = 0$ (the projective line $\mathbb{P}^1$), which has the
    most points relative to its genus.

    ---
    4. The Hasse-Weil Bound and Why Curves Matter

    The number of $\mathbb{F}_q$-rational points on a curve of genus $g$ satisfies:
    $$|, |\mathcal{X}(\mathbb{F}_q)| - q - 1 ,| \leq 2g\sqrt{q}$$

    More points $\Rightarrow$ longer codes with better parameters. Shimura curves, Hermitian curves, and Garcia-Stichtenoth
    towers are used to build asymptotically good codes that beat the Gilbert-Varshamov bound — something impossible with
    classical constructions.

    ---
    5. The Syndrome = Cohomology

    The syndrome $s(y) = Hy^\top$ can be interpreted as a coboundary map in a short exact sequence of $\mathbb{F}_2$-vector
    spaces:

    $$0 \to C \to \mathbb{F}_2^7 \xrightarrow{H} \mathbb{F}_2^3 \to 0$$

    This is precisely $H^0$ of a sheaf on $\mathbb{P}^2(\mathbb{F}_2)$. The cosets of $C$ (the 8 syndromes) are elements of
    $H^1$ in the associated cohomology — a shadow of Serre duality.

    ---
    Summary Table

    ┌─────────────────────┬──────────────────────────────────────────────┐
    │    Coding Theory    │              Algebraic Geometry              │
    ├─────────────────────┼──────────────────────────────────────────────┤
    │ Codeword length $n$ │ Number of $\mathbb{F}_q$-points              │
    ├─────────────────────┼──────────────────────────────────────────────┤
    │ Dimension $k$       │ $\dim \mathcal{L}(G)$ via Riemann-Roch       │
    ├─────────────────────┼──────────────────────────────────────────────┤
    │ Min distance $d$    │ $n - \deg G$ (geometric bound)               │
    ├─────────────────────┼──────────────────────────────────────────────┤
    │ Parity-check matrix │ Points of $\mathbb{P}^{r-1}(\mathbb{F}_q)$   │
    ├─────────────────────┼──────────────────────────────────────────────┤
    │ Syndrome            │ Cohomology class in $H^1$                    │
    ├─────────────────────┼──────────────────────────────────────────────┤
    │ Dual code           │ Residue code via differentials $\Omega(G-D)$ │
    └─────────────────────┴──────────────────────────────────────────────┘

    ---
    The Hamming code is, in this sense, the genus-0 case of a vast theory connecting curves, function fields, and error
    correction — with the full power of algebraic geometry (Riemann-Roch, étale cohomology, moduli spaces) available for
    constructing better and better codes.
