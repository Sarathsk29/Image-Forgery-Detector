from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import cloudinary
import cloudinary.uploader

from app.core.config import get_settings


@dataclass
class StoredAsset:
    label: str
    storage_path: str
    public_url: str
    local_path: str


class BaseStorageService:
    def save_upload(self, case_id: str, filename: str, data: bytes, content_type: str | None = None) -> StoredAsset:
        raise NotImplementedError

    def save_artifact(self, case_id: str, filename: str, data: bytes, content_type: str | None = None, label: str = "artifact") -> StoredAsset:
        raise NotImplementedError

    def save_report(self, case_id: str, filename: str, data: bytes) -> StoredAsset:
        raise NotImplementedError


class LocalStorageService(BaseStorageService):
    def __init__(self) -> None:
        settings = get_settings()
        self.upload_root = Path(settings.local_storage_dir)
        self.artifact_root = Path(settings.local_artifact_dir)
        self.upload_root.mkdir(parents=True, exist_ok=True)
        self.artifact_root.mkdir(parents=True, exist_ok=True)

    def _save_bytes(self, root: Path, subfolder: str, filename: str, data: bytes, label: str) -> StoredAsset:
        suffix = Path(filename).suffix or ".bin"
        safe_name = f"{Path(filename).stem}-{uuid4().hex[:8]}{suffix}"
        target_dir = root / subfolder
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / safe_name
        target_path.write_bytes(data)
        relative_dir = "uploads" if root == self.upload_root else "artifacts"
        public_url = f"/storage/{relative_dir}/{subfolder}/{safe_name}"
        return StoredAsset(label=label, storage_path=str(target_path), public_url=public_url, local_path=str(target_path))

    def save_upload(self, case_id: str, filename: str, data: bytes, content_type: str | None = None) -> StoredAsset:
        return self._save_bytes(self.upload_root, case_id, filename, data, "uploaded evidence")

    def save_artifact(self, case_id: str, filename: str, data: bytes, content_type: str | None = None, label: str = "artifact") -> StoredAsset:
        return self._save_bytes(self.artifact_root, case_id, filename, data, label)

    def save_report(self, case_id: str, filename: str, data: bytes) -> StoredAsset:
        return self._save_bytes(self.artifact_root, case_id, filename, data, "analysis report")


class CloudinaryStorageService(LocalStorageService):
    def __init__(self) -> None:
        super().__init__()
        settings = get_settings()
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )

    def _upload_to_cloudinary(self, file_path: str, folder: str, resource_type: str = "auto") -> str:
        result = cloudinary.uploader.upload(file_path, folder=folder, resource_type=resource_type)
        return result["secure_url"]

    def save_upload(self, case_id: str, filename: str, data: bytes, content_type: str | None = None) -> StoredAsset:
        asset = super().save_upload(case_id, filename, data, content_type)
        asset.public_url = self._upload_to_cloudinary(asset.local_path, f"forensic-platform/uploads/{case_id}")
        return asset

    def save_artifact(self, case_id: str, filename: str, data: bytes, content_type: str | None = None, label: str = "artifact") -> StoredAsset:
        asset = super().save_artifact(case_id, filename, data, content_type, label)
        asset.public_url = self._upload_to_cloudinary(asset.local_path, f"forensic-platform/artifacts/{case_id}")
        return asset

    def save_report(self, case_id: str, filename: str, data: bytes) -> StoredAsset:
        asset = super().save_report(case_id, filename, data)
        asset.public_url = self._upload_to_cloudinary(asset.local_path, f"forensic-platform/reports/{case_id}", resource_type="raw")
        return asset


def guess_content_type(filename: str) -> str:
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"


def get_storage_service() -> BaseStorageService:
    settings = get_settings()
    cloudinary_ready = all(
        [settings.cloudinary_cloud_name, settings.cloudinary_api_key, settings.cloudinary_api_secret]
    )
    if settings.storage_backend == "cloudinary" and cloudinary_ready:
        return CloudinaryStorageService()
    return LocalStorageService()

