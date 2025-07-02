import asyncio
import edge_tts
import pygame
import os
import sys
from contextlib import contextmanager

@contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = devnull, devnull
        yield
        sys.stdout, sys.stderr = old_stdout, old_stderr

def speak(text):
    VOICE = 'en-US-AriaNeural'
    OUTPUT_FILE = "test.mp3"

    async def amain():
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(OUTPUT_FILE)

    with suppress_output():
        loop = asyncio.get_event_loop_policy().get_event_loop()
        try:
            loop.run_until_complete(amain())

            pygame.mixer.init()

            pygame.mixer.music.load(OUTPUT_FILE)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        finally:
            loop.close()
            pygame.quit()

speak("hi there")
