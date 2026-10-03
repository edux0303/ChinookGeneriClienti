import networkx as nx
from database.DAO import DAO
from itertools import combinations


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
        self.idMap = {}
        self._solBest = []
        self._pesoBest = 0
        self._maxSpesa = 0

    # ---------- PUNTO 1 ----------
    def getAnni(self):
        return DAO.getAnni()

    def buildGraph(self, anno1, anno2):
        self._grafo.clear()
        self.idMap = {}

        self._nodes = DAO.getNodi(anno1, anno2)
        for n in self._nodes:
            self.idMap[n.CustomerId] = n

        self._grafo.add_nodes_from(self._nodes)

        for s1, s2 in DAO.getArtistiClienti(anno1, anno2):
            if s1 in self.idMap:
                self.idMap[s1].artisti.add(s2)

        for c1, c2 in combinations(self._nodes, 2):
            peso = len(c1.artisti & c2.artisti)
            if peso > 0:
                self._grafo.add_edge(c1, c2, weight=peso)

    def getNodes(self):
        return self._nodes

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    # ---------- PUNTO 1d ----------
    def getGradoMax(self):
        best = None
        for n in sorted(self._nodes, key=str):
            if best is None or self._grafo.degree(n) > self._grafo.degree(best):
                best = n
        return best, self._grafo.degree(best)

    def getPesoMax(self):
        best = None
        for n in sorted(self._nodes, key=str):
            if best is None or self._grafo.degree(n, weight="weight") > self._grafo.degree(best, weight="weight"):
                best = n
        return best, self._grafo.degree(best, weight="weight")

    def getSpesaMaxMin(self):
        ordinati = sorted(self._nodes, key=str)
        massimo = ordinati[0]
        minimo = ordinati[0]
        for n in ordinati:
            if n.spesa > massimo.spesa:
                massimo = n
            if n.spesa < minimo.spesa:
                minimo = n
        return massimo, minimo

    def getComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        numero = len(componenti)
        piuGrande = 0
        for c in componenti:
            if len(c) > piuGrande:
                piuGrande = len(c)
        return numero, piuGrande

    def getTopArchi(self):
        archi = []
        for u, v, dati in self._grafo.edges(data=True):
            nomi = sorted([str(u), str(v)])
            archi.append((nomi[0], nomi[1], dati["weight"]))
        archi.sort(key=lambda x: (-x[2], x[0], x[1]))
        return archi[:5]

    # ---------- PUNTO 2 ----------
    def getGruppo(self, start, N):
        self._solBest = []
        self._pesoBest = 0

        self._maxSpesa = 0
        for c in self._nodes:
            if c.spesa > self._maxSpesa:
                self._maxSpesa = c.spesa

        self._ricorsione([start], start.spesa, N)
        return self._solBest, self._pesoBest

    def _ricorsione(self, parziale, spesaParziale, N):
        if len(parziale) == N:
            if spesaParziale > self._pesoBest:
                self._pesoBest = spesaParziale
                self._solBest = list(parziale)
            return

        mancanti = N - len(parziale)
        if spesaParziale + mancanti * self._maxSpesa <= self._pesoBest:
            return

        candidati = []
        for c in self._nodes:
            if self._ammissibile(c, parziale):
                candidati.append(c)
        candidati.sort(key=lambda x: x.spesa, reverse=True)

        for c in candidati:
            parziale.append(c)
            self._ricorsione(parziale, spesaParziale + c.spesa, N)
            parziale.pop()

    def _ammissibile(self, c, parziale):
        if c in parziale:
            return False
        adiacente = False
        for p in parziale:
            if p.Country == c.Country:
                return False
            if self._grafo.has_edge(c, p):
                adiacente = True
        return adiacente