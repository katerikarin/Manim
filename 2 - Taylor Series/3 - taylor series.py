from manim import *
import math

class Taylorseries(Scene):
    def construct(self):
        self.wait()
        axes = Axes(
            x_range=(-2, 12, 2),
            y_range=(-1, 2, 2)
            )
        self.play(Create(axes))
        self.wait()



        def f(x):
            # while x>0:
            #     return np.cos(np.log(x))
            # while x<0:
            #     return np.cos(np.log(-x))
            # else:
            #     return 1


            sigma, mu = 4.0, 0.5  # bell curve
            z = np.exp(-((x - mu) ** 2) / (2.0 * sigma ** 2))
            return z
        

        a = 1.5 # Point of approximation

        sg = axes.plot(f, color=BLUE, stroke_width=3)
        self.play(Create(sg))
        self.wait()

        func_text = MathTex(r"f(x) = e^{-\frac{(x - \mu)^2}{2\sigma^2}}", font_size=30).to_edge(UP + RIGHT)
        ttt = Text(f"approximation done at point {a}", font_size=20).to_edge(UP*2.25 + RIGHT)
        self.play(Write(func_text))
        self.play(Write(ttt))

        def fd(f, x, n, dx=1e-2):
            if n == 0:
                return f(x)
            else:
                return (fd(f, x + dx, n - 1, dx) - fd(f, x - dx, n - 1, dx)) / (2 * dx)

        def tff(a, n_terms):
            apprxs = []
            all_ts = []
            
            for n in range(n_terms):
                def apprx(n):
                    return lambda x: sum(
                        fd(f, a, k)*((x-a)**k) / math.factorial(k) for k in range(n+1)
                        )
                apprxs.append(apprx(n))

                ts = [
                    f"{round(fd(f, a, k), 2)}\\frac{{(x-{a})^{{{k}}}}}{{{k}!}}"
                    for k in range(n+1)
                ]
                ts_str = " + ".join(ts).replace("+ -", "- ").replace("--", "+ ").replace("x-0", "x")
                all_ts.append(ts_str)                
            return apprxs, all_ts
        
        colors = [RED, YELLOW, GREEN, ORANGE, PURPLE]
        fns, terms = tff(a, 5)
        
        fnccurrent = axes.plot(lambda x: fns[0](x), color=colors[0])
        txtcurrent = MathTex(terms[0], font_size=30).shift(DOWN *3.5)
        
        self.play(Create(fnccurrent), Write(txtcurrent))
        self.wait(2)

        for j in range(1, len(fns)):
            nfn = axes.plot(lambda x: fns[j](x), color = colors[j % len(colors)])
            ntxt = MathTex(terms[j], font_size=30).shift(DOWN*3.5)
            self.play(Transform(fnccurrent, nfn), Transform(txtcurrent, ntxt))
            self.wait(2)
        
        self.play(FadeOut(sg, fnccurrent, txtcurrent, axes, func_text, ttt))
        self.wait()
