from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JournalEntry
from .serializers import JournalEntrySerializer, JournalEntryUpdateSerializer
from .services import process_journal_entry
from .tasks import process_journal_entry_task

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        entry = serializer.save(user=self.request.user)
        # Lancer tâche Celery asynchrone
        process_journal_entry.delay(entry.id)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return JournalEntryUpdateSerializer
        return JournalEntrySerializer

    @action(detail=False, methods=['post'], url_path='upload-audio')
    def upload_audio(self, request):
        if 'audio_file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES['audio_file']
        # Validation
        valid_mimes = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/x-m4a']
        if file.content_type not in valid_mimes:
            return Response({'error': 'Invalid audio format'}, status=status.HTTP_400_BAD_REQUEST)
        # Créer une entrée
        entry = JournalEntry.objects.create(user=request.user, audio_file=file)
        process_journal_entry.delay(entry.id)
        serializer = self.get_serializer(entry)
        return Response(serializer.data, status=status.HTTP_201_CREATED)