from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, DEFAULT_PROFILE_URL
from werkzeug.utils import secure_filename

class SupabaseStorage:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.bucket_name = "ssis-student-photos"
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    
    def upload_student_photo(self, photo, id_number):
        if not photo or not photo.filename:
            return DEFAULT_PROFILE_URL
        
        filename = secure_filename(photo.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in self.allowed_extensions:
            raise ValueError("Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.")
        
        try:
            storage_filename = f"{id_number}.{file_ext}"
            file_path = f"students/{storage_filename}"
            file_content = photo.read()
            
            self.supabase.storage.from_(self.bucket_name).upload(
                file_path,
                file_content,
                file_options={"content-type": photo.content_type}
            )
            
            return self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)
        
        except Exception as e:
            print(f"Upload error: {str(e)}")
            raise Exception(f"Failed to upload photo: {str(e)}")
    
    def update_student_photo(self, photo, id_number, old_id_number=None):
        if not photo or not photo.filename:
            return "KEEP_EXISTING"
        
        filename = secure_filename(photo.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in self.allowed_extensions:
            raise ValueError("Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.")
        
        try:
            if old_id_number and old_id_number != id_number:
                self.delete_student_photo(old_id_number)
            
            storage_filename = f"{id_number}.{file_ext}"
            file_path = f"students/{storage_filename}"
            file_content = photo.read()
            
            self.supabase.storage.from_(self.bucket_name).upload(
                file_path,
                file_content,
                file_options={"content-type": photo.content_type, "upsert": "true"}
            )
            
            return self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)
        
        except Exception as e:
            print(f"Upload error: {str(e)}")
            raise Exception(f"Failed to upload photo: {str(e)}")
    
    def delete_student_photo(self, id_number):
        try:
            old_files = self.supabase.storage.from_(self.bucket_name).list("students")
            for file in old_files:
                if file['name'].startswith(id_number + "."):
                    self.supabase.storage.from_(self.bucket_name).remove([f"students/{file['name']}"])
        except Exception as e:
            print(f"Delete error: {str(e)}")

supabase_storage = SupabaseStorage()