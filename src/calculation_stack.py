from gettext import gettext as _

from gi.repository import Adw
from gi.repository import Gtk, Gdk, GLib, Gio

from .magic import tokenize, Parser, evaluate, sanitize_expression, format_result, ast_to_string, replace_superscripts, replace_display_operators

error_message = _("Invalid")

@Gtk.Template(resource_path='/io/github/heidefinnischen/cuneo/calculation-stack.ui')
class CalculationStack(Gtk.Box):
    __gtype_name__ = "CalculationStack"

    root_box = Gtk.Template.Child()

    # Calculator Widgets
    calc_entry = Gtk.Template.Child()
    calc_result = Gtk.Template.Child()
    calc_equation = Gtk.Template.Child()
    calc_equation_box = Gtk.Template.Child()
    operator_menu = Gtk.Template.Child()
    expression_button = Gtk.Template.Child()
    copy_button = Gtk.Template.Child()


    def __init__(self, main_window, **kwargs):
        super().__init__(**kwargs)

        self.main_window = main_window

        child = self.root_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.root_box.remove(child)
            self.append(child)
            child = next_child

        self.calculation_history = []
        self.history_update_timeout_id = None
        self.pending_history_entry = None

        self._calc_changed_handler_id = self.calc_entry.connect("changed", self.on_entry_changed)

################### CALCULATOR AREA

    @Gtk.Template.Callback()
    def on_copy_button_clicked(self, button):
        text = self.calc_result.get_text()
        clipboard = self.calc_result.get_display().get_clipboard()
        content_provider = Gdk.ContentProvider.new_for_value(text)
        clipboard.set_content(content_provider)

    # Update Math
    @Gtk.Template.Callback()
    def on_entry_changed(self, entry):
        raw_expression = self.calc_entry.get_text()
        cursor_pos = entry.get_position()

        filtered_expression, new_cursor_pos = self.filter_calc_entry(raw_expression, cursor_pos)

        if filtered_expression != raw_expression:
            entry.handler_block(self._calc_changed_handler_id)
            entry.set_text(filtered_expression)
            entry.set_position(new_cursor_pos)
            entry.handler_unblock(self._calc_changed_handler_id)

            # Use filtered expression going forward
            raw_expression = filtered_expression

        expression = sanitize_expression(raw_expression)

        try:
            expression = replace_display_operators(expression)
            expression = replace_superscripts(expression)
            tokens = tokenize(expression)
            ast = Parser(tokens).parse()
            result = evaluate(ast)
            output = format_result(result)

            if output.strip() != expression.strip():
                self.calc_result.set_text(output)

                # Calculate pixel width of the text in the entry
                layout = self.calc_entry.create_pango_layout(raw_expression)
                width, _ = layout.get_pixel_size()

                # Add some padding/margin adjustment for spacing
                self.calc_equation_box.set_margin_start(width + 18)
                self.calc_equation.set_visible(True)
                self.copy_button.set_visible(True)
                self.calc_entry.add_css_class("entry-pad")
                self.calc_equation_box.add_css_class("entry-pad")
                self.expression_button.set_visible(True)


                # Update interpreted expression preview
                interpreted = ast_to_string(ast)
                self.expression_button.set_label(interpreted)

                # Add calculation to calculator history
                self.update_calc_history(expression.strip(), output.strip())

            else:
                # Hide result and UI elements if no meaningful difference
                self.calc_result.set_text("")
                self.calc_equation.set_visible(False)
                self.copy_button.set_visible(False)
                self.expression_button.set_label(error_message)
                self.cancel_pending_history_update()

        except (SyntaxError, ValueError, ZeroDivisionError):
            self.calc_result.set_text("")
            self.expression_button.set_label(error_message)
            self.calc_equation.set_visible(False)
            self.copy_button.set_visible(False)
            self.cancel_pending_history_update()

    def filter_calc_entry(self, text, cursor_pos):
        replacements = {
            'x': '×',
            'X': '×',
            '*': '×',
            '/': '÷',
            ':': '÷',
            '-': '−'
        }

        result = ''
        new_cursor_pos = cursor_pos
        i = 0

        while i < len(text):
            ch = text[i]
            replacement = replacements.get(ch, ch)
            result += replacement

            # Adjust cursor position
            if i < cursor_pos:
                new_cursor_pos += len(replacement) - len(ch)

            i += 1

        return result, new_cursor_pos


    def update_calc_history(self, expression, output):
        self.pending_history_entry = [expression, output]

        # If a timeout is already scheduled, reset it
        if self.history_update_timeout_id is not None:
            GLib.source_remove(self.history_update_timeout_id)

        # Schedule history update in 1 second (1000 ms)
        self.history_update_timeout_id = GLib.timeout_add(
            750, self._commit_history_entry
        )

    def _commit_history_entry(self):
        entry = self.pending_history_entry

        if entry in self.calculation_history:
            self.calculation_history.remove(entry)

        self.calculation_history.append(entry)

        if self.main_window.history_window:
            self.main_window.history_window.populate_calc_history(self.calculation_history)

        self.history_update_timeout_id = None  # Clear the timeout ID
        self.pending_history_entry = None
        return False  # Stop timeout

    def cancel_pending_history_update(self):
        if self.history_update_timeout_id is not None:
            GLib.source_remove(self.history_update_timeout_id)
            self.history_update_timeout_id = None
            self.pending_history_entry = None

    def insert_operator(self, operator):
        entry = self.calc_entry
        text = entry.get_text()

        try:
            start, end = entry.get_selection_bounds()
        except Exception:
            start = end = entry.get_position()  # Fallback to cursor position

        if start != end:
            selected_text = text[start:end]
            new_text = text[:start] + f"{operator}({selected_text})" + text[end:]
            cursor_pos = start + len(f"{operator}({selected_text})")
        else:
            pos = entry.get_position()
            new_text = text[:pos] + f"{operator}()" + text[pos:]
            cursor_pos = pos + len(f"{operator}(")

        entry.set_text(new_text)
        entry.grab_focus()
        self.operator_menu.get_popover().hide()
        entry.set_position(cursor_pos)
        entry.select_region(cursor_pos, cursor_pos)

    @Gtk.Template.Callback()
    def on_btn_sqrt_clicked(self, button):
        self.insert_operator("√")

    @Gtk.Template.Callback()
    def on_btn_sin_clicked(self, button):
        self.insert_operator("sin")

    @Gtk.Template.Callback()
    def on_btn_cos_clicked(self, button):
        self.insert_operator("cos")

    @Gtk.Template.Callback()
    def on_btn_tan_clicked(self, button):
        self.insert_operator("tan")

    @Gtk.Template.Callback()
    def on_btn_log_clicked(self, button):
        self.insert_operator("log")

    def insert_constant(self, constant: str):
        entry = self.calc_entry
        text = entry.get_text()

        pos = entry.get_position()
        new_text = text[:pos] + constant + text[pos:]

        entry.set_text(new_text)
        entry.grab_focus()
        self.operator_menu.get_popover().hide()
        entry.set_position(pos + len(constant))

    @Gtk.Template.Callback()
    def on_btn_pi_clicked(self, button):
        self.insert_constant("π")

    @Gtk.Template.Callback()
    def on_entry_focus(self, entry, param):
        def select_all():
            entry.select_region(0, -1)

        GLib.idle_add(select_all)


