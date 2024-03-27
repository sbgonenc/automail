import yagmail
import json
import os
from pprint import pprint
import time

def get_current_dir(attach_file_name_rel):
    cwd = os.getcwd()
    paths = attach_file_name_rel.split("/")
    return os.path.join(cwd, paths[-2], paths[-1])

def parse_sent_emails(infile):
    mail_list = []
    with open(infile, "r") as f:
        for line in f:
            sent_email = line.strip().split(" ")[-1]
            mail_list.append(sent_email)
    return mail_list

def json_parser(injson):
    ### returns name, e-mail, diploma_path
    with open(injson, "r", encoding="utf-8") as j:

       the_j = json.load(j)
       for keys in the_j:

           name = the_j[keys]["isim"]
           email = the_j[keys]["eposta"]
           diploma_path = get_current_dir(the_j[keys]["png_dosya_mutlak"])

           yield (name, email, diploma_path)


def yagmail_setter(sender_email, applicationpassword):
    return yagmail.SMTP(user=sender_email, password=applicationpassword)


def mail_sender(set_yag, email, name, diploma_path):

    contents = [f'Merhaba {name}!',
                '\nMezuniyetin için tebrikler.\n',
                '\nEkte senin için hazırladığımız diplomayı bulabilirsin. '
                'Diplomayı kod ile hazırladığımızdan hatalar olabilir. Bu durumda en kısa sürede (deadline cumartesi 23:59) bu maile cevap vererek problemini iletmen gerek ki diplomanı doğru haline getirerek bastırabilelim.\n',
                '\nEğer diploma örneğinde bir sorun yoksa bu maile cevap vermen gerekmiyor.\n',
                '\n8 Eylül tarihinde görüşmek üzere!\n',
                '\nSevgiler,',
                "Alternatif Mezuniyet Ekibi"]

    if "Gelmiyor" in diploma_path:
        contents.append("\n\n\nNOT: Diplomanız törene gelmediğinizden ötürü basılmayacaktır. Hata olduğunu düşünüyorsanız lütfen iletişime geçin")

    elif "Basilacak" in diploma_path:
        contents.append("\n\n\nNOT: Diplomanız törene geleceğinizden basılacaktır. Hata olduğunu düşünüyorsanız lütfen iletişime geçin")


    set_yag.send(email, 'Alternatif Diploman', contents, attachments=r"{}".format(diploma_path))


def main(injson, sender_address, application_password, sent_mail_list=None):

    yag_set = yagmail_setter(sender_address, application_password)

    logger = open("sent_emails.txt", "w")
    for the_tpl in json_parser(injson):

        if the_tpl[1] in sent_mail_list: continue

        mail_sender(yag_set, the_tpl[1], the_tpl[0], the_tpl[2])

        logger.write(f"Sent email to:  {the_tpl[1]}\n")
        print(f"Sent email to:  {the_tpl[1]}")

    logger.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.time()
    sent_mail_list = parse_sent_emails()
    the_json = "email_list.json"
    main(the_json, "sender@gmail.com", "your_sender_api_key", sent_mail_list=sent_mail_list)
    print(time.time()-start)


