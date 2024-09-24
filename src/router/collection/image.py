from datetime import timedelta
from typing import List
from uuid import UUID

from fastapi import File, UploadFile

import conf
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
        self.minio_client.upload_file(conf.MINIO_BUCKET_NAME, file_location, file.file, file.size)
        
        download_url = conf.DOMAIN + conf.MINIO_BUCKET_NAME + f"/{file_location}"
        
        # Store the image info in the database
        image_create = ImageCreate(
            name=file.filename,
            url=download_url,
            user_profile_id=user_profile_id,
            index=index,
            avatar=self.str_to_bool(avatar),
        )
        
        db_images = crud.post_profile_image(self.db, image_create)
        return db_images
    
    def delete_image(self, user_profile_id: UUID, image_id: UUID):
        # Get the image info from the database
        db_image = crud.get_image(self.db, image_id)
        
        # Delete the image from MinIO
        file_location = f"{user_profile_id}/{db_image.name}"
        self.minio_client.remove_file(conf.MINIO_BUCKET_NAME, file_location)
        
        # Delete the image info from the database
        crud.delete_image_by_id(self.db, image_id)
        return True