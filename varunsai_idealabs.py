import os
import whisper

# Initialize Whisper model
model = whisper.load_model("tiny")

def transcribe_media_files(input_dir, output_dir=None):
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Supported media file extensions
    media_extensions = ('.mp3', '.wav', '.m4a', '.mp4', '.mkv', '.avi')

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(media_extensions):
                file_path = os.path.join(root, file)
                print(f"Transcribing: {file_path}")

                # Transcription
                result = model.transcribe(file_path)
                transcription = result["text"]

                # Determine output path
                if output_dir:
                    rel_path = os.path.relpath(root, input_dir)
                    target_dir = os.path.join(output_dir, rel_path)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    output_file = os.path.join(target_dir, f"{os.path.splitext(file)[0]}.txt")
                else:
                    output_file = os.path.join(root, f"{os.path.splitext(file)[0]}.txt")

                # Save transcription
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(transcription)

                print(f"Saved transcription to: {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transcribe media files using Whisper.")
    parser.add_argument("input_dir", help="Directory containing media files")
    parser.add_argument("-o", "--output_dir", help="Directory to save transcriptions", default=None)

    args = parser.parse_args()

    transcribe_media_files(args.input_dir, args.output_dir)
