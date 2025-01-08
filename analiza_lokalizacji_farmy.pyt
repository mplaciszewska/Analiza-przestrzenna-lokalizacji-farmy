# -*- coding: utf-8 -*-

import arcpy
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Analiza lokalizacji farmy fotowoltaicznej"
        self.description = "Narzędzie znajduje działki w danej gminie odpowiednie pod inwestycję farmy fotowoltaicznej"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        workspace = arcpy.Parameter(
            displayName="Workspace",
            name="workspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )

        output_folder = arcpy.Parameter(
            displayName="Folder wyjściowy",
            name="output_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        warstwa_gminy = arcpy.Parameter(
            displayName="Warstwa gminy",
            name="warstwa_gminy",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        bufor_gminy = arcpy.Parameter(
            displayName="Bufor gminy",
            name="bufor_gminy",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        warstwa_nmt = arcpy.Parameter(
            displayName="Warstwa NMT",
            name="warstwa_nmt",
            datatype="GPRasterLayer",
            parameterType="Required",
            direction="Input"
        )

        drogi = arcpy.Parameter(
            displayName="Warstwa dróg",
            name="drogi",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        rzeki = arcpy.Parameter(
            displayName="Warstwa rzek",
            name="rzeki",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        jeziora = arcpy.Parameter(
            displayName="Warstwa jezior",
            name="jeziora",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        lasy = arcpy.Parameter(
            displayName="Warstwa lasów",
            name="lasy",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        budynki = arcpy.Parameter(
            displayName="Warstwa budynków",
            name="budynki",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        dzialki = arcpy.Parameter(
            displayName="Warstwa działek",
            name="dzialki",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )

        raster_wezlow = arcpy.Parameter(
            displayName="Mapa odległości od węzłów komunikacyjnych",
            name="raster_wezlow",
            datatype="GPRasterLayer",
            parameterType="Optional",
            direction="Input"
        )

        tworzyc_mape_kosztow = arcpy.Parameter(
            displayName="Czy tworzyć mapę kosztów?",
            name="tworzyc_mape_kosztow",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input"
        )
        tworzyc_mape_kosztow.value = False

        linie_energ = arcpy.Parameter(
            displayName="Warstwa linii energetycznych",
            name="linie_energ",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input"
        )
        linie_energ.enabled = False

        pokrycie = arcpy.Parameter(
            displayName="Warstwa pokrycia terenu",
            name="pokrycie",
            datatype="GPFeatureLayer",
            parameterType="Optional",
            direction="Input"
        )
        pokrycie.enabled = False

        params = [workspace, output_folder, warstwa_gminy, bufor_gminy, warstwa_nmt, drogi, rzeki, jeziora, lasy, budynki, dzialki, raster_wezlow]
        params.extend([tworzyc_mape_kosztow, linie_energ, pokrycie])
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        tworzyc_mape_kosztow = parameters[12].value
        parameters[13].enabled = tworzyc_mape_kosztow
        parameters[14].enabled = tworzyc_mape_kosztow
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""


        def create_folder_if_not_exists(folder_path):
            """
            Funkcja sprawdza, czy folder istnieje. Jeśli nie, tworzy go.
            """
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        # Parametry i warstwy wejściowe
        output_folder = parameters[1].valueAsText

        folders_to_create = [
            "warstwy_wejsciowe",
            "kryteria",
            "przydatnosc_dzialek",
            "dzialki_pod_inwestycje",
            "mapy_kosztow"
        ]

        for folder in folders_to_create:
            folder_path = os.path.join(output_folder, folder)
            create_folder_if_not_exists(folder_path)


        bufor_gminy = parameters[3].value
        bufor_gminy_path = fr"{output_folder}\warstwy_wejsciowe\bufor_gminy"
        arcpy.management.CopyFeatures(bufor_gminy, bufor_gminy_path, '', None, None, None)

        warstwa_nmt = parameters[4].value
        extent = arcpy.Describe(bufor_gminy).extent
        cellsize = 5

        workspace = parameters[0].valueAsText
        arcpy.env.workspace = workspace
        arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("ETRS 1989 Poland CS92")
        arcpy.env.overwriteOutput = True
        arcpy.env.extent = extent
        arcpy.env.mask = bufor_gminy_path
        arcpy.env.cellSize =  cellsize

        aprx = arcpy.mp.ArcGISProject("CURRENT") 
        m = aprx.activeMap

        arcpy.env.addOutputsToMap = False

        drogi_wszystkie = parameters[5].value
        rzeki = parameters[6].value
        jeziora = parameters[7].value
        lasy = parameters[8].value
        budynki_wszystkie = parameters[9].value
        dzialki = parameters[10].value
        raster_wezlow = parameters[11].value
        gmina = parameters[2].value

        tworzyc_mape_kosztow = parameters[12].value

        
        # Wyselekcjonowanie drog utwardzonych
        drogi_layer = arcpy.management.MakeFeatureLayer(drogi_wszystkie, "drogi_layer").getOutput(0)

        drogi = arcpy.management.SelectLayerByAttribute(drogi_layer, "NEW_SELECTION", "MATE_NAWIE IN ('beton','bruk', 'kostka kamienna', 'kostka prefabrykowana', 'masa bitumiczna', 'płyty betonowe')", None)

        arcpy.management.CopyFeatures(drogi, fr"{output_folder}\warstwy_wejsciowe\drogi_selected", '', None, None, None)
        drogi_selected = fr"{output_folder}\warstwy_wejsciowe\drogi_selected"
        arcpy.SelectLayerByAttribute_management(drogi, "CLEAR_SELECTION")

        # Wyselekcjonowanie budynkow mieszkalnych
        budynki_layer = arcpy.management.MakeFeatureLayer(budynki_wszystkie, "budynki_layer").getOutput(0)

        budynki = arcpy.management.SelectLayerByAttribute(budynki_layer, "NEW_SELECTION", "FOBUD IN ('budynki mieszkalne')", None)
        arcpy.management.CopyFeatures(budynki, fr"{output_folder}\warstwy_wejsciowe\budynki_selected", '', None, None, None)
        budynki_selected = fr"{output_folder}\warstwy_wejsciowe\budynki_selected"
        arcpy.SelectLayerByAttribute_management(budynki, "CLEAR_SELECTION")

        # Utworzenie map odległości
        rzeki = arcpy.management.CopyFeatures(rzeki, fr"{output_folder}\warstwy_wejsciowe\rzeki", '', None, None, None)
        jeziora = arcpy.management.CopyFeatures(jeziora, fr"{output_folder}\warstwy_wejsciowe\jeziora", '', None, None, None)
        lasy = arcpy.management.CopyFeatures(lasy, fr"{output_folder}\warstwy_wejsciowe\lasy", '', None, None, None)

        distance_rzeki = arcpy.sa.EucDistance(rzeki, None, cellsize)
        distance_jeziora = arcpy.sa.EucDistance(jeziora, None, cellsize)
        # distance_drogi = arcpy.sa.EucDistance(drogi_selected, None, cellsize)
        distance_budynki = arcpy.sa.EucDistance(budynki_selected, None, cellsize)
        distance_lasy = arcpy.sa.EucDistance(lasy, None, cellsize)
        distance_wezly = raster_wezlow

        arcpy.AddMessage("Utworzono mapy odległości")
        arcpy.AddMessage("Rozpoczęto realizację kryteriów...")

        # ------------------------- KRYTERIUM 1 - rzeki i jeziora ---------------------------
        #kryterium ostre dla strefy ochronnej 100m 
        rzeki_ostre = arcpy.ddd.Reclassify(distance_rzeki, "VALUE", f"0 100 0;100 {distance_rzeki.maximum} 1")
        jeziora_ostre = arcpy.ddd.Reclassify(distance_jeziora, "VALUE", f"0 100 0;100 {distance_jeziora.maximum} 1")
        wody_ostre = arcpy.sa.FuzzyOverlay([rzeki_ostre, jeziora_ostre], "AND")
        
        #kryterium rozmyte dla obszarów w odległości powyżej 100m
        rzeki_rozmyte = arcpy.sa.FuzzyMembership(distance_rzeki, arcpy.sa.FuzzyLinear(500, 200))
        jeziora_rozmyte = arcpy.sa.FuzzyMembership(distance_jeziora, arcpy.sa.FuzzyLinear(500, 200))
        wody_rozmyte = arcpy.sa.FuzzyOverlay([rzeki_rozmyte, jeziora_rozmyte], "OR")

        kryterium_wody = arcpy.sa.FuzzyOverlay([wody_ostre, wody_rozmyte], 'AND')
        kryterium_wody.save(f"{output_folder}\kryteria\kryterium_wody.tif")
        # ------------------------- KRYTERIUM 2 - budynki  -----------------------------------
        kryterium_budynki = arcpy.sa.FuzzyMembership(distance_budynki,  arcpy.sa.FuzzyLinear(150, 400))
        kryterium_budynki.save(f"{output_folder}\kryteria\kryterium_budynki.tif")

        # ------------------------- KRYTERIUM 3 - lasy  --------------------------------------
        kryterium_lasy = arcpy.sa.FuzzyMembership(distance_lasy, arcpy.sa.FuzzyLinear(15, 100))
        kryterium_lasy.save(f"{output_folder}\kryteria\kryterium_lasy.tif")

        # ------------------------- KRYTERIUM 4 - drogi  -------------------------------------
        raster_zageszczenia = arcpy.sa.LineDensity(
            in_polyline_features=drogi_selected,
            population_field="NONE",
            cell_size=cellsize,
            search_radius=1000,
            area_unit_scale_factor="SQUARE_METERS"
        )
        arcpy.management.CalculateStatistics(raster_zageszczenia)

        kryterium_drogi = arcpy.sa.RescaleByFunction(
            in_raster=raster_zageszczenia,
            transformation_function= f"LINEAR 0 1,{raster_zageszczenia.maximum} 0 # {raster_zageszczenia.maximum} #",
            from_scale=0,
            to_scale=1
        )

        kryterium_drogi.save(f"{output_folder}\kryteria\kryterium_drogi.tif")

        # ------------------------- KRYTERIUM 5 - nachylenie stoków  --------------------------
        spadki_output = f"{workspace}\spadki"
        spadki = arcpy.ddd.Slope(warstwa_nmt, spadki_output, "PERCENT_RISE", 1)

        kryterium_spadki = arcpy.sa.FuzzyMembership(spadki, arcpy.sa.FuzzyLinear(10, 3))
        kryterium_spadki.save(f"{output_folder}\kryteria\kryterium_spadki.tif")

        # ------------------------- KRYTERIUM 6 - nasłonecznienie stoków  ---------------------
        stoki_output = f"{workspace}\stoki"
        stoki = arcpy.ddd.Aspect(warstwa_nmt, stoki_output)

        stoki_ES = arcpy.sa.FuzzyMembership(stoki, arcpy.sa.FuzzyLinear(90, 113))
        stoki_WS = arcpy.sa.FuzzyMembership(stoki, arcpy.sa.FuzzyLinear(270, 248))

        # ustawienie przydatności płaskich stoków na 1
        plaskie_stoki = arcpy.sa.Con(stoki, 1, 0, "VALUE = -1") 

        stoki_rozmyte = arcpy.sa.FuzzyOverlay([stoki_ES, stoki_WS], 'AND')
        kryterium_stoki = arcpy.sa.FuzzyOverlay([stoki_rozmyte, plaskie_stoki], 'OR')

        kryterium_stoki.save(f"{output_folder}\kryteria\kryterium_stoki.tif")

        # ------------------------- KRYTERIUM 7 - węzły komunikacyjne  ------------------------
        if distance_wezly and arcpy.Describe(distance_wezly).dataType == 'RasterDataset':
            max_value = arcpy.GetRasterProperties_management(distance_wezly, "MAXIMUM").getOutput(0)
            kryterium_wezly = arcpy.sa.FuzzyMembership(distance_wezly, arcpy.sa.FuzzyLinear(max_value, 300))
        else:
            kryterium_wezly = arcpy.sa.CreateConstantRaster(1, "FLOAT", warstwa_nmt)

        kryterium_wezly.save(f"{output_folder}\kryteria\kryterium_wezly.tif")
        m.addDataFromPath(f"{output_folder}\kryteria\kryterium_wezly.tif")
           
        # POŁĄCZENIE KRYTERIÓW
        arcpy.AddMessage("Łączenie kryteriów i tworzenie map przydatności...")   
        # połączenie kryteriów stosując równe wagi dla kryteriów
        rowna_waga = 1/7
        kryteria_rowne = arcpy.sa.WSTable(
            [
                [kryterium_budynki, "VALUE", rowna_waga],
                [kryterium_drogi, "VALUE", rowna_waga],
                [kryterium_lasy, "VALUE", rowna_waga],
                [kryterium_spadki, "VALUE", rowna_waga],
                [kryterium_stoki, "VALUE", rowna_waga],
                [kryterium_wody, "VALUE", rowna_waga],
                [kryterium_wezly, "VALUE", rowna_waga],
            ]
        )
        polaczone_kryteria_rowne = arcpy.sa.WeightedSum(kryteria_rowne)
        polaczone_kryteria_rowne.save(f"{output_folder}\kryteria\polaczone_kryteria_rowne.tif")

        # połączenie kryteriów stosując różne wagi dla kryteriów 
        kryteria_rozne = arcpy.sa.WSTable(
            [
                [kryterium_budynki, "VALUE", 0.120244],
                [kryterium_drogi, "VALUE", 0.051404],
                [kryterium_lasy, "VALUE", 0.248666],
                [kryterium_spadki, "VALUE", 0.187234],
                [kryterium_stoki, "VALUE", 0.163683],
                [kryterium_wody, "VALUE", 0.207279],
                [kryterium_wezly, "VALUE", 0.021489],
            ]
        )
        polaczone_kryteria_rozne = arcpy.sa.WeightedSum(kryteria_rozne)
        polaczone_kryteria_rozne.save(f"{output_folder}\kryteria\polaczone_kryteria_rozne.tif")

        # Uwzględnienie nieprzekraczalnych stref dla wody, lasów i budynków
        budynki_ostre = arcpy.ddd.Reclassify(distance_budynki, "VALUE", f"0 150 0; 150 {distance_budynki.maximum} 1")
        lasy_ostre = arcpy.ddd.Reclassify(distance_lasy, "VALUE", f"0 15 0; 15 {distance_lasy.maximum} 1")

        def times(in_raster1, in_raster2):
            out_raster = arcpy.ia.Times(
                in_raster_or_constant1=in_raster1,
                in_raster_or_constant2=in_raster2
            )
            return out_raster

        # przemnożenie mapy przydatności przez kryteria ostre:
        def polacz_ostre(polaczone_kryteria):
            mapa_przydatnosci1 = times(polaczone_kryteria, wody_ostre)
            mapa_przydatnosci2 = times(mapa_przydatnosci1, budynki_ostre)
            mapa_przydatnosci = times(mapa_przydatnosci2, lasy_ostre)
            return mapa_przydatnosci

        mapa_przydatnosci_rowne = polacz_ostre(polaczone_kryteria_rowne)
        mapa_przydatnosci_rozne = polacz_ostre(polaczone_kryteria_rozne)

        mapa_przydatnosci_rowne.save(f"{output_folder}\kryteria\mapa_przydatnosci_rowne.tif")
        mapa_przydatnosci_rozne.save(f"{output_folder}\kryteria\mapa_przydatnosci_rozne.tif")
        m.addDataFromPath(f"{output_folder}\kryteria\mapa_przydatnosci_rowne.tif")
        

        # Reklasyfikacja map przydatnosci w celu wyodrębnienia obszarów o 70% przydatności
        def reklasyfikuj_mape(mapa_przydatnosci):
            granica = 70/100 * mapa_przydatnosci.maximum
            mapa_reclass = arcpy.sa.Reclassify(mapa_przydatnosci, "VALUE", f"0 {granica} 0; {granica} {mapa_przydatnosci.maximum} 1")
            return mapa_reclass

        # wyciecie jedynie do obszaru gminy (bez bufora)
        mapa_przydatnosci_rowne = arcpy.sa.ExtractByMask(
            in_raster=mapa_przydatnosci_rowne,
            in_mask_data=gmina,
            extraction_area="INSIDE"
        )

        mapa_przydatnosci_rozne = arcpy.sa.ExtractByMask(
            in_raster=mapa_przydatnosci_rozne,
            in_mask_data=gmina,
            extraction_area="INSIDE"
        )

        mapa_przydatnosci_reclass_rowne = reklasyfikuj_mape(mapa_przydatnosci_rowne)
        mapa_przydatnosci_reclass_rozne = reklasyfikuj_mape(mapa_przydatnosci_rozne)
        mapa_przydatnosci_reclass_rowne.save(f"{output_folder}\kryteria\mapa_przydatnosci_reclass_rowne.tif")
        mapa_przydatnosci_reclass_rozne.save(f"{output_folder}\kryteria\mapa_przydatnosci_reclass_rozne.tif")

        # Przekształcenie map przydatności do postaci wektorowej
        def oblicz_przydatnosc_dzialki(mapa_przydatnosci, out_str):
            mapa_przydatnosci_wektor = fr"{workspace}\mapa_przydatnosci_wektor_{out_str}"
            with arcpy.EnvManager(outputZFlag="Disabled", outputMFlag="Disabled"):
                arcpy.conversion.RasterToPolygon(
                    in_raster=mapa_przydatnosci,
                    out_polygon_features=mapa_przydatnosci_wektor,
                    simplify="SIMPLIFY",
                    raster_field="Value",
                    create_multipart_features="SINGLE_OUTER_PART",
                    max_vertices_per_feature=None
                )

            # Intersect aby przyciąć poligony przydatności do działek:
            przydatnosc_dzialki_przeciecie = arcpy.analysis.Intersect(
                in_features=[mapa_przydatnosci_wektor, dzialki],
                out_feature_class=fr"{workspace}\przydatnosc_dzialki_przeciecie_{out_str}",
                join_attributes="ALL",
                cluster_tolerance=None,
                output_type="INPUT"
            )

            # Selekcja tylko przydatnych poligonów 
            przydatne_poligony = arcpy.management.MakeFeatureLayer(
                in_features=przydatnosc_dzialki_przeciecie,
                out_layer=fr"{workspace}\przydatne_poligony{out_str}",
                where_clause="gridcode = 1",
                workspace=None,
            )

            # Zliczenie jaka część działki jest pokryta przydatnymi obszarami
            przydatnosc_dzialki_pole = arcpy.analysis.SummarizeWithin(
                in_polygons=dzialki, 
                in_sum_features=przydatne_poligony,  
                out_feature_class=fr"{workspace}\przydatnosc_dzialki_pole_{out_str}",
                keep_all_polygons="ONLY_INTERSECTING",  
                sum_fields="Shape_Area Sum", 
                shape_unit="SQUAREMETERS"
            )
            
            # Dodanie atrybutu o % przydatności działki
            arcpy.management.CalculateField(
                in_table=przydatnosc_dzialki_pole,
                field="Procent_powierzchni_przydatnej",
                field_type = "DOUBLE",
                expression="(!SUM_Shape_Area! / !Shape_Area!) * 100",
                expression_type="PYTHON3"
            )
            return przydatnosc_dzialki_pole

        przydatnosc_dzialki_rowne = oblicz_przydatnosc_dzialki(mapa_przydatnosci_reclass_rowne, "rowne")
        przydatnosc_dzialki_rozne = oblicz_przydatnosc_dzialki(mapa_przydatnosci_reclass_rozne, "rozne")

        # Selekcja działek o min. 70% przydatności:
        def selekcja_przydatnych_dzialek(przydatnosc_dzialki, out_str):
            przydatnosc_dzialki_layer = arcpy.management.MakeFeatureLayer(przydatnosc_dzialki, "przydatnosc_dzialki_layer").getOutput(0)
            przydatne_dzialki = arcpy.management.SelectLayerByAttribute(przydatnosc_dzialki_layer, "NEW_SELECTION", '"Procent_powierzchni_przydatnej" > 60', None)
            przydatne_dzialki_path = f"{workspace}\przydatne_dzialki_{out_str}"
            arcpy.management.CopyFeatures(przydatne_dzialki, przydatne_dzialki_path, '', None, None, None)

            arcpy.SelectLayerByAttribute_management(przydatne_dzialki, "CLEAR_SELECTION")

            # Połączenie sąsiadujących działek w jeden obiekt
            polaczone_dzialki = arcpy.management.Dissolve(
                in_features=przydatne_dzialki_path,
                out_feature_class=f"{workspace}\polaczone_dzialki_{out_str}",
                dissolve_field=None,
                statistics_fields="Shape_Area SUM",
                multi_part="SINGLE_PART",
                unsplit_lines="UNSPLIT_LINES",
                concatenation_separator=""
            )
            
            return polaczone_dzialki

        polaczone_dzialki_rowne = selekcja_przydatnych_dzialek(przydatnosc_dzialki_rowne, "rowne")
        # m.addDataFromPath(f"{output_folder}\przydatnosc_dzialek\polaczone_dzialki_rowne.shp")
        polaczone_dzialki_rozne = selekcja_przydatnych_dzialek(przydatnosc_dzialki_rozne, "rozne")
        # m.addDataFromPath(f"{output_folder}\przydatnosc_dzialek\polaczone_dzialki_rozne.shp")

        # Wybranie działek spełniających kryterium powierzchni i szerokości (min 2ha i 50m)
        def dodaj_szerokosc(polaczone_dzialki, sciezka_wyjscia):
            # Utworzenie prostokątów ograniczających wokół działek 
            prostokaty_ograniczajace = arcpy.management.MinimumBoundingGeometry(
                polaczone_dzialki, 
                sciezka_wyjscia,
                "RECTANGLE_BY_WIDTH")

            arcpy.management.AddField(
                prostokaty_ograniczajace,
                field_name="Width",
                field_type="DOUBLE",
            )

            arcpy.topographic.CalculateMetrics(
                in_features=prostokaty_ograniczajace,
                in_metric_types="WIDTH",
                in_length_attributes="Shape_Length",
                in_width_attributes="Width",
                in_area_attributes="Shape_Area",
            )

            # Wykonanie Join, aby przekazać atrybut szerokości do działek
            fields = arcpy.ListFields(polaczone_dzialki)
            for field in fields:
                if field.name == "Width":
                    arcpy.management.DeleteField(polaczone_dzialki, "Width")

            arcpy.management.JoinField(
                in_data=polaczone_dzialki,         
                in_field="OBJECTID",                      
                join_table=prostokaty_ograniczajace,      
                join_field="OBJECTID",                   
                fields=["Width"],                  
            )
            return polaczone_dzialki

        polaczone_dzialki_rowne = f"{workspace}\polaczone_dzialki_rowne"
        sciezka_wyjscia_rowne = f"{workspace}\polaczone_dzialki_rowne_prostokaty"

        polaczone_dzialki_rozne = f"{workspace}\polaczone_dzialki_rozne"
        sciezka_wyjscia_rozne = f"{workspace}\polaczone_dzialki_rozne_prostokaty"

        dodaj_szerokosc(polaczone_dzialki_rowne, sciezka_wyjscia_rowne)
        dodaj_szerokosc(polaczone_dzialki_rozne, sciezka_wyjscia_rozne)

        # selekcja działek:
        dzialki_rowne_copy = arcpy.management.MakeFeatureLayer(
            in_features=polaczone_dzialki_rowne,
            out_layer=f"{output_folder}\przydatnosc_dzialek\dzialki_rowne_copy.shp",
            where_clause='"Shape_Area" >= 20000 AND "Width" >= 50',
        )

        dzialki_rowne = arcpy.management.CopyFeatures(
            in_features=dzialki_rowne_copy,  
            out_feature_class=f"{output_folder}\dzialki_pod_inwestycje\dzialki_rowne.shp"
        )

        dzialki_rozne_copy = arcpy.management.MakeFeatureLayer(
            in_features=polaczone_dzialki_rozne,
            out_layer=f"{output_folder}\przydatnosc_dzialek\dzialki_rozne_copy.shp",
            where_clause='"Shape_Area" >= 20000 AND "Width" >= 50',
        )

        dzialki_rozne = arcpy.management.CopyFeatures(
            in_features=dzialki_rozne_copy,  
            out_feature_class=f"{output_folder}\dzialki_pod_inwestycje\dzialki_rozne.shp"
        )

        m.addDataFromPath(f"{output_folder}\dzialki_pod_inwestycje\dzialki_rowne.shp")
        m.addDataFromPath(f"{output_folder}\dzialki_pod_inwestycje\dzialki_rozne.shp")

        # ----------------------------- TWORZENIE MAPY KOSZTOW -------------------------------- 
        if tworzyc_mape_kosztow:
            linie_energ = parameters[13].value
            pokrycie = parameters[14].value
            pokrycie = arcpy.management.MakeFeatureLayer(pokrycie, "pokrycie").getOutput(0)

            # Wyselekcjonowanie linii energetycznych średniego napięcia
            # linie_energ_layer = arcpy.management.MakeFeatureLayer(linie_energ, "linie_energ_layer").getOutput(0)
            # linie_energ = arcpy.management.SelectLayerByAttribute(linie_energ_layer, "NEW_SELECTION", "rodzaj = 'linia elektroenergetyczna średniego napięcia'", None)
            # arcpy.management.CopyFeatures(linie_energ, fr"{output_folder}\warstwy_wejsciowe\linie_energ_selected", '', None, None, None)
            # linie_energ_selected = fr"{output_folder}\warstwy_wejsciowe\linie_energ_selected"
            # arcpy.SelectLayerByAttribute_management(linie_energ, "CLEAR_SELECTION")

            raster_pokrycia = arcpy.conversion.FeatureToRaster(
                in_features= pokrycie,
                field="X_KOD",
                out_raster=f"raster_pokrycia",
                cell_size=5
            )

            # Reklasyfikacja w celu przypisania kosztów dla różnych wartości X_KOD (mapa kosztów względnych)
            raster_kosztow = arcpy.ddd.Reclassify(
                in_raster=raster_pokrycia,
                reclass_field="X_KOD",
                remap="PTZB01 200;PTZB02 100;PTZB05 50;PTZB03 200;PTZB04 200;PTWZ01 NODATA;PTWP02 200;PTWP03 NODATA;PTUT03 100;PTUT01 NODATA;PTTR02 1;PTTR01 20;PTPL01 50;PTNZ01 150;PTNZ02 150;PTLZ01 100;PTLZ03 50;PTLZ02 50;PTKM01 100;PTWP01 NODATA;PTRK01 15;PTRK02 15;PTUT02 90;PTUT04 20;PTUT05 20;PTKM02 200;PTKM03 200;PTKM04 NODATA;PTGN01 1;PTGN02 1;PTGN03 1;PTGN04 1;PTSO01 NODATA;PTSO02 NODATA;PTWZ02 NODATA",
                out_raster="raster_kosztow",
                missing_values="NODATA"
            )
            

            def utworz_sciezki_przylacza(dzialki, dzialki_str):
                with arcpy.da.SearchCursor(dzialki,['SHAPE@', 'FID']) as cursor:
                    for row in cursor:
                        geometry = row[0]
                        object_id = row[1]

                        warstwa = f"in_memory\\dzialka{object_id}_{dzialki_str}"
                        arcpy.management.CopyFeatures([geometry], warstwa)

                        sciezka_wyjsciowa = (f"{output_folder}\mapy_kosztow\dzialka_{object_id}_{dzialki_str}")
                        dzialka = arcpy.management.CopyFeatures(warstwa, sciezka_wyjsciowa)

                        # Utworzenie mapy kosztów skumulowanych i mapy kierunków
                        mapa_kosztow = arcpy.sa.CostDistance(
                            in_source_data=dzialka,
                            in_cost_raster=raster_kosztow,
                            out_backlink_raster=f"{workspace}\mki_{object_id}_{dzialki_str}"
                        )
                        mapa_kosztow.save(f"{workspace}\mko_{object_id}_{dzialki_str}")
                        mapa_kierunkow = f"{workspace}\mki_{object_id}_{dzialki_str}"

                        # Utworzenie ścieżki przyłącza od działek do istniejących linii energetycznych
                        out_raster = arcpy.sa.CostPath(
                            in_destination_data=linie_energ,
                            in_cost_distance_raster=mapa_kosztow,
                            in_cost_backlink_raster=mapa_kierunkow,
                            path_type="BEST_SINGLE",
                            destination_field="FID",
                            force_flow_direction_convention="INPUT_RANGE"
                        )
                        out_raster.save(f"{workspace}\path_{object_id}_{dzialki_str}")
                        
                        arcpy.conversion.RasterToPolyline(
                            in_raster=out_raster,
                            out_polyline_features=f"{workspace}\sciezka_przylacza_{object_id}_{dzialki_str}",
                            background_value="ZERO",
                            minimum_dangle_length=0,
                            simplify="SIMPLIFY",
                            raster_field="Value"
                        )
                        m.addDataFromPath(f"{workspace}\sciezka_przylacza_{object_id}_{dzialki_str}")

                        
            utworz_sciezki_przylacza(dzialki_rowne, "rowne")
            utworz_sciezki_przylacza(dzialki_rozne, "rozne")



        arcpy.AddMessage("Zakończono analizę lokalizacji farmy fotowoltaicznej")
        

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
