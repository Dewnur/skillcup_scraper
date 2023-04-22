import re

import docx
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.shared import Mm
from docx.shared import Pt

from db_models_manager import *
from models import *
from tools.text_preprocessor import comment_tokens


class WordReportGenerator:

    def __init__(self, path: str):
        self.path = path
        self._doc = Document()

    def _init_styles(self):
        header_style = self._doc.styles.add_style('Header1', WD_STYLE_TYPE.PARAGRAPH)
        header_style.font.name = 'Times New Roman'
        header_style.font.size = Pt(11)
        header_style.font.bold = True
        header_style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        header_style.paragraph_format.left_indent = Mm(-3)
        homework_title = self._doc.styles.add_style('homework_title', WD_STYLE_TYPE.PARAGRAPH)
        homework_title.font.name = 'Times New Roman'
        homework_title.font.size = Pt(12)
        homework_title.font.bold = True
        homework_title.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        homework_task_name = self._doc.styles.add_style('homework_task_name', WD_STYLE_TYPE.PARAGRAPH)
        homework_task_name.font.name = 'Roboto'
        homework_task_name.font.size = Pt(11)
        homework_task_name.font.bold = True
        homework_task_name.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        comment = self._doc.styles.add_style('comment', WD_STYLE_TYPE.PARAGRAPH)
        comment.font.name = 'Arial'
        comment.font.size = Pt(11)
        comment.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        comment.paragraph_format.left_indent = Mm(-10)

    def generate_report(self, person: Person):
        self._init_styles()
        header = self._doc.add_paragraph(f'ФИ: {person.name}\nТариф: {person.rate}\nСсылка на канал: ', style='Header1')
        self._add_hyperlink(header, text=f'{person.tg_url}', url=f'{person.tg_url}', color='0000FF', underline=False)
        punc = '________'
        header.add_run(f'\n{punc * 10}')
        cards = fetchall(Card)
        sorted_cards = sorted(cards, key=lambda card: card.sequence_number)
        for card in sorted_cards:
            self._doc.add_paragraph(f'ДОМАШКА {card.sequence_number}:', style='homework_title')
            tasks = fetchall(Task, card_id=card.id)
            sorted_tasks = sorted(tasks, key=lambda task: task.sequence_number)
            for task in sorted_tasks:
                self._doc.add_paragraph(f'{task.name}:', style='homework_task_name')
                comments = fetchall(Comment, task_id=task.id, person_id=person.id)
                if comments is None:
                    self._doc.add_paragraph(f'Нет ответа', style='comment')
                    continue
                sorted_comments = sorted(comments, key=lambda comment: comment.sequence_number)
                content_list = [comment.content for comment in sorted_comments]
                content = '\n'.join(content_list)
                content_tokens = comment_tokens(content)
                comment_paragraph = self._doc.add_paragraph(f'', style='comment')
                for substring, link in content_tokens:
                    if link:
                        self._add_hyperlink(
                            comment_paragraph,
                            text=f'{substring}',
                            url=f'{substring}',
                            color='0000FF',
                            underline=False
                        )
                    else:
                        comment_paragraph.add_run(f'{substring}')

        self._doc.save(self.path)

    def _add_hyperlink(self, paragraph, text, url, color, underline):
        # This gets access to the document.xml.rels file and gets a new relation id value
        part = paragraph.part
        r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

        # Create the w:hyperlink tag and add needed values
        hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
        hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

        # Create a w:r element
        new_run = docx.oxml.shared.OxmlElement('w:r')

        # Create a new w:rPr element
        rPr = docx.oxml.shared.OxmlElement('w:rPr')

        # Add color if it is given
        if not color is None:
            c = docx.oxml.shared.OxmlElement('w:color')
            c.set(docx.oxml.shared.qn('w:val'), color)
            rPr.append(c)

        # Remove underlining if it is requested
        if not underline:
            u = docx.oxml.shared.OxmlElement('w:u')
            u.set(docx.oxml.shared.qn('w:val'), 'single')
            rPr.append(u)

        # Join all the xml elements together add add the required text to the w:r element
        new_run.append(rPr)
        new_run.text = text
        hyperlink.append(new_run)

        paragraph._p.append(hyperlink)
        return hyperlink

    def _split_text_and_link(self, s: str):
        pattern = r'(https?://[^\s]+)'
        result = re.split(pattern, s)
        return result
