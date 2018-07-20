# Dialogue-Tagger
Tag dialogue utterances with Dialogue Acts and Adjacency Pairs

Button colour = 88, 88, 88
Button down colour = 50, 164, 206
# TODO
## Menu
- Menu?
- Load functionality
- Save as
- Fit text to labels/labels to text?
- Tooltips https://gist.github.com/opqopq/15c707dc4cffc2b6455f

## Dialogue View
- Size of text btn/color of text 
- Background for labels/color of text
- Label clear button?
- Label/button text wrap
- Speaker labels (remove colon in button labels)
- Scrollable?
- Edit utterance
- Delete utterance

## Button bars
- Group AP labels by type? Four boxes (FPPbase, SPPbase and None AP for example)
- Text/button colours?
- Highlight buttons for utterance labels? (Group/toggle buttons)
- Make labels generic (model, controller and view)??

## Model

## MISC
- De kivify?
- Documentation/readme
- Add datasets
- Popup for exit and saving

#Misc
    ### EXAMPLE FOR DE-KIVY-FYING ###
    # CANVAS
    #     with self.canvas:  # Instead of Kivy?
    #         Color(53 / 255.0, 53 / 255.0, 53 / 255.0, 1)
    #         self.rect = Rectangle(source='resources/background.png', pos=self.pos, size=self.size)
    #     self.bind(pos=self.update_rect, size=self.update_rect)
    #
    # def update_rect(self, *args):# Instead of Kivy?
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size
    
    # IMAGE BUTTON
    # self.menu_btn_layout = AnchorLayout(anchor_x='center', anchor_y='center', width=50, size_hint=(None, 1))
    # self.menu_btn = Button(size=(40, 40))
    # self.menu_btn.bind(on_press=ctrl.menu)
    # self.menu_img = Image(source='resources/menu.png', height=40, width=40)
    # self.menu_btn_layout.add_widget(self.menu_btn)
    # self.menu_btn_layout.add_widget(self.menu_img)
