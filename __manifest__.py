{
    'name': 'Attendance Sync',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Synchronize attendance logs from eSSL to Odoo',
    'author': 'Your Name',
    'depends': ['hr'],
    'data': [
        'data/ir.cron.xml',
    ],
    'installable': True,
    'application': False,
}
