from textblob import TextBlob
from rest_framework import viewsets
from .serializers import JournalEntrySerializer
from rest_framework.permissions import IsAuthenticated
from .models import JournalEntry

class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]
    entry.sentiment = analyze_sentiment(entry.text)

    
    # Add the queryset attribute
    queryset = JournalEntry.objects.all()

    def get_queryset(self):
        """Return journal entries belonging to the currently authenticated user."""
        return JournalEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Perform the sentiment analysis and mood detection before saving the entry."""
        entry = serializer.save(user=self.request.user)

        # Ensure that the text is not empty
        if entry.text:
            # Sentiment Analysis using TextBlob
            analysis = TextBlob(entry.text)
            polarity = analysis.sentiment.polarity

            if polarity > 0:
                entry.sentiment = "Positive"
            elif polarity < 0:
                entry.sentiment = "Negative"
            else:
                entry.sentiment = "Neutral"

            # Mood Detection based on keywords (Simple Example)
            mood_keywords = {
                "happy": ["joy", "excited", "glad"],
                "sad": ["depressed", "unhappy", "lonely"],
                "angry": ["frustrated", "mad", "annoyed"],
            }

            for mood, words in mood_keywords.items():
                if any(word in entry.text.lower() for word in words):
                    entry.mood = mood
                    break
            else:
                entry.mood = "Neutral"  # Default if no mood detected

            # Save the updated entry with sentiment and mood
            entry.save()
