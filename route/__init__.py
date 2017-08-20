from route.db import db_session
from route.models import Domain

import os
import subprocess


class Route(object):
    def __init__(self, ip, domain):
        self.ip = ip
        self.domain = domain

    def __str__(self):
        return self.domain

    def search(self, option, value):
        """ search domain routing info """
        d = Domain

        if option == "ip":
            d.filter(Domain.ip == value)

        elif option == "domain":
            d.filter(Domain.domain == value)

        elif option == "user":
            d.filter(Domain.user == value)

        return d.all()

    def register(self, user):
        """ register domain nginx reverse proxy """
        self.action_nginx("stop")
        self.generate_cert()
        self.write_file()
        self.action_nginx("start")

        db_session.add(Domain(self.ip, self.domain, user))
        db_session.commit()

    def action_nginx(self, action):
        s = subprocess.Popen(
            ["service", "nginx", action],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = s.communicate()

        print(out, err)

    def generate_cert(self):
        s = subprocess.Popen(
            ["letsencrypt", "certonly", "-a", "standalone", "-d", self.domain],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = s.communicate()

        print(out, err)

    def write_file(self):
        data = "server {\n"\
            "\tlisten 443 ssl;\n"\
            "\tserver_name " + self.domain + ";\n\n"\
            "\tssl_certificate /etc/letsencrypt/live/" + self.domain + "/fullchain.pem;\n"\
            "\tssl_certificate_key /etc/letsencrypt/live/" + self.domain + "/privkey.pem;\n\n"\
            "\tlocation / {\n"\
            "\t\tproxy_redirect off;\n"\
            "\t\tproxy_pass_header Server;\n"\
            "\t\tproxy_set_header Host $http_host;\n"\
            "\t\tproxy_set_header X-Real-IP $remote_addr;\n"\
            "\t\tproxy_set_header X-Scheme $scheme;\n"\
            "\t\tproxy_pass http://" + self.ip + ";\n"\
            "\t}\n"\
            "}\n\n"\
            "server {\n"\
            "\tlisten 80;\n"\
            "\tserver_name " + self.domain + ";\n\n"\
            "\tlocation / {\n"\
            "\t\trewrite ^(.*) https://$host$1 permanent;\n"\
            "\t}\n"\
            "}\n"

        with open("/etc/nginx/sites-available/{}".format(self.domain), "a") as f:
            f.write(data)

        os.symlink("/etc/nginx/sites-available/{}".format(self.domain), "/etc/nginx/sites-enabled/{}".format(self.domain))

    def __del__(self):
        del self
