from string import Template

from flask import render_template


class ContentSupplier:
    @staticmethod
    def get_simple_web_page_content(part, parts_amount, page):
        part_number = int(part)
        if part_number > parts_amount:
            part = part % parts_amount
        if part_number < 1:
            render_template(page, video_url='Saba_Haim_Part_1.mp4',
                            next='2', prev='0')
        video_template = Template('Saba_Haim_Part_$num.mp4')
        next_part = part_number + 1
        prev_part = part_number - 1
        return render_template(page, video_url=video_template.substitute(num=str(part)),
                               next=str(next_part), prev=str(prev_part), curr=str(part))
