import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib

@Gtk.Template(resource_path='/io/github/heidefinnischen/cuneo/history-window.ui')
class HistoryWindow(Adw.Window):
    __gtype_name__ = 'HistoryWindow'

    calc_history_box = Gtk.Template.Child()
    calc_history_scrolled = Gtk.Template.Child()
    conv_history_box = Gtk.Template.Child()
    conv_history_scrolled = Gtk.Template.Child()
    window_title = Gtk.Template.Child()

    history_mode_stack = Gtk.Template.Child()

    clear_button = Gtk.Template.Child()

    def __init__(self, app, main_window):
        super().__init__(application=app)

        self.main_window = main_window

        self.set_default_size(300, 440)  # initial size
        self.set_size_request(300, 440)  # minimum size

        self.window_title.set_label("Calculation History")

    def clear_conv_history(self):
        child = self.conv_history_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.conv_history_box.remove(child)
            child = next_child

    def populate_conv_history(self, previous_conversions):
        # Clear previous buttons
        self.clear_conv_history()

        first_entry = True

        for unit_type, conversion_input, in_unit, conversion_result, out_unit in previous_conversions:

            if not first_entry:
                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_valign(Gtk.Align.CENTER)
                self.conv_history_box.append(separator)

            insert_icon = Gtk.Image.new_from_icon_name("arrow-into-box-flipped-symbolic")
            insert_button = Gtk.Button()
            insert_button.set_child(insert_icon)
            insert_button.add_css_class("flat")
            insert_button.add_css_class("dim-hover")
            #insert_button.connect("clicked", self.on_insert_clicked)

            conv_in_button = Gtk.Button()
            conv_in_box = Gtk.Box()
            conv_in_box.set_spacing(4)
            conv_in_button.add_css_class("flat")
            conv_in_button.connect("clicked", self.on_button_child_to_clipboard)
            conv_in_button.set_hexpand(True)
            conv_in_button.set_halign(Gtk.Align.START)
            conv_in_val = Gtk.Label(label=conversion_input)
            conv_in_unit = Gtk.Label(label=in_unit)
            conv_in_unit.add_css_class("raised")
            conv_in_box.append(conv_in_val)
            conv_in_box.append(conv_in_unit)
            conv_in_button.set_child(conv_in_box)

            arrow_icon = Gtk.Image.new_from_icon_name("network-transmit-receive-symbolic")
            arrow_icon.add_css_class("heading")
            arrow_icon.add_css_class("dimmed")
            arrow_icon.set_halign(Gtk.Align.END)

            conv_out_button = Gtk.Button()
            conv_out_box = Gtk.Box()
            conv_out_box.set_spacing(4)
            conv_out_button.add_css_class("flat")
            conv_out_button.connect("clicked", self.on_button_child_to_clipboard)
            conv_out_button.set_halign(Gtk.Align.END)
            conv_out_val = Gtk.Label(label=conversion_result)
            conv_out_unit = Gtk.Label(label=out_unit)
            conv_out_box.append(conv_out_val)
            conv_out_box.append(conv_out_unit)
            conv_out_button.set_child(conv_out_box)

            item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            item_box.append(insert_button)
            item_box.append(conv_in_button)
            item_box.append(arrow_icon)
            item_box.append(conv_out_button)

            self.conv_history_box.append(item_box)

            self.scroll_to_bottom(self.conv_history_box, self.conv_history_scrolled)

            if first_entry == True:
                first_entry = False

    def clear_calc_history(self):
        child = self.calc_history_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.calc_history_box.remove(child)
            child = next_child

    def populate_calc_history(self, previous_calculations):
        # Clear previous buttons
        self.clear_calc_history()

        first_entry = True

        for calculation_input, calculation_result in previous_calculations:

            if not first_entry:
                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_valign(Gtk.Align.CENTER)
                self.calc_history_box.append(separator)

            insert_icon = Gtk.Image.new_from_icon_name("arrow-into-box-flipped-symbolic")
            insert_button = Gtk.Button()
            insert_button.set_child(insert_icon)
            insert_button.add_css_class("flat")
            insert_button.add_css_class("dim-hover")
            insert_button.connect("clicked", self.on_insert_clicked)

            calc_in_button = Gtk.Button(label=calculation_input)
            calc_in_button.add_css_class("flat")
            calc_in_button.connect("clicked", self.on_button_to_clipboard)
            calc_in_button.set_hexpand(True)
            calc_in_button.set_halign(Gtk.Align.START)

            equation_label = Gtk.Label(label="=")
            equation_label.add_css_class("heading")
            equation_label.add_css_class("dimmed")
            equation_label.set_halign(Gtk.Align.END)

            calc_result_button = Gtk.Button(label=calculation_result)
            calc_result_button.add_css_class("flat")
            calc_result_button.connect("clicked", self.on_button_to_clipboard)
            calc_result_button.set_halign(Gtk.Align.END)

            item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            item_box.append(insert_button)
            item_box.append(calc_in_button)
            item_box.append(equation_label)
            item_box.append(calc_result_button)

            self.calc_history_box.append(item_box)
            calc_result_button.grab_focus()

            if first_entry == True:
                first_entry = False

        self.scroll_to_bottom(self.calc_history_box, self.calc_history_scrolled)


    def scroll_to_bottom(self, history_box, scrolled_box):
        self.history_box = history_box
        self.scrolled_box = scrolled_box
        # Ensure widgets are realized and laid out
        self.history_box.queue_allocate()

        def _delay_scroll():
            # Scroll to bottom of GtkScrolledWindow
            vadjustment = self.scrolled_box.get_vadjustment()
            vadjustment.set_value(vadjustment.get_upper() - vadjustment.get_page_size())

        GLib.idle_add(_delay_scroll)

    def on_button_child_to_clipboard(self, button):
        # Get the first child of the button (the box)
        box = button.get_first_child()
        if not box:
            return  # no child

        # Get the label inside the box
        label = box.get_first_child()
        if not label:
            return  # no label found

        # Get text from the label
        text = label.get_text()

        # Put text on clipboard
        clipboard = button.get_display().get_clipboard()
        content_provider = Gdk.ContentProvider.new_for_value(text)
        clipboard.set_content(content_provider)

    def on_button_to_clipboard(self, button):
        text = button.get_label()
        clipboard = button.get_display().get_clipboard()
        content_provider = Gdk.ContentProvider.new_for_value(text)
        clipboard.set_content(content_provider)

    def on_insert_clicked(self, button):
        # Get the parent box (the container)
        box = button.get_parent()
        if not box:
            return

        # Start with the first child of the box
        child = box.get_first_child()

        while child:
            # Skip the insert button itself
            if isinstance(child, Gtk.Button) and child is not button:
                label = child.get_label()
                if label:
                    self.main_window.calc_entry.set_text(label)
                    break
            child = child.get_next_sibling()

    def update_visible_stack(self, visible):
        if visible == "convert_history":
            self.history_mode_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
            self.history_mode_stack.set_visible_child_name("convert_history")
            self.remove_css_class("smooth-transition")
            self.add_css_class("yellow-ruler")
            self.window_title.set_label("Conversion History")
            self.scroll_to_bottom(self.conv_history_box, self.conv_history_scrolled)
        else:
            self.history_mode_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)
            self.history_mode_stack.set_visible_child_name("calculate_history")
            self.add_css_class("smooth-transition")
            self.remove_css_class("yellow-ruler")
            self.window_title.set_label("Calculation History")
            self.scroll_to_bottom(self.calc_history_box, self.calc_history_scrolled)

    @Gtk.Template.Callback()
    def on_clear_history_button_clicked(self, button):
        if self.history_mode_stack.get_visible_child_name() == "convert_history":
            self.main_window.conv_stack.conversion_history.clear()
            self.clear_conv_history()
        else:
            self.main_window.calc_stack.calculation_history.clear()
            self.clear_calc_history()
        #self.set_default_size(300, 440)
