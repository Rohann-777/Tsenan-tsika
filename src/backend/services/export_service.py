from datetime import datetime
from io import BytesIO
from fpdf import FPDF
from sqlalchemy.orm import Session
from src.backend.services.alerte_service import AlerteService
from src.backend.repositories.prix_repository import PrixRepository

VERT = (5, 150, 105)
VERT_FONCE = (4, 120, 87)
ORANGE = (234, 88, 12)
GRIS = (75, 85, 99)
GRIS_CLAIR = (243, 244, 246)
ROUGE = (239, 68, 68)


class RapportPDF(FPDF):
    def header(self):
        self.set_fill_color(*VERT)
        self.rect(0, 0, 210, 22, style="F")
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 6)
        self.cell(0, 10, "Tsenan'tsika", align="L")
        self.set_font("Helvetica", "", 9)
        self.set_xy(10, 6)
        self.cell(0, 10, "Rapport de surveillance des prix", align="R")
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(*GRIS)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRIS)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


class ExportService:
    def __init__(self):
        self.alerte_service = AlerteService()
        self.prix_repository = PrixRepository()

    def generer_rapport_hebdomadaire(self, db: Session) -> bytes:
        donnees = self.alerte_service.obtenir_tableau_bord(db)

        pdf = RapportPDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()

        self._ajouter_titre(pdf)
        self._ajouter_synthese(pdf, donnees)
        self._ajouter_alertes(pdf, donnees)
        self._ajouter_top_5(pdf, donnees)
        self._ajouter_prix_moyens(pdf, db)

        tampon = BytesIO()
        pdf.output(tampon)
        return tampon.getvalue()

    def _ajouter_titre(self, pdf: RapportPDF):
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(*VERT_FONCE)
        pdf.cell(0, 10, "Rapport hebdomadaire", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*GRIS)
        date_generation = datetime.now().strftime("%d/%m/%Y à %H:%M")
        pdf.cell(0, 7, f"Généré le {date_generation}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

    def _ajouter_synthese(self, pdf: RapportPDF, donnees: dict):
        nombre_alertes = donnees["nombre_alertes_actives"]

        pdf.set_fill_color(*GRIS_CLAIR)
        pdf.set_draw_color(*VERT)
        pdf.set_line_width(0.5)

        y_depart = pdf.get_y()
        pdf.rect(10, y_depart, 190, 22, style="DF")
        pdf.set_xy(15, y_depart + 4)
        pdf.set_font("Helvetica", "B", 28)
        pdf.set_text_color(*ROUGE if nombre_alertes > 0 else VERT)
        pdf.cell(20, 14, str(nombre_alertes))

        pdf.set_xy(40, y_depart + 5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(*GRIS)
        libelle = "situation en alerte" if nombre_alertes <= 1 else "situations en alerte"
        pdf.cell(0, 6, f"{libelle} cette semaine", new_x="LMARGIN", new_y="NEXT")
        pdf.set_xy(40, y_depart + 12)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 6, "Variations de prix supérieures au seuil de 20%")

        pdf.ln(28)

    def _ajouter_alertes(self, pdf: RapportPDF, donnees: dict):
        self._titre_section(pdf, "Alertes récentes")

        alertes = donnees["alertes_recentes"]

        if not alertes:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(*GRIS)
            pdf.cell(0, 8, "Aucune alerte sur la période. Le marché est stable.",
                     new_x="LMARGIN", new_y="NEXT")
            pdf.ln(4)
            return

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(*VERT)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(70, 8, "  Produit", border=0, fill=True)
        pdf.cell(70, 8, "  Ville", border=0, fill=True)
        pdf.cell(50, 8, "  Date", border=0, fill=True, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*GRIS)
        for index, alerte in enumerate(alertes):
            fill = index % 2 == 0
            if fill:
                pdf.set_fill_color(*GRIS_CLAIR)
            date_formatee = self._formater_date(alerte["date"])
            pdf.cell(70, 7, f"  {alerte['produit_nom']}", border=0, fill=fill)
            pdf.cell(70, 7, f"  {alerte['ville_nom']}", border=0, fill=fill)
            pdf.cell(50, 7, f"  {date_formatee}", border=0, fill=fill,
                     new_x="LMARGIN", new_y="NEXT")

        pdf.ln(6)

    def _ajouter_top_5(self, pdf: RapportPDF, donnees: dict):
        self._titre_section(pdf, "Top 5 des plus fortes hausses")

        top_5 = donnees["top_5_hausses"]

        if not top_5:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(*GRIS)
            pdf.cell(0, 8, "Aucune hausse significative enregistrée sur la période.",
                     new_x="LMARGIN", new_y="NEXT")
            pdf.ln(4)
            return

        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(*VERT)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(20, 8, "  Rang", border=0, fill=True)
        pdf.cell(120, 8, "  Produit", border=0, fill=True)
        pdf.cell(50, 8, "  Variation", border=0, fill=True, new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*GRIS)
        for index, entree in enumerate(top_5):
            fill = index % 2 == 0
            if fill:
                pdf.set_fill_color(*GRIS_CLAIR)
            pdf.cell(20, 7, f"  {entree['rang']}", border=0, fill=fill)
            pdf.cell(120, 7, f"  {entree['produit_nom']}", border=0, fill=fill)
            pdf.set_text_color(*ROUGE)
            pdf.cell(50, 7, f"  +{entree['variation_pourcent']}%", border=0, fill=fill,
                     new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(*GRIS)

        pdf.ln(6)

    def _ajouter_prix_moyens(self, pdf: RapportPDF, db: Session):
        self._titre_section(pdf, "Prix moyens récents par produit")

        produits = self.prix_repository.lister_produits(db)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*GRIS)
        for index, produit in enumerate(produits):
            # Calcul de la moyenne du produit sur toutes les villes
            moyenne = self._calculer_moyenne_produit(db, produit.id)

            fill = index % 2 == 0
            if fill:
                pdf.set_fill_color(*GRIS_CLAIR)
            pdf.cell(110, 7, f"  {produit.nom_fr} ({produit.unite})",
                     border=0, fill=fill)
            valeur = f"{moyenne:,.0f}".replace(",", " ") if moyenne else "Aucune donnée"
            pdf.cell(80, 7, f"  {valeur}", border=0, fill=fill,
                     new_x="LMARGIN", new_y="NEXT")

    def _calculer_moyenne_produit(self, db: Session, produit_id: int):
        from datetime import timedelta
        from src.backend.models.modeles import PrixMarche

        date_limite = datetime.now() - timedelta(days=30)
        prix = db.query(PrixMarche).filter(
            PrixMarche.produit_id == produit_id,
            PrixMarche.date_saisie >= date_limite
        ).all()

        if not prix:
            return None
        return sum(p.prix for p in prix) / len(prix)

    def _titre_section(self, pdf: RapportPDF, titre: str):
        pdf.ln(2)
        y = pdf.get_y()
        pdf.set_fill_color(*ORANGE)
        pdf.rect(10, y + 1, 3, 6, style="F")
        pdf.set_xy(16, y)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(*VERT_FONCE)
        pdf.cell(0, 8, titre, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    def _formater_date(self, date_valeur) -> str:
        if isinstance(date_valeur, str):
            try:
                date_valeur = datetime.fromisoformat(date_valeur)
            except ValueError:
                return date_valeur
        return date_valeur.strftime("%d/%m/%Y")