from django.db import models
from django.contrib.auth.models import User
from textblob import TextBlob

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each entry is linked to a user
    content = models.TextField()  # Journal entry text
    mood = models.CharField(max_length=50, blank=True, null=True)  # AI-detected mood
    sentiment = models.CharField(max_length=10, blank=True, null=True)  # Positive/Negative/Neutral
    suggestion = models.TextField(blank=True, null=True)  # AI-based mood suggestion
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def analyze_sentiment(self):
        """Analyzes the sentiment of the journal entry using TextBlob."""
        analysis = TextBlob(self.content)
        polarity = analysis.sentiment.polarity

        if polarity > 0:
            return "Positive"
        elif polarity < 0:
            return "Negative"
        else:
            return "Neutral"

    def infer_mood(self):
        """Automatically assigns a mood based on sentiment."""
        mood_mapping = {
            "Positive": "Happy",
            "Negative": "Sad",
            "Neutral": "Calm"
        }
        return mood_mapping.get(self.sentiment, "Unknown")

    def suggest_activity(self):
        """Suggests an activity based on detected sentiment."""
        mood_suggestions = {
            "Positive": "Keep up the good mood! Write more happy moments. 😊",
            "Negative": "Try meditating, listening to music, or talking to a friend. ❤️",
            "Neutral": "Consider taking a walk or reading a book. 📖"
        }
        return mood_suggestions.get(self.sentiment, "Reflect on your thoughts.")

    def save(self, *args, **kwargs):
        """Auto-set sentiment, mood, and suggestion before saving."""
        if not self.sentiment:
            self.sentiment = self.analyze_sentiment()
        if not self.mood:
            self.mood = self.infer_mood()
        if not self.suggestion:
            self.suggestion = self.suggest_activity()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.created_at})"
