"""
Skeleton example of a Ginga local plugin called 'MyLocalPlugin'

To enable it, run ginga with the command
    $ ginga --plugins=MyLocalPlugin

it will then be available from the "Operations" button.

"""

from ginga import GingaPlugin
from ginga.gw import Widgets

# import any other modules you want here--it's a python world!
from datetime import datetime as dt
import numpy as np
from ginga import GingaPlugin, RGBImage, colors
from ginga.gw import Widgets
from ginga.misc import ParamSet, Bunch
from ginga.util import dp
from ginga.gw.GwHelp import FileSelection
from astropy.io import fits

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

        self.layertag = 'bars-canvas'
        self.dc = fv.get_draw_classes()
        canvas = self.dc.DrawingCanvas()
        canvas.enable_draw(False)
        canvas.set_surface(self.fitsimage)
        self.canvas = canvas

        self.colornames = colors.get_colors()
        self.canvas_img = None
        
        self.mfilesel = FileSelection(self.fv.w.root.get_widget())
        
        ## Define dimensions and angles relative to the pixels of the image
#         self.slit_angle = (4.00-0.22) * np.pi/180.
#         pixels = np.array([ (721, 2022), # pixels
#                             (1068, 1934),
#                             (984, 1804),
#                             (1112, 40),
#                           ])
#         physical = np.array([ (179.155, self.bar_to_slit(2)), # mm, slit number
#                               (133.901, self.bar_to_slit(6)),
#                               (144.962, self.bar_to_slit(12)),
#                               (129.033, self.bar_to_slit(92))
#                             ])

        pixels = np.array([ (1026.6847023205248, 31.815757489924671),
                            (1031.1293065907989, 31.815757489924671),
                            (1100.0527926274958, 76.568051304306408),
                            (1104.4723170387663, 76.568051304306408),
                            (869.79921202733158, 119.71402079180322),
                            (874.17468615739256, 119.71402079180322),
                            (790.04504261037619, 163.97941699869187),
                            (794.38269316256697, 163.97941699869187),
                            (844.76764696920873, 208.45498973235158),
                            (849.06840834451555, 208.45498973235158),
                            (918.16119587182891, 253.46863795483193),
                            (922.57167115281891, 253.46863795483193),
                            (667.1708458173706, 296.83477802171569),
                            (671.58750566149126, 296.83477802171569),
                            (1210.6743343816352, 342.85304935109269),
                            (1215.1047501727178, 342.85304935109269),
                            (1037.1504738673596, 386.56200191364559),
                            (1041.5376839155629, 386.56200191364559),
                            (1380.9733624348846, 431.75478066748974),
                            (1385.3923546613969, 431.75478066748974),
                            (1392.3137244788115, 476.40898670973735),
                            (1396.5838727543558, 476.40898670973735),
                            (701.99737614209846, 518.12290417047029),
                            (706.31972548163674, 518.12290417047029),
                            (775.43118955263321, 562.76481942553085),
                            (779.76336695630744, 562.76481942553085),
                            (695.39446696825667, 606.9386852721824),
                            (699.68592870194686, 606.9386852721824),
                            (1225.8966927438423, 652.79237015375304),
                            (1230.2681865131638, 652.79237015375304),
                            (1299.3047613957535, 697.52305237026349),
                            (1303.6542557465727, 697.52305237026349),
                            (953.60567493512144, 740.39597570556316),
                            (957.91890612112604, 740.39597570556316),
                            (1027.0080928255736, 784.70486151318767),
                            (1031.3650789520013, 784.70486151318767),
                            (1241.625753053888, 830.10892664282756),
                            (1245.9181149708163, 830.10892664282756),
                            (1266.796600696397, 874.17188807394371),
                            (1271.1082253968038, 874.17188807394371),
                            (1404.8881828516335, 919.85774261912377),
                            (1409.9449171925908, 919.85774261912377),
                            (1325.0207484270156, 963.32163630950686),
                            (1329.3681702175545, 963.32163630950686),
                            (1185.9570564396361, 1007.0164717446025),
                            (1190.2368155733498, 1007.0164717446025),
                            (1306.6628878384579, 1051.9073888851103),
                            (1310.9679069215179, 1051.9073888851103),
                            (1151.3860791138529, 1095.4860726831637),
                            (1155.7367238283309, 1095.4860726831637),
                            (1224.7162502034391, 1140.436681012593),
                            (1229.0598756552718, 1140.436681012593),
                            (904.70409145100268, 1183.267412335555),
                            (908.99297982589781, 1183.267412335555),
                            (978.00762214758913, 1227.9731804278615),
                            (982.41054057239705, 1227.9731804278615),
                            (869.65543493075677, 1271.3564678397893),
                            (873.95299108698168, 1271.3564678397893),
                            (942.99396243198464, 1316.2391922602001),
                            (947.36667894787513, 1316.2391922602001),
                            (1256.7806430753744, 1361.195495916817),
                            (1261.0847133245632, 1361.195495916817),
                            (1330.1305637595844, 1406.3795550431571),
                            (1334.3960288420271, 1406.3795550431571),
                            (1060.9423305503171, 1449.3586376395574),
                            (1065.3182032594575, 1449.3586376395574),
                            (1108.6465868246237, 1493.9756362677167),
                            (1112.9382994207679, 1493.9756362677167),
                            (662.84522896384874, 1536.9734554153649),
                            (667.12956877347722, 1536.9734554153649),
                            (712.5287834914659, 1581.2712766110319),
                            (716.80585127180609, 1581.2712766110319),
                            (956.48762939159371, 1626.1728182002655),
                            (960.9581522740466, 1626.1728182002655),
                            (723.23974640617337, 1670.0165354200499),
                            (727.67208274341931, 1670.0165354200499),
                            (1172.3594885486252, 1715.8650599984883),
                            (1176.8341929555718, 1715.8650599984883),
                            (1015.7329598422145, 1759.5446833817025),
                            (1020.1920698607528, 1759.5446833817025),
                            (935.82358262678224, 1803.5644982617907),
                            (940.3126440130676, 1803.5644982617907),
                            (989.98752991018682, 1847.9507718487364),
                            (994.40511955530712, 1847.9507718487364),
                            (1278.2218422583971, 1892.8072028048214),
                            (1282.7070969966558, 1892.8072028048214),
                            (1351.5377751257745, 1938.5923374638328),
                            (1355.9221844080257, 1938.5923374638328),
                            (1171.5812780061251, 1981.4914424153424),
                            (1176.0817255338613, 1981.4914424153424),
                            ])

        physical = np.array([ (139.917, self.bar_to_slit(92)),
                              (139.41,  self.bar_to_slit(91)),
                              (130.322, self.bar_to_slit(90)),
                              (129.815, self.bar_to_slit(89)),
                              (160.334, self.bar_to_slit(88)),
                              (159.827, self.bar_to_slit(87)),
                              (170.738, self.bar_to_slit(86)),
                              (170.231, self.bar_to_slit(85)),
                              (163.579, self.bar_to_slit(84)),
                              (163.072, self.bar_to_slit(83)),
                              (153.983, self.bar_to_slit(82)),
                              (153.476, self.bar_to_slit(81)),
                              (186.718, self.bar_to_slit(80)),
                              (186.211, self.bar_to_slit(79)),
                              (115.773, self.bar_to_slit(78)),
                              (115.266, self.bar_to_slit(77)),
                              (138.413, self.bar_to_slit(76)),
                              (137.906, self.bar_to_slit(75)),
                              (93.508,  self.bar_to_slit(74)),
                              (93.001,  self.bar_to_slit(73)),
                              (92.021,  self.bar_to_slit(72)),
                              (91.514,  self.bar_to_slit(71)),
                              (182.097, self.bar_to_slit(70)),
                              (181.59,  self.bar_to_slit(69)),
                              (172.502, self.bar_to_slit(68)),
                              (171.995, self.bar_to_slit(67)),
                              (182.905, self.bar_to_slit(66)),
                              (182.398, self.bar_to_slit(65)),
                              (113.665, self.bar_to_slit(64)),
                              (113.158, self.bar_to_slit(63)),
                              (104.069, self.bar_to_slit(62)),
                              (103.562, self.bar_to_slit(61)),
                              (149.161, self.bar_to_slit(60)),
                              (148.654, self.bar_to_slit(59)),
                              (139.566, self.bar_to_slit(58)),
                              (139.059, self.bar_to_slit(57)),
                              (111.528, self.bar_to_slit(56)),
                              (111.021, self.bar_to_slit(55)),
                              (108.22,  self.bar_to_slit(54)),
                              (107.713, self.bar_to_slit(53)),
                              (90.189,  self.bar_to_slit(52)),
                              (89.681,  self.bar_to_slit(51)),
                              (100.593, self.bar_to_slit(50)),
                              (100.086, self.bar_to_slit(49)),
                              (118.731, self.bar_to_slit(48)),
                              (118.223, self.bar_to_slit(47)),
                              (102.94,  self.bar_to_slit(46)),
                              (102.432, self.bar_to_slit(45)),
                              (123.212, self.bar_to_slit(44)),
                              (122.704, self.bar_to_slit(43)),
                              (113.615, self.bar_to_slit(42)),
                              (113.108, self.bar_to_slit(41)),
                              (155.354, self.bar_to_slit(40)),
                              (154.847, self.bar_to_slit(39)),
                              (145.759, self.bar_to_slit(38)),
                              (145.251, self.bar_to_slit(37)),
                              (159.887, self.bar_to_slit(36)),
                              (159.38,  self.bar_to_slit(35)),
                              (150.292, self.bar_to_slit(34)),
                              (149.785, self.bar_to_slit(33)),
                              (109.338, self.bar_to_slit(32)),
                              (108.83,  self.bar_to_slit(31)),
                              (99.742,  self.bar_to_slit(30)),
                              (99.235,  self.bar_to_slit(29)),
                              (134.842, self.bar_to_slit(28)),
                              (134.335, self.bar_to_slit(27)),
                              (128.616, self.bar_to_slit(26)),
                              (128.109, self.bar_to_slit(25)),
                              (186.778, self.bar_to_slit(24)),
                              (186.271, self.bar_to_slit(23)),
                              (180.272, self.bar_to_slit(22)),
                              (179.765, self.bar_to_slit(21)),
                              (148.417, self.bar_to_slit(20)),
                              (147.91,  self.bar_to_slit(19)),
                              (178.822, self.bar_to_slit(18)),
                              (178.314, self.bar_to_slit(17)),
                              (120.197, self.bar_to_slit(16)),
                              (119.689, self.bar_to_slit(15)),
                              (140.601, self.bar_to_slit(14)),
                              (140.094, self.bar_to_slit(13)),
                              (151.005, self.bar_to_slit(12)),
                              (150.498, self.bar_to_slit(11)),
                              (143.947, self.bar_to_slit(10)),
                              (143.44,  self.bar_to_slit(9)),
                              (106.313, self.bar_to_slit(8)),
                              (105.806, self.bar_to_slit(7)),
                              (96.717,  self.bar_to_slit(6)),
                              (96.21,   self.bar_to_slit(5)),
                              (120.202, self.bar_to_slit(4)),
                              (119.695, self.bar_to_slit(3)),
                              ])

        tick = dt.now()
        self.fit_transforms(pixels, physical)
        tock = dt.now()
        elapsed = (tock-tick).total_seconds()
        print('  Fitted transforms in {:.3f} s'.format(elapsed))

        ## Determine slit angle and bar center to center distance in pixels
        ## from the transformation and the known longslit positions
        ##   in longslit, bar 02 is at 145.472
        ##   in longslit, bar 92 is at 129.480
        physical = [ [145.472, self.bar_to_slit(2)],
                     [129.480, self.bar_to_slit(92)] ]
        pixels = self.physical_to_pixel(physical)
        dx = pixels[1][0] - pixels[0][0]
        dy = pixels[0][1] - pixels[1][1]
        self.slit_angle_pix = np.arctan(dx/dy)
        print("Slit Angle on CCD = {:.3f} deg".format(self.slit_angle_pix * 180./np.pi))
        self.slit_height_pix = dy / (self.bar_to_slit(92) - self.bar_to_slit(2))
        print("Slit Height on CCD = {:.3f} pix".format(self.slit_height_pix))


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
        fr1 = Widgets.Frame("Image the CSU Mask")
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
        ## Full Mask Initialization
        ## -----------------------------------------------------
#         fr3 = Widgets.Frame("Full Mask Initialization")
# 
#         captions = [
#             ("Fast Init from Keywords", 'button'),
#             ("Fast Init from Header", 'button'),
#             ("Fast Init from Image Analysis", 'button'),
#             ("Full Init", 'button'),
#             ]
# 
#         w, b = Widgets.build_info(captions, orientation=orientation)
#         self.w.update(b)
# 
#         b.fast_init_from_keywords.add_callback('activated', lambda w: self.fast_init_from_keywords_cb())
#         b.fast_init_from_header.add_callback('activated', lambda w: self.fast_init_from_header_cb())
#         b.fast_init_from_image_analysis.add_callback('activated', lambda w: self.fast_init_from_image_analysis_cb())
#         b.full_init.add_callback('activated', lambda w: self.full_init_cb())
# 
# 
#         fr3.set_widget(w)
#         vbox.add_widget(fr3, stretch=0)


        ## -----------------------------------------------------
        ## Bar Control
        ## -----------------------------------------------------
#         tw_bar_control = Widgets.TextArea(wrap=True, editable=False)
#         tw_bar_control.set_font(self.msg_font)
#         self.tw_bar_control = tw_bar_control

        # Frame for instructions and add the text widget with another
        # blank widget to stretch as needed to fill emp
        fr4 = Widgets.Frame("CSU Bar Control")
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
        b.bar_dist.set_text('{:+.1f}'.format(bar_dist))
        b.set_bar_dist.set_text(str(bar_dist))
        b.set_bar_dist.add_callback('activated', self.set_bar_dist_cb)
        b.set_bar_dist.set_tooltip("Set distance to move bar")

        b.move_to_open.set_tooltip("Move bar to open position before initialization")
        move_to_open = self.settings.get('move_to_open', False)
        b.move_to_open.set_state(move_to_open)
        b.move_to_open.add_callback('activated', self.move_to_open_cb)
        b.initialize_bar.add_callback('activated', lambda w: self.initialize_bar_cb())

        b.move_bar.add_callback('activated', lambda w: self.move_bar_cb())


        fr4.set_widget(w)
        vbox.add_widget(fr4, stretch=0)


        ## -----------------------------------------------------
        ## Bar Overlay
        ## -----------------------------------------------------
        fr5 = Widgets.Frame("Bar Overlay")

        captions = (('Overlay bar positions from csu_bar_state file', 'button'),
                    ('Overlay bar positions from FITS header', 'button'),
                    ('Clear', 'button'))
    
        w, b = Widgets.build_info(captions, orientation=orientation)
        self.w.update(b)

        b.overlay_bar_positions_from_csu_bar_state_file.add_callback('activated',
                   lambda w: self.overlaybars_from_file())
        b.overlay_bar_positions_from_fits_header.add_callback('activated',
                   lambda w: self.overlaybars_from_header())

        b.clear.add_callback('activated', lambda w: self.clear_canvas())
        fr5.set_widget(w)
        vbox.add_widget(fr5, stretch=0)


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
        # start ruler drawing operation
        p_canvas = self.fitsimage.get_canvas()
        try:
            obj = p_canvas.get_object_by_tag(self.layertag)

        except KeyError:
            # Add ruler layer
            p_canvas.add(self.canvas, tag=self.layertag)

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
        return 'CSU Initializer Plugin'


    ## ------------------------------------------------------------------
    ##  Coordinate Transformation Utilities
    ## ------------------------------------------------------------------
    def slit_to_bars(self, slit):
        return (slit*2-1, slit*2)

    def bar_to_slit(self, bar):
        return int((bar+1)/2)

    def pad(self, x):
        return np.hstack([x, np.ones((x.shape[0], 1))])

    def unpad(self, x):
        return x[:,:-1]

    def fit_transforms(self, pixels, physical):
        assert pixels.shape[1] == 2
        assert physical.shape[1] == 2
        assert pixels.shape[0] == physical.shape[0]

        # Pad the data with ones, so that our transformation can do translations too
        n = pixels.shape[0]
        pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
        unpad = lambda x: x[:,:-1]
        X = pad(pixels)
        Y = pad(physical)

        # Solve the least squares problem X * A = Y
        # to find our transformation matrix A
        A, res, rank, s = np.linalg.lstsq(X, Y)
        Ainv, res, rank, s = np.linalg.lstsq(Y, X)
        A[np.abs(A) < 1e-10] = 0
        Ainv[np.abs(A) < 1e-10] = 0
        self.Apixel_to_physical = A
        self.Aphysical_to_pixel = Ainv

    def pixel_to_physical(self, x):
        x = np.array(x)
        result = self.unpad(np.dot(self.pad(x), self.Apixel_to_physical))
        return result

    def physical_to_pixel(self, x):
        x = np.array(x)
        result =  self.unpad(np.dot(self.pad(x), self.Aphysical_to_pixel))
        return result

    ## ------------------------------------------------------------------
    ##  Read Bar Positions and Overlay
    ## ------------------------------------------------------------------
    def read_csu_bar_state(self, filename):
        with open(filename, 'r') as FO:
            lines = FO.readlines()
        bars = {}
        state = {}
        state_trans = {0: 'OK', 1: 'SETUP', 2: 'MOVING', -3: 'ERROR'}
        for line in lines:
            barno, pos, statestr = line.strip('\n').split(',')
            bars[int(barno)] = float(pos)
            state[int(barno)] = state_trans[int(statestr)]
        return bars, state

    def read_bars_from_header(self, header):
        bars = {}
        for i in range(1,93):
            bars[i] = float(header['B{:02d}POS'.format(i)])
        return bars

    def overlaybars(self, bars, state=None):
        colormap = {'OK': 'green', 'ERROR': 'red'}
        draw_height = 0.45
        for j in range(1, 47):
            b1, b2 = self.slit_to_bars(j)

            physical1 = [ [8.0, j-draw_height],
                          [8.0, j+draw_height],
                          [bars[b1], j+draw_height],
                          [bars[b1], j-draw_height] ]
            physical1 = np.array(physical1)
            pixels1 = self.physical_to_pixel(physical1)
            pixels1[2][0] += draw_height * self.slit_height_pix * np.sin(self.slit_angle_pix)
            pixels1[3][0] -= draw_height * self.slit_height_pix * np.sin(self.slit_angle_pix)

            physical2 = [ [270.4+2.0, j-draw_height],
                          [270.4+2.0, j+draw_height],
                          [bars[b2], j+draw_height],
                          [bars[b2], j-draw_height] ]
            physical2 = np.array(physical2)
            pixels2 = self.physical_to_pixel(physical2)
            pixels2[2][0] += draw_height * self.slit_height_pix * np.sin(self.slit_angle_pix)
            pixels2[3][0] -= draw_height * self.slit_height_pix * np.sin(self.slit_angle_pix)

            try:
                b1color = colormap[state[b1]]
            except:
                b1color = 'blue'
            try:
                b2color = colormap[state[b2]]
            except:
                b2color = 'blue'

            self.canvas.add(self.dc.Polygon(pixels1, color=b1color))
            self.canvas.add(self.dc.Polygon(pixels2, color=b2color))
            x1, y1 = self.physical_to_pixel([[14.0, j+0.3]])[0]
            self.canvas.add(self.dc.Text(x1, y1, '{:d}'.format(b1),
                                         fontsize=10, color='white'))
            x2, y2 = self.physical_to_pixel([[270.4-2.0, j+0.3]])[0]
            self.canvas.add(self.dc.Text(x2, y2, '{:d}'.format(b2),
                                         fontsize=10, color='white'))

    def overlaybars_from_file(self):
        bars, state = self.read_csu_bar_state('/Users/jwalawender/MOSFIRE_Test_Data/20170414/csu_bar_state')
        self.overlaybars(bars, state=state)

    def overlaybars_from_header(self):
        ## Get header
        channel = self.fv.get_channel(self.chname)
        image = channel.get_current_image()
        header = image.get_header()
        bars = self.read_bars_from_header(header)
        self.overlaybars(bars)

    def clear_canvas(self):
        self.canvas.delete_all_objects()

    ## ------------------------------------------------------------------
    ##  Button Callbacks
    ## ------------------------------------------------------------------
    def set_bar_num_cb(self, w):
        bar_num = int(w.get_text())
        self.settings.set(bar_num=bar_num)
        self.w.bar_num.set_text('{:2d}'.format(bar_num))

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
        self.w.bar_dist.set_text('{:+.1f}'.format(bar_dist))

    def move_bar_cb(self):
        pass

    def load_cb(self):
        self.mfilesel.popup('Load bar file', self.overlaybars,
                            initialdir='.', filename='txt files (*.txt)')



