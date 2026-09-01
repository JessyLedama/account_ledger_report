{
    'name': 'Account Ledger Report',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Generate and preview a detailed account ledger report',
    'author': 'SIMI Technologies',
    'website': 'https://simitechnologies.co.ke',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',

        # 'views/account_ledger_menu.xml',
        'views/account_ledger_wizard_view.xml',
        'views/account_ledger_view.xml',
        
        'reports/account_ledger_template.xml',
    ],
    'installable': True,
    'application': False,
}
