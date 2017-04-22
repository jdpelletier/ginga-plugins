#
# MultiBars.py -- Overlay expected bar positions over image
#
#
import re
import os
import numpy as np
from ginga import GingaPlugin, RGBImage, colors
from ginga.gw import Widgets
from ginga.misc import ParamSet, Bunch
from ginga.util import dp
from ginga.gw.GwHelp import FileSelection

class MultiBars(GingaPlugin.LocalPlugin):
    """
    MultiBars
    =========
    Plugin Type: Local
    ------------------
    TVMask is a local plugin, which means it is associated with a
    channel.  An instance can be opened for each channel.

    Usage
    -----
    This plugin adds cartoon bars with expected positions over 
    and image of the MOSFIRE CSU.  Click overlay to load your
    position file and have it overlay your image.    
    """

    def __init__(self, fv, fitsimage):
        super(MultiBars, self).__init__(fv, fitsimage)

        self.layertag = 'bars-canvas'

        self.dc = fv.get_draw_classes()
        canvas = self.dc.DrawingCanvas()
        canvas.enable_draw(False)
        canvas.set_surface(self.fitsimage)
        self.canvas = canvas

        self.colornames = colors.get_colors()
        self.canvas_img = None
        
        self.mfilesel = FileSelection(self.fv.w.root.get_widget())

    def build_gui(self, container):
        top = Widgets.VBox()
        top.set_border_width(4)

        vbox, sw, orientation = Widgets.get_oriented_box(container)
        vbox.set_border_width(4)
        vbox.set_spacing(2)

        fr = Widgets.Frame("Bar Input")

        captions = (('Overlay', 'button'),
            ('Clear', 'button'))
    
        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w.update(b)

        b.overlay.add_callback('activated',
                   lambda w: self.load_cb())

        b.clear.add_callback('activated', lambda w: self.clear_canvas())
        fr.set_widget(w)
        vbox.add_widget(fr, stretch=0)

        spacer = Widgets.Label('')
        vbox.add_widget(spacer, stretch=1)

        top.add_widget(sw, stretch=1)

        btns = Widgets.HBox()
        btns.set_spacing(3)

        btn = Widgets.Button("Close")
        btn.add_callback('activated', lambda w: self.close())
        btns.add_widget(btn, stretch=0)
        btn = Widgets.Button("Help")
        btn.add_callback('activated', lambda w: self.help())
        btns.add_widget(btn, stretch=0)
        btns.add_widget(Widgets.Label(''), stretch=1)
        top.add_widget(btns, stretch=0)

        container.add_widget(top, stretch=1)
    
    
    
    def help(self):
        name = str(self).capitalize()
        self.fv.help_text(name, self.__doc__, text_kind='rst', trim_pfx=4)

    def close(self):
        self.fv.stop_local_plugin(self.chname, str(self))
        return True

    def start(self):
        # start ruler drawing operation
        p_canvas = self.fitsimage.get_canvas()
        try:
            obj = p_canvas.get_object_by_tag(self.layertag)

        except KeyError:
            # Add ruler layer
            p_canvas.add(self.canvas, tag=self.layertag)

        self.resume()

    def pause(self):
        self.canvas.ui_setActive(False)

    def resume(self):
        self.canvas.ui_setActive(True)
        self.fv.show_status("Enter a value for bar length")

    def stop(self):
        self.arrsize = None
        self.rgbobj.set_data(self.rgbarr)

        # remove the canvas from the image
        p_canvas = self.fitsimage.get_canvas()
        try:
            p_canvas.delete_object_by_tag(self.layertag)
        except:
            pass
        #self.canvas.ui_setActive(False)
        self.fv.show_status("")

    def redo(self):
        pass

####Main function#####
    def overlaybars(self, filename):
        bf = open(filename)
        lines = bf.readlines()
        for j in range(0, 46):
            start = 12
            height = (2044-8)/46
            y1 = start + height*j + 0.11/0.1798
            y2 = start + height*(j+1) - 0.11/0.1798
            cols1 = lines[(6*j)].split()
            cols2 = lines[(6*j)+3].split()
            x1 = (float(cols2[2])-8.34)/0.124
            x2 = (float(cols1[2])-8.34)/0.124
            self.canvas.add(self.dc.Rectangle(2044, int(np.floor(y2)), x1, int(np.ceil(y1))))
            self.canvas.add(self.dc.Rectangle(0, int(np.floor(y2)), x2, int(np.ceil(y1))))    
   
#####For loading file with popup#########
    def load_cb(self):
        self.mfilesel.popup('Load bar file', self.overlaybars,
                            initialdir='.', filename='txt files (*.txt)')

    def clear_canvas(self):
        self.canvas.delete_all_objects()

    def __str__(self):
        return 'MultiBars'

#END
