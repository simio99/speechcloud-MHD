from dialog import SpeechCloudWS, Dialog, ABNF_INLINE
import random
import asyncio
import logging
from pprint import pprint, pformat

class ExampleDialog(Dialog):
    def on_asr_signal(self, level, speech):
        print(level, speech)

    async def main(self):
        self.sc.on("asr_signal", self.on_asr_signal)
        await self.sc.asr_recognize()
        await asyncio.sleep(10)
        await self.sc.asr_pause()
        

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s', level=logging.DEBUG)

    SpeechCloudWS.run(ExampleDialog, address="0.0.0.0", port=8888)
