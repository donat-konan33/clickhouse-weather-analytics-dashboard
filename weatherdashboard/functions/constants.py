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
        return ['Ain', 'Ardèche', 'Drôme', 'Isère', 'Loire', 'Lozère',
                'Pyrénées-Orientales', 'Corrèze', 'Creuse', 'Haute-Vienne',
                'Yvelines', 'Essonne', 'Hauts-de-Seine', 'Seine-Saint-Denis',
                'Val-de-Marne', "Val-d'Oise", 'Seine-et-Marne', 'Paris',
                'Seine-Maritime', 'Eure', 'Calvados', 'Manche', 'Orne', 'Sarthe',
                'Mayenne', 'Charente', 'Charente-Maritime', 'Dordogne', 'Gironde',
                'Landes', 'Lot-et-Garonne', 'Pyrénées-Atlantiques',
                'Alpes-Maritimes', 'Tarn-et-Garonne', 'Ariège', 'Loire-Atlantique',
                'Maine-et-Loire', 'Vendée', 'Deux-Sèvres', 'Vienne', 'Aveyron',
                'Haute-Garonne', 'Gers', 'Lot', 'Hautes-Pyrénées', 'Tarn', 'Aude',
                'Gard', 'Hérault', 'Loiret', 'Alpes-de-Haute-Provence',
                'Hautes-Alpes', 'Bouches-du-Rhône', 'Var', 'Cher', 'Eure-et-Loir',
                'Indre', 'Indre-et-Loire', 'Loir-et-Cher', 'Vrigne-Meuse',
                'Moselle', 'Vosges', 'Bas-Rhin', 'Haut-Rhin', 'Oise', 'Somme',
                'Pas-de-Calais', 'Nord', 'Meurthe-et-Moselle', 'Haute-Loire',
                'Puy-de-Dôme', "Côte-d'Or", 'Nièvre', 'Saône-et-Loire',
                 'Aube', 'Marne', 'Haute-Marne', 'Ardennes', 'Aisne', 'Doubs', 'Jura',
                'Haute-Saône', 'Territoire de Belfort',
                'Yonne', "Côtes-d'Armor", 'Finistère', 'Ille-et-Vilaine',
                'Morbihan', 'Rhône', 'Savoie', 'Haute-Savoie', 'Allier', 'Cantal', 'Corse',
                #'Mayotte',  'Guyane-France', 'Martinique-France', 'Guadeloupe-France',
                ]

    @staticmethod
    def region():
        """
        """
        return [
                "Occitanie",
                "Provence-Alpes-Côte d'Azur",
                "Auvergne-Rhône-Alpes",
                "Grand Est",
                "Nouvelle-Aquitaine",
                "Bourgogne-Franche-Comté",
                "Hauts-de-France",
                "Pays de la Loire",
                "Centre-Val de Loire",
                "Bretagne",
                "Île-de-France",
                "Normandie",
            ]
