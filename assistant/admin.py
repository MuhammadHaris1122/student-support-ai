from django.contrib import admin
from .models import TrainingDocument, ChatMessage
from .rag_service import ingest_document

@admin.register(TrainingDocument)
class TrainingDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_processed')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not obj.is_processed and obj.file:
            try:
                ingest_document(obj.file.path)
                obj.is_processed = True
                obj.save()
            except Exception as e:
                print(f"Error processing RAG document: {e}")

admin.site.register(ChatMessage)