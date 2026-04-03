Summary of the animation (hamming_animation.py):                                                                            
                                                                                                                              
  ┌───────────────────┬────────────────────────────────────────────────────────────────────────┐                              
  │    Scene class    │                                Content                                 │                              
  ├───────────────────┼────────────────────────────────────────────────────────────────────────┤                              
  │ S1_Title          │ Title card                                                             │
  ├───────────────────┼────────────────────────────────────────────────────────────────────────┤                              
  │ S2_NoisyChannel   │ Alice → Bob, bit gets flipped by noise                                 │
  ├───────────────────┼────────────────────────────────────────────────────────────────────────┤                              
  │ S3_Positions      │ 7 slots, powers-of-2 = parity, rest = data; binary addresses shown     │
  ├───────────────────┼────────────────────────────────────────────────────────────────────────┤                              
  │ S4_Matrix         │ Parity-check matrix H, syndrome definition, key property               │
  ├───────────────────┼────────────────────────────────────────────────────────────────────────┤                              
  │ S5_DecodePipeline │ Full encode → corrupt → syndrome → correct pipeline with bit registers │
  ├───────────────────┼────────────────────────────────────────────────────────────────────────┤                              
  │ S6_CubeFinale     │ F₂³ cube, 7 nonzero vertices ↔ 7 bit positions, coset structure        │
  ├───────────────────┼────────────────────────────────────────────────────────────────────────┤                              
  │ HammingFull       │ All acts chained into one video                                        │
  └───────────────────┴────────────────────────────────────────────────────────────────────────┘                              
                  
  Render commands:                                                                                                            
  # Full video (recommended)
  manim -pqh hamming_animation.py HammingFull
                                                                                                                              
  # Individual scenes
  manim -pql hamming_animation.py S5_DecodePipeline  
