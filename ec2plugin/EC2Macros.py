from trac.wiki.api import WikiSystem
from trac.wiki.macros import WikiMacroBase
from trac.config import Option

from genshi.builder import tag
from boto.ec2.connection import EC2Connection

class AWSInstanceTableMacro(WikiMacroBase):
    """Draws a table of your EC2 instances. Configure your keys in trac.ini"""

    ACCESS_KEY = Option('ec2','access_key',doc="AWS Access Key")
    SECRET_KEY = Option('ec2','secret_key',doc="AWS Secret Key")
    
    def expand_macro(self, formatter, name, content):

        if self.ACCESS_KEY is None:
            return tag.p("[EC2 access key is missing from trac.ini]")
        
        if self.SECRET_KEY is None:
            return tag.p("[EC2 secret key is missing from trac.ini]")

        ec2 = EC2Connection(self.ACCESS_KEY, self.SECRET_KEY)

        headings = ("Instance", "AMI", "Key", "IP", "State", "Monitored")
        table = tag.table(tag.thead(tag.tr([tag.th(title) for title in headings])), class_="listing")
        tbody = tag.tbody()
        
        for r in ec2.get_all_instances():
            groups = [g.id for g in r.groups]
            for i in r.instances:
                if i.state == "terminated":
                    continue
                tbody.append(tag.tr(tag.td(i.id),
                                    tag.td(i.image_id),
                                    tag.td(i.key_name),
                                    tag.td(i.ip_address),
                                    tag.td(i.state),
                                    tag.td(i.monitored and True or ''),
                                    ))
        table.append(tbody)
        
        return table
