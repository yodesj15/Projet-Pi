 def trouver_distance_angle(self, tab):
        tabDistanceX= [] # index0 à 359 degré 
        tabDistanceY= [] # index0 à 359 degré 
        
          
        for d in tab:
            tabDistanceX.append(self.calculer_distance_point_mm("x",d,tab[d])) #ajoute dans le tabX
            tabDistanceY.append(self.calculer_distance_point_mm("y",d,tab[d])) #ajoute dans le tabY
        return tabDistanceX,tabDistanceY
    
    def calculer_distance_point_mm(self,type_point,angle,distance):
        distance_mm = 0
        if type_point == "x":
            distance_mm = (math.cos(angle)) * distance
        else:
            distance_mm = (math.sin(angle)) * distance
            
        return distance_mm