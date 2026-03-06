# manim -pql hamming.py HammingCode
# manim -pql hamming.py EncodingProcess
# manim -pql hamming.py HammingMaster

from manim import *

class HammingMaster(MovingCameraScene):
    def construct(self):
        # ---------------------------------------------------------
        # SETTING UP OUR CANVAS COORDINATES
        # ---------------------------------------------------------
        POS_INTRO = ORIGIN
        POS_ENC = RIGHT * 15
        POS_CHAN = RIGHT * 15 + DOWN * 10
        POS_DEC = DOWN * 10

        # ---------------------------------------------------------
        # PART 1: THE THEORY (Center)
        # ---------------------------------------------------------
        title = Title("The Life of a Linear Block Code").move_to(POS_INTRO + UP * 3)
        
        view1 = MathTex(r"\text{1. Subset: } C \subseteq \mathbb{F}_2^n").move_to(POS_INTRO + UP * 1)
        view2 = MathTex(r"\text{2. Image: } C = \{ xG \mid x \in \mathbb{F}_2^k \}").move_to(POS_INTRO)
        view3 = MathTex(r"\text{3. Kernel: } C = \ker(H) = \{ y \in \mathbb{F}_2^n \mid Hy^\top = 0 \}").move_to(POS_INTRO + DOWN * 1)

        self.play(Write(title))
        self.play(FadeIn(view1, shift=UP))
        self.play(FadeIn(view2, shift=UP))
        self.play(FadeIn(view3, shift=UP))
        self.wait(2)

        # Highlight the Encoding and Decoding definitions before moving
        self.play(view2.animate.set_color(BLUE), view3.animate.set_color(YELLOW))
        self.wait(1)

        # ---------------------------------------------------------
        # PART 2: ENCODING (Pan Right)
        # ---------------------------------------------------------
        # Smoothly pan the camera to the encoding station
        self.play(self.camera.frame.animate.move_to(POS_ENC), run_time=2)

        enc_title = Text("Step 1: Encoding (c = xG)", color=BLUE).move_to(POS_ENC + UP * 3)
        self.play(Write(enc_title))

        x_matrix = Matrix([[1, 0, 1, 1]]).scale(0.8).move_to(POS_ENC + LEFT * 3.5)
        
        G_matrix = Matrix([
            [1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1]
        ]).scale(0.7).next_to(x_matrix, RIGHT)

        self.play(Write(x_matrix), Write(G_matrix))
        self.wait(1)

        # Highlight rows based on the message vector
        x_entries = x_matrix.get_entries()
        g_rows = G_matrix.get_rows()
        active_indices = [0, 2, 3] # Indices where x has a '1'
        
        self.play(
            *[x_entries[i].animate.set_color(BLUE) for i in active_indices],
            *[g_rows[i].animate.set_color(BLUE) for i in active_indices],
            run_time=1.5
        )
        self.wait(1)

        equals_enc = MathTex("=").next_to(G_matrix, RIGHT)
        c_matrix = Matrix([[1, 0, 1, 1, 0, 1, 0]]).scale(0.7).next_to(equals_enc, RIGHT)
        c_matrix.get_entries().set_color(BLUE)

        self.play(Write(equals_enc), Write(c_matrix))
        self.wait(2)

        # ---------------------------------------------------------
        # PART 3: THE CHANNEL ERROR (Pan Down)
        # ---------------------------------------------------------
        self.play(self.camera.frame.animate.move_to(POS_CHAN), run_time=2)

        chan_title = Text("Step 2: The Noisy Channel", color=RED).move_to(POS_CHAN + UP * 3)
        self.play(Write(chan_title))

        # Show c + e = y
        c_copy = c_matrix.copy().move_to(POS_CHAN + LEFT * 4)
        plus = MathTex("+").next_to(c_copy, RIGHT)
        
        # Error vector (error at position 3)
        e_matrix = Matrix([[0, 0, 1, 0, 0, 0, 0]]).scale(0.7).next_to(plus, RIGHT)
        e_matrix.get_entries()[2].set_color(RED) # Highlight the flipped bit
        
        equals_chan = MathTex("=").next_to(e_matrix, RIGHT)
        
        # Received vector y
        y_matrix = Matrix([[1, 0, 0, 1, 0, 1, 0]]).scale(0.7).next_to(equals_chan, RIGHT)
        y_matrix.get_entries()[2].set_color(RED)

        self.play(FadeIn(c_copy, shift=DOWN))
        self.play(Write(plus), Write(e_matrix))
        self.wait(1)
        self.play(Write(equals_chan), Write(y_matrix))
        self.wait(2)

        # ---------------------------------------------------------
        # PART 4: DECODING (Pan Left)
        # ---------------------------------------------------------
        self.play(self.camera.frame.animate.move_to(POS_DEC), run_time=2)

        dec_title = Text("Step 3: Syndrome Decoding", color=YELLOW).move_to(POS_DEC + UP * 3)
        syndrome_math = MathTex(r"s(y) = H y^\top = H(c+e)^\top = He^\top").move_to(POS_DEC + UP * 2)
        
        self.play(Write(dec_title))
        self.play(Write(syndrome_math))
        self.wait(1)

        H_matrix = Matrix([
            [0, 1, 1, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1]
        ]).scale(0.7).move_to(POS_DEC + LEFT * 2)

        # y transposed (column vector)
        y_col = Matrix([[1], [0], [0], [1], [0], [1], [0]]).scale(0.6).next_to(H_matrix, RIGHT)
        y_col.get_entries()[2].set_color(RED)

        self.play(Write(H_matrix), Write(y_col))
        self.wait(1)

        equals_dec = MathTex("=").next_to(y_col, RIGHT)
        
        # The resulting syndrome
        s_matrix = Matrix([[1], [1], [0]]).scale(0.7).next_to(equals_dec, RIGHT)
        s_matrix.get_entries().set_color(YELLOW)

        self.play(Write(equals_dec), Write(s_matrix))
        self.wait(1)

        # The AHA Moment: Match syndrome to the 3rd column of H
        h_columns = H_matrix.get_columns()
        self.play(
            h_columns[2].animate.set_color(YELLOW),
            Indicate(s_matrix, color=YELLOW, scale_factor=1.2),
            run_time=2
        )

        conclusion = Text("Syndrome matches Column 3. Error found!", color=YELLOW, font_size=30).move_to(POS_DEC + DOWN * 2.5)
        self.play(Write(conclusion))
        self.wait(3)

        # Final zoom out to show the whole journey
        self.play(
            self.camera.frame.animate.move_to(RIGHT * 7.5 + DOWN * 5).set(width=35),
            run_time=4
        )
        self.wait(3)
