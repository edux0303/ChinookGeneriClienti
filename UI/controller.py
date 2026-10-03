import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    # ---------- PUNTO 1a ----------
    def fillDDAnni(self):
        for a in self._model.getAnni():
            self._view._ddAnnoDa.options.append(ft.dropdown.Option(str(a)))
            self._view._ddAnnoA.options.append(ft.dropdown.Option(str(a)))

    # ---------- PUNTO 1b/1c ----------
    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        anno1 = self._view._ddAnnoDa.value
        anno2 = self._view._ddAnnoA.value
        if anno1 is None or anno2 is None:
            self._errore("Selezionare entrambi gli anni!")
            return
        anno1 = int(anno1)
        anno2 = int(anno2)
        if anno1 > anno2:
            self._errore("Range non valido: 'Anno da' deve essere minore o uguale ad 'Anno a'!")
            return

        self._model.buildGraph(anno1, anno2)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato per il range {anno1}-{anno2}!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view._ddCliente.options.clear()
        self._view._ddCliente.value = None
        for c in sorted(self._model.getNodes(), key=str):
            self._view._ddCliente.options.append(ft.dropdown.Option(key=str(c.CustomerId), text=str(c)))
        self._view.update_page()

    # ---------- PUNTO 1d ----------
    def handleStampaInfo(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        cliente, grado = self._model.getGradoMax()
        self._view.txt_result.controls.append(
            ft.Text(f"Cliente con grado maggiore: {cliente} (grado: {grado})"))

        cliente, somma = self._model.getPesoMax()
        self._view.txt_result.controls.append(
            ft.Text(f"Cliente con somma pesi incidenti massima: {cliente} (somma: {somma})"))

        massimo, minimo = self._model.getSpesaMaxMin()
        self._view.txt_result.controls.append(
            ft.Text(f"Cliente che ha speso di più: {massimo} ({massimo.spesa:.2f})"))
        self._view.txt_result.controls.append(
            ft.Text(f"Cliente che ha speso di meno: {minimo} ({minimo.spesa:.2f})"))

        numero, piuGrande = self._model.getComponenti()
        self._view.txt_result.controls.append(
            ft.Text(f"Componenti connesse: {numero} (la più grande ha {piuGrande} clienti)"))

        self._view.txt_result.controls.append(ft.Text("Top 5 archi con peso maggiore:"))
        i = 1
        for nome1, nome2, peso in self._model.getTopArchi():
            self._view.txt_result.controls.append(ft.Text(f"{i}. {nome1} -- {nome2} (peso: {peso})"))
            i += 1
        self._view.update_page()

    # ---------- PUNTO 2 ----------
    def handleGruppo(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return
        if self._view._ddCliente.value is None:
            self._errore("Selezionare un cliente!")
            return
        start = self._model.idMap.get(int(self._view._ddCliente.value))
        if start is None:
            self._errore("Cliente non trovato!")
            return

        N = self._view._txtN.value
        if N is None or N == "":
            self._errore("Inserire il numero di clienti N!")
            return
        try:
            N = int(N)
        except ValueError:
            self._errore("N deve essere un numero intero!")
            return
        if N <= 0:
            self._errore("N deve essere maggiore di 0!")
            return
        if N > self._model.getNumNodi():
            self._errore("N è maggiore del numero di clienti nel grafo!")
            return

        gruppo, spesaTot = self._model.getGruppo(start, N)
        if len(gruppo) == 0:
            self._errore(f"Nessun gruppo di {N} clienti trovato a partire da {start}!")
            return

        self._view.txt_result.controls.append(ft.Text("Gruppo di clienti trovato:"))
        for c in sorted(gruppo, key=str):
            self._view.txt_result.controls.append(
                ft.Text(f"{c} - {c.Country} - {len(c.artisti)} artisti - spesa {c.spesa:.2f}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di clienti selezionati: {len(gruppo)}"))
        self._view.txt_result.controls.append(ft.Text(f"Spesa complessiva: {spesaTot:.2f}"))
        self._view.update_page()