"""
Skeleton example of a Ginga local plugin called 'MyLocalPlugin'

To enable it, run ginga with the command
    $ ginga --plugins=MyLocalPlugin

it will then be available from the "Operations" button.

"""

from ginga import GingaPlugin
from ginga.gw import Widgets

# import any other modules you want here--it's a python world!

class CSU_initializer(GingaPlugin.LocalPlugin):

    def __init__(self, fv, fitsimage):
        """
        This method is called when the plugin is loaded for the  first
        time.  ``fv`` is a reference to the Ginga (reference viewer) shell
        and ``fitsimage`` is a reference to the specific ImageViewCanvas
        object associated with the channel on which the plugin is being
        invoked.
        You need to call the superclass initializer and then do any local
        initialization.
        """
        super(CSU_initializer, self).__init__(fv, fitsimage)

        # Load plugin preferences
        prefs = self.fv.get_preferences()
        self.settings = prefs.createCategory('plugin_CSU_initializer')
        self.settings.setDefaults(bar_num=1,
                                  move_to_open=False,
                                  bar_dist=0.0,
                                 )
        self.settings.load(onError='silent')





    def build_gui(self, container):
        """
        This method is called when the plugin is invoked.  It builds the
        GUI used by the plugin into the widget layout passed as
        ``container``.
        This method may be called many times as the plugin is opened and
        closed for modal operations.  The method may be omitted if there
        is no GUI for the plugin.

        This specific example uses the GUI widget set agnostic wrappers
        to build the GUI, but you can also just as easily use explicit
        toolkit calls here if you only want to support one widget set.
        """
        top = Widgets.VBox()
        top.set_border_width(4)

        # this is a little trick for making plugins that work either in
        # a vertical or horizontal orientation.  It returns a box container,
        # a scroll widget and an orientation ('vertical', 'horizontal')
        vbox, sw, orientation = Widgets.get_oriented_box(container)
        vbox.set_border_width(4)
        vbox.set_spacing(2)

        self.msg_font = self.fv.get_font("sansFont", 12)

        ## -----------------------------------------------------
        ## Acquire or Load Image
        ## -----------------------------------------------------
#         tw_image = Widgets.TextArea(wrap=True, editable=False)
#         tw_image.set_font(self.msg_font)
#         self.tw_image = tw_image

        # Frame for instructions and add the text widget with another
        # blank widget to stretch as needed to fill emp
        fr1 = Widgets.Frame("Image the CSU Mask")
#         fr1.set_widget(tw_image)
        vbox.add_widget(fr1, stretch=0)

        # A button box that is always visible at the top
        btns1 = Widgets.HBox()
        btns1.set_spacing(3)

        # Add mask image buttons
        btn_acq_im = Widgets.Button("Acquire Mask Image")
        btn_acq_im.add_callback('activated', lambda w: self.acq_mask_image())
        btns1.add_widget(btn_acq_im, stretch=0)
        btns1.add_widget(Widgets.Label(''), stretch=1)

        btn_load_im = Widgets.Button("Load Mask Image")
        btn_load_im.add_callback('activated', lambda w: self.load_mask_image())
        btns1.add_widget(btn_load_im, stretch=0)
        btns1.add_widget(Widgets.Label(''), stretch=1)

        vbox.add_widget(btns1, stretch=0)


        ## -----------------------------------------------------
        ## Analyze Image
        ## -----------------------------------------------------
#         tw_analyze = Widgets.TextArea(wrap=True, editable=False)
#         tw_analyze.set_font(self.msg_font)
#         self.tw_analyze = tw_analyze

        fr2 = Widgets.Frame("Analyze CSU Mask Image")
#         fr2.set_widget(tw_analyze)
        vbox.add_widget(fr2, stretch=0)

        btns2 = Widgets.HBox()
        btns2.set_spacing(3)

        btn_analyze = Widgets.Button("Analyze Mask Image")
        btn_analyze.add_callback('activated', lambda w: self.analyze_mask_image())
        btns2.add_widget(btn_analyze, stretch=0)
        btns2.add_widget(Widgets.Label(''), stretch=1)

        vbox.add_widget(btns2, stretch=0)

        ## -----------------------------------------------------
        ## Bar Control
        ## -----------------------------------------------------
#         tw_bar_control = Widgets.TextArea(wrap=True, editable=False)
#         tw_bar_control.set_font(self.msg_font)
#         self.tw_bar_control = tw_bar_control

        # Frame for instructions and add the text widget with another
        # blank widget to stretch as needed to fill emp
        fr1 = Widgets.Frame("CSU Bar Control")
#         fr1.set_widget(tw_bar_control)

        captions = [
            ("CSU Bar: ", 'label', 'bar_num', 'llabel', 'set_bar_num', 'entry'),
            ("Distance: ", 'label', 'bar_dist', 'llabel', 'set_bar_dist', 'entry'),
            ("Initialize Bar", 'button', "Move to open", 'checkbutton'),
            ("Move Bar", 'button'),
            ]

        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w.update(b)

        bar_num = self.settings.get('bar_num', 1)
        b.bar_num.set_text('{:2d}'.format(bar_num))
        b.set_bar_num.set_text(str(bar_num))
        b.set_bar_num.add_callback('activated', self.set_bar_num_cb)
        b.set_bar_num.set_tooltip("Set bar number")

        bar_dist = self.settings.get('bar_dist', 0.0)
        b.bar_dist.set_text('{:.1f}'.format(bar_dist))
        b.set_bar_dist.set_text(str(bar_dist))
        b.set_bar_dist.add_callback('activated', self.set_bar_dist_cb)
        b.set_bar_dist.set_tooltip("Set distance to move bar")

        b.move_to_open.set_tooltip("Move bar to open position before initialization")
        move_to_open = self.settings.get('move_to_open', False)
        b.move_to_open.set_state(move_to_open)
        b.move_to_open.add_callback('activated', self.move_to_open_cb)
        b.initialize_bar.add_callback('activated', lambda w: self.initialize_bar_cb())

        b.move_bar.add_callback('activated', lambda w: self.move_bar_cb())


        fr1.set_widget(w)
        vbox.add_widget(fr1, stretch=0)



        ## -----------------------------------------------------
        ## Spacer
        ## -----------------------------------------------------

        # Add a spacer to stretch the rest of the way to the end of the
        # plugin space
        spacer = Widgets.Label('')
        vbox.add_widget(spacer, stretch=1)

        # scroll bars will allow lots of content to be accessed
        top.add_widget(sw, stretch=1)

        ## -----------------------------------------------------
        ## Bottom
        ## -----------------------------------------------------

        # A button box that is always visible at the bottom
        btns_close = Widgets.HBox()
        btns_close.set_spacing(3)

        # Add a close button for the convenience of the user
        btn = Widgets.Button("Close")
        btn.add_callback('activated', lambda w: self.close())
        btns_close.add_widget(btn, stretch=0)

        btns_close.add_widget(Widgets.Label(''), stretch=1)
        top.add_widget(btns_close, stretch=0)

        # Add our GUI to the container
        container.add_widget(top, stretch=1)
        # NOTE: if you are building a GUI using a specific widget toolkit
        # (e.g. Qt) GUI calls, you need to extract the widget or layout
        # from the non-toolkit specific container wrapper and call on that
        # to pack your widget, e.g.:
        #cw = container.get_widget()
        #cw.addWidget(widget, stretch=1)

    def close(self):
        """
        Example close method.  You can use this method and attach it as a
        callback to a button that you place in your GUI to close the plugin
        as a convenience to the user.
        """
        self.fv.stop_local_plugin(self.chname, str(self))
        return True

    def start(self):
        """
        This method is called just after ``build_gui()`` when the plugin
        is invoked.  This method may be called many times as the plugin is
        opened and closed for modal operations.  This method may be omitted
        in many cases.
        """
#         self.tw_image.set_text(
#         'Acquire or load an image of the mask to be analyzed.')

#         self.tw_analyze.set_text(
#         'Click "Analyze Mask Image" to initiate the analysis.')

#         self.tw_bar_control.set_text(
#         'Move or initialize a bar.')

        self.resume()

    def pause(self):
        """
        This method is called when the plugin loses focus.
        It should take any actions necessary to stop handling user
        interaction events that were initiated in ``start()`` or
        ``resume()``.
        This method may be called many times as the plugin is focused
        or defocused.  It may be omitted if there is no user event handling
        to disable.
        """
        pass

    def resume(self):
        """
        This method is called when the plugin gets focus.
        It should take any actions necessary to start handling user
        interaction events for the operations that it does.
        This method may be called many times as the plugin is focused or
        defocused.  The method may be omitted if there is no user event
        handling to enable.
        """
        pass

    def stop(self):
        """
        This method is called when the plugin is stopped.
        It should perform any special clean up necessary to terminate
        the operation.  The GUI will be destroyed by the plugin manager
        so there is no need for the stop method to do that.
        This method may be called many  times as the plugin is opened and
        closed for modal operations, and may be omitted if there is no
        special cleanup required when stopping.
        """
        pass

    def redo(self):
        """
        This method is called when the plugin is active and a new
        image is loaded into the associated channel.  It can optionally
        redo the current operation on the new image.  This method may be
        called many times as new images are loaded while the plugin is
        active.  This method may be omitted.
        """
        pass

    def __str__(self):
        """
        This method should be provided and should return the lower case
        name of the plugin.
        """
        return 'mylocalplugin'

    def set_bar_num_cb(self, w):
        bar_num = int(w.get_text())
        self.settings.set(bar_num=bar_num)
        self.w.bar_num.set_text(str(bar_num))
        
    def initialize_bar_cb(self):
        if self.settings.get('move_to_open'):
            pass
        else:
            pass

    def move_to_open_cb(self, widget, tf):
        self.settings.set(move_to_open_cb=tf)

    def set_bar_dist_cb(self, w):
        bar_dist = float(w.get_text())
        self.settings.set(bar_dist=bar_dist)
        self.w.bar_dist.set_text(str(bar_dist))

    def move_bar_cb(self):
        pass
