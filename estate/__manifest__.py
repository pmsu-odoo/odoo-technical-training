{
 
    'name' : 'Real Estate',
    'description':'Dummy real estate model',
    'category': 'Real Estate/Brokerage',
    'depends':['base','website','web','web_cohort'],
    'version': "1",
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/property_offer.xml',
        'wizard/offer_wizard_view.xml',
        'views/controller_template.xml',  #controller
        'views/property.xml',
        'views/property_type.xml',
        'views/property_tags.xml',
        'views/res_user.xml',
        'views/estate_menus.xml',
        'report/estate_template.xml',
        'report/estate_report.xml'
        ],
 
    'demo':['demo/estate_demo.xml', 
            'demo/web_demo.xml'  # controller
        ],
    'installable': True,
    'application':True,
    'license': 'LGPL-3'
    }