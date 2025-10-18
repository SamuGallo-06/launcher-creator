import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, Gdk

class MainWindow(Gtk.ApplicationWindow):
    
    APP_TITLE = "Launcher Creator"
    MAIN_HEADER = "#!/usr/bin/env xdg-open\n"
    DESKTOP_HEADER = "[Desktop Entry]\n"
    VERSION_HEADER = "Version="
    TYPE_HEADER = "Type="
    TERMINAL_HEADER = "Terminal="
    EXEC_HEADER = "Exec="
    NAME_HEADER = "Name="
    ICON_HEADER = "Icon="
    COMMENT_HEADER = "Comment="
    CATEGORIES_HEADER = "Categories="
    
    # Lista delle categorie principali
    MAIN_CATEGORIES = [
        "AudioVideo", "Audio", "Video", "Development", "Education", 
        "Game", "Graphics", "Network", "Office", "Science", 
        "Settings", "System", "Utility"
    ]
    
    file_path = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUI()

    def setupUI(self):
        self.set_title(self.APP_TITLE)
        self.set_default_size(464, 624)
        self.set_resizable(False) 

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.main_box)

        self.grid = Gtk.Grid(
            column_spacing=6,
            row_spacing=6,
            margin_start=20,
            margin_end=20,
            margin_top=10,
            margin_bottom=10
        )
        self.main_box.append(self.grid)

        self.label_nome = Gtk.Label(label="Nome", halign=Gtk.Align.START)
        self.grid.attach(self.label_nome, 0, 0, 3, 1)
        self.name_entry = Gtk.Entry()
        self.grid.attach(self.name_entry, 0, 1, 3, 1)

        self.label_comando = Gtk.Label(label="Comando", halign=Gtk.Align.START)
        self.grid.attach(self.label_comando, 0, 2, 3, 1)
        self.command_entry = Gtk.Entry()
        self.grid.attach(self.command_entry, 0, 3, 3, 1)

        self.label_versione = Gtk.Label(label="Versione", halign=Gtk.Align.START)
        self.grid.attach(self.label_versione, 0, 4, 3, 1)
        self.version_entry = Gtk.Entry(text="1.0")
        self.grid.attach(self.version_entry, 0, 5, 3, 1)

        self.label_commento = Gtk.Label(label="Commento", halign=Gtk.Align.START)
        self.grid.attach(self.label_commento, 0, 6, 3, 1)
        self.comment_entry = Gtk.Entry()
        self.grid.attach(self.comment_entry, 0, 7, 3, 1)

        self.label_icona = Gtk.Label(label="Icona", halign=Gtk.Align.START)
        self.grid.attach(self.label_icona, 0, 8, 3, 1)
        self.icon_entry = Gtk.Entry()
        self.grid.attach(self.icon_entry, 0, 9, 3, 1)

        self.label_tipo = Gtk.Label(label="Tipo", halign=Gtk.Align.START)
        self.grid.attach(self.label_tipo, 0, 10, 3, 1)
        
        self.application_type_entry = Gtk.ComboBoxText()
        self.application_type_entry.append_text("Applicazione")
        self.application_type_entry.append_text("Link")
        self.application_type_entry.append_text("Directory")
        self.application_type_entry.set_active(0)
        self.grid.attach(self.application_type_entry, 0, 11, 3, 1)
        
        self.label_tipo = Gtk.Label(label="Categorie", halign=Gtk.Align.START)
        self.grid.attach(self.label_tipo, 0, 12, 3, 1)
        
        #Categorie principali launcher
        self.expander = Gtk.Expander(label="Categorie")
        self.expander.set_expanded(False)
        self.grid.attach(self.expander, 0, 13, 3, 1)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_height(200)

        self.categories_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.categories_box.set_margin_top(5)
        self.categories_box.set_margin_bottom(5)
        self.categories_box.set_margin_start(10)
        scrolled_window.set_child(self.categories_box)
        self.expander.set_child(scrolled_window)
        
        self.checkbox_list = []
        
        for category_name in self.MAIN_CATEGORIES:
            check_button = Gtk.CheckButton(label=category_name)
            self.categories_box.append(check_button)
            self.checkbox_list.append(check_button)

        self.terminal_check_box = Gtk.CheckButton(label="Apri nel terminale")
        self.terminal_check_box.set_margin_top(20)
        self.grid.attach(self.terminal_check_box, 0, 14, 3, 1)
        
        self.export_button = Gtk.Button(label="Esporta")
        self.export_button.set_margin_top(20)
        self.grid.attach(self.export_button, 1, 15, 1, 1)
        
        self.open_button = Gtk.Button(label="Apri")
        self.open_button.set_margin_top(20)
        self.grid.attach(self.open_button, 2, 15, 1, 1)
        
        self.save_button = Gtk.Button(label="Salva")
        self.save_button.set_margin_top(20)
        self.grid.attach(self.save_button, 3, 15, 1, 1)

        self.statusbar = Gtk.Statusbar()
        self.statusbar_context_id = self.statusbar.get_context_id("main")
        self.statusbar.push(self.statusbar_context_id, "Pronto")
        self.main_box.append(self.statusbar) # Aggiunge la statusbar al box

        self.open_button.connect("clicked", self.on_open_clicked)
        self.save_button.connect("clicked", self.on_save_clicked)
        self.export_button.connect("clicked", self.on_export_clicked)

    def on_open_clicked(self, widget):
        """Apre il dialog per selezionare un file .desktop"""
        native = Gtk.FileChooserNative.new(
            "Apri file",
            self,
            Gtk.FileChooserAction.OPEN,
            "_Apri",
            "_Annulla"
        )
        
        filter_desktop = Gtk.FileFilter()
        filter_desktop.set_name("Desktop Entries (*.desktop)")
        filter_desktop.add_pattern("*.desktop")
        native.add_filter(filter_desktop)
        
        native.connect("response", self.on_open_dialog_response)
        native.show()

    def on_open_dialog_response(self, dialog, response_id):
        """Chiamato alla chiusura del dialog 'Apri'"""
        if response_id == Gtk.ResponseType.ACCEPT:
            gfile = dialog.get_file()
            self.file_path = gfile.get_path()
            try:
                self.load_file_data(self.file_path)
            except Exception as e:
                self.statusbar.push(self.statusbar_context_id, f"Errore lettura: {e}")
        dialog.destroy()

    def load_file_data(self, path):
        """Legge il file .desktop e popola i campi dell'interfaccia"""
        desktop_values = {}
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                # Salta commenti, righe vuote e righe non valide
                if line and not line.startswith("#") and "=" in line:
                    # Divide solo al primo "="
                    key, value = line.split("=", 1)
                    desktop_values[key.strip()] = value.strip()
        
        self.name_entry.set_text(desktop_values.get("Name", ""))
        self.command_entry.set_text(desktop_values.get("Exec", ""))
        self.version_entry.set_text(desktop_values.get("Version", "1.0"))
        self.icon_entry.set_text(desktop_values.get("Icon", ""))
        self.comment_entry.set_text(desktop_values.get("Comment", ""))
        
        type_val = desktop_values.get("Type", "Application")
        if type_val == "Application":
            self.application_type_entry.set_active(0)
        elif type_val == "Link":
            self.application_type_entry.set_active(1)
        elif type_val == "Directory":
            self.application_type_entry.set_active(2)
        else:
            self.application_type_entry.set_active(0) # Default
        
        terminal_val = desktop_values.get("Terminal", "false").lower() == "true"
        self.terminal_check_box.set_active(terminal_val)
        
        self.statusbar.push(self.statusbar_context_id, "File caricato")


    def on_save_clicked(self, widget):
        """Salva il file. Se non è mai stato salvato, esegue 'Esporta'."""
        if self.file_path is None:
            # Nessun file caricato, si comporta come "Esporta"
            self.on_export_clicked(widget)
        else:
            # Sovrascrive il file esistente
            try:
                self.write_file_data(self.file_path)
            except Exception as e:
                self.statusbar.push(self.statusbar_context_id, f"Errore salvataggio: {e}")

    def on_export_clicked(self, widget):
        """Apre il dialog 'Salva con nome'."""
        native = Gtk.FileChooserNative.new(
            "Esporta file",
            self,
            Gtk.FileChooserAction.SAVE,
            "_Salva",
            "_Annulla"
        )
        
        # Suggerisce un nome file
        suggested_name = "nuovo-launcher.desktop"
        if self.name_entry.get_text():
             suggested_name = self.name_entry.get_text() + ".desktop"
        native.set_current_name(suggested_name)

        filter_desktop = Gtk.FileFilter()
        filter_desktop.set_name("Desktop Entries (*.desktop)")
        filter_desktop.add_pattern("*.desktop")
        native.add_filter(filter_desktop)
        
        native.connect("response", self.on_save_dialog_response)
        native.show()

    def on_save_dialog_response(self, dialog, response_id):
        """Chiamato alla chiusura del dialog 'Salva'"""
        if response_id == Gtk.ResponseType.ACCEPT:
            gfile = dialog.get_file()
            path = gfile.get_path()
            
            if not path.endswith(".desktop"):
                path += ".desktop"
            
            self.file_path = path
            try:
                self.write_file_data(self.file_path)
            except Exception as e:
                self.statusbar.push(self.statusbar_context_id, f"Errore salvataggio: {e}")
        dialog.destroy()

    def write_file_data(self, path):
        """Scrive i dati dell'interfaccia nel file .desktop specificato"""
        with open(path, 'w') as f:
            f.write(self.MAIN_HEADER)
            f.write(self.DESKTOP_HEADER)
            f.write(f"{self.VERSION_HEADER}{self.version_entry.get_text()}\n")
            f.write(f"{self.NAME_HEADER}{self.name_entry.get_text()}\n")
            f.write(f"{self.COMMENT_HEADER}{self.comment_entry.get_text()}\n")
            
            selected_categories = []
        
            for check_button in self.checkbox_list:
                if check_button.get_active():
                    selected_categories.append(check_button.get_label())
            
            if not selected_categories:
                self.statusbar.push(self.statusbar_context_id, "Selezionare almeno una categoria")
                return

            categories_string = ";".join(selected_categories) + ";"
            f.write(f"{self.CATEGORIES_HEADER}{categories_string}")

            type_text = self.application_type_entry.get_active_text()
            type_val = "Application" # Default
            if type_text == "Link":
                type_val = "Link"
            elif type_text == "Directory":
                type_val = "Directory"
            f.write(f"{self.TYPE_HEADER}{type_val}\n")
            
            f.write(f"{self.EXEC_HEADER}{self.command_entry.get_text()}\n")
            f.write(f"{self.ICON_HEADER}{self.icon_entry.get_text()}\n")
            
            # Converte il booleano (True/False) in stringa
            terminal_bool = self.terminal_check_box.get_active()
            f.write(f"{self.TERMINAL_HEADER}{str(terminal_bool)}\n")
        
        self.statusbar.push(self.statusbar_context_id, f"File salvato: {path}")

# --- Classe Application (per avviare Gtk) ---

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_activate(self):
        # Attiva l'applicazione
        self.win = MainWindow(application=self)
        self.win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

if __name__ == "__main__":
    app = MyApp(application_id="org.example.GtkLauncherCreator")
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)