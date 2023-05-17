from dialog import SpeechCloudWS, Dialog
import logging

class ExampleDialog(Dialog):
    async def main(self):
        pass

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s',level=logging.DEBUG)

    SpeechCloudWS.run(ExampleDialog, address="0.0.0.0", port=8888)
