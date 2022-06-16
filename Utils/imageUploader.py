import cloudinary;
import cloudinary.uploader
from globals.config import cloudinary_api_key, cloudinary_api_secret, cloudinary_name;

cloudPhoto = cloudinary.config(
    cloud_name = cloudinary_name,
    api_key = cloudinary_api_key,
    api_secret = cloudinary_api_secret,
    secure = True
),
