from datetime import timedelta
from typing import List
from uuid import UUID

from fastapi import File, UploadFile

import crud
from minio_client import MinioClient
from schema.image import ImageCreate


class UserImagesCollection(object):
    def __init__(self, db) -> None:
        self.db = db
        self.minio_client = MinioClient()
        
    def str_to_bool(self, value: str) -> bool:
        return value.lower() == 'true'
        
    def upload_image(self, user_profile_id: UUID, index, avatar, file: UploadFile = File(...)):
        # Upload the file to MinIO
        file_location = f"{user_profile_id}/{file.filename}"
        self.minio_client.upload_file("image", file.filename, file.file, file.size)
        
        download_url = self.minio_client.client.get_presigned_url("GET", "image", file.filename, expires=timedelta(days=7))
        print(download_url)
        # Store the image info in the database
        print(file)
        image_create = ImageCreate(
            name=file.filename,
            url=file_location,
            user_profile_id=user_profile_id,
            index=index,
            avatar=self.str_to_bool(avatar),
        )
        
        db_images = crud.post_profile_image(self.db, image_create)
        return db_images