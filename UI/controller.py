import flet as ft
from database.DAO import DAO
from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        nerc = DAO.getNerc(self._view._ddNerc.value)
        maxX = float(self._view._txtYears.value)
        maxY = float(self._view._txtHours.value)

        soluzione, customers, tot_hours = self._model.worstCase(nerc, maxX, maxY)
        self._view._txtOut.controls.append(
                ft.Text(f"Tot people affected: {customers}\nTot hours of outage: {tot_hours}"))
        self._view.update_page()
        for e in soluzione:
            self._view._txtOut.controls.append(
                ft.Text(e))
            self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key = n._id, text = n._value))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
