from manim import *

class GoBoard(VGroup):
    def __init__(self, black = [], white = [], showpdist = False, pdist = [], **kwargs):
        if showpdist:
            dist = [[.001 for _ in range(9)] for _ in range(9)]
            for x, y, p in pdist:
                dist[x][y] = p
            super().__init__(Square(color=LIGHT_BROWN, stroke_width=0.9), 
                    *[Line(np.array([-1, 0.225*i, 0]), np.array([1, 0.225*i, 0]), color=LIGHT_BROWN, stroke_width=1.2) for i in range(-4, 5)],
                    *[Line(np.array([0.225*i, -1, 0]), np.array([0.225*i, 1, 0]), color=LIGHT_BROWN, stroke_width=1.2) for i in range(-4, 5)],
                    *[Circle(radius=0.1, color=WHITE, fill_color=BLACK, fill_opacity=1, stroke_width=0.5).move_to(np.array([0.225*x, 0.225*y, 0])) for x, y in black],
                    *[Circle(radius=0.1, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0.5).move_to(np.array([0.225*x, 0.225*y, 0])) for x, y in white],
                    *[DecimalNumber(dist[x][y], color=PINK, font_size=dist[x][y]*6+6).move_to(np.array([0.225*(x-4), 0.225*(y-4), 0])) for x in range(9) for y in range(9)] if showpdist else Mobject(),
                    **kwargs)
        else:
            super().__init__(Square(color=LIGHT_BROWN, stroke_width=0.9), 
                    *[Line(np.array([-1, 0.225*i, 0]), np.array([1, 0.225*i, 0]), color=LIGHT_BROWN, stroke_width=1.2) for i in range(-4, 5)],
                    *[Line(np.array([0.225*i, -1, 0]), np.array([0.225*i, 1, 0]), color=LIGHT_BROWN, stroke_width=1.2) for i in range(-4, 5)],
                    *[Circle(radius=0.1, color=WHITE, fill_color=BLACK, fill_opacity=1, stroke_width=0.5).move_to(np.array([0.225*x, 0.225*y, 0])) for x, y in black],
                    *[Circle(radius=0.1, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0.5).move_to(np.array([0.225*x, 0.225*y, 0])) for x, y in white],
                    **kwargs)
        
class ExplainNNs(Scene):
    def construct(self):

        topic = Text("The Base AlphaZero MCTS Algorithm").scale(1)

        self.play(Write(topic))
        self.wait(0.5)
        self.play(Unwrite(topic))

        header = Text("The First Building Block: Neural Networks").scale(1.2)

        self.play(Write(header))
        self.play(header.animate.move_to(UP * 3).scale(0.7))

        pnet = MarkupText(f'<span fgcolor="{PINK}">P</span>olicy Net').move_to(np.array(UP * 2))
        ptype = MarkupText(f'<span fgcolor="{PINK}">A probability distribution</span> of how good a move is in a certain position').scale(0.5).next_to(pnet, DOWN)
        
        self.play(Write(pnet))
        self.play(Write(ptype))

        pdesc = BulletedList("Doesn't have to be too accurate", "Meant to sort out the definitely bad moves from the possibly good moves", height=10, width=10).scale(0.8).next_to(ptype, DOWN)
        self.play(Write(pdesc))

        board = GoBoard(black=[(0, 0)], white=[(-2, 1)], showpdist=True, pdist=[(2, 3, 0.61), (3, 6, 0.25), (4, 6, 0.11)]).scale(1.8).move_to(DOWN * 1.8)

        self.play(*[Create(obj) for obj in board], run_time=3)

        self.wait(1)

        self.play(Unwrite(pdesc), Unwrite(ptype), Unwrite(pnet), *[Uncreate(obj) for obj in board])
        
        vnet = MarkupText(f'<span fgcolor="{GREEN}">V</span>alue Net').move_to(UP*2)
        vtype = MarkupText(f'<span fgcolor="{GREEN}">A value from 0 to 1</span> of how good a position is for a player').scale(0.5).next_to(vnet, DOWN)

        
        self.play(Write(vnet))
        self.play(Write(vtype))

        left_board = GoBoard(black=[(-4, -4), (-4, 2), (-4, 4), (-3, -3), (-3, 1), (-2, -4), (-2, -2), (-2, 2), (-1, -3), (-1, 0), (0, -4), (0, -3), (0, 1), (1, -4), (1, -2), (2, -3), (2, -2), (2, 0), (3, -4), (3, 0), (4, -4), (4, 4)], 
                             white=[(-4, -2), (-4, 0), (-3, -1), (-2, -3), (-2, 0), (-1, -4), (0, -1), (1, 1), (2, 2), (3, -1)]
                             ).scale(1.8).move_to(DOWN * 1.8 + LEFT * 3)
        left_value = DecimalNumber(0.78, color=GREEN, font_size=30).next_to(left_board, UP)
        self.play(*[Create(obj) for obj in left_board], Write(left_value), run_time=3)

        right_board = GoBoard(
            black=[(-4, 4), (-3, -1), (-3, 3), (-3, 4), (-2, -1), (-2, 3), (-2, 4), (-1, -2), (-1, -1), (0, -3), (1, -2), (2, -1), (3, -2), (3, -1), (3, 2), (4, -4), (4, -3)], 
            white=[(-4, -4), (-4, -2), (-4, 2), (-3, -4), (-3, -3), (-2, -3), (-1, -4), (-1, -3), (-1, 0), (0, -2), (0, -1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]
            ).scale(1.8).move_to(DOWN * 1.8 + RIGHT * 3)
        right_value = DecimalNumber(0.21, color=GREEN, font_size=30).next_to(right_board, UP)
        self.play(*[Create(obj) for obj in right_board], Write(right_value), run_time=3)
        self.wait(1)

        self.play(Unwrite(left_value), Unwrite(right_value), Unwrite(vtype), Unwrite(vnet), *[Uncreate(obj) for obj in left_board], *[Uncreate(obj) for obj in right_board], Unwrite(header))

class ExplainMCTS(Scene):
    def construct(self):
        header = Text("The Next Piece: Monte Carlo Tree Search").scale(1.2)

        self.play(Write(header))
        self.play(header.animate.move_to(UP * 3).scale(0.7))
        self.wait(0.5)

        title = Text("The Game Tree").move_to(UP * 2)

        root = Circle(radius=0.4, color=WHITE).next_to(title, DOWN*2)
        left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(root, 2*DOWN + 6*LEFT)
        middle_child = Circle(radius=0.4, color=DARK_GRAY).next_to(root, 2*DOWN)
        right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(root, 2*DOWN + 6*RIGHT)
        left_action = Line(root.get_bottom(), left_child.get_top(), color=DARK_GRAY)
        middle_action = Line(root.get_bottom(), middle_child.get_top(), color=DARK_GRAY)
        right_action = Line(root.get_bottom(), right_child.get_top(), color=DARK_GRAY)

        self.play(Write(title), Create(root), Create(left_child), Create(middle_child), Create(right_child), Create(left_action), Create(middle_action), Create(right_action))

        rootlabel = Text("Root Node", color=WHITE, font_size=17).next_to(root, LEFT)
        self.play(Write(rootlabel))


        rootboard = GoBoard(black=[(0, 0)], white=[(-2, 1)]).scale(0.4).next_to(root, RIGHT)
        leftboard = GoBoard(black=[(0, 0), (-2, -1)], white=[(-2, 1)]).scale(0.4).next_to(left_child, RIGHT) #27%
        middleboard = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1)]).scale(0.4).next_to(middle_child, RIGHT) #42%
        rightboard = GoBoard(black=[(0, 0), (-2, 0)], white=[(-2, 1)]).scale(0.4).next_to(right_child, RIGHT) #12%
        self.play(*[Create(obj) for obj in [rootboard, leftboard, middleboard, rightboard]], run_time=3)

        gametree = VGroup(title, root, left_child, middle_child, right_child, left_action, middle_action, right_action, rootlabel, rootboard, leftboard, middleboard, rightboard)
        self.play(gametree.animate.shift(LEFT * 4), Unwrite(title))

        uctscore = Text("UCT Score", font_size=50).move_to(UP * 2 + RIGHT * 4)
        context = Text("Next move is determined by").scale(0.5).next_to(uctscore, LEFT)
        self.play(Write(uctscore), Write(context))
        q_arrow = Arrow(uctscore.get_bottom(), uctscore.get_bottom() + DOWN + LEFT * 1, buff=0.1)
        u_arrow = Arrow(uctscore.get_bottom(), uctscore.get_bottom() + DOWN + RIGHT * 1, buff=0.1)
        q_text = Text("Q", font_size=40).next_to(q_arrow.get_end(), DOWN)
        u_text = Text("U", font_size=40).next_to(u_arrow.get_end(), DOWN)

        self.play(Create(q_arrow), Write(q_text), Unwrite(context))

        q_formula = MathTex(r"Q(s, a) = \frac{W(s, a)}{N(s, a)}").next_to(uctscore, DOWN * 8).scale(0.7)
        w_desc = MarkupText(f"<span fgcolor='{GREEN}'>W</span> - Sum of all evaluations (here's where the value net is used)", font_size=15).next_to(q_formula, DOWN)
        n_desc = Text("N - Number of evaluations (number of node visits)", font_size=15).next_to(w_desc, DOWN)
        q_desc = Text("Basically, a running average of how good MCTS has found this state to be", font_size=15).next_to(n_desc, DOWN)
        self.play(Write(q_formula))
        self.play(Write(w_desc), Write(n_desc), Write(q_desc))
        self.wait(2)

        uct_left = Tex(r"$\frac{0}{0} + $", font_size=24).move_to(left_child)
        uct_middle = Tex(r"$\frac{0}{0} + $", font_size=24).move_to(middle_child)
        uct_right = Tex(r"$\frac{0}{0} + $", font_size=24).move_to(right_child)
        self.play(Write(uct_left), Write(uct_middle), Write(uct_right), Unwrite(q_formula), Unwrite(w_desc), Unwrite(n_desc), Unwrite(q_desc))

        self.play(Create(u_arrow), Write(u_text))

        u_formula = MathTex(r"U(s, a) = C \cdot P(s, a) \cdot \frac{\sqrt{N(s)}}{1 + N(s, a)}").next_to(uctscore, DOWN * 8).scale(0.7)
        c_desc = Text("C - Exploration Function (increases very slowly with simulations)", font_size=15).next_to(u_formula, DOWN)
        p_desc = MarkupText(f"<span fgcolor='{PINK}'>P</span> - Initial probability (here's where the policy net is used)", font_size=15).next_to(c_desc, DOWN)
        n1_desc = Text("N(s) - Number of times the parent node has been visited", font_size=15).next_to(p_desc, DOWN)
        u_desc1 = Text("Basically, how much potential does this state have?", font_size=15).next_to(n1_desc, DOWN)
        u_desc2 = Text("The rightmost term helps out nodes less explored than its siblings", font_size=15).next_to(u_desc1, DOWN)

        self.play(Write(u_formula))
        self.play(Write(c_desc), Write(p_desc), Write(n1_desc), Write(u_desc1), Write(u_desc2))
        self.wait(2)

        self.play(Unwrite(u_formula), Unwrite(c_desc), Unwrite(p_desc), Unwrite(n1_desc), Unwrite(u_desc1), Unwrite(u_desc2))

        k_formula = MathTex(r"k = C \cdot \sqrt{\frac{N(s)}{1 + N(s, a)}}").next_to(uctscore, DOWN * 8).scale(0.7)
        self.play(Write(k_formula))
        self.play(k_formula.animate.next_to(header, DOWN).scale(0.5),
                  uct_left.animate.become(Tex(r"$\frac{0}{0} + k \cdot 0.27$", font_size=15).move_to(uct_left)),
                  uct_middle.animate.become(Tex(r"$\frac{0}{0} + k \cdot 0.42$", font_size=15).move_to(uct_middle)),
                    uct_right.animate.become(Tex(r"$\frac{0}{0} + k \cdot 0.12$", font_size=15).move_to(uct_right)),)

        left_action_prob = DecimalNumber(0.34, color=YELLOW, font_size=20).move_to(left_action.get_center())
        middle_action_prob = DecimalNumber(0.53, color=YELLOW, font_size=20).move_to(middle_action.get_center())
        right_action_prob = DecimalNumber(0.15, color=YELLOW, font_size=20).move_to(right_action.get_center())

        self.play(Write(left_action_prob), Write(middle_action_prob), Write(right_action_prob))

        self.play(Unwrite(uctscore), Uncreate(q_arrow), Uncreate(u_arrow), Unwrite(q_text), Unwrite(u_text))

        desc = Text("Select a leaf node to expand via UCT score").scale(0.5).move_to(UP * 1 + RIGHT * 4)

        self.play(middle_action.animate.set_color(WHITE), middle_child.animate.set_color(WHITE), Write(desc))

        new_left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(middle_child, 2*DOWN + 6*LEFT)
        new_middle_child = Circle(radius=0.4, color=DARK_GRAY).next_to(middle_child, 2*DOWN)
        new_right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(middle_child, 2*DOWN + 6*RIGHT)
        new_left_action = Line(middle_child.get_bottom(), new_left_child.get_top(), color=DARK_GRAY)
        new_middle_action = Line(middle_child.get_bottom(), new_middle_child.get_top(), color=DARK_GRAY)
        new_right_action = Line(middle_child.get_bottom(), new_right_child.get_top(), color=DARK_GRAY)
        new_left_board = GoBoard(black=[(0, 0), (-2, -1)], white=[(-2, 1), (2, 0)]).scale(0.4).next_to(new_left_child, RIGHT) #16%
        new_middle_board = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1)]).scale(0.4).next_to(new_middle_child, RIGHT) #12%
        new_right_board = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1), (-2, 2)]).scale(0.4).next_to(new_right_child, RIGHT) #44%

        self.play(Create(new_left_child), Create(new_middle_child), Create(new_right_child), Create(new_left_action), Create(new_middle_action), Create(new_right_action), *[Create(obj) for obj in [new_left_board, new_middle_board, new_right_board]], Unwrite(desc))

        evaluation = Text("Evaluation", color=GREEN, font_size=50).move_to(UP * 2 + RIGHT * 4)
        self.play(Write(evaluation))

        big_middle_board = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1)]).next_to(evaluation, DOWN)
        self.play(*[Create(obj) for obj in big_middle_board])
        
        eval = DecimalNumber(0.542, color=GREEN, font_size=30).next_to(big_middle_board, DOWN)
        self.play(Write(eval))


        desc = Text("Update node parameters and UCT scores up the tree").scale(0.4).next_to(evaluation, DOWN)
        self.play(Unwrite(eval), *[Uncreate(obj) for obj in big_middle_board], evaluation.animate.become(Text("Backpropagation", color=WHITE, font_size=50).move_to(UP * 2 + RIGHT * 4)), Write(desc))

        self.play(uct_middle.animate.become(MathTex(r"\frac{0.542}{1} + k \cdot 0.42", font_size=10).move_to(uct_middle)))

        self.play(left_action_prob.animate.become(DecimalNumber(0.68, color=YELLOW, font_size=20).move_to(left_action.get_center())),
                  middle_action_prob.animate.become(DecimalNumber(0.81, color=YELLOW, font_size=20).move_to(middle_action.get_center())),
                  right_action_prob.animate.become(DecimalNumber(0.30, color=YELLOW, font_size=20).move_to(right_action.get_center())))

        self.play(evaluation.animate.become(Text("Repeat!", color=WHITE, font_size=50).move_to(UP * 2 + RIGHT * 4)), Unwrite(desc))
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        , run_time=0.5)


class ExplainMinimax(Scene):
    def construct(self):
        header = Text("The Minimax Algorithm: Upgrading the Evaluation").scale(1)
        self.play(Write(header))
        self.play(header.animate.move_to(UP * 3).scale(0.7))


        earlyboard = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1)]).scale(2).to_edge(LEFT)
        lateboard = GoBoard(
            black=[(-4, 4), (-3, -1), (-3, 3), (-3, 4), (-2, -1), (-2, 3), (-2, 4), (-1, -2), (-1, -1), (0, -3), (1, -2), (2, -1), (3, -2), (3, -1), (3, 2), (4, -4), (4, -3)], 
            white=[(-4, -4), (-4, -2), (-4, 2), (-3, -4), (-3, -3), (-2, -3), (-1, -4), (-1, -3), (-1, 0), (0, -2), (0, -1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]
            ).scale(2).to_edge(RIGHT)
        desc = Text("The later a board state, the more accurate the evaluation").scale(0.6).to_edge(DOWN, buff=0.6)
        t = Text("Minimax lets us evaluate in later states").scale(0.6).next_to(desc, DOWN)

        self.play(*[Create(obj) for obj in earlyboard])
        self.play(*[Create(obj) for obj in lateboard])
        self.play(Write(desc))
        self.play(Write(t))
        self.play(*[Uncreate(obj) for obj in earlyboard], *[Uncreate(obj) for obj in lateboard], Unwrite(desc), Unwrite(t))

        node = Circle(radius=0.4, color=WHITE).next_to(header, DOWN * 2)
        nodedesc = Text("Node we want to evaluate").scale(0.4).next_to(node, LEFT)
        self.play(Create(node), Write(nodedesc))

        left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(node, 2*DOWN + 3*LEFT)
        right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(node, 2*DOWN + 3*RIGHT)
        left_action = Line(node.get_bottom(), left_child.get_top(), color=DARK_GRAY)
        right_action = Line(node.get_bottom(), right_child.get_top(), color=DARK_GRAY)
        left_left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(left_child, 2*DOWN + 1*LEFT)
        left_right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(left_child, 2*DOWN + 1*RIGHT)
        right_left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(right_child, 2*DOWN + 1*LEFT)
        right_right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(right_child, 2*DOWN + 1*RIGHT)
        left_left_action = Line(left_child.get_bottom(), left_left_child.get_top(), color=DARK_GRAY)
        left_right_action = Line(left_child.get_bottom(), left_right_child.get_top(), color=DARK_GRAY)
        right_left_action = Line(right_child.get_bottom(), right_left_child.get_top(), color=DARK_GRAY)
        right_right_action = Line(right_child.get_bottom(), right_right_child.get_top(), color=DARK_GRAY)
        self.play(Create(left_child), Create(right_child), Create(left_action), Create(right_action), Create(left_left_child), Create(left_right_child), Create(right_left_child), Create(right_right_child), Create(left_left_action), Create(left_right_action), Create(right_left_action), Create(right_right_action))

        desc = Text("We expand the node we want to evaluate downwards, k_best moves on each level, and minimax_depth levels").scale(0.45).to_edge(DOWN, buff=1.5)
        k_best = Text("k_best = 2").scale(0.5).move_to(UP + RIGHT*4)
        minimax_depth = Text("minimax_depth = 2").scale(0.5).next_to(k_best, DOWN)
        self.play(Write(desc))
        self.play(Write(k_best), Write(minimax_depth))

        desc2 = Text("The k_best moves selected are the highest probability moves from the policy net").scale(0.45).next_to(desc, DOWN)
        self.play(Write(desc2))

        left_right_eval = DecimalNumber(0.78, color=GREEN, font_size=20).move_to(left_right_child)
        left_left_eval = DecimalNumber(0.21, color=GREEN, font_size=20).move_to(left_left_child)
        right_right_eval = DecimalNumber(0.54, color=GREEN, font_size=20).move_to(right_right_child)
        right_left_eval = DecimalNumber(0.42, color=GREEN, font_size=20).move_to(right_left_child)

        desc3 = Text("We evaluate leaf nodes using the value net").scale(0.45).next_to(desc2, DOWN)
        self.play(Write(desc3))
        self.play(Write(left_right_eval), Write(left_left_eval), Write(right_right_eval), Write(right_left_eval))
        self.play(Unwrite(desc), Unwrite(desc2), Unwrite(desc3))

        player = Text("Black's Turn").scale(0.5).next_to(node, LEFT).to_edge(LEFT)
        player2 = Text("White's Turn").scale(0.5).next_to(left_child, LEFT).to_edge(LEFT)
        self.play(Write(player), Write(player2))

        desc = Text("White seeks to minimize the value").scale(0.5).to_edge(DOWN, buff=0.6)
        self.play(Write(desc))

        left_eval = left_left_eval.copy()
        right_eval = right_left_eval.copy()
        self.add(left_eval, right_eval)
        self.play(left_eval.animate.move_to(left_child), right_eval.animate.move_to(right_child))

        
        desc2 = Text("Black seeks to maximize the value").scale(0.5).next_to(desc, DOWN)
        self.play(Write(desc2))

        node_eval = right_eval.copy()
        self.add(node_eval)
        self.play(node_eval.animate.move_to(node))

        self.play(Unwrite(desc), Unwrite(desc2))

        self.play(right_action.animate.set_color(WHITE), right_child.animate.set_color(WHITE), right_left_action.animate.set_color(WHITE), right_left_child.animate.set_color(WHITE))
        
        desc = Text("The algorithm approximates optimal play for minimax_depth moves, and evaluates at a later node, granting more accurate evaluation.").scale(0.38).to_edge(DOWN)
        self.play(Write(desc))

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        , run_time=0.5)



class Full(Scene):
    def construct(self):
        topic = Text("The Base AlphaZero MCTS Algorithm").scale(1)

        self.play(Write(topic))
        self.wait(0.5)
        self.play(Unwrite(topic))

        header = Text("The First Building Block: Neural Networks").scale(1.2)

        self.play(Write(header))
        self.play(header.animate.move_to(UP * 3).scale(0.7))

        pnet = MarkupText(f'<span fgcolor="{PINK}">P</span>olicy Net').move_to(np.array(UP * 2))
        ptype = MarkupText(f'<span fgcolor="{PINK}">A probability distribution</span> of how good a move is in a certain position').scale(0.5).next_to(pnet, DOWN)
        
        self.play(Write(pnet))
        self.play(Write(ptype))

        pdesc = BulletedList("Doesn't have to be too accurate", "Meant to sort out the definitely bad moves from the possibly good moves", height=10, width=10).scale(0.8).next_to(ptype, DOWN)
        self.play(Write(pdesc))

        board = GoBoard(black=[(0, 0)], white=[(-2, 1)], showpdist=True, pdist=[(2, 3, 0.61), (3, 6, 0.25), (4, 6, 0.11)]).scale(1.8).move_to(DOWN * 1.8)

        self.play(*[Create(obj) for obj in board], run_time=3)

        self.wait(1)

        self.play(Unwrite(pdesc), Unwrite(ptype), Unwrite(pnet), *[Uncreate(obj) for obj in board])
        
        vnet = MarkupText(f'<span fgcolor="{GREEN}">V</span>alue Net').move_to(UP*2)
        vtype = MarkupText(f'<span fgcolor="{GREEN}">A value from 0 to 1</span> of how good a position is for a player').scale(0.5).next_to(vnet, DOWN)

        
        self.play(Write(vnet))
        self.play(Write(vtype))

        left_board = GoBoard(black=[(-4, -4), (-4, 2), (-4, 4), (-3, -3), (-3, 1), (-2, -4), (-2, -2), (-2, 2), (-1, -3), (-1, 0), (0, -4), (0, -3), (0, 1), (1, -4), (1, -2), (2, -3), (2, -2), (2, 0), (3, -4), (3, 0), (4, -4), (4, 4)], 
                             white=[(-4, -2), (-4, 0), (-3, -1), (-2, -3), (-2, 0), (-1, -4), (0, -1), (1, 1), (2, 2), (3, -1)]
                             ).scale(1.8).move_to(DOWN * 1.8 + LEFT * 3)
        left_value = DecimalNumber(0.78, color=GREEN, font_size=30).next_to(left_board, UP)
        self.play(*[Create(obj) for obj in left_board], Write(left_value), run_time=3)

        right_board = GoBoard(
            black=[(-4, 4), (-3, -1), (-3, 3), (-3, 4), (-2, -1), (-2, 3), (-2, 4), (-1, -2), (-1, -1), (0, -3), (1, -2), (2, -1), (3, -2), (3, -1), (3, 2), (4, -4), (4, -3)], 
            white=[(-4, -4), (-4, -2), (-4, 2), (-3, -4), (-3, -3), (-2, -3), (-1, -4), (-1, -3), (-1, 0), (0, -2), (0, -1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]
            ).scale(1.8).move_to(DOWN * 1.8 + RIGHT * 3)
        right_value = DecimalNumber(0.21, color=GREEN, font_size=30).next_to(right_board, UP)
        self.play(*[Create(obj) for obj in right_board], Write(right_value), run_time=3)
        self.wait(1)

        self.play(Unwrite(left_value), Unwrite(right_value), Unwrite(vtype), Unwrite(vnet), *[Uncreate(obj) for obj in left_board], *[Uncreate(obj) for obj in right_board], Unwrite(header))
        header = Text("The Next Piece: Monte Carlo Tree Search").scale(1.2)

        self.play(Write(header))
        self.play(header.animate.move_to(UP * 3).scale(0.7))
        self.wait(0.5)

        title = Text("The Game Tree").move_to(UP * 2)

        root = Circle(radius=0.4, color=WHITE).next_to(title, DOWN*2)
        left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(root, 2*DOWN + 6*LEFT)
        middle_child = Circle(radius=0.4, color=DARK_GRAY).next_to(root, 2*DOWN)
        right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(root, 2*DOWN + 6*RIGHT)
        left_action = Line(root.get_bottom(), left_child.get_top(), color=DARK_GRAY)
        middle_action = Line(root.get_bottom(), middle_child.get_top(), color=DARK_GRAY)
        right_action = Line(root.get_bottom(), right_child.get_top(), color=DARK_GRAY)

        self.play(Write(title), Create(root), Create(left_child), Create(middle_child), Create(right_child), Create(left_action), Create(middle_action), Create(right_action))

        rootlabel = Text("Root Node", color=WHITE, font_size=17).next_to(root, LEFT)
        self.play(Write(rootlabel))


        rootboard = GoBoard(black=[(0, 0)], white=[(-2, 1)]).scale(0.4).next_to(root, RIGHT)
        leftboard = GoBoard(black=[(0, 0), (-2, -1)], white=[(-2, 1)]).scale(0.4).next_to(left_child, RIGHT) #27%
        middleboard = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1)]).scale(0.4).next_to(middle_child, RIGHT) #42%
        rightboard = GoBoard(black=[(0, 0), (-2, 0)], white=[(-2, 1)]).scale(0.4).next_to(right_child, RIGHT) #12%
        self.play(*[Create(obj) for obj in [rootboard, leftboard, middleboard, rightboard]], run_time=3)

        gametree = VGroup(title, root, left_child, middle_child, right_child, left_action, middle_action, right_action, rootlabel, rootboard, leftboard, middleboard, rightboard)
        self.play(gametree.animate.shift(LEFT * 4), Unwrite(title))

        uctscore = Text("UCT Score", font_size=50).move_to(UP * 2 + RIGHT * 4)
        context = Text("Next move is determined by").scale(0.5).next_to(uctscore, LEFT)
        self.play(Write(uctscore), Write(context))
        q_arrow = Arrow(uctscore.get_bottom(), uctscore.get_bottom() + DOWN + LEFT * 1, buff=0.1)
        u_arrow = Arrow(uctscore.get_bottom(), uctscore.get_bottom() + DOWN + RIGHT * 1, buff=0.1)
        q_text = Text("Q", font_size=40).next_to(q_arrow.get_end(), DOWN)
        u_text = Text("U", font_size=40).next_to(u_arrow.get_end(), DOWN)

        self.play(Create(q_arrow), Write(q_text), Unwrite(context))

        q_formula = MathTex(r"Q(s, a) = \frac{W(s, a)}{N(s, a)}").next_to(uctscore, DOWN * 8).scale(0.7)
        w_desc = MarkupText(f"<span fgcolor='{GREEN}'>W</span> - Sum of all evaluations (here's where the value net is used)", font_size=15).next_to(q_formula, DOWN)
        n_desc = Text("N - Number of evaluations (number of node visits)", font_size=15).next_to(w_desc, DOWN)
        q_desc = Text("Basically, a running average of how good MCTS has found this state to be", font_size=15).next_to(n_desc, DOWN)
        self.play(Write(q_formula))
        self.play(Write(w_desc), Write(n_desc), Write(q_desc))
        self.wait(2)

        uct_left = Tex(r"$\frac{0}{0} + $", font_size=24).move_to(left_child)
        uct_middle = Tex(r"$\frac{0}{0} + $", font_size=24).move_to(middle_child)
        uct_right = Tex(r"$\frac{0}{0} + $", font_size=24).move_to(right_child)
        self.play(Write(uct_left), Write(uct_middle), Write(uct_right), Unwrite(q_formula), Unwrite(w_desc), Unwrite(n_desc), Unwrite(q_desc))

        self.play(Create(u_arrow), Write(u_text))

        u_formula = MathTex(r"U(s, a) = C \cdot P(s, a) \cdot \frac{\sqrt{N(s)}}{1 + N(s, a)}").next_to(uctscore, DOWN * 8).scale(0.7)
        c_desc = Text("C - Exploration Function (increases very slowly with simulations)", font_size=15).next_to(u_formula, DOWN)
        p_desc = MarkupText(f"<span fgcolor='{PINK}'>P</span> - Initial probability (here's where the policy net is used)", font_size=15).next_to(c_desc, DOWN)
        n1_desc = Text("N(s) - Number of times the parent node has been visited", font_size=15).next_to(p_desc, DOWN)
        u_desc1 = Text("Basically, how much potential does this state have?", font_size=15).next_to(n1_desc, DOWN)
        u_desc2 = Text("The rightmost term helps out nodes less explored than its siblings", font_size=15).next_to(u_desc1, DOWN)

        self.play(Write(u_formula))
        self.play(Write(c_desc), Write(p_desc), Write(n1_desc), Write(u_desc1), Write(u_desc2))
        self.wait(2)

        self.play(Unwrite(u_formula), Unwrite(c_desc), Unwrite(p_desc), Unwrite(n1_desc), Unwrite(u_desc1), Unwrite(u_desc2))

        k_formula = MathTex(r"k = C \cdot \sqrt{\frac{N(s)}{1 + N(s, a)}}").next_to(uctscore, DOWN * 8).scale(0.7)
        self.play(Write(k_formula))
        self.play(k_formula.animate.next_to(header, DOWN).scale(0.5),
                  uct_left.animate.become(Tex(r"$\frac{0}{0} + k \cdot 0.27$", font_size=15).move_to(uct_left)),
                  uct_middle.animate.become(Tex(r"$\frac{0}{0} + k \cdot 0.42$", font_size=15).move_to(uct_middle)),
                    uct_right.animate.become(Tex(r"$\frac{0}{0} + k \cdot 0.12$", font_size=15).move_to(uct_right)),)

        left_action_prob = DecimalNumber(0.34, color=YELLOW, font_size=20).move_to(left_action.get_center())
        middle_action_prob = DecimalNumber(0.53, color=YELLOW, font_size=20).move_to(middle_action.get_center())
        right_action_prob = DecimalNumber(0.15, color=YELLOW, font_size=20).move_to(right_action.get_center())

        self.play(Write(left_action_prob), Write(middle_action_prob), Write(right_action_prob))

        self.play(Unwrite(uctscore), Uncreate(q_arrow), Uncreate(u_arrow), Unwrite(q_text), Unwrite(u_text))

        desc = Text("Select a leaf node to expand via UCT score").scale(0.5).move_to(UP * 1 + RIGHT * 4)

        self.play(middle_action.animate.set_color(WHITE), middle_child.animate.set_color(WHITE), Write(desc))

        new_left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(middle_child, 2*DOWN + 6*LEFT)
        new_middle_child = Circle(radius=0.4, color=DARK_GRAY).next_to(middle_child, 2*DOWN)
        new_right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(middle_child, 2*DOWN + 6*RIGHT)
        new_left_action = Line(middle_child.get_bottom(), new_left_child.get_top(), color=DARK_GRAY)
        new_middle_action = Line(middle_child.get_bottom(), new_middle_child.get_top(), color=DARK_GRAY)
        new_right_action = Line(middle_child.get_bottom(), new_right_child.get_top(), color=DARK_GRAY)
        new_left_board = GoBoard(black=[(0, 0), (-2, -1)], white=[(-2, 1), (2, 0)]).scale(0.4).next_to(new_left_child, RIGHT) #16%
        new_middle_board = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1)]).scale(0.4).next_to(new_middle_child, RIGHT) #12%
        new_right_board = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1), (-2, 2)]).scale(0.4).next_to(new_right_child, RIGHT) #44%

        self.play(Create(new_left_child), Create(new_middle_child), Create(new_right_child), Create(new_left_action), Create(new_middle_action), Create(new_right_action), *[Create(obj) for obj in [new_left_board, new_middle_board, new_right_board]], Unwrite(desc))

        evaluation = Text("Evaluation", color=GREEN, font_size=50).move_to(UP * 2 + RIGHT * 4)
        self.play(Write(evaluation))

        big_middle_board = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1)]).next_to(evaluation, DOWN)
        self.play(*[Create(obj) for obj in big_middle_board])
        
        eval = DecimalNumber(0.542, color=GREEN, font_size=30).next_to(big_middle_board, DOWN)
        self.play(Write(eval))


        desc = Text("Update node parameters and UCT scores up the tree").scale(0.4).next_to(evaluation, DOWN)
        self.play(Unwrite(eval), *[Uncreate(obj) for obj in big_middle_board], evaluation.animate.become(Text("Backpropagation", color=WHITE, font_size=50).move_to(UP * 2 + RIGHT * 4)), Write(desc))

        self.play(uct_middle.animate.become(MathTex(r"\frac{0.542}{1} + k \cdot 0.42", font_size=10).move_to(uct_middle)))

        self.play(left_action_prob.animate.become(DecimalNumber(0.68, color=YELLOW, font_size=20).move_to(left_action.get_center())),
                  middle_action_prob.animate.become(DecimalNumber(0.81, color=YELLOW, font_size=20).move_to(middle_action.get_center())),
                  right_action_prob.animate.become(DecimalNumber(0.30, color=YELLOW, font_size=20).move_to(right_action.get_center())))

        self.play(evaluation.animate.become(Text("Repeat!", color=WHITE, font_size=50).move_to(UP * 2 + RIGHT * 4)), Unwrite(desc))
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        , run_time=0.5)

        header = Text("The Minimax Algorithm: Upgrading the Evaluation").scale(1)
        self.play(Write(header))
        self.play(header.animate.move_to(UP * 3).scale(0.7))


        earlyboard = GoBoard(black=[(0, 0), (-1, 2)], white=[(-2, 1)]).scale(2).to_edge(LEFT)
        lateboard = GoBoard(
            black=[(-4, 4), (-3, -1), (-3, 3), (-3, 4), (-2, -1), (-2, 3), (-2, 4), (-1, -2), (-1, -1), (0, -3), (1, -2), (2, -1), (3, -2), (3, -1), (3, 2), (4, -4), (4, -3)], 
            white=[(-4, -4), (-4, -2), (-4, 2), (-3, -4), (-3, -3), (-2, -3), (-1, -4), (-1, -3), (-1, 0), (0, -2), (0, -1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]
            ).scale(2).to_edge(RIGHT)
        desc = Text("The later a board state, the more accurate the evaluation").scale(0.6).to_edge(DOWN, buff=0.6)
        t = Text("Minimax lets us evaluate in later states").scale(0.6).next_to(desc, DOWN)

        self.play(*[Create(obj) for obj in earlyboard])
        self.play(*[Create(obj) for obj in lateboard])
        self.play(Write(desc))
        self.play(Write(t))
        self.play(*[Uncreate(obj) for obj in earlyboard], *[Uncreate(obj) for obj in lateboard], Unwrite(desc), Unwrite(t))

        node = Circle(radius=0.4, color=WHITE).next_to(header, DOWN * 2)
        nodedesc = Text("Node we want to evaluate").scale(0.4).next_to(node, LEFT)
        self.play(Create(node), Write(nodedesc))

        left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(node, 2*DOWN + 3*LEFT)
        right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(node, 2*DOWN + 3*RIGHT)
        left_action = Line(node.get_bottom(), left_child.get_top(), color=DARK_GRAY)
        right_action = Line(node.get_bottom(), right_child.get_top(), color=DARK_GRAY)
        left_left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(left_child, 2*DOWN + 1*LEFT)
        left_right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(left_child, 2*DOWN + 1*RIGHT)
        right_left_child = Circle(radius=0.4, color=DARK_GRAY).next_to(right_child, 2*DOWN + 1*LEFT)
        right_right_child = Circle(radius=0.4, color=DARK_GRAY).next_to(right_child, 2*DOWN + 1*RIGHT)
        left_left_action = Line(left_child.get_bottom(), left_left_child.get_top(), color=DARK_GRAY)
        left_right_action = Line(left_child.get_bottom(), left_right_child.get_top(), color=DARK_GRAY)
        right_left_action = Line(right_child.get_bottom(), right_left_child.get_top(), color=DARK_GRAY)
        right_right_action = Line(right_child.get_bottom(), right_right_child.get_top(), color=DARK_GRAY)
        self.play(Create(left_child), Create(right_child), Create(left_action), Create(right_action), Create(left_left_child), Create(left_right_child), Create(right_left_child), Create(right_right_child), Create(left_left_action), Create(left_right_action), Create(right_left_action), Create(right_right_action))

        desc = Text("We expand the node we want to evaluate downwards, k_best moves on each level, and minimax_depth levels").scale(0.45).to_edge(DOWN, buff=1.5)
        k_best = Text("k_best = 2").scale(0.5).move_to(UP + RIGHT*4)
        minimax_depth = Text("minimax_depth = 2").scale(0.5).next_to(k_best, DOWN)
        self.play(Write(desc))
        self.play(Write(k_best), Write(minimax_depth))

        desc2 = Text("The k_best moves selected are the highest probability moves from the policy net").scale(0.45).next_to(desc, DOWN)
        self.play(Write(desc2))

        left_right_eval = DecimalNumber(0.78, color=GREEN, font_size=20).move_to(left_right_child)
        left_left_eval = DecimalNumber(0.21, color=GREEN, font_size=20).move_to(left_left_child)
        right_right_eval = DecimalNumber(0.54, color=GREEN, font_size=20).move_to(right_right_child)
        right_left_eval = DecimalNumber(0.42, color=GREEN, font_size=20).move_to(right_left_child)

        desc3 = Text("We evaluate leaf nodes using the value net").scale(0.45).next_to(desc2, DOWN)
        self.play(Write(desc3))
        self.play(Write(left_right_eval), Write(left_left_eval), Write(right_right_eval), Write(right_left_eval))
        self.play(Unwrite(desc), Unwrite(desc2), Unwrite(desc3))

        player = Text("Black's Turn").scale(0.5).next_to(node, LEFT).to_edge(LEFT)
        player2 = Text("White's Turn").scale(0.5).next_to(left_child, LEFT).to_edge(LEFT)
        self.play(Write(player), Write(player2))

        desc = Text("White seeks to minimize the value").scale(0.5).to_edge(DOWN, buff=0.6)
        self.play(Write(desc))

        left_eval = left_left_eval.copy()
        right_eval = right_left_eval.copy()
        self.add(left_eval, right_eval)
        self.play(left_eval.animate.move_to(left_child), right_eval.animate.move_to(right_child))

        
        desc2 = Text("Black seeks to maximize the value").scale(0.5).next_to(desc, DOWN)
        self.play(Write(desc2))

        node_eval = right_eval.copy()
        self.add(node_eval)
        self.play(node_eval.animate.move_to(node))

        self.play(Unwrite(desc), Unwrite(desc2))

        self.play(right_action.animate.set_color(WHITE), right_child.animate.set_color(WHITE), right_left_action.animate.set_color(WHITE), right_left_child.animate.set_color(WHITE))
        
        desc = Text("The algorithm approximates optimal play for minimax_depth moves, and evaluates at a later node, granting more accurate evaluation.").scale(0.38).to_edge(DOWN)
        self.play(Write(desc))




                  


