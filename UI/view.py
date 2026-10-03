import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "TdP - Clienti e artisti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self.txt_result = None

    def load_interface(self):
        self._page.controls.append(
            ft.Text("TdP - Chinook: clienti e artisti", color="blue", size=24))

        # ---------- RIGA 1: anni + crea grafo + stampa info (PUNTO 1) ----------
        self._ddAnnoDa = ft.Dropdown(label="Anno da", width=150)
        self._ddAnnoA = ft.Dropdown(label="Anno a", width=150)
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                               on_click=self._controller.handleCreaGrafo, width=200)
        self._btnStampaInfo = ft.ElevatedButton(text="Stampa Info",
                                                on_click=self._controller.handleStampaInfo, width=200)
        row1 = ft.Row([self._ddAnnoDa, self._ddAnnoA, self._btnCreaGrafo, self._btnStampaInfo],
                      alignment=ft.MainAxisAlignment.CENTER)

        # ---------- RIGA 2: cliente + N + trova gruppo (PUNTO 2) ----------
        self._ddCliente = ft.Dropdown(label="Cliente", width=310)
        self._txtN = ft.TextField(label="Numero di clienti (N)", width=200)
        self._btnGruppo = ft.ElevatedButton(text="Trova gruppo clienti",
                                            on_click=self._controller.handleGruppo, width=200)
        row2 = ft.Row([self._ddCliente, self._txtN, self._btnGruppo],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)

        # ---------- area risultati ----------
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)

        # riempio i due menu degli anni all'avvio (punto 1a)
        self._controller.fillDDAnni()

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()