"""Uses the MicTranscriber class to transcribe audio from a microphone."""

import argparse
import sys
import time
import popup
import threading
import signal

from moonshine_voice import (
    MicTranscriber,
    TranscriptEventListener,
    get_model_for_language,
)


stop_event = threading.Event()


class TerminalListener(TranscriptEventListener):
    def __init__(self):
        self.last_line_text_length = 0

    # Assume we're on a terminal, and so we can use a carriage return to
    # overwrite the last line with the latest text.
    def update_last_terminal_line(self, new_text: str):
        print(f"\r{new_text}", end="", flush=True)
        if len(new_text) < self.last_line_text_length:
            # If the new text is shorter than the last line, we need to
            # overwrite the last line with spaces.
            diff = self.last_line_text_length - len(new_text)
            print(f"{' ' * diff}", end="", flush=True)
        # Update the length of the last line text.
        self.last_line_text_length = len(new_text)
        if "fluffy cloud" in new_text.lower():
            popup.root.after(0, popup.open_popup, "fluffy cloud")
        elif "christmas tree" in new_text.lower():
            popup.root.after(0, popup.open_popup, "christmas tree")

    def on_line_started(self, event):
        self.last_line_text_length = 0

    def on_line_text_changed(self, event):
        self.update_last_terminal_line(event.line.text)

    def on_line_completed(self, event):
        self.update_last_terminal_line(event.line.text)
        print("\n", end="", flush=True)


# If we're not on an interactive terminal, print each line as it's completed.


class FileListener(TranscriptEventListener):
    def on_line_completed(self, event):
        print(event.line.text)


def start_listening():
    parser = argparse.ArgumentParser(description="Fluffy Cloud and Christmas Tree - Intro to CS")
    parser.add_argument(
        "--language", 
        type=str, 
        default="en", 
        help="Language to use for transcription"
    )
    parser.add_argument(
        "--model-arch",
        type=str,
        default=None,
        help="Model architecture to use for transcription",
    )
    args = parser.parse_args()
    model_path, model_arch = get_model_for_language(args.language, args.model_arch)

    mic_transcriber = MicTranscriber(model_path=model_path, model_arch=model_arch)

    if sys.stdout.isatty():
        listener = TerminalListener()
    else:
        listener = FileListener()

    print("Listening to the microphone, press Ctrl+C to stop...", file=sys.stderr)
    mic_transcriber.add_listener(listener)
    mic_transcriber.start()
    try:
        while not stop_event.is_set():
            time.sleep(0.1)
    finally:
        mic_transcriber.stop()
        mic_transcriber.close()


def shutdown():
    print("\nShutting down...")
    stop_event.set()
    popup.root.quit()


def handle_sigint(sig, frame):
    shutdown()


signal.signal(signal.SIGINT, handle_sigint)


if __name__ == "__main__":
    listener_thread = threading.Thread(
        target=start_listening,
        daemon=True
    )
    listener_thread.start()

    popup.init()