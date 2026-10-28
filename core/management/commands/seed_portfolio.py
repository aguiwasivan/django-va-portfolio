import csv
import io
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from core.models import Profile, Skill
from projects.models import Project, ProjectAttachment
from core.skill_content import seed_skills

BIO = '''I am an aspiring Virtual Administrative Assistant passionate about organization, productivity, and providing reliable administrative support.

Although I am beginning my professional journey, I am committed to developing practical skills in data entry, email management, calendar scheduling, document preparation, and digital organization.

I am eager to learn, detail-oriented, adaptable, and motivated to support businesses and professionals in their daily operations.'''

class Command(BaseCommand):
    help = 'Create editable practice content without overwriting existing content.'

    @transaction.atomic
    def handle(self, *args, **options):
        if not Profile.objects.exists(): Profile.objects.create(biography=BIO)
        seed_skills()
        names = ['Avery Bennett','Jordan Ellis','Morgan Chen','Riley Patel','Casey Brooks','Taylor Reed','Quinn Foster','Cameron Lee','Dakota Hayes','Alex Rivera','Jamie Park','Reese Carter','Drew Morgan','Skyler James','Parker Lane']
        headers = ['Employee ID','Full Name','Department','Email Address','Employment Status','Date Joined']
        rows = [[f'EMP-{i+1:03}',name,['Operations','Finance','Marketing','People','Customer Support'][i%5],name.lower().replace(' ','.')+'@example.com','On leave' if i == 8 else 'Active',f'2026-{i%6+1:02}-{i+3:02}'] for i,name in enumerate(names)]
        days = []
        for i,day in enumerate(['Monday','Tuesday','Wednesday','Thursday','Friday']):
            days.append({'name':day,'date':f'Nov {2+i}', 'events':[{'time':'09:00–09:30','title':'Inbox & daily priorities','kind':'admin'},{'time':'09:30–10:30','title':['Weekly team meeting','Client appointment','Project check-in','Client appointment','Weekly team review'][i],'kind':'meeting'},{'time':'10:30–12:00','title':'Focus: project planning','kind':'focus'},{'time':'12:00–13:00','title':'Lunch break','kind':'break'},{'time':'13:00–14:00','title':'Documents & follow-ups','kind':'admin'},{'time':'14:00–15:00','title':'Focus: weekly deliverables','kind':'focus'},{'time':'15:00–15:30','title':'Schedule coordination','kind':'admin'},{'time':'15:30–16:00','title':'Daily deadline check','kind':'meeting'}]})
        emails = [
            {'subject':'Confirmed: project planning meeting — November 3','to':'Jordan Ellis <jordan.ellis@example.com>','body':'Hi Jordan,\n\nThank you for confirming your availability. Our project planning meeting is scheduled for Tuesday, November 3, 2026, from 9:30 to 10:30 AM UTC.\n\nWe will review priorities, confirm deliverables, and agree on next steps. A video meeting invitation would be sent separately in a real workflow. Please let me know if you would like to add an agenda item.\n\nBest regards,\nYour Name','label':'Meeting confirmation'},
            {'subject':'Request to reschedule our appointment','to':'Morgan Chen <morgan.chen@example.com>','body':'Hi Morgan,\n\nWould it be possible to move our Thursday, November 5 appointment from 9:30 AM to either 11:00 AM Thursday or 9:30 AM Friday, November 6 (UTC)? An unexpected scheduling conflict has come up.\n\nI apologize for the inconvenience. Please let me know which option works best; I will update the invitation after your confirmation.\n\nThank you for your flexibility,\nYour Name','label':'Appointment rescheduling'},
            {'subject':'Following up: feedback on the draft agenda','to':'Avery Bennett <avery.bennett@example.com>','body':'Hi Avery,\n\nI am following up on the draft agenda shared on Monday. When convenient, could you review the discussion topics and send any additions by Thursday, November 5 at 3:00 PM UTC?\n\nYour input will help me prepare the final version before Friday’s meeting. Please let me know if you need more time.\n\nThank you,\nYour Name','label':'Professional follow-up'}]
        agenda = {'title':'Weekly Operations Planning','date':'November 2, 2026 · 09:30–10:30 UTC','attendees':['Avery Bennett — Operations','Jordan Ellis — Finance','Morgan Chen — Marketing'],'topics':[{'time':'09:30','topic':'Welcome & review of previous actions','presenter':'Avery Bennett'},{'time':'09:40','topic':'Budget and resource update','presenter':'Jordan Ellis'},{'time':'09:55','topic':'Upcoming campaign priorities','presenter':'Morgan Chen'},{'time':'10:10','topic':'Timeline, blockers & ownership','presenter':'Avery Bennett'},{'time':'10:25','topic':'Confirm decisions & next steps','presenter':'All attendees'}],'actions':['Jordan: circulate budget summary by Nov 3.','Morgan: share campaign draft by Nov 4.','Avery: update the task tracker by Nov 5.']}
        specs = [
            ('employee-data-entry','Employee Data Entry & Organization','Data Entry','Created a structured employee information tracker using fictional data to demonstrate spreadsheet organization, formatting, sorting, and record management.','Microsoft Excel\nGoogle Sheets','Data entry\nSpreadsheet formatting\nData organization\nSorting and filtering\nAttention to detail','spreadsheet',{'headers':headers,'rows':rows},'I organized 15 fictional employee records into a consistent six-column structure. IDs are unique, dates use ISO format, and departments and statuses use consistent labels. The preview supports searching; the CSV can be opened in a spreadsheet and sorted or filtered.'),
            ('executive-calendar','Executive Calendar Management','Scheduling','Designed a weekly executive calendar demonstrating meeting scheduling, appointment coordination, deadline tracking, and time management.','Google Calendar\nGoogle Sheets','Calendar scheduling\nAppointment coordination\nDeadline tracking\nTime management','calendar',{'days':days},'This fictional workweek balances meetings, focused work, administrative follow-ups, and lunch breaks. All times are UTC. Sessions do not overlap, and the end-of-day review makes deadlines visible. Real invitations would be sent only after confirming availability.'),
            ('professional-email','Professional Email Management','Communication','Prepared professional email templates demonstrating clear communication, appointment coordination, and business correspondence.','Gmail\nGoogle Docs','Professional communication\nEmail organization\nFollow-up\nAttention to detail','email',{'emails':emails},'These three fictional drafts use descriptive subjects, clear requests, explicit dates and time zones, and courteous closings. They demonstrate how I would confirm a meeting, propose a schedule change, and follow up on a document.'),
            ('meeting-agenda','Meeting Agenda & Document Preparation','Documentation','Prepared a structured business meeting agenda demonstrating document formatting, information organization, and professional communication.','Microsoft Word\nGoogle Docs','Document preparation\nInformation organization\nMeeting coordination\nProfessional communication','agenda',agenda,'This one-hour practice agenda gives each topic a time and presenter, then records example follow-up actions with owners and due dates. The PDF is a ready-to-review sample document, using fictional participants throughout.')]
        for order,(slug,title,category,description,tools_used,skills,kind,data,details) in enumerate(specs):
            project,_ = Project.objects.get_or_create(slug=slug,defaults={'title':title,'category':category,'description':description,'detailed_content':details,'tools_used':tools_used,'demonstrated_skills':skills,'preview_type':kind,'preview_data':data,'featured':True,'display_order':order})
            if kind == 'spreadsheet':
                output = io.StringIO(newline='')
                writer = csv.writer(output)
                writer.writerow(headers)
                writer.writerows(rows)
                self.attach(project,'Employee tracker','csv',output.getvalue().encode('utf-8-sig'))
            if kind == 'agenda':
                buffer = io.BytesIO()
                pdf = canvas.Canvas(buffer,pagesize=A4)
                pdf.setTitle('Practice Project - Weekly Operations Planning')
                pdf.setFillColor(colors.HexColor('#0F172A'))
                pdf.rect(0,690,600,152,fill=1,stroke=0)
                pdf.setFillColor(colors.white)
                pdf.setFont('Helvetica',11)
                pdf.drawString(45,795,'PRACTICE PROJECT / MEETING AGENDA')
                pdf.setFont('Helvetica-Bold',22)
                pdf.drawString(45,752,agenda['title'])
                pdf.setFont('Helvetica',11)
                pdf.drawString(45,720,agenda['date'].replace('·','|').replace('–','-'))
                y = 650
                for line in ['ATTENDEES',*agenda['attendees'],'','DISCUSSION TOPICS',*[f"{t['time']}  {t['topic']} / {t['presenter']}" for t in agenda['topics']],'','EXAMPLE ACTION ITEMS',*agenda['actions'],'','Sample only. All people and events are fictional.']:
                    pdf.setFillColor(colors.HexColor('#334155'))
                    pdf.setFont('Helvetica',10)
                    pdf.drawString(45,y,line.replace('—','-'))
                    y -= 24
                pdf.showPage()
                pdf.save()
                self.attach(project,'Meeting agenda','pdf',buffer.getvalue())
        self.stdout.write(self.style.SUCCESS('Portfolio seeded. Existing edits preserved.'))

    def attach(self,project,label,extension,data):
        attachment,created = ProjectAttachment.objects.get_or_create(project=project,label=label,defaults={'file_type':extension})
        if created or not attachment.file or not attachment.file.storage.exists(attachment.file.name):
            attachment.file.save(f'{project.slug}.{extension}',ContentFile(data),save=True)
