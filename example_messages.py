from dialog import SpeechCloudWS, Dialog, ABNF_INLINE
import random
import asyncio
import logging
from pprint import pprint, pformat

class ExampleDialog(Dialog):
    def on_receive_message(self, data):
        self.logger.debug("Received message:\n{}".format(pformat(data)))

    async def main(self):
        await self.send_message({"message": "Libovolná zpráva od dialogového manažeru", "data": [1, 2, 3]})
        await self.display("Použijte vstupní box u tlačítka Send message")
        recv = await self.pop_message(timeout=5)
        if recv is None:
            await self.display("Nic jste mi neposlali")
        else:
            await self.send_message({"message": "Poslali jste data", "data": recv})


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s', level=logging.DEBUG)

    SpeechCloudWS.run(ExampleDialog, address="0.0.0.0", port=8888)
