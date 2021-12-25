import os
import textract
import moviepy.editor as mpe


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
        if fext not in ftypes:
            raise KeyError("Unsupported file type")
        return fext

    def get_supported_ftypes(self):
        return ['.html', '.jpeg', '.jpg', '.mp3', '.pdf', '.png', '.txt', '.wav', '.mp4', '.mov']

    def _prep_text(self):
        text_prepped = self.text[2:-1].replace("\\r\\n", " ")
        text_prepped = text_prepped.replace("\\n", " ")
        text_prepped = text_prepped.replace("\\x0c", " ")
        text_prepped = ' '.join(text_prepped.split()).strip()
        print(text_prepped)
        return text_prepped

    def _parse_text(self):
        ftype = self.get_ftype()

        if ftype in ('.mp4', '.mov'):
            new_path = ''
            with mpe.VideoFileClip(self.path) as clip:
                audio = clip.audio
                new_path = self.path[:-4] + ".wav"
                audio.write_audiofile(filename=new_path)    
                
            if os.path.exists(self.path):
                os.remove(self.path)
            self.path = new_path

        text = ''
        print(self.path)
        text = str(textract.process(self.path))
        print(text)
        return text
