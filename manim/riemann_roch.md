  riemann_roch.py — 8-scene Riemann-Roch animation                                                                            
                                                                                                                              
  ┌─────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │      Scene      │                                               Content                                                │  
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤  
  │ S1_Title        │ Title card · the full formula appears as a "promise"                                                 │
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ S2_Surfaces     │ Genus-0/1/2 surface schematics · Euler characteristic χ = 2−2g                                       │  
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤  
  │ S3_Divisors     │ Smooth oval curve X · 4 marked points with integer coefficients · formal sum D · deg(D) · pole vs.   │  
  │                 │ zero meaning                                                                                         │  
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ S4_SpaceLD      │ Definition of L(D) · the condition div(f)+D ≥ 0 · ℓ(D) = dim L(D) · basis {1,z,…,zⁿ} on ℙ¹ · ℓ(D)=0  │  
  │                 │ for deg<0                                                                                            │  
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ S5_Canonical    │ K_X = div(ω) · deg(K) = 2g−2 · table for g=0,1,2                                                     │  
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤  
  │ S6_Examples     │ g=0 full verification · g=1 table of ℓ(nP) for n=0..3 with Weierstrass basis {1,℘,℘′}                │
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤  
  │ S7_Theorem      │ Formula built term by term · theorem box · colour-coded annotations · Serre duality                  │
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤  
  │ S8_Consequences │ 4 corollaries: Riemann's inequality · ℓ(K)=g · g=0⟹ℙ¹ · elliptic embedding into ℙ²                   │
  ├─────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────┤  
  │ RiemannRochFull │ All 8 acts chained in one video                                                                      │
  └─────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────┘  
                  
  Render commands:                                                                                                            
  manim -pqh riemann_roch.py RiemannRochFull    # full HD video
  manim -pql riemann_roch.py S7_Theorem         # just the theorem reveal
  manim -pql riemann_roch.py S6_Examples        # just the examples 
