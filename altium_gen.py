import os

class AltiumScriptGenerator:
    def __init__(self):
        self.commands = []
        self.header = (
            "Procedure GeneratePCBObjects;\n"
            "Var\n"
            "    Board     : IPCB_Board;\n"
            "    Track     : IPCB_Track;\n"
            "    Via       : IPCB_Via;\n"
            "Begin\n"
            "    Board := PCBServer.GetCurrentPCBBoard;\n"
            "    If Board = Nil Then Exit;\n"
            "    PCBServer.PreProcess;\n"
        )
        self.footer = (
            "    PCBServer.PostProcess;\n"
            "    ResetParameters;\n"
            "End;"
        )

    def _mm_to_coord(self, mm):
        """Converte millimetri in unità interne di Altium (Mils/10000 o Coord)"""
        #Altium usa le unità 'Coord'. 1mm è circa 393700.787 unità interne
        return int(mm * 393700.787)

    def add_track(self, x1, y1, x2, y2, thickness, layer='TopLayer'):
        """Aggiunge una traccia usando il metodo globale con casting implicito"""
        
        if(layer == 'TopLayer'):
            l = 'eTopLayer'
        elif(layer == 'InLayer1'):
            l = 'eMidLayer1'
        elif(layer == 'InLayer2'):
            l = 'eMidLayer2'
        elif(layer == 'BottomLayer'):
            l = 'eBottomLayer'
        
        cmd = f"""
    Track := PCBServer.PCBObjectFactory(eTrackObject, eNoDimension, eCreate_Default);
    Track.X1 := {self._mm_to_coord(x1)};
    Track.Y1 := {self._mm_to_coord(y1)};
    Track.X2 := {self._mm_to_coord(x2)};
    Track.Y2 := {self._mm_to_coord(y2)};
    Track.Width := {self._mm_to_coord(thickness)};
    Track.Layer := {l};
    Board.AddPCBObject(Track);
    """
        self.commands.append(cmd)

    def add_via(self, x, y, via_diam, hole_diam, layer_from='TopLayer', layer_to='BottomLayer'):
        """Aggiunge un via usando il metodo globale"""
        
        if(layer_to == 'TopLayer'):
            l_to = 'eTopLayer'
        elif(layer_to == 'InLayer1'):
            l_to = 'eMidLayer1'
        elif(layer_to == 'InLayer2'):
            l_to = 'eMidLayer2'
        elif(layer_to == 'BottomLayer'):
            l_to = 'eBottomLayer'

        if(layer_from == 'TopLayer'):
            l_from = 'eTopLayer'
        elif(layer_from == 'InLayer1'):
            l_from = 'eMidLayer1'
        elif(layer_from == 'InLayer2'):
            l_from = 'eMidLayer2'
        elif(layer_from == 'BottomLayer'):
            l_from = 'eBottomLayer'

        cmd = f"""
    Via := PCBServer.PCBObjectFactory(eViaObject, eNoDimension, eCreate_Default);
    Via.X := {self._mm_to_coord(x)};
    Via.Y := {self._mm_to_coord(y)};
    Via.Size := {self._mm_to_coord(via_diam)};
    Via.HoleSize := {self._mm_to_coord(hole_diam)};
    Via.LowLayer := {l_from};
    Via.HighLayer := {l_to};
    Board.AddPCBObject(Via);
    """
        self.commands.append(cmd)

    def save_script(self, name):
        """Salva il contenuto in un file .pas"""
        if not name.endswith('.pas'):
            name += '.pas'
        
        full_content = self.header + "\n".join(self.commands) + "\n" + self.footer
        with open(name, 'w') as f:
            f.write(full_content)
        print(f"Script Altium salvato correttamente: {os.path.abspath(name)}")