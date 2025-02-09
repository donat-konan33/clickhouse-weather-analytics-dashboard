class WeatherConstants:
    @staticmethod
    def dataset():
        """
        list of datasets of projects
        """
        return [
            "raw_olddata_weatherteam_mart",
        ]

    @staticmethod
    def temp_feature():
        """
        select a feature of temperature
        """
        return ["temp", "tempmin", "tempmax", "feelslike", "feelslikemin", "feelslikemax"]

    @staticmethod
    def department():
        """
        list od departments
        """
        return ['Essonne', 'Seine-et-Marne', 'Val-de-Marne', 'Yvelines',
                'Paris', 'Hauts-de-Seine', "Val-d'Oise", 'Cher',
                'Indre', 'Indre-et-Loire', 'Loir-et-Cher', 'Loiret',
                    'Eure-et-Loir', 'Jura', 'Doubs', 'Territoire de Belfort',
                    'Yonne', 'Orne', 'Eure', 'Manche', 'Calvados',
                    'Seine-Maritime', 'Aisne', 'Oise', 'Somme', 'Pas-de-Calais',
                    'Nord', 'Haut-Rhin', 'Haute-Marne', 'Vosges', 'Bas-Rhin',
                    'Meurthe-et-Moselle', 'Aube', 'Moselle', 'Ardennes',
                    'Loire-Atlantique', 'Maine-et-Loire', 'Sarthe', 'Mayenne',
                    'Morbihan', 'Ille-et-Vilaine',
                    'Lot-et-Garonne',
                    'Gironde',
                    'Dordogne',
                    'Vienne',
                    'Charente',
                    'Haute-Vienne',
                    'Landes',
                    'Charente-Maritime',
                    'Creuse',
                    'Aude',
                    'Haute-Garonne',
                    'Gers',
                    'Gard',
                    'Tarn',
                    'Tarn-et-Garonne',
                    'Aveyron',
                    'Lot',
                    'Allier',
                    'Cantal',
                    'Haute-Loire',
                    'Savoie',
                    'Haute-Savoie',
                    'Ain',
                    'Var',
                    'Alpes-Maritimes',
                    'Alpes-de-Haute-Provence',
                    'Hautes-Alpes']
