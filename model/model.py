from database.DAO import DAO
from model.nerc import Nerc
from datetime import timedelta


class Model:
    def __init__(self):
        self._solBest = []
        self._BestCustomers = None
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()



    def worstCase(self, nerc, maxX, maxY):
        self._BestCustomers = 0
        self.loadEvents(nerc)
        parziale = []
        pos = 0
        self.ricorsione(parziale, maxX, maxY, pos)

        ore = sum((ev._date_event_finished - ev._date_event_began for ev in self._solBest), timedelta()).total_seconds()/3600
        return self._solBest, self._BestCustomers, ore

    def ricorsione(self, parziale, maxX, maxY, pos) -> None:

        #numero di customers affected dalla soluzione corrente
        customers = sum(e.customers_affected for e in parziale)
        if customers > self._BestCustomers:
            self._solBest = parziale.copy()
            self._BestCustomers = customers

        # CONDIZIONE DI TERMINAZIONE
        if pos == len(self._listEvents)-1:
            return

        for i in range(pos, len(self._listEvents)):
            e = self._listEvents[i]
            # check se l'evento è già nel parziale
            if any(e._id == ev._id for ev in parziale):
                continue

            # check su vincolo 1 (ore disservizio totali <= Y)
            ore = (sum((ev._date_event_finished - ev._date_event_began for ev in parziale), timedelta())
                   + e._date_event_finished - e._date_event_began).total_seconds()/3600
            if ore > maxY:
                continue

            #check su vincolo 2 (differenza tra l'anno più recente e quello più vecchio)
            anni = [ev._date_event_began.year for ev in parziale] + [e._date_event_began.year]
            if max(anni) - min(anni) > maxX:
                continue

            #update dei parametri
            parziale.append(e)
            pos += 1
            self.ricorsione(parziale, maxX, maxY, pos)
            parziale.pop()


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc


