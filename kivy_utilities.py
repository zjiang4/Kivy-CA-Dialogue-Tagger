from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.image import Image
from kivy.uix.widget import Widget


class ImageButton(ButtonBehavior, Image):
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):

        # Check this is the current window
        if not self.get_root_window():
            return

        # Get mouse position
        pos = args[1]

        # Convert position to local widgets co-ordianates and check if inside
        inside = self.collide_point(*self.to_widget(*pos))

        # Check if already hovered
        if self.hovered == inside:
            return

        # Set state and dispatch events
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        with self.canvas.before:
            Color(88 / 255.0, 88 / 255.0, 88 / 255.0, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
            Line(rectangle=(self.x+1, self.y+1, self.width-1, self.height-1), width=1)

    def on_leave(self):
        self.canvas.before.clear()

    def on_press(self):
        with self.canvas.before:
            Color(50 / 255.0, 164 / 255.0, 206 / 255.0, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
            Line(rectangle=(self.x + 1, self.y + 1, self.width - 1, self.height - 1), width=1)

    def on_release(self):
        with self.canvas.before:
            Color(88 / 255.0, 88 / 255.0, 88 / 255.0, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
            Line(rectangle=(self.x+1, self.y+1, self.width-1, self.height-1), width=1)


class ImageToggleButton(ToggleButtonBehavior, Image):
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ImageToggleButton, self).__init__(**kwargs)
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)

        # Default rectangle
        with self.canvas:
            Color(53 / 255.0, 53 / 255.0, 53 / 255.0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Bind to any changes in state
        self.bind(pos=self.set_state, size=self.set_state)

    def on_mouse_pos(self, *args):

        # Check this is the current window
        if not self.get_root_window():
            return

        # Get mouse position
        pos = args[1]

        # Convert position to local widgets co-ordianates and check if inside
        inside = self.collide_point(*self.to_widget(*pos))

        # Check if already hovered
        if self.hovered == inside:
            return

        # Set state and dispatch events
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        self.set_state()
        # if self.state == 'down':
        #     with self.canvas.before:
        #         Color(50 / 255.0, 164 / 255.0, 206 / 255.0, 1)
        #         Rectangle(pos=self.pos, size=self.size)
        #         Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
        #         Line(rectangle=(self.x + 1, self.y + 1, self.width - 1, self.height - 1), width=1)
        # else:
        #     with self.canvas.before:
        #         Color(88 / 255.0, 88 / 255.0, 88 / 255.0, 1)
        #         Rectangle(pos=self.pos, size=self.size)
        #         Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
        #         Line(rectangle=(self.x+1, self.y+1, self.width-1, self.height-1), width=1)

    def on_leave(self):
        if self.state == 'down':
            return
        else:
            self.canvas.before.clear()

    def on_state(self, widget, value):
        self.set_state()
        # if value == 'down':
        #     with self.canvas.before:
        #         Color(50 / 255.0, 164 / 255.0, 206 / 255.0, 1)
        #         Rectangle(pos=self.pos, size=self.size)
        #         Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
        #         Line(rectangle=(self.x + 1, self.y + 1, self.width - 1, self.height - 1), width=1)
        # else:
        #     with self.canvas.before:
        #         Color(88 / 255.0, 88 / 255.0, 88 / 255.0, 1)
        #         Rectangle(pos=self.pos, size=self.size)
        #         Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
        #         Line(rectangle=(self.x + 1, self.y + 1, self.width - 1, self.height - 1), width=1)

    def set_state(self,  *args):
        if self.state == 'down':
            with self.canvas.before:
                Color(50 / 255.0, 164 / 255.0, 206 / 255.0, 1)
                Rectangle(pos=self.pos, size=self.size)
                Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
                Line(rectangle=(self.x + 1, self.y + 1, self.width - 1, self.height - 1), width=1)
        else:
            if self.hovered:
                with self.canvas.before:
                    Color(88 / 255.0, 88 / 255.0, 88 / 255.0, 1)
                    Rectangle(pos=self.pos, size=self.size)
                    Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
                    Line(rectangle=(self.x+1, self.y+1, self.width-1, self.height-1), width=1)
            else:
                with self.canvas.before:
                    Color(53 / 255.0, 53 / 255.0, 53 / 255.0, 1)
                    Rectangle(pos=self.pos, size=self.size)


class Separator(Widget):
    def __init__(self, **kwargs):
        super(Separator, self).__init__(**kwargs)
        with self.canvas:
            Color(111 / 255.0, 111 / 255.0, 111 / 255.0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
