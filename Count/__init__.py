plugin_name = "Count"
plugin_create_menu = True
__all__ = {"Junctions":1, "Pipes":2}
from PyQt4.QtGui import QMessageBox as Qmb
def run(session=None, choice=None):
  if choice == 1:
    n = format(len(session.project.junctions.value))
    Qmb.information(None, '', "Number of Junctions: " + n, Qmb.Ok)
  elif choice == 2:
    n = format(len(session.project.pipes.value))
    Qmb.information(None, '', "Number of Pipes: " + n, Qmb.Ok)
        