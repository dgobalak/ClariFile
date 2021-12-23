import os
import textract
import moviepy.editor as mpe
import pdfplumber
import speech_recognition as sr

class Parser:
    def __init__(self, path):
        self.path = path
        self.text = self._parse_text()
        self.ftype = self.get_ftype()
        self.prepped_text = self._prep_text()

    def get_text(self):
        return self.prepped_text if self.prepped_text else self._prep_text(self.text)

    def get_ftype(self):
        _, fext = os.path.splitext(self.path)
        ftypes = self.get_supported_ftypes()
        if fext not in ftypes.keys():
            raise KeyError("Unsupported file type") 
        return ftypes[fext]

    def get_supported_ftypes(self):
        return {
            ".wav": "Audio",
            ".mp4": "Video",
            ".pdf": "PDF",
            ".png": "Image",
        }

    def _prep_text(self):
        text_prepped = self.text[2:-1].replace("\\r\\n", " ")
        text_prepped = text_prepped.replace("\\n", " ")
        text_prepped = text_prepped.replace("\\x0c", " ")
        text_prepped = ' '.join(text_prepped.split()).strip()
        return text_prepped

    def _parse_text(self):
        ftype = self.get_ftype()
        if ftype == "PDF":
            all_text = ''
            with pdfplumber.open(self.path) as pdf:
                for pdf_page in pdf.pages:
                    single_page_text = pdf_page.extract_text()
                    all_text = all_text + '\n' + single_page_text
            return str(all_text)                        
        elif ftype == "Audio":
            text = ''
            recognizer = sr.Recognizer()
            with sr.AudioFile(self.path) as source:
                audio_data = recognizer.record(source)
                text = str(recognizer.recognize_google(audio_data))
            return text
        elif ftype == "Video":
            audio = mpe.VideoFileClip(self.path).audio
            self.path = self.path[:-4] + ".wav"
            audio.write_audiofile(filename=self.path)
            return self._parse_text()
        elif ftype == "Image":
            pass
