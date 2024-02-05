init python:
    class ColorGame:
        def __init__(self,path_to_reward, path_to_cover, dim=6, colors=None, tries=10):
            self.path_to_cover = path_to_cover
            self.path_to_reward = path_to_reward
            self.pic_xsize = 450
            self.pic_ysize = 450

            self.cover_xpos = 0
            self.cover_xrect = self.pic_xsize
            self.cover_ypos = 0
            self.cover_yrect = 0


            self.dim = dim
            self.tries = tries
            if colors is not None:
                self.colors = colors
            else:
                self.colors = [u'#ed2024',u'#292394',u'#54c2d6',u'#3bbf31',u'#f5841f',u'#7f1e94']

            self.dim1 = 600//dim
            self.button_size = 600//dim - 20

            self.tileset = []

            self.flagger = []

            for i in range(dim):
                self.tileset.append([])
                self.flagger.append([])
                for j in range(dim):
                    self.tileset[i].append(renpy.random.choice(self.colors))
                    self.flagger[i].append(False)

            self.old_color = self.tileset[0][0]
            self.new_color = None

            self.num_done = 0

            self.calcs()

        def reset_flagger(self):
            for i in range(self.dim):
                for j in range(self.dim):
                    self.flagger[i][j] = False

        def set_new_color(self, new_color):
            self.reset_flagger()
            self.new_color = new_color
            self.old_color = self.tileset[0][0]
            self.num_done = 0

        def change_color(self, ii, jj):
            if self.tileset[ii][jj] == self.old_color:
                self.tileset[ii][jj] = self.new_color
                if ii+1 <= self.dim-1:
                    self.change_color(ii+1,jj)
                if ii-1 >= 0:
                    self.change_color(ii-1,jj)
                if jj+1 <= self.dim-1:
                    self.change_color(ii,jj+1)
                if jj-1 >= 0:
                    self.change_color(ii,jj-1)

            return

        def count_filled(self,ii,jj):
            if self.tileset[ii][jj] == self.new_color and not self.flagger[ii][jj]:
                self.num_done += 1
                self.flagger[ii][jj] = True
                if ii+1 <= self.dim-1:
                    self.count_filled(ii+1,jj)
                if ii-1 >= 0:
                    self.count_filled(ii-1,jj)
                if jj+1 <= self.dim-1:
                    self.count_filled(ii,jj+1)
                if jj-1 >= 0:
                    self.count_filled(ii,jj-1)
            return

        def calcs(self):
            precentage = self.num_done / self.dim/self.dim

            if precentage > 1:
                precentage = 1

            self.cover_xpos = 0
            self.cover_xrect = self.pic_xsize

            pom = int(self.pic_ysize * precentage)
            


            self.cover_ypos = pom
            if self.cover_ypos > self.pic_ysize:
                self.cover_ypos = self.pic_ysize

            self.cover_yrect = self.pic_ysize - pom
            if self.cover_yrect < 0:
                self.cover_yrect = 0

            renpy.restart_interaction()







    


default X_SIZE = 450

default Y_SIZE = 450

screen color_game_screen(g):
    zorder 20
    modal True
    fixed:
        add u'#555'
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 150
            vbox:
                spacing 50
                frame:
                    xalign 0.5
                    xsize 612
                    ysize 612
                    for i in range(g.dim):
                        for j in range(g.dim):
                            button:
                                background g.tileset[i][j]
                                xsize g.dim1
                                ysize g.dim1
                                pos (g.dim1*j,g.dim1*i)
                                action NullAction()

                hbox:
                    xalign 0.5
                    spacing 35
                    for i in range(len(g.colors)):
                        frame:
                            button:
                                background g.colors[i]
                                xsize g.button_size
                                ysize g.button_size
                                sensitive g.colors[i] != g.tileset[0][0]
                                action [Function(g.set_new_color,new_color=g.colors[i]),Function(g.change_color,ii=0,jj=0), Function(g.count_filled,ii=0,jj=0), Function(g.calcs)]

            frame:
                yalign 0.5
                background '#333'
                xsize 463
                ysize 463
                add g.path_to_reward
                add im.Crop(g.path_to_cover,(g.cover_xpos,g.cover_ypos,g.cover_xrect,g.cover_yrect)) ypos g.cover_ypos
                #add im.Crop(g.path_to_cover, (0,int(700*g.num_done/g.dim/g.dim),400,700-int(700*g.num_done/g.dim/g.dim))) ypos int(700*g.num_done/g.dim/g.dim)



label start:
    $ game_trial1 = ColorGame(path_to_reward = "images/pika.png", path_to_cover = "images/pika_overlay.png", dim=6)
    show screen color_game_screen(g=game_trial1)
    window hide
    pause


    return
