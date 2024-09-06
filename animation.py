from manim import *

class NeuralNetworkLSTM(ThreeDScene):
    def construct(self):
        # Title
        title = Text("Keystroke Dynamics LSTM Model", font_size=48).to_edge(UP)
        self.play(Write(title))
        
        # Input layer representation
        input_text = Text("Input Layer (Features)", font_size=24).shift(LEFT * 4)
        input_circle = Circle(radius=0.5, color=BLUE).shift(LEFT * 4)
        self.play(Write(input_text), Create(input_circle))
        
        # Arrow to LSTM layer 1
        arrow_1 = Arrow(start=LEFT * 3, end=LEFT, buff=0.1)
        self.play(Create(arrow_1))
        
        # First LSTM layer
        lstm_1_text = Text("LSTM Layer 1", font_size=24).shift(LEFT * 1.5)
        lstm_1_square = Square(side_length=1.0, color=GREEN).shift(LEFT * 1.5)
        self.play(Write(lstm_1_text), Create(lstm_1_square))
        
        # Arrow to LSTM layer 2
        arrow_2 = Arrow(start=LEFT * 0.5, end=RIGHT * 1, buff=0.1)
        self.play(Create(arrow_2))
        
        # Second LSTM layer
        lstm_2_text = Text("LSTM Layer 2", font_size=24).shift(RIGHT * 1.5)
        lstm_2_square = Square(side_length=1.0, color=GREEN).shift(RIGHT * 1.5)
        self.play(Write(lstm_2_text), Create(lstm_2_square))
        
        # Arrow to Dense Layer
        arrow_3 = Arrow(start=RIGHT * 2, end=RIGHT * 4, buff=0.1)
        self.play(Create(arrow_3))
        
        # Dense Layer
        dense_text = Text("Dense Layer", font_size=24).shift(RIGHT * 4.5)
        dense_square = Square(side_length=1.0, color=YELLOW).shift(RIGHT * 4.5)
        self.play(Write(dense_text), Create(dense_square))
        
        # Arrow to Output Layer
        arrow_4 = Arrow(start=RIGHT * 5.5, end=RIGHT * 7, buff=0.1)
        self.play(Create(arrow_4))
        
        # Output Layer
        output_text = Text("Output Layer", font_size=24).shift(RIGHT * 7.5)
        output_circle = Circle(radius=0.5, color=RED).shift(RIGHT * 7.5)
        self.play(Write(output_text), Create(output_circle))
        
        # Animation showing data flow through the network
        for _ in range(3):
            data_dot = Dot(color=WHITE).move_to(input_circle.get_center())
            self.play(data_dot.animate.move_to(lstm_1_square.get_center()), run_time=1)
            self.play(data_dot.animate.move_to(lstm_2_square.get_center()), run_time=1)
            self.play(data_dot.animate.move_to(dense_square.get_center()), run_time=1)
            self.play(data_dot.animate.move_to(output_circle.get_center()), run_time=1)
            self.play(FadeOut(data_dot))
        
        # Display accuracy text
        accuracy_text = Text("Model Accuracy: 85%", font_size=36).shift(DOWN * 2)
        self.play(Write(accuracy_text))
        
        self.wait(3)

