from gettext import gettext as _

from gi.repository import Adw
from gi.repository import Gtk, Gdk, GLib, Gio

from collections import defaultdict

from .units import *
from .conversion import Conversion

@Gtk.Template(resource_path='/io/github/heidefinnischen/cuneo/conversion-stack.ui')
class ConversionStack(Gtk.Box):
    __gtype_name__ = "ConversionStack"

    root_box = Gtk.Template.Child()

    # Converter Widgets
    unit_type_button = Gtk.Template.Child()
    unit_type_popover = Gtk.Template.Child()
    unit_type_box = Gtk.Template.Child()
    unit_type_icon = Gtk.Template.Child()

    from_unit_entry = Gtk.Template.Child()
    from_unit_popover = Gtk.Template.Child()
    from_unit_box = Gtk.Template.Child()
    from_unit_label = Gtk.Template.Child()

    to_unit_entry = Gtk.Template.Child()
    to_unit_popover = Gtk.Template.Child()
    to_unit_box = Gtk.Template.Child()
    to_unit_label = Gtk.Template.Child()




    def __init__(self, main_window, **kwargs):
        super().__init__(**kwargs)

        self.main_window = main_window

        child = self.root_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.root_box.remove(child)
            self.append(child)
            child = next_child

        self.conversion = Conversion()

        self.conversion_types = CONVERSION_TYPES
        self.temperature_units = TEMPERATURE_UNITS

        initial_category = 'length'
        self.state = ConverterState()
        self.state.set_category(initial_category)
        self.populate_type_buttons(initial_category)

        icon_name = UNIT_TYPE_ICONS.get(initial_category, "item-missing-symbolic") #item missing is fallback
        self.unit_type_icon.set_from_icon_name(icon_name)
        self.populate_units(self.conversion_types[initial_category], self.from_unit_box, self.on_from_unit_selected, active_unit_id=self.state.from_unit)
        self.populate_units(self.conversion_types[initial_category], self.to_unit_box, self.on_to_unit_selected, active_unit_id=self.state.to_unit)

        self.conversion_history = []

    def update_unit_labels(self):
            def get_short_unit_label(container):
                child = container.get_first_child()
                while child:
                    if isinstance(child, Gtk.ToggleButton) and child.get_active():
                        label_box = child.get_child()
                        if isinstance(label_box, Gtk.Box):
                            label = label_box.get_first_child()
                            found_one = False
                            while label:
                                if isinstance(label, Gtk.Label):
                                    if found_one:
                                        return label.get_text()  # This is the second label (short name)
                                    found_one = True
                                label = label.get_next_sibling()
                    child = child.get_next_sibling()
                return "—"

            self.from_unit_label.set_text(get_short_unit_label(self.from_unit_box))
            self.to_unit_label.set_text(get_short_unit_label(self.to_unit_box))



    def populate_units(self, units_dict, container, on_clicked_handler, active_unit_id=None):
        self.clear_container(container)

        # Group units by tag
        grouped_units = defaultdict(dict)
        for unit_id, values in units_dict.items():
            tag = values[4] if len(values) > 4 else None
            grouped_units[tag][unit_id] = values

        self.toggle_buttons = []
        first_button = None
        is_first_category = True  # Track if we’re processing the first group

        for tag, units_in_tag in grouped_units.items():
            if tag in UNIT_TAGS:
                display_name, subtitle = UNIT_TAGS[tag]
            else:
                display_name = ""
                subtitle = ""

            if not (is_first_category and tag == None):
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True)
                box.set_margin_top(6)
                box.set_margin_bottom(6)

                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_valign(Gtk.Align.CENTER)
                separator.set_size_request(10, 1)
                box.append(separator)

                # Main category label
                category_label = Gtk.Label(label=display_name)
                category_label.set_halign(Gtk.Align.START)
                category_label.add_css_class("caption")
                category_label.add_css_class("dimmed")
                box.append(category_label)

                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_hexpand(True)  # fill the remaining space
                separator.set_valign(Gtk.Align.CENTER)
                box.append(separator)

                # Subtitle label (smaller, dimmed)
                subtitle_label = Gtk.Label(label=subtitle)
                subtitle_label.set_halign(Gtk.Align.END)
                subtitle_label.add_css_class("caption")
                subtitle_label.add_css_class("dimmed")
                box.append(subtitle_label)

                separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                separator.set_valign(Gtk.Align.CENTER)
                separator.set_size_request(10, 1)
                box.append(separator)

                container.append(box)

            is_first_category = False  # After first loop

            for unit_id, values in units_in_tag.items():
                singular, plural, short = values[:3]

                button = Gtk.ToggleButton()
                button.set_name(unit_id)
                button.add_css_class("flat")

                row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True)
                label_left = Gtk.Label(label=plural)
                label_left.set_hexpand(True)
                label_left.set_halign(Gtk.Align.START)
                label_left.add_css_class("body")
                label_left.set_margin_end(30)

                label_right = Gtk.Label(label=short)
                label_right.set_halign(Gtk.Align.END)
                label_right.add_css_class("dimmed")

                row_box.append(label_left)
                row_box.append(label_right)
                button.set_child(row_box)

                button.connect("clicked", on_clicked_handler)

                if first_button is None:
                    first_button = button
                else:
                    button.set_group(first_button)

                if active_unit_id:
                    if unit_id == active_unit_id:
                        button.set_active(True)
                else:
                    if first_button == button:
                        button.set_active(True)

                container.append(button)
                self.toggle_buttons.append(button)

        self.update_unit_labels()



    # Update UI in Converter
    @Gtk.Template.Callback()
    def on_convert_entry_changed(self, entry):
        text = entry.get_text()
        try:
            self.state.input_value = float(text)
        except ValueError:
            self.state.input_value = None
        self.update_conversion_result()

    def on_to_unit_selected(self, button):
        unit_id = button.get_name()

        self.state.to_unit = unit_id
        self.update_unit_labels()

        self.to_unit_popover.hide()  # hide popover after selection if desired
        self.update_conversion_result()

    def on_from_unit_selected(self, button):
        unit_id = button.get_name()

        self.state.from_unit = unit_id
        self.update_unit_labels()

        self.from_unit_popover.hide()  # hide popover after selection if desired
        self.update_conversion_result()


    # Update UI when inverting units
    @Gtk.Template.Callback()
    def on_invert_units_clicked(self, param):

        self.state.invert_units()

        if self.from_unit_entry.get_text() != None and self.from_unit_entry.get_text() != "":
            self.from_unit_entry.set_text(str(self.conversion.format_conversion_result(round(self.state.input_value, 6))))
            self.to_unit_entry.set_text(str(self.conversion.format_conversion_result(round(self.state.result, 6))))

        # Update unit buttons (just by name, based on model)
        self.activate_button_by_unit(self.from_unit_box, self.state.from_unit)
        self.activate_button_by_unit(self.to_unit_box, self.state.to_unit)

        # Refresh any labels if needed
        self.update_unit_labels()

    def update_conversion_result(self):
        value = self.state.input_value
        if value is None:
            self.to_unit_entry.set_text("")
            return

        from_unit = self.state.from_unit
        to_unit = self.state.to_unit
        category = self.state.selected_category

        if not from_unit or not to_unit or not category:
            self.update_convert_result_text(None)
            return

        if value != None and value != "":
            result = self.conversion.convert_value(value, from_unit, to_unit, category, self.conversion_types)
            self.update_convert_result_text(result)
            self.update_conv_history(category, self.from_unit_entry.get_text(), from_unit, self.to_unit_entry.get_text(), to_unit)


    def populate_type_buttons(self, active_type_id=None):
        # Clear previous buttons
        child = self.unit_type_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.unit_type_box.remove(child)
            child = next_child

        first_button = None
        for type_id in sorted(self.conversion_types):
            title = UNIT_TYPE_NAMES.get(type_id, type_id.title())

            label = Gtk.Label(label=title)
            label.set_halign(Gtk.Align.START)
            label.set_hexpand(True)
            label.add_css_class("body")
            label.set_margin_end(30)

            icon_name = UNIT_TYPE_ICONS.get(type_id, "item-missing-symbolic")
            icon = Gtk.Image.new_from_icon_name(icon_name)
            icon.set_halign(Gtk.Align.END)

            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            box.append(label)
            box.append(icon)

            # Create button with box as child
            button = Gtk.ToggleButton()
            button.set_name(type_id)
            button.add_css_class("flat")
            button.set_child(box)
            button.connect("clicked", self.on_type_button_clicked)

            if first_button is None:
                first_button = button
            else:
                button.set_group(first_button)

            if active_type_id:
                if type_id == active_type_id:
                    button.set_active(True)
            else:
                if first_button == button:
                    button.set_active(True)

            self.unit_type_box.append(button)

    def on_type_button_clicked(self, button):
        selected_type = button.get_name()

        self.state.set_category(selected_type)

        units_dict = self.conversion_types.get(selected_type)
        if units_dict:
            self.populate_units(units_dict, self.from_unit_box, self.on_from_unit_selected, active_unit_id=self.state.from_unit)
            self.populate_units(units_dict, self.to_unit_box, self.on_to_unit_selected, active_unit_id=self.state.to_unit)

        icon_name = UNIT_TYPE_ICONS.get(selected_type, "item-missing-symbolic") #item missing is fallback
        self.unit_type_icon.set_from_icon_name(icon_name)

        self.state.update()
        self.from_unit_entry.set_text("")
        self.to_unit_entry.set_text("")

    def update_convert_result_text(self, result):
            if result != None and result != "":
                try:
                    self.state.result = result
                    output = self.conversion.format_conversion_result(round(result, 6))
                    self.to_unit_entry.set_text(str(output))
                except Exception as e:
                    self.state.result = None
                    print("Conversion failed:", e)
                    self.to_unit_entry.set_text("")
            else:
                self.state.result = None
                self.to_unit_entry.set_text("")

    def activate_button_by_unit(self, container, unit_name):
        child = container.get_first_child()
        while child is not None:
            if child.get_name() == unit_name:
                child.set_active(True)
                return
            child = child.get_next_sibling()

    @Gtk.Template.Callback()
    def on_entry_focus(self, entry, param):
        def select_all():
            entry.select_region(0, -1)

        GLib.idle_add(select_all)

    def clear_container(self, container):
        child = container.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            container.remove(child)
            child = next_child

    def update_conv_history(self, unit_type, input_val, from_unit, result_val, to_unit):
        new_list = [unit_type, input_val, from_unit, result_val, to_unit]
        try:
            if not self.conversion_history or new_list != self.conversion_history[-1]:
                self.conversion_history.append(new_list)
                if self.main_window.history_window:
                    self.main_window.history_window.populate_conv_history(self.conversion_history)
        except:
            self.conversion_history.append(new_list)
            pass

class ConverterState:

    DEFAULT_UNITS = {
        "length": ("cm", "in"),
        "speed": ("kmh", "mph"),
        "temperature": ("c", "f"),
        "area": ("m2","ft2"),
        "time": ("h","d"),
        "mass": ("kg","lb"),
        "volume": ("l","gal"),
        "data": ("mb","mbit"),
        "pressure": ("bar","psi"),
        "energy": ("j","cal"),
        "frequency": ("hz","rpm"),
    }

    def __init__(self):
        self.selected_category = 'length' #Fallback
        self.input_value = None
        self.result = None
        self.update()

    def update(self):
        self.from_unit, self.to_unit = self.DEFAULT_UNITS.get(self.selected_category, ("", ""))
        self.input_value = ""
        self.result = ""

    def set_category(self, category):
        self.selected_category = category
        self.update()

    def invert_units(self):
        self.from_unit, self.to_unit = self.to_unit, self.from_unit
        self.input_value, self.result = self.result, self.input_value

    # Not in use currently, history window directly clears list, should change though
    def clear_conversion_history(self):
        self.conversion_history.clear()
