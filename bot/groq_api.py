from groq import Groq, BadRequestError
from util.translation import Translation
from util.settings import Settings

client = Groq(
    api_key=Settings.GROQ_API_KEY,
)

def generate_reply(message_history: list, model: str) -> str:
    # Ensure message history is correctly formatted
    formatted_history = [{"role": msg["role"], "content": msg["content"]} for msg in message_history]
    try:
        chat_completion = client.chat.completions.create(
            messages=formatted_history,
            model=model,
        )
        return chat_completion.choices[0].message.content
    except BadRequestError as e:
        if e.error['code'] == 'context_length_exceeded':
            return Translation.get_text('context_length_exceeded')
        else:
            raise e

def transcribe_audio(audio_data):
    transcription = client.audio.transcriptions.create(
        file=("audio.ogg", audio_data),  # Using the in-memory audio data
        model="whisper-large-v3",
        response_format="verbose_json",
    )
    transcription_text = transcription.text
    return transcription_text