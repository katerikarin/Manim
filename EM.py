from manim import *

class EM(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=120 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-10, 10, 2], 
            y_range=[-1, 1, 0.5], 
            z_range=[-10, 10, 2],
            axis_config={"color": WHITE}
        )

        dt = ValueTracker(0)

        def ewave(t):
            return np.array([t, 0.5 * np.sin(0.5 * np.pi * (t - dt.get_value())), 0])
        def bwave(t):
            return np.array([t, 0, 0.5 * np.sin(0.5 * np.pi * (t - dt.get_value()))])
        
        Ewave = ParametricFunction(
            ewave, 
            t_range=(-TAU, TAU), 
            color=BLUE
        ).set_stroke(width=3)

        Bwave = ParametricFunction(
            bwave, 
            t_range=(-TAU, TAU), 
            color=RED
        ).set_stroke(width=3)
        
        Ewave.add_updater(lambda mob: mob.become(
            ParametricFunction(
                ewave, 
                t_range=np.array([-TAU, TAU]), 
                color=BLUE
            ).set_stroke(width=3)
        ))
        Bwave.add_updater(lambda mob: mob.become(
            ParametricFunction(
                bwave,
                t_range=np.array([-TAU, TAU]),
                color=RED
            ).set_stroke(width=3)
        ))

        x_pstns = np.linspace(-TAU, TAU, 40)
        
        e_arrs = VGroup(*[
            Arrow(
                start=np.array([x, 0, 0]), 
                end=np.array([x, 0, 0]), 
                color=BLUE
            ).set_stroke(width=2)
            for x in x_pstns
        ])

        b_arrs = VGroup(*[
            Arrow(
                start=np.array([x, 0, 0]), 
                end=np.array([x, 0, 0]), 
                color=RED
            ).set_stroke(width=2)
            for x in x_pstns
        ])

        for i, e_arr in enumerate(e_arrs):
            x = x_pstns[i]
            e_arr.add_updater(lambda mob, x=x: mob.become(
                Arrow(
                    start=np.array([x, 0, 0]),
                    end=np.array([x, 0.5 * np.sin(0.5 * np.pi * (x - dt.get_value())), 0]),
                    color=BLUE
                ).set_stroke(width=2)
            ))
        
        for j, b_arr in enumerate(b_arrs):
            x = x_pstns[j]
            b_arr.add_updater(lambda mob, x=x: mob.become(
                Arrow(
                    start=np.array([x, 0, 0]),
                    end=np.array([x, 0, 0.5 * np.sin(0.5 * np.pi * (x - dt.get_value()))]),
                    color=RED
                ).set_stroke(width=2)
            ))
        
        # self.play(Create(axes))
        self.play(Create(Ewave))   
        self.play(Create(e_arrs))
        self.play(Create(Bwave))   
        self.play(Create(b_arrs))
        self.play(dt.animate.increment_value(2 * np.pi), run_time=8, rate_func=linear)
        self.wait()

class EM2d(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10, 1], 
            y_range=[-1, 1, 0.5], 
            axis_config={"color": WHITE}
        )
        
        dt = ValueTracker(0)
        
        def ewave(t):
            return np.array([t, 0.5 * np.sin(0.5 * np.pi * (t - dt.get_value())), 0])
        
        # Create the electric wave as a parametric function
        Ewave = ParametricFunction(
            ewave, 
            t_range=(-TAU, TAU), 
            color=RED
        ).set_stroke(width=3)
        
        # Update the wave's motion
        Ewave.add_updater(lambda mob: mob.become(
            ParametricFunction(
                ewave, 
                t_range=np.array([-TAU, TAU]), 
                color=RED
            ).set_stroke(width=3)
        ))

        # Set up x positions for arrows
        x_pstns = np.linspace(-TAU, TAU, 40)
        
        # Create arrows based on the wave function
        e_arrs = VGroup(*[
            Arrow(
                start=np.array([x, 0, 0]), 
                end=np.array([x, 0, 0]), 
                color=RED
            ).set_stroke(width=2)
            for x in x_pstns
        ])

        # Update arrows' end points based on the wave's y-coordinate at each x position
        for i, e_arr in enumerate(e_arrs):
            x = x_pstns[i]
            e_arr.add_updater(lambda mob, x=x: mob.become(
                Arrow(
                    start=np.array([x, 0, 0]),  # Fixed base at each x position in 3D
                    end=np.array([x, 0.5 * np.sin(0.5 * np.pi * (x - dt.get_value())), 0]),  # End point based on wave in 3D
                    color=RED
                ).set_stroke(width=2)
            ))
        
        # Play the scene
        self.play(Create(axes))
        self.play(Create(Ewave))   
        self.play(Create(e_arrs))
        self.play(dt.animate.increment_value(2 * np.pi), run_time=4, rate_func=linear)
        self.wait()