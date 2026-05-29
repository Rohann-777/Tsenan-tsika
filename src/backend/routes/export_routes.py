from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.export_controller import ExportController
from src.backend.auth.dependances import verifier_role
from src.backend.models.modeles import Utilisateur


router = APIRouter(prefix="/api/export", tags=["Export"])
controller = ExportController()


@router.get("/rapport-pdf")
def exporter_rapport_pdf(
    db: Session = Depends(get_db),
    analyste: Utilisateur = Depends(verifier_role(["analyste"]))
):
    contenu_pdf = controller.generer_rapport_hebdomadaire(db)

    horodatage = datetime.now().strftime("%Y%m%d")
    nom_fichier = f"tsenantsika_rapport_{horodatage}.pdf"

    return Response(
        content=contenu_pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{nom_fichier}"'
        }
    )