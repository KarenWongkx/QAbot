import os
import time
from Bani.Bani import Bani
from Bani.core.FAQ import FAQ
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class BaniBot:
    FAQSTORE_PATH = "./faqStore"
    CSV_PATH = "./csv_folder/"
    MODEL_PATH = "./generatedModel"

    def __init__(self):
        self.load_faq()

    def load_faq(self):
        faq_list = []
        # this look at the faqStore for .pkl extension, create faq with the file_name
        for file_name in os.listdir(self.FAQSTORE_PATH):
            if file_name.endswith(".pkl"):
                print(f"Reading {file_name}")
                faq_name = file_name.partition('.')[0]
                faq_name = FAQ(name=faq_name)
                faq_name.load(self.FAQSTORE_PATH)
                faq_list.append(faq_name)
        
        global masterBot
        masterBot = Bani(FAQs=faq_list, modelPath=self.MODEL_PATH)
        print(f"MasterBot created")
        return masterBot

def check_bot_answering():
    print("Test bot, answering ...")
    out = masterBot.findClosest("My parents usually come over to help me with caring for my children on weekdays. Can they do so?", K = 5)
    print(out[0].answer)


class OnMyWatch:
    watchDirectory = "./generatedModel"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created' or event.event_type == 'modified':
            print(f"Changes made to {event.src_path}")
            BaniBot()


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()

    