from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, DEFAULT_PROFILE_URL
from werkzeug.utils import secure_filename
import hashlib
import time

class SupabaseStorage:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.bucket_name = "ssis-student-photos"
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    
    def _generate_filename_hash(self, id_number, file_ext):
        timestamp = str(time.time())
        hash_input = f"{id_number}_{timestamp}"
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"{id_number}_{hash_value}.{file_ext}"
    
    def _find_student_photo(self, id_number):
        try:
            files = self.supabase.storage.from_(self.bucket_name).list("students")
            for file in files:
                if file['name'].startswith(f"{id_number}_"):
                    return file['name']
            return None
        except Exception as e:
            print(f"Error finding photo: {str(e)}")
            return None
    
    def upload_student_photo(self, photo, id_number):
        if not photo or not photo.filename:
            return DEFAULT_PROFILE_URL
        
        filename = secure_filename(photo.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in self.allowed_extensions:
            raise ValueError("Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.")
        
        try:
            storage_filename = self._generate_filename_hash(id_number, file_ext)
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
    
    def rename_student_photo(self, old_id_number, new_id_number):
        try:
            old_filename = self._find_student_photo(old_id_number)
            
            if old_filename:
                old_file_path = f"students/{old_filename}"
                file_ext = old_filename.rsplit('.', 1)[1].lower()
                
                file_data = self.supabase.storage.from_(self.bucket_name).download(old_file_path)
                
                new_filename = self._generate_filename_hash(new_id_number, file_ext)
                new_file_path = f"students/{new_filename}"
                
                self.supabase.storage.from_(self.bucket_name).upload(
                    new_file_path,
                    file_data,
                    file_options={"content-type": f"image/{file_ext}"}
                )
                
                self.supabase.storage.from_(self.bucket_name).remove([old_file_path])
                
                return self.supabase.storage.from_(self.bucket_name).get_public_url(new_file_path)
            
            return "KEEP_EXISTING"
                    
        except Exception as e:
            print(f"Rename error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to rename photo: {str(e)}")

    def update_student_photo(self, photo, id_number, old_id_number=None):
        if not photo or not photo.filename:
            if old_id_number and old_id_number != id_number:
                return self.rename_student_photo(old_id_number, id_number)
            return "KEEP_EXISTING"
        
        filename = secure_filename(photo.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in self.allowed_extensions:
            raise ValueError("Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.")
        
        try:
            if old_id_number and old_id_number != id_number:
                self.delete_student_photo(old_id_number)
            
            self.delete_student_photo(id_number)
            
            storage_filename = self._generate_filename_hash(id_number, file_ext)
            file_path = f"students/{storage_filename}"
            file_content = photo.read()
            
            self.supabase.storage.from_(self.bucket_name).upload(
                file_path,
                file_content,
                file_options={"content-type": photo.content_type}
            )
            
            return self.supabase.storage.from_(self.bucket_name).get_public_url(file_path)
        
        except Exception as e:
            print(f"Update error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to update photo: {str(e)}")
    
    def delete_student_photo(self, id_number):
        try:
            filename = self._find_student_photo(id_number)
            if filename:
                file_path = f"students/{filename}"
                self.supabase.storage.from_(self.bucket_name).remove([file_path])
                
        except Exception as e:
            print(f"Delete error: {str(e)}")

supabase_storage = SupabaseStorage()