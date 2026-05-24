# Dashboard routes will be implemented here
from fastapi import APIRouter, HTTPException

from backend.database.db import uploads_collection

router = APIRouter()


@router.get("/{user_id}")
def get_dashboard(user_id: str):

    latest_upload = uploads_collection.find_one(
        {"user_id": user_id},
        sort=[("_id", -1)]
    )

    if not latest_upload:
        raise HTTPException(
            status_code=404,
            detail="No dashboard data found"
        )

    return {
        "metrics": latest_upload.get("metrics", {}),
        "insights": latest_upload.get("insights", []),
        "debug": latest_upload.get("debug", {}),
        "clusters": latest_upload.get("clusters", {}),
    }